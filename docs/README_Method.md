# Algo Mini Modules - Entwicklungsmethodik

## Übersicht
Dieses Repository enthält eine Sammlung von Mini-Modulen für algorithmisches Trading mit Fokus auf die Börsen BitGet und KuCoin. Die Module sind so konzipiert, dass sie unabhängig voneinander verwendet oder zu größeren Anwendungen kombiniert werden können.

## Entwicklungsprinzipien

### 1. Modulare Entwicklung
- **Mini-Module**: Kleine, fokussierte Module, die eine spezifische Aufgabe erfüllen
- **Micro-Module**: Noch kleinere Funktionseinheiten in der `utils/common.py` Datei
- **Wiederverwendbarkeit**: Jedes Modul kann eigenständig oder als Teil größerer Systeme verwendet werden

### 2. Schrittweise Vorgehensweise
Unsere Entwicklungsmethodik folgt einem klaren, schrittweisen Ansatz:

1. **Analyse des Problems**: Klare Definition der Anforderungen
2. **Prüfung vorhandener Module**: Vor der Entwicklung neuer Funktionalität immer prüfen, ob bereits Module oder Funktionen existieren
3. **Entwicklung in kleinen Schritten**: Inkrementelle Entwicklung mit Tests nach jedem Schritt
4. **Validierung**: Überprüfung der Funktionalität in verschiedenen Kontexten
5. **Dokumentation**: Klare Dokumentation der Funktionalität und Verwendung

### 3. Code-Wiederverwendung
Bevor neue Funktionalität entwickelt wird, sollte immer geprüft werden:
- Gibt es bereits ein Mini-Modul, das diese Funktionalität bietet?
- Existieren Micro-Module in `utils/common.py`, die verwendet werden können?
- Können vorhandene Module erweitert werden, anstatt neue zu erstellen?

## Beispiel: Credentials_Validator

Das `Credentials_Validator`-Modul demonstriert unsere Entwicklungsprinzipien:

1. **Problemanalyse**: Bedarf an zuverlässiger Validierung von API-Zugangsdaten
2. **Wiederverwendung**: Nutzung des `setup_logging`-Micro-Moduls aus `utils/common.py`
3. **Schrittweise Entwicklung**:
   - Implementierung der Grundfunktionalität für eine Börse
   - Erweiterung auf mehrere Börsen
   - Hinzufügen von Kommandozeilenparametern
   - Anpassung für verschiedene Ausführungskontexte
4. **Validierung**: Tests als Modul und als Standalone-Skript
5. **Dokumentation**: Ausführliche Kommentare und diese README

### Verwendung des Credentials_Validator

Das Modul kann auf verschiedene Arten verwendet werden:

```bash
# Alle Zugangsdaten überprüfen
python -m modules.Credentials.Credentials_Validator

# Als Standalone-Skript ausführen
python modules/Credentials/Credentials_Validator.py

# Nur BitGet-Zugangsdaten überprüfen
python modules/Credentials/Credentials_Validator.py bitget

# Nur KuCoin-Zugangsdaten überprüfen
python modules/Credentials/Credentials_Validator.py kucoin
```

## Projektstruktur

```
Algo_Mini_Modules/
├── modules/
│   ├── Credentials/
│   │   └── Credentials_Validator.py
│   └── ... (weitere Module)
├── utils/
│   └── common.py
├── docs/
│   └── README_Method.md
├── .env
└── README.md
```

## Best Practices

1. **DRY-Prinzip** (Don't Repeat Yourself): Wiederverwendung von Code durch Module
2. **Einzelverantwortlichkeit**: Jedes Modul hat eine klar definierte Aufgabe
3. **Klare Benennung**: Aussagekräftige Namen für Module und Funktionen
4. **Fehlerbehandlung**: Robuste Fehlerbehandlung und aussagekräftige Logging
5. **Konfigurierbarkeit**: Module sollten konfigurierbar sein (z.B. über Parameter)

## Nächste Schritte

Nach Abschluss eines Moduls oder Meilensteins:
1. Code auf GitHub committen
2. Dokumentation aktualisieren
3. Überprüfen, ob das Modul in anderen Projekten wiederverwendet werden kann 