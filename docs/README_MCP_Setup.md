# Browser Tools MCP Setup Guide



## Voraussetzungen

- Node.js v20+ (getestet mit v20.14.0)
- Chrome Browser
- Streamlit App auf Port 8501
- Browser Tools MCP Extension v1.2.0
- Cursor IDE mit korrekter MCP Konfiguration

## Installation & Setup

### 1. Node.js Installation
```bash
# Via winget
winget install OpenJS.NodeJS.LTS
```

### 2. Cursor MCP Konfiguration
WICHTIG: Die korrekte Konfiguration in Cursor (Settings → MCP) ist entscheidend:

```json
{
  "mcpServers": {
    "browser-tools": {
      "type": "command",
      "command": "cmd",
      "args": ["/c", "npx", "@agentdeskai/browser-tools-server@1.2.0", "--port", "3025", "--log-level", "debug"],
      "env": {
        "PORT": "3025"
      }
    }
  }
}
```

⚠️ Wichtige Konfigurationsdetails:
- `command` MUSS `cmd` sein (nicht `npx` direkt)
- `/c` Flag ist notwendig für Windows
- Korrekte Paketversion: `browser-tools-server` (nicht `browser-tools-mcp`)
- `--log-level debug` hilft beim Troubleshooting
- Port muss in `args` UND `env` gesetzt werden

### 3. Chrome Extension Setup
- Extension von [BrowserTools MCP v1.2.0](https://github.com/AgentDeskAI/browser-tools-mcp/releases/tag/v1.2.0) installieren
- In Chrome DevTools zum "BrowserToolsMCP" Tab wechseln
- Verbindung testen über "Test Connection"
- Status sollte grün sein mit: "Connected to browser-tools-server v1.2.0 at localhost:3025"

### 4. Screenshot Konfiguration
```
Screenshot Path: B:\Nextcloud\CODE\proj\Algo_Mini_Modules\screenshots
```

## Konfiguration

### Cursor Settings (Aktuelle Methode)
Die Konfiguration erfolgt ausschließlich über die Cursor IDE Settings (GUI). Eine separate JSON-Konfigurationsdatei in der Codebase ist nicht mehr erforderlich.

> ⚠️ **Wichtiger Hinweis zur Konfiguration**  
> Die Konfiguration erfolgt ausschließlich in den Cursor Settings. JSON-Konfigurationsdateien in der Codebase werden nicht mehr unterstützt.

### MCP Server Konfiguration in Cursor Settings
Füge folgende Konfiguration in den Cursor Settings (GUI) unter dem MCP-Bereich ein:

```json
{
  "mcpServers": {
    "browser-tools": {
      "type": "command",
      "command": "cmd",
      "args": ["/c", "npx", "@agentdeskai/browser-tools-server@1.2.0", "--port", "3025", "--log-level", "debug"],
      "env": {
        "PORT": "3025"
      }
    }
  }
}
```

Diese Konfiguration muss in den Cursor Settings vorgenommen werden, NICHT als separate Datei in der Codebase.

## Funktionen & Features

### Aktiv und getestet
- [x] Screenshots (funktioniert)
- [x] Network Monitoring
- [x] Console Logs
- [x] Browser Integration
- [x] Streamlit Integration
- [x] Element Selection Tool
- [x] Log Wiping
- [x] Accessibility Audit
- [x] Performance Audit
- [x] SEO Audit
- [x] Best Practices Audit
- [x] Debugger Mode
- [x] Audit Mode

### Audit Scores & Metriken
- Accessibility: 0-100 Score mit detaillierten ARIA und Label Checks
- Performance: LCP, FCP, CLS Metriken und Optimierungsvorschläge
- SEO: Meta-Tags, robots.txt und sitemap.xml Validierung
- Best Practices: JavaScript, Security und Browser Compatibility Checks

### Verfügbare Modi
1. **Debugger Mode**
   - Systematische Problem-Analyse
   - Console & Network Log Integration
   - Step-by-Step Debugging Workflow

2. **Audit Mode**
   - Automatisierte Audit-Sequenz
   - Comprehensive Analysis
   - Optimization Planning

## Bekannte Einschränkungen
- MCP Features nur über Chrome Extension zugänglich
- Direkte API/WebSocket Kommunikation nicht möglich
- Port 3025 muss frei sein
- Server muss als Administrator laufen

## Debugging

### Typische Probleme & Lösungen

1. **Verbindungsprobleme**
   - Server als Admin neu starten
   - Chrome Extension neu laden
   - "Test Connection" klicken

2. **Screenshot Fehler**
   - Pfad überprüfen
   - Berechtigungen prüfen
   - "Wipe All Logs" und neu versuchen

3. **Node.js Prozesse aufräumen**
```bash
taskkill /F /IM node.exe
```

## Monitoring

Die Extension zeigt folgende Metriken:
- Console Logs Count
- Network Requests (Success/Errors)
- WebSocket Connection Status
- URL Updates & Navigation Events

## Best Practices
1. Immer als Administrator ausführen
2. Einen sauberen Port (3025) verwenden
3. Streamlit auf Port 8501 starten
4. Chrome DevTools offen halten für Monitoring
5. "Allow Auto-paste to Cursor" aktivieren für bessere Integration
6. Regelmäßige Audit-Durchführung:
   - Accessibility Score > 90 anstreben
   - Performance Score > 80 anstreben
   - SEO Score > 90 anstreben
   - Best Practices Score = 100 anstreben
7. Log Management:
   - Regelmäßiges Log Wiping durchführen
   - Console Errors sofort beheben
   - Network Errors tracken und analysieren
8. Debugging Workflow:
   - Debugger Mode für systematische Problemanalyse nutzen
   - Audit Mode für regelmäßige Qualitätschecks einsetzen
   - Element Selection für UI/UX Optimierung verwenden

## Anti-Patterns und bekannte Probleme

### NICHT tun
1. Node.js NICHT über Python/UV installieren - führt zu PATH-Problemen
2. NICHT mehrere Browser-Tools-Server parallel starten - verursacht Reconnect-Loops
3. KEINE direkten WebSocket/API-Aufrufe versuchen - nur über Chrome Extension möglich
4. NICHT den Port während der Laufzeit ändern - Server neu starten erforderlich
5. NICHT die venv aktivieren bevor der MCP-Server läuft - kann PATH-Konflikte verursachen

### Was nicht funktioniert
1. Direkte API-Kommunikation mit dem Server (`curl`, `wget`, etc.)
2. WebSocket-Verbindungen außerhalb der Chrome Extension
3. Automatische Port-Weiterleitung/Proxying
4. Parallele Server-Instanzen
5. Node.js Installation über alternative Paketmanager (UV, pip)

### Typische Fehlermeldungen und ihre Bedeutung
```
Error: Cannot POST /browser-tools/console-logs
→ API-Endpunkte sind nicht direkt zugänglich

Chrome extension disconnected
→ Mehrere Server-Instanzen oder Port-Konflikt

Der Befehl "node" ist entweder falsch geschrieben oder konnte nicht gefunden werden
→ Node.js nicht im System-PATH oder falsch installiert
```

## Änderungsprotokoll

- **05.04.2025**:
  - Audit-Funktionen als aktiv markiert
  - Neue Features dokumentiert (Element Selection, Log Wiping)
  - Audit Scores & Metriken hinzugefügt
  - Best Practices für Auditing & Debugging ergänzt
  - Debugger und Audit Mode dokumentiert
  - Konfigurationshinweise präzisiert (Cursor Settings JSON-Format dokumentiert)
  - Klarstellung: Konfiguration ausschließlich in Cursor Settings

- **04.04.2025**: 
  - Initiale MCP Setup-Dokumentation
  - Anti-Patterns dokumentiert

## Korrekte Startreihenfolge

1. Cursor IDE starten
2. Sicherstellen, dass die MCP Konfiguration exakt wie oben angegeben ist
3. Warten bis der MCP Server automatisch startet (Debug-Logs sollten erscheinen)
4. Chrome mit der Extension öffnen
5. In den Chrome DevTools prüfen ob "Connected" angezeigt wird
6. Streamlit App starten:
   ```bash
   python -m streamlit run gui/login.py --server.port 8501
   ```

## Troubleshooting

### Häufige Probleme

1. **MCP Server startet nicht**
   - Cursor MCP Konfiguration auf exakte Übereinstimmung prüfen
   - Besonders auf `cmd` und `/c` Flag achten
   - Debug-Logs in der Cursor Konsole prüfen

2. **Verbindungsprobleme**
   - Chrome Extension neu laden
   - "Test Connection" klicken
   - Debug-Logs auf Fehlermeldungen prüfen

3. **Instabile Verbindung**
   - Sicherstellen dass `browser-tools-server` (nicht mcp) verwendet wird
   - Port-Konflikte durch `netstat -ano | findstr 3025` prüfen
   - Nur eine Instanz von Cursor laufen lassen



## ⚠️ WICHTIG: Startup-Sequenz

Die folgende Befehlssequenz MUSS im internen Cursor-Terminal ausgeführt werden, NICHT in einem externen Terminal:

```bash
# 1. Alle laufenden Prozesse beenden
taskkill /F /IM python.exe & taskkill /F /IM node.exe & exit

# 2. MCP Server starten (im Hintergrund)
cmd /c "npx -y @agentdeskai/browser-tools-server@1.2.0 --port 3025 --log-level debug & exit"

# 3. Streamlit App starten (im Hintergrund)
cmd /c "python -m streamlit run gui/login.py --server.port 8501 & exit"
```

> ⚡ **Kritische Hinweise zur Startup-Sequenz:**
> - Befehle MÜSSEN im internen Cursor-Terminal ausgeführt werden
> - Reihenfolge MUSS exakt eingehalten werden
> - Zwischen den Befehlen warten, bis die Logs erscheinen
> - MCP Server muss "Connected" melden, bevor Streamlit startet
> - Externe Terminals oder PowerShell funktionieren NICHT
> - Terminal-Fenster schließen sich automatisch nach erfolgreicher Ausführung