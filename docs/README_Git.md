# Git und GitHub Guide

## Grundlegende Git-Befehle

### Repository Status

```cmd
# Status des Repositories überprüfen
git status | type

# Remote Repository Verbindungen anzeigen
git remote -v

# Unterschiede zwischen lokal und remote prüfen
git fetch && git status | type
```

### Änderungen nach GitHub übertragen

```cmd
# 1. ALLE Änderungen stagen (neue, geänderte und gelöschte Dateien)
git add -A

# 2. Änderungen committen
git commit -m "Beschreibende Nachricht über die Änderungen"

# 3. Änderungen nach GitHub pushen
git push
```

Wichtig: Immer `git add -A` verwenden, um sicherzustellen, dass:
- Alle neuen Dateien getrackt werden
- Alle Änderungen gestaged werden
- Alle Löschungen berücksichtigt werden
- Das GitHub-Repository exakt den lokalen Stand widerspiegelt

### Repository Informationen

```cmd
# Commit-Historie (letzte 5 Commits)
git log --oneline -n 5 | type

# Alle getrackten Dateien auflisten
git ls-tree -r --name-only HEAD | type

# Ungetrackte Dateien auflisten
git ls-files --others --exclude-standard | type
```

### Updates holen

```cmd
# Neueste Änderungen vom Remote holen
git fetch

# Änderungen pullen (fetch + merge)
git pull origin master
```

## Häufige Herausforderungen und Lösungen

### 1. Problem: Unvollständige Git-Ausgaben

**Symptome:**
- Git-Befehle wie `git status` zeigen unvollständige Ausgaben
- Teile der Terminal-Ausgabe fehlen

**Lösungen:**
- Bei Windows CMD immer `| type` an Git-Befehle anhängen, z.B. `git status | type`
- Dies verhindert, dass Git einen Pager verwendet
- Alternative: `git config --global core.pager type`

### 2. Problem: Änderungen werden nicht erkannt

**Symptome:**
- Nach `git add` werden Änderungen nicht erkannt
- "no changes added to commit" Meldung erscheint

**Lösungen:**
- Status überprüfen: `git status | type`
- Vollständigen Pfad verwenden: `git add docs/README_Git.md`
- Bei Bedarf `git add -A` für alle Änderungen (vorsichtig verwenden)

### 3. Problem: Push ohne Upstream-Branch

**Symptome:**
- `git push` schlägt fehl mit "no upstream branch"

**Lösungen:**
- Bei neuem Branch: `git push --set-upstream origin <branch-name>`
- Oder kurz: `git push -u origin <branch-name>`
- Optional: `git config --global push.autoSetupRemote true`

## Best Practices für Git-Workflow

### Pre-Commit Check
```cmd
# 1. Git-Status prüfen
git status | type

# 2. Prüfen ob Git initialisiert ist und Remote korrekt eingerichtet ist
git remote -v

# 3. Wenn keine Remote-Verbindung existiert:
git remote add origin https://github.com/username/repository.git
```

### Grundlegender Workflow

```cmd
# 1. Status prüfen
git status | type

# 2. Änderungen prüfen (optional)
git diff datei | type

# 3. ALLE Änderungen stagen
git add -A

# 4. Committen
git commit -m "Aussagekräftige Commit-Nachricht"

# 5. Pushen
git push
```

### Post-Push Verifikation (Optional)
```cmd
# 1. Lokalen und Remote-Stand vergleichen
git fetch
git status | type

# 2. Detaillierte Unterschiede anzeigen (falls Status nicht clean)
git diff origin/master | type

# 3. Log der letzten Commits prüfen
git log --oneline -n 5 | type

# 4. Für kritische Änderungen: Liste aller Dateien im Remote
git ls-tree -r --name-only origin/master | type
```

### Branching-Strategie

1. **Feature-Branches**
   ```cmd
   # Neuen Feature-Branch erstellen
   git checkout -b feature/neue-funktion
   
   # Nach Fertigstellung in master/main mergen
   git checkout master
   git merge feature/neue-funktion
   ```

2. **Mit Hauptbranch synchron bleiben**
   ```cmd
   # Auf Feature-Branch
   git fetch origin
   git rebase origin/master
   ```

## Projekt Setup

Dieses Projekt verwendet eine Python Virtual Environment:

1. Environment aktivieren:
   ```cmd
   .\activate.bat
   ```

2. Dependencies installieren:
   ```cmd
   pip install -r requirements.txt
   ```

## Fehlerbehebung

### Bei abgelehntem Push ("rejected")

```cmd
# Aktuelle Änderungen holen
git fetch origin

# Entweder mit Merge
git merge origin/master

# Oder mit Rebase (saubere Historie)
git rebase origin/master

# Erneut pushen
git push
```

### Bei Merge-Konflikten

1. Konflikte in den Dateien beheben
2. Gelöste Dateien stagen: `git add datei`
3. Merge fortsetzen: 
   - Bei merge: `git commit`
   - Bei rebase: `git rebase --continue`

### Notfall-Reset

```cmd
# Harter Reset auf Remote-Zustand (Vorsicht: Lokale Änderungen gehen verloren!)
git fetch origin
git reset --hard origin/master
```

## Initial Setup

1. **Git installieren** (falls nötig)
2. **Identität einrichten**:
   ```cmd
   git config --global user.name "dein-username"
   git config --global user.email "deine.email@example.com"
   ```
3. **Nützliche Konfigurationen**:
   ```cmd
   # Automatisches Branch-Tracking
   git config --global push.autoSetupRemote true
   
   # Bessere Ausgabe ohne Pager
   git config --global core.pager type
   ```

## Projekt-spezifische Guidelines

- Vor dem Push Code-Funktionalität sicherstellen
- Kleine, thematisch zusammenhängende Commits
- Aussagekräftige Commit-Nachrichten verwenden
- Bei Unsicherheit Pull Request statt direktem Push

Zuletzt aktualisiert: 13.03.2024 