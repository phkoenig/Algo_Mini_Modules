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

### Repository Informationen

```cmd
# Commit-Historie (letzte 5 Commits)
git log --oneline -n 5 | type

# Alle getrackten Dateien auflisten
git ls-tree -r --name-only HEAD | type

# Ungetrackte Dateien auflisten
git ls-files --others --exclude-standard | type
```

### Änderungen durchführen

```cmd
# Dateien zum Commit hinzufügen
git add dateiname
# Alle Dateien hinzufügen
git add .

# Änderungen committen
git commit -m "Beschreibende Nachricht über die Änderungen"

# Änderungen nach GitHub pushen
git push origin master
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

### Grundlegender Workflow

```cmd
# 1. Status prüfen
git status | type

# 2. Änderungen prüfen
git diff datei | type

# 3. Änderungen stagen
git add datei

# 4. Committen
git commit -m "Aussagekräftige Commit-Nachricht"

# 5. Pushen
git push
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