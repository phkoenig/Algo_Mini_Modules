# Streamlit UI Outline für Cursor AI

## Allgemeine Hinweise

- Erstelle eine Streamlit-App mit mehreren Tabs oder Seiten.
- Jede Seite soll klar strukturiert, minimalistisch und einfach gehalten werden.
- Dark Theme mit Matrix-/Hacker-Style verwenden.
- Immer vorhandene Mini-Module aus der bestehenden Codebase verwenden; keinen doppelten Code erzeugen.

---

## 1. Login-Seite

- Native Oauth von Streamlet für Google verwenden.
- Nach erfolgreicher Authentifikation eine Bestätigung der Login Credentials anzeigen und einen Lockout Button anbieten. 

## 2. Broker-Auswahl und Konto-Verbindung

- Zwei Buttons: Button 1: Connect to KuKaIn, Button 2: Connect to BitGet.
- Nach Auswahl automatische Verbindung zum Broker-Konto herstellen.
- Anzeige eines Statusindikators (grünes Licht bei erfolgreicher Verbindung, Fehlermeldung bei Problemen).
- Ausgabe der verfügbaren Informationen über den Account. 

## 3. Auswahl des Währungspaares

- Alphabetische Auflistung der verfügbaren Währungspaare.
- Korrekte und verständliche Darstellung der Broker-Symbole inklusive weiterer technischer Informationen.
- Texteingabefeld mit Autofokus und "Search-as-you-type"-Funktionalität.
- Sofortige Filterung und Anzeige relevanter Ergebnisse.

## 4. Live-Daten und Preisverlauf

- Automatische Websocket-Verbindung herstellen.
- Live-Daten in einem übersichtlichen Ticker-Fenster anzeigen.
- Einfache, klar strukturierte Chart-Darstellung des Preisverlaufs.

## 5. Trading-Indikatoren

- Übersichtliche Liste gängiger Trading-Indikatoren (z. B. RSI, EMA, Bollinger Bands).
- Für jeden Indikator:
  - Ein/Aus-Schalter (Toggle)
  - Minimalistische Einstellung wichtiger Parameter
  - Einstellung der Phasenverschiebung für Trading-Signale

## 6. Sentiment-Analyse

- Auswahl mehrerer Sentiment-Quellen mittels Checkbox oder Dropdown.
- Schieberegler zur Auswahl der Sentiment-Zeitspanne:
  - Kurzfristig (z. B. Alerts)
  - Mittelfristig (für Swing-Trading)
  - Langfristig
- Klare und übersichtliche Darstellung der Ergebnisse.

## 7. Backtesting-Funktion

- Button zum Starten des Backtests der definierten Strategie.
- Eingabemöglichkeit für eine Trading-Fee-Hypothese.
- Ergebnisse des Backtests übersichtlich darstellen:
  - Gewinn/Verlust
  - Wichtige Kennzahlen (z. B. Sharpe Ratio, Drawdown)

## 8. Reinforcement Learning (Dummy-Seite)

- Platzhalter-Seite zur zukünftigen Integration von Reinforcement Learning.
- Kurze Erklärung zur Optimierung der Trading-Parameter durch neuronale Netze.
- Keine komplexen Elemente, nur erklärender Text.

## 9. Dry Run und Live-Trading

- Auswahl zwischen Paper Trading (Dry Run) und echtem Live-Trading (Bot scharf stellen).
- Eingabemöglichkeit für die Anzahl parallel laufender Bots.
- Live-Chart zur Darstellung aktueller Trades.
- Live-Chart zur Übersicht von Profit und Loss.

