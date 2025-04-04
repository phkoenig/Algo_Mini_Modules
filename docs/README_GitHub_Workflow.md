# GitHub Workflow Guide

## Häufige Herausforderungen und deren Lösungen

Bei der Arbeit mit Git und GitHub über die Kommandozeile können verschiedene Herausforderungen auftreten. Dieser Guide fasst häufige Probleme und deren Lösungen zusammen.

### 1. Problem: Unvollständige oder abgeschnittene Git-Ausgaben

**Symptome:**
- Git-Befehle wie `git status` zeigen unvollständige Ausgaben
- Teile der Terminal-Ausgabe fehlen

**Lösungen:**
- Bei Windows-Systemen immer `| cat` an Git-Befehle anhängen, z.B. `git status | cat`
- Dies verhindert, dass Git einen Pager wie `less` oder `more` verwendet
- Alternative: Konfiguriere Git mit `git config --global core.pager cat`

### 2. Problem: Änderungen werden nicht zum Commit vorgemerkt

**Symptome:**
- Nach `git add` werden die Änderungen nicht erkannt
- Die Meldung "no changes added to commit" erscheint

**Lösungen:**
- Überprüfe den Status mit `git status | cat`
- Stelle sicher, dass der Dateipfad korrekt ist
- Verwende den vollständigen Pfad: `git add docs/README_Streamlit_UI_Outline.md`
- Bei Problemen verwende `git add -A` für alle Änderungen (mit Vorsicht)

### 3. Problem: Push ohne Upstream-Branch

**Symptome:**
- `git push` schlägt fehl mit "no upstream branch"
- Neue Branches müssen erst mit dem Remote verbunden werden

**Lösungen:**
- Bei neuem Branch: `git push --set-upstream origin <branch-name>`
- Oder kurz: `git push -u origin <branch-name>`
- Alternativ: Konfiguriere automatisches Tracking mit `git config --global push.autoSetupRemote true`

## Best Practices für Git-Workflow

### Grundlegender Workflow

```bash
# 1. Aktuellen Status überprüfen
git status | cat

# 2. Änderungen überprüfen
git diff <datei> | cat

# 3. Änderungen stagen
git add <datei>

# 4. Änderungen committen
git commit -m "Aussagekräftige Commit-Nachricht"

# 5. Änderungen pushen
git push
```

### Branching-Strategie

1. **Feature-Branches verwenden**
   ```bash
   # Neuen Feature-Branch erstellen
   git checkout -b feature/neue-funktion
   
   # Nach Fertigstellung in master/main mergen
   git checkout master
   git merge feature/neue-funktion
   ```

2. **Regelmäßig mit dem Hauptbranch synchronisieren**
   ```bash
   # Auf Feature-Branch
   git fetch origin
   git rebase origin/master
   ```

### Kommandozeilen-Tipps für Windows

- `cls` zum Löschen des Terminals
- Verwende PowerShell statt CMD für bessere Ausgabeformatierung
- Bei komplexen Befehlen: Skripte in einer `.bat` oder `.ps1` Datei speichern
- Git Bash installieren für eine Unix-ähnliche Erfahrung

## Empfohlene Tools

1. **GUI-Clients für bessere Übersicht:**
   - GitHub Desktop
   - GitKraken
   - SourceTree
   - VS Code mit Git-Erweiterungen

2. **Hilfsbefehle und Aliase:**
   ```bash
   # .gitconfig Beispiel-Aliase
   [alias]
     st = status
     co = checkout
     cm = commit -m
     unstage = reset HEAD --
     last = log -1 HEAD
   ```

## Fehlerbehebung

### Wenn ein Push abgelehnt wird ("rejected")

```bash
# Aktuelle Änderungen holen
git fetch origin

# Entweder:
# 1. Änderungen integrieren mit Merge
git merge origin/master

# 2. Oder mit Rebase (saubere Historie)
git rebase origin/master

# Dann erneut pushen
git push
```

### Bei Merge-Konflikten

1. Konflikte in den betroffenen Dateien beheben
2. Gelöste Dateien stagen: `git add <datei>`
3. Merge fortsetzen: 
   - Bei merge: `git commit` (Editor wird geöffnet)
   - Bei rebase: `git rebase --continue`

### Wenn alles schiefgeht

```bash
# Harte Reset auf Remotezustand (Vorsicht: Lokale Änderungen gehen verloren)
git fetch origin
git reset --hard origin/master
```

## Speziell für dieses Projekt

- Vor dem Pushen immer sicherstellen, dass der Code funktioniert
- Commits sinnvoll aufteilen: Lieber mehrere kleine, thematisch zusammenhängende Commits als ein großer
- Aussagekräftige Commit-Nachrichten verwenden
- Bei Unsicherheiten einen Pull Request erstellen statt direkt in den master zu pushen 