# Browser Tools MCP Setup Guide

## Voraussetzungen

- Node.js v20+ (getestet mit v20.14.0)
- Chrome Browser
- Streamlit App auf Port 8501
- Browser Tools MCP Extension v1.2.0

## Installation & Setup

### 1. Node.js Installation
```bash
# Via winget
winget install OpenJS.NodeJS.LTS
```

### 2. Browser-Tools-Server Installation
```bash
# Globale Installation
npm install -g @agentdeskai/browser-tools-server@1.2.0

# Server starten (WICHTIG: Als Administrator!)
npx @agentdeskai/browser-tools-server@1.2.0 --port 3025 --log-level debug
```

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
      "command": "npx",
      "args": ["-y", "@agentdeskai/browser-tools-mcp@1.2.0"],
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