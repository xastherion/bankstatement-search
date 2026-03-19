# Bank Statement PDF Search

Ein Python-Skript zum Durchsuchen von PDF-Kontoauszügen nach bestimmtem Text und automatischem Extrahieren von Transaktionsdaten.

## Das Problem

Nach vielen Jahren ist es nicht mehr möglich, Kontoauszüge direkt in der Weboberfläche des Bankensystems zu `CSV` zu exportieren. Die Suche nach bestimmten Transaktionen oder Benefiziären über die Web-Plattform ist unpraktisch und zeitaufwändig. 

Dieses Skript löst das Problem, indem es eine **lokale Batch-Suche** durch Ihre gesammelten PDF-Kontoauszüge durchführt und automatisch alle Transaktionen mit einem bestimmten Benefiziar oder Kreditgeber extrahiert.

## Optimiert für VB Kontoauszüge

Dieses Skript ist speziell für die **PDF-Kontoauszüge der Volksbank (VB) Deutschland** optimiert. Es berücksichtigt:
- Das spezifische PDF-Layout der VB-Kontoauszüge (zwei-spaltig)
- Deutsche Datumsformate (`DD.MM.YYYY`)
- Deutsche Zahlenformate mit Komma als Dezimaltrennzeichen
- Buchungslogik mit `S` (Soll) und `H` (Haben)
- Beide PDF-Formate: Legacy-Format (2016-2023) und neues Format (2024+)

## Features

- 🔍 **Textsuche**: Durchsuchen Sie alle PDF-Kontoauszüge nach beliebigem Text
- 📊 **Datenextraktion**: Extrahiert automatisch Datum, Betrag und Suchtext
- 💱 **Zahlenseparation**: Konvertiert deutsche Beträge (mit Komma) in Excel-kompatibles Format
- ✅ **Vorzeichenlogik**: 
  - `S` (Soll) = positive Beträge (Ausgaben)
  - `H` (Haben) = negative Beträge (Eingänge)
- 📁 **Batch-Verarbeitung**: Verarbeitet alle PDF-Dateien im Verzeichnis
- 📈 **CSV-Export**: Ergebnisse als `ergebnisse.csv` mit `|` als Trennzeichen

- 🔍 **Textsuche**: Durchsuchen Sie alle PDF-Kontoauszüge nach beliebigem Text
- 📊 **Datenextraktion**: Extrahiert automatisch Datum, Betrag und Suchtext
- 💱 **Zahlenseparation**: Konvertiert deutsche Beträge (mit Komma) in Excel-kompatibles Format
- ✅ **Vorzeichenlogik**: 
  - `S` (Soll) = positive Beträge (Ausgaben)
  - `H` (Haben) = negative Beträge (Eingänge)
- 📁 **Batch-Verarbeitung**: Verarbeitet alle PDF-Dateien im Verzeichnis
- 📈 **CSV-Export**: Ergebnisse als `ergebnisse.csv` mit `|` als Trennzeichen

## Anforderungen

- Python 3.7+
- `pdftotext` (Teil von Poppler-Utils)

### Installation der Abhängigkeiten

**macOS (Homebrew):**
```bash
brew install poppler
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install poppler-utils
```

**Linux (Red Hat/Fedora):**
```bash
sudo yum install poppler-utils
```

**Windows:**
Laden Sie Poppler für Windows herunter: https://blog.alivate.com.au/poppler-windows/

## Verwendung

### Grundlegende Verwendung

```bash
cd /path/to/bank/statements
python3 bankstatement_search.py "Suchtext"
```

oder mit dem Bash-Wrapper:

```bash
sh bankstatement_search.sh "Suchtext"
```

### Beispiele

```bash
# Suche nach einer Versicherung
python3 bankstatement_search.py "Versicherung"

# Suche nach einem Unternehmen
python3 bankstatement_search.py "Telekom"

# Suche nach teilweisem Text
python3 bankstatement_search.py "Amazon"
```

