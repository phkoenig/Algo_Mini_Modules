"""
Data Display - Komponente zur Anzeige der WebSocket-Daten

Diese Komponente bietet eine Benutzeroberfläche zur Anzeige der empfangenen WebSocket-Daten
in verschiedenen Formaten (Tabelle, Chart, Statistiken).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

class DataDisplay:
    """Komponente zur Anzeige der WebSocket-Daten"""
    
    def __init__(self):
        """Initialisiert die Data-Display-Komponente"""
        # Initialisiere Session State für persistente Daten
        if 'display_mode' not in st.session_state:
            st.session_state.display_mode = "table"
        if 'chart_timeframe' not in st.session_state:
            st.session_state.chart_timeframe = "1min"
        if 'max_points' not in st.session_state:
            st.session_state.max_points = 100
    
    def render(self, data, symbol=None, exchange=None):
        """
        Rendert die Data-Display-Komponente
        
        Args:
            data: Die anzuzeigenden Daten als DataFrame
            symbol: Das Währungspaar (optional)
            exchange: Die Exchange (optional)
        """
        if data is None or data.empty:
            st.info("Keine Daten zum Anzeigen vorhanden. Bitte stelle eine Verbindung her.")
            return
        
        # Tabs für verschiedene Ansichten
        tab1, tab2, tab3, tab4 = st.tabs(["Live-Daten", "Chart", "Statistiken", "Rohdaten"])
        
        with tab1:
            self._render_table(data)
        
        with tab2:
            self._render_chart(data, symbol, exchange)
        
        with tab3:
            self._render_statistics(data, symbol, exchange)
        
        with tab4:
            self._render_raw_data(data)
    
    def _render_table(self, data):
        """
        Rendert die Daten als Tabelle
        
        Args:
            data: Die anzuzeigenden Daten als DataFrame
        """
        st.subheader("Live-Daten")
        
        # Einstellungen für die Tabelle
        col1, col2 = st.columns(2)
        
        with col1:
            max_rows = st.slider(
                "Anzahl der Zeilen",
                min_value=5,
                max_value=100,
                value=10,
                step=5,
                key="table_max_rows"
            )
        
        with col2:
            sort_by = st.selectbox(
                "Sortieren nach",
                ["timestamp", "price", "volume"],
                index=0,
                key="table_sort_by"
            )
        
        # Sortiere und begrenze die Daten
        display_data = data.sort_values(by=sort_by, ascending=False).head(max_rows)
        
        # Formatiere die Daten für die Anzeige
        if 'timestamp' in display_data.columns:
            display_data['timestamp'] = display_data['timestamp'].dt.strftime('%H:%M:%S.%f').str[:-3]
        
        if 'price' in display_data.columns:
            display_data['price'] = display_data['price'].apply(lambda x: f"{x:.8f}")
        
        # Entferne die Rohdaten-Spalte für die Anzeige
        if 'raw_data' in display_data.columns:
            display_data = display_data.drop(columns=['raw_data'])
        
        # Zeige die Tabelle
        st.dataframe(display_data, use_container_width=True)
        
        # Zeige Aktualisierungszeit
        st.caption(f"Letzte Aktualisierung: {datetime.now().strftime('%H:%M:%S')}")
    
    def _render_chart(self, data, symbol=None, exchange=None):
        """
        Rendert die Daten als Chart
        
        Args:
            data: Die anzuzeigenden Daten als DataFrame
            symbol: Das Währungspaar (optional)
            exchange: Die Exchange (optional)
        """
        st.subheader("Preis-Chart")
        
        # Einstellungen für den Chart
        col1, col2, col3 = st.columns(3)
        
        with col1:
            chart_type = st.selectbox(
                "Chart-Typ",
                ["Linie", "Kerzen", "Bereich"],
                index=0,
                key="chart_type"
            )
        
        with col2:
            timeframe = st.selectbox(
                "Zeitrahmen",
                ["1min", "5min", "15min", "30min", "1h"],
                index=0,
                key="chart_timeframe"
            )
            st.session_state.chart_timeframe = timeframe
        
        with col3:
            max_points = st.slider(
                "Max. Datenpunkte",
                min_value=10,
                max_value=1000,
                value=st.session_state.max_points,
                step=10,
                key="chart_max_points"
            )
            st.session_state.max_points = max_points
        
        # Bereite die Daten für den Chart vor
        if data.empty or 'price' not in data.columns or 'timestamp' not in data.columns:
            st.info("Keine geeigneten Daten für die Chart-Erstellung vorhanden.")
            return
        
        # Begrenze die Datenmenge
        chart_data = data.tail(max_points).copy()
        
        # Erstelle den Chart je nach Typ
        if chart_type == "Linie":
            fig = px.line(
                chart_data,
                x='timestamp',
                y='price',
                title=f"{symbol or 'Symbol'} Preisentwicklung ({exchange or 'Exchange'})"
            )
            
            # Füge Volumen als Balken hinzu, falls vorhanden
            if 'volume' in chart_data.columns:
                fig.add_trace(
                    go.Bar(
                        x=chart_data['timestamp'],
                        y=chart_data['volume'],
                        name='Volumen',
                        yaxis='y2',
                        opacity=0.3
                    )
                )
                
                # Konfiguriere die zweite Y-Achse für das Volumen
                fig.update_layout(
                    yaxis2=dict(
                        title='Volumen',
                        overlaying='y',
                        side='right'
                    )
                )
            
        elif chart_type == "Kerzen":
            # Erstelle OHLC-Daten, falls nicht vorhanden
            if not all(col in chart_data.columns for col in ['open', 'high', 'low', 'close']):
                # Resample die Daten nach dem gewählten Zeitrahmen
                chart_data.set_index('timestamp', inplace=True)
                ohlc = chart_data['price'].resample(timeframe).ohlc()
                
                # Füge Volumen hinzu, falls vorhanden
                if 'volume' in chart_data.columns:
                    volume = chart_data['volume'].resample(timeframe).sum()
                    ohlc['volume'] = volume
                
                # Setze den Index zurück
                ohlc.reset_index(inplace=True)
                chart_data = ohlc
            
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=chart_data['timestamp'],
                        open=chart_data['open'],
                        high=chart_data['high'],
                        low=chart_data['low'],
                        close=chart_data['close'],
                        name='OHLC'
                    )
                ]
            )
            
            # Füge Volumen als Balken hinzu, falls vorhanden
            if 'volume' in chart_data.columns:
                fig.add_trace(
                    go.Bar(
                        x=chart_data['timestamp'],
                        y=chart_data['volume'],
                        name='Volumen',
                        yaxis='y2',
                        opacity=0.3
                    )
                )
                
                # Konfiguriere die zweite Y-Achse für das Volumen
                fig.update_layout(
                    yaxis2=dict(
                        title='Volumen',
                        overlaying='y',
                        side='right'
                    )
                )
            
            fig.update_layout(
                title=f"{symbol or 'Symbol'} OHLC-Chart ({exchange or 'Exchange'})"
            )
            
        else:  # Bereich
            fig = px.area(
                chart_data,
                x='timestamp',
                y='price',
                title=f"{symbol or 'Symbol'} Preisentwicklung ({exchange or 'Exchange'})"
            )
        
        # Konfiguriere das Layout
        fig.update_layout(
            xaxis_title='Zeit',
            yaxis_title='Preis',
            height=500
        )
        
        # Zeige den Chart
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_statistics(self, data, symbol=None, exchange=None):
        """
        Rendert Statistiken zu den Daten
        
        Args:
            data: Die anzuzeigenden Daten als DataFrame
            symbol: Das Währungspaar (optional)
            exchange: Die Exchange (optional)
        """
        st.subheader("Statistiken")
        
        if data.empty or 'price' not in data.columns:
            st.info("Keine Daten für die Statistikberechnung vorhanden.")
            return
        
        # Zeige grundlegende Metriken
        col1, col2, col3 = st.columns(3)
        
        with col1:
            current_price = data['price'].iloc[-1]
            st.metric(
                "Aktueller Preis",
                f"{current_price:.8f}"
            )
        
        with col2:
            if len(data) > 1:
                price_change = data['price'].iloc[-1] - data['price'].iloc[0]
                price_change_pct = (price_change / data['price'].iloc[0]) * 100
                st.metric(
                    "Preisänderung",
                    f"{price_change:.8f}",
                    f"{price_change_pct:.2f}%"
                )
            else:
                st.metric("Preisänderung", "N/A")
        
        with col3:
            st.metric("Datenpunkte", len(data))
        
        # Zeige detaillierte Statistiken
        st.subheader("Detaillierte Statistiken")
        
        # Berechne Statistiken
        stats = data['price'].describe()
        
        # Formatiere die Statistiken
        stats_df = pd.DataFrame({
            'Statistik': stats.index,
            'Wert': stats.values
        })
        
        # Zeige die Statistiken
        st.dataframe(stats_df, use_container_width=True)
        
        # Zeige Zeitraum
        if 'timestamp' in data.columns:
            start_time = data['timestamp'].min()
            end_time = data['timestamp'].max()
            duration = end_time - start_time
            
            st.caption(f"Zeitraum: {start_time.strftime('%H:%M:%S')} - {end_time.strftime('%H:%M:%S')} ({duration.total_seconds():.2f} Sekunden)")
    
    def _render_raw_data(self, data):
        """
        Rendert die Rohdaten
        
        Args:
            data: Die anzuzeigenden Daten als DataFrame
        """
        st.subheader("Rohdaten")
        
        if 'raw_data' not in data.columns:
            st.info("Keine Rohdaten verfügbar.")
            return
        
        # Zeige die letzten Rohdaten
        raw_data = data['raw_data'].iloc[-1]
        
        try:
            # Versuche, die Rohdaten als JSON zu parsen
            json_data = json.loads(raw_data)
            
            # Zeige die Rohdaten als JSON
            st.json(json_data)
            
        except Exception as e:
            # Fallback: Zeige die Rohdaten als Text
            st.text(raw_data)
            st.error(f"Fehler beim Parsen der Rohdaten: {str(e)}")
    
    def render_empty_state(self):
        """
        Rendert einen Platzhalter, wenn keine Daten vorhanden sind
        """
        st.title("WebSocket Daten Explorer")
        
        st.info("Bitte wähle eine Exchange und ein Symbol aus und klicke auf 'Verbinden', um Daten zu sehen.")
        
        # Zeige Beispiel-Chart
        st.subheader("Beispiel-Visualisierung")
        
        # Erstelle Beispieldaten
        dates = pd.date_range(start='2023-01-01', periods=30, freq='D')
        prices = [50000 + i * 100 + (i % 5) * 200 for i in range(30)]
        example_df = pd.DataFrame({'timestamp': dates, 'price': prices})
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=example_df['timestamp'],
            y=example_df['price'],
            mode='lines+markers',
            name='BTC Preis'
        ))
        
        fig.update_layout(
            title='Beispiel: Bitcoin Preisentwicklung',
            xaxis_title='Datum',
            yaxis_title='Preis (USD)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True) 