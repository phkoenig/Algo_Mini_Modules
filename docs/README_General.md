# AlgotradingProject

Diese README-Datei bietet einen umfassenden Überblick über das Projekt, die einzelnen Module und die empfohlene Ordnerstruktur. Sie dient als Grundlage für die Entwicklung des Algotrading-Systems, das auf den Handel von gehebelten perpetual Futures im Kryptobereich fokussiert ist. Dabei werden Bitget und KuCoin als primäre Börsen verwendet – jeweils mit eigenen spezifischen Modulen.

---

## Projektüberblick

### Zielsetzung
- **Handel** von gehebelten perpetual Futures im Kryptobereich.
- **Optionale Arbitrage** zwischen Kryptowährungen.
- Nutzung von **Bitget** und **KuCoin** als Handelsplattformen.

### Datenakquise und -verarbeitung
- **Rohdaten** werden über die Websocket-Verbindungen beider Börsen abgerufen.
- Die unterschiedlichen Formate der Rohdaten werden durch **spezifische Parser-Module** verarbeitet:
  - `Parser_Raw_Data_Bitget.py` für Bitget
  - `Parser_Raw_Data_KuCoin.py` für KuCoin
- Daten können wahlweise in **Dataframes** oder direkt in **Supabase** gespeichert werden.

### Module und Funktionalitäten
- **Websocket Raw Data**  
  Abfangen und Speichern der Rohdaten (jeweils spezifisch für Bitget und KuCoin).
  
- **Account Info**  
  Abruf von Accountdaten (z. B. Assets, laufende Orders) über die jeweiligen API-Schnittstellen.
  
- **Candle Aggregator**  
  Aggregation von Candlestick-Daten in flexiblen Zeitintervallen (z. B. 1 sec, 15 sec).
  
- **Background Service**  
  Ein Windows Service, der die Websocket-Feeds im Hintergrund kontinuierlich abruft und alle Rohdaten in die Supabase schreibt.
  
- **Monitoring Modul**  
  Überwachung der Verbindungsstabilität und grafische Darstellung (mit Streamlit) von Spread, Trading-Volumen und weiteren Kennzahlen.
  
- **Trading Pairs Modul**  
  Abfrage und Anzeige der verfügbaren Handelspaare im perpetual Futures Bereich.
  
- **Trading Strategien**  
  Sammlung von Handelsstrategien und Indikatoren in separaten, parameterisierten Modulen.  
  Ermöglicht die flexible Kombination verschiedener Indikatoren (z. B. MACD, RSI), bei denen alle Parameter als Funktionsargumente übergeben werden.

---

## Empfohlene Ordnerstruktur

```plaintext
AlgotradingProject/
├── README.md                 # Projektbeschreibung, Zielsetzungen, Setup-Anleitung
├── requirements.txt          # Abhängigkeiten (z. B. Supabase CLI, Github CLI)
├── config/                   # Konfigurationsdateien für Bitget, KuCoin & Supabase
│   ├── bitget_config.json
│   ├── kucoin_config.json
│   └── supabase_config.json
├── modules/                  # Hauptmodule des Projekts (für beide Börsen)
│   ├── Websocket_Raw_Data/   # Rohdaten aus Websockets
│   │   ├── Websocket_Raw_Data_Bitget.py
│   │   └── Websocket_Raw_Data_KuCoin.py
│   ├── Account_Info/         # Abruf von Accountdaten
│   │   ├── Account_Info_Bitget.py
│   │   └── Account_Info_KuCoin.py
│   ├── Candle_Aggregator/    # Aggregation von Candlestick-Daten
│   │   ├── Candle_Aggregator_Bitget.py
│   │   └── Candle_Aggregator_KuCoin.py
│   ├── Background_Service/   # Windows Service für kontinuierliche Datensammlung
│   │   ├── Service_Bitget.py
│   │   └── Service_KuCoin.py
│   ├── Monitoring/           # Überwachung (mit Streamlit) und Visualisierung
│   │   ├── Monitoring_Bitget.py
│   │   └── Monitoring_KuCoin.py
│   └── Trading_Pairs/        # Abfrage der verfügbaren Handelspaare
│       ├── Trading_Pairs_Bitget.py
│       └── Trading_Pairs_KuCoin.py
├── parser/                   # Parser-Module zur Umwandlung der rohen Trading-Daten
│   ├── Parser_Raw_Data_Bitget.py
│   └── Parser_Raw_Data_KuCoin.py
├── strategies/               # Sammlung von Handelsstrategien und Indikatoren
│   ├── indicator_macd.py     # Beispiel: MACD-Indikator
│   ├── indicator_rsi.py      # Beispiel: RSI-Indikator
│   ├── strategy_trend.py     # Beispiel: Trendfolgestrategie
│   └── ...                   # Weitere Indikatoren/Strategien
├── utils/                    # Gemeinsame Hilfsfunktionen (z. B. Supabase-Anbindung, Logging)
│   ├── supabase_interface.py
│   └── common.py
├── tests/                    # Unit-Tests und Integrations-Tests
│   ├── test_websocket.py
│   ├── test_candle_aggregator.py
│   ├── test_account_info.py
│   └── ... 
└── docs/                     # Projektdokumentation und weitere Unterlagen
    └── architecture.md       # Detaillierte Architekturübersicht