## Dateiformat

Die PDF-Kontoauszüge sollten folgende Namensstruktur haben:

```
[KONTONUMMER]_[YYYY]_Nr.[NNN]_[BESCHREIBUNG].pdf
```

Beispiele:
- `1008581_2024_Nr.001_Kontoauszug_vom_2024.01.31.pdf`
- `1008581_2024_Nr.012_Kontoauszug_vom_2024.12.31.pdf`

Das Skript extrahiert das Jahr (`YYYY`) automatisch aus dem Dateinamen.

## Ausgabe

Das Skript erstellt eine `ergebnisse.csv`-Datei mit folgender Struktur:

```
datum|suchtext|betrag
01.03.2024|Versicherung|85,52
15.04.2024|Versicherung|-150,00
```

**Spalten:**
- `datum`: Transaktionsdatum im Format `DD.MM.YYYY`
- `suchtext`: Der eingegebene Suchbegriff
- `betrag`: Der Betrag als Dezimalzahl (Excel-kompatibel)

## PDF-Formate

Das Skript unterstützt zwei gängige PDF-Layouts:

### Format 1: Ältere Kontoauszüge (2016-2023)
Zweispaltige Layouts mit:
- Linke Spalte: Transaktionsdetails
- Rechte Spalte: Beträge in nachfolgenden Zeilen

### Format 2: Neuere Kontoauszüge (2024+)
Zweispaltige Layouts mit:
- Linke Spalte: Transaktionsdetails  
- Rechte Spalte: Beträge in der gleichen Zeile

## Technische Details

### Regex-Muster

Das Skript erkennt automatisch:

- **Datumsformat**: `DD.MM.` (deutsches Format)
- **Betragsformat**: `XXX,XX S/H`
  - Dezimalzeichen: Komma (`,`)
  - Trennzeichen zwischen Spalten: Leerraum

### Transaktionslogik

1. Jede Zeile die mit `DD.MM.` beginnt, wird als Transaktionbeginn erkannt
2. Der Suchtext wird case-insensitive gesucht
3. Der erste Betrag (`XXX,XX S/H`) nach dem Transaktionsbeginn wird zugeordnet
4. S (Soll) bleibt positiv, H (Haben) wird negativ konvertiert

## Erweiterung für andere Bankformate

Für Bankauszüge mit anderen Formaten können folgende Parameter angepasst werden:

1. **Dateiname-Muster**: Zeile 19 in `bankstatement_search.py`
   ```python
   match = re.search(r'(\d{4})_Nr\.\d{3}', filename)
   ```

2. **Datumsformat**: Zeile 50 in `bankstatement_search.py`
   ```python
   if re.match(r'^\d{2}\.\d{2}\.', line.strip()):
   ```

3. **Betragsformat**: Zeilen 76-77 in `bankstatement_search.py`
   ```python
   amount_match = re.search(r'(\d+,\d{2})\s+([SH])\s*$', first_line)
   ```

## Lizenz

MIT License - Frei verwendbar und modifizierbar

## Beitragen

Verbesserungen und Anpassungen sind willkommen! Bitte erstellen Sie einen Pull Request.

## Bekannte Limitationen

- Funktioniert mit deutschem Datumsformat (DD.MM.YYYY)
- Beträge müssen als `XXX,XX` mit Komma formatiert sein
- Transaktionstyp-Markierungen müssen `S` oder `H` sein
- Das PDF muss Textinformationen (keine Scans) enthalten

## Fehlerbehandlung

Falls das Skript Fehler meldet:

1. **"Keine PDF-Dateien gefunden"** → Stellen Sie sicher, dass Sie im richtigen Verzeichnis sind
2. **"Konnte Jahr nicht extrahieren"** → Überprüfen Sie das Dateiname-Format
3. **"pdftotext nicht gefunden"** → Poppler muss installiert sein

## Support

Für Fragen oder Probleme bitte ein Issue erstellen.
