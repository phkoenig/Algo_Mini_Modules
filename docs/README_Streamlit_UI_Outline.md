# Streamlit UI Outline für Cursor AI

## Allgemeine Hinweise

- Erstelle eine Streamlit-App mit mehreren Seiten.
- Die Sidebar wird als navigation verwendet.
- Jede Seite soll klar strukturiert, minimalistisch und einfach gehalten werden.
- Dark Theme mit Matrix-/Hacker-Style verwenden.
- Immer vorhandene Module aus der bestehenden Codebase aus dem Ordner "Modules" verwenden; keinen doppelten Code erzeugen.


---

## 1. Login-Seite

- Sidebar-Navigation-Title: "1. Log in / log out"
- Native Oauth von Streamlet für Google verwenden, gemäß README_Google_Auth.md
- Nach erfolgreicher Authentifikation eine Bestätigung der Login Credentials anzeigen und einen Logout Button anbieten. 

## 2. Broker-Auswahl und Konto-Verbindung

- Sidebar-Navigation-Title: "2. Account-Info"
- Zwei Buttons: Button 1: Connect to KuKaIn, Button 2: Connect to BitGet.
- Nach Button click Verbindung zum Broker-Konto herstellen.
- Anzeige eines Statusindikators (grünes Licht bei erfolgreicher Verbindung, Fehlermeldung bei Problemen).
- Ausgabe der verfügbaren Informationen über den Account, Daten vom entsprechenden Account-Info-Modul 

## 3. Auswahl des Währungspaares

- Sidebar-Navigation-Title: "3. Traiding-Pairs"
- Alphabetische tabellarische Auflistung der verfügbaren Währungspaare.
- Korrekte und verständliche Darstellung der Broker-Symbole inklusive weiterer technischer Informationen.
- Texteingabefeld mit Autofokus und "Search-as-you-type"-Funktionalität.
- Sofortige Filterung und Anzeige relevanter Ergebnisse.
- Auswahl des Währungspars durch klick

## 4. Live-Daten und Preisverlauf

- Sidebar-Navigation-Title: "4. Live-Trading-Data"
- Automatische Websocket-Verbindung herstellen.
- Live-Daten der Trades als durchlauf-Tabelle anzeigen. immer die letzten 10 Datensätze.
- Chart, der die live-trading-daten darstellt.

## 5. Trading-Indikatoren

- Sidebar-Navigation-Title: "5. Technical Indicators"
- Übersichtliche Liste gängiger Trading-Indikatoren (z. B. RSI, EMA, Bollinger Bands).
- Für jeden Indikator:
  - Ein/Aus-Schalter (Toggle)
  - Minimalistische Einstellung wichtiger Parameter
  - Einstellung der Phasenverschiebung für Trading-Signale

## 6. Sentiment-Analyse

- Sidebar-Navigation-Title: "6. Sentiment Analys"
- Auswahl mehrerer Sentiment-Quellen mittels Checkbox oder Dropdown.
- Schieberegler zur Auswahl der Sentiment-Zeitspanne:
  - Kurzfristig (z. B. Alerts)
  - Mittelfristig (für Swing-Trading)
  - Langfristig
- Klare und übersichtliche Darstellung der Ergebnisse.

## 7. Backtesting-Funktion

- Sidebar-Navigation-Title: "7. Backtesting"
- Button zum Starten des Backtests der definierten Strategie.
- Eingabemöglichkeit für eine Trading-Fee-Hypothese.
- Ergebnisse des Backtests übersichtlich darstellen:
  - Gewinn/Verlust
  - Wichtige Kennzahlen (z. B. Sharpe Ratio, Drawdown)

## 8. Reinforcement Learning (Dummy-Seite)

- Sidebar-Navigation-Title: "8. Self-Learning"
- Platzhalter-Seite zur zukünftigen Integration von Reinforcement Learning.
- Kurze Erklärung zur Optimierung der Trading-Parameter durch neuronale Netze.
- Keine komplexen Elemente, nur erklärender Text.

## 9. Dry Run und Live-Trading

- Sidebar-Navigation-Title: "9. Dry rund / go live"
- Auswahl zwischen Paper Trading (Dry Run) und echtem Live-Trading (Bot scharf stellen).
- Eingabemöglichkeit für die Anzahl parallel laufender Bots.
- Live-Chart zur Darstellung aktueller Trades.
- Live-Chart zur Übersicht von Profit und Loss.

