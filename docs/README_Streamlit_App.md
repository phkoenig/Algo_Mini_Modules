# WebSocket Data Explorer - Streamlit App

Diese Streamlit-Anwendung ermöglicht die Verbindung zu WebSocket-APIs von KuCoin und BitGet, um Echtzeit-Marktdaten zu empfangen und zu visualisieren.

## Funktionen

- **Multi-Exchange-Unterstützung**: Verbindung zu KuCoin und BitGet WebSocket-APIs
- **Markttyp-Auswahl**: Unterstützung für Futures- und Spot-Märkte
- **Symbol-Auswahl**: Auswahl von Handelssymbolen mit Autovervollständigung
- **Kanal-Auswahl**: Flexibles Abonnieren verschiedener Datenkanäle (Ticker, Kline, Trades, etc.)
- **Live-Datenvisualisierung**: Anzeige der Daten in Echtzeit als Tabelle, Chart und Statistiken
- **Datenexport**: Speichern der empfangenen Daten als CSV-Datei
- **Responsive Benutzeroberfläche**: Optimiert für Desktop und Tablet

## Architektur

Die Anwendung ist modular aufgebaut und besteht aus folgenden Komponenten:

### GUI-Komponenten

- **ExchangeSelector**: Auswahl der Exchange und des Markttyps
- **PairSelector**: Auswahl des Handelssymbols mit Autovervollständigung
- **ChannelSelector**: Auswahl der zu abonnierenden Kanäle
- **DataDisplay**: Anzeige der empfangenen Daten in verschiedenen Formaten

### Utility-Komponenten

- **WebSocketManager**: Verwaltung der WebSocket-Verbindungen zu den Exchanges
- **DataProcessor**: Verarbeitung und Speicherung der empfangenen Daten

## Installation

1. Stelle sicher, dass Python 3.8 oder höher installiert ist
2. Klone das Repository
3. Installiere die erforderlichen Abhängigkeiten:

```bash
pip install -r requirements.txt
```

## Verwendung

Starte die Anwendung mit:

```bash
streamlit run app.py
```

Die Anwendung wird im Standard-Webbrowser geöffnet und ist unter `http://localhost:8501` erreichbar.

### Schritt-für-Schritt-Anleitung

1. **Exchange und Markttyp auswählen**: Wähle KuCoin oder BitGet und den gewünschten Markttyp (Futures oder Spot)
2. **Symbol auswählen**: Wähle ein Handelssymbol aus der Liste oder nutze die Suchfunktion
3. **Kanäle auswählen**: Wähle die zu abonnierenden Datenkanäle aus
4. **Verbinden**: Klicke auf "Verbinden", um die WebSocket-Verbindung herzustellen
5. **Daten anzeigen**: Die empfangenen Daten werden in Echtzeit angezeigt
6. **Daten speichern**: Klicke auf "Daten speichern", um die empfangenen Daten als CSV-Datei zu speichern

## API-Schlüssel (Optional)

Für einige private Kanäle werden API-Schlüssel benötigt. Diese können in einer `.env`-Datei im Hauptverzeichnis der Anwendung gespeichert werden:

```
KUCOIN_API_KEY=dein_kucoin_api_key
KUCOIN_API_SECRET=dein_kucoin_api_secret
KUCOIN_API_PASSPHRASE=dein_kucoin_api_passphrase

BITGET_API_KEY=dein_bitget_api_key
BITGET_API_SECRET=dein_bitget_api_secret
BITGET_API_PASSPHRASE=dein_bitget_api_passphrase
```

## Abhängigkeiten

- streamlit
- pandas
- plotly
- websocket-client
- python-dotenv
- requests

## Fehlerbehebung

### Verbindungsprobleme

- Stelle sicher, dass du eine stabile Internetverbindung hast
- Überprüfe, ob die Exchange-API erreichbar ist
- Prüfe, ob die API-Schlüssel korrekt sind (falls private Kanäle verwendet werden)

### Datenprobleme

- Stelle sicher, dass das gewählte Symbol auf der Exchange verfügbar ist
- Überprüfe, ob die gewählten Kanäle für das Symbol unterstützt werden
- Bei leeren Daten: Warte einige Sekunden, bis die ersten Daten empfangen werden

## Weiterentwicklung

Die Anwendung kann leicht erweitert werden:

- Hinzufügen weiterer Exchanges
- Implementierung zusätzlicher Datenvisualisierungen
- Integration von Trading-Funktionen
- Hinzufügen von Alarmen und Benachrichtigungen

## Lizenz

MIT

## Autor

Philip

## Letzte Aktualisierung

26.02.2025 