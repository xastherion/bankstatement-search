# Changelog

Alle bemerkenswerten Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [1.0.0] - 2024-03-19

### Hinzugefügt
- Initiale Veröffentlichung
- Unterstützung für die Suche in PDF-Kontoauszügen
- Automatische Extraktion von Transaktionsdaten (Datum, Betrag)
- Unterstützung für zwei PDF-Formate (alt und neu)
- CSV-Export mit Pipe-Trennzeichen
- Deutsche Ausgabemeldungen
- Umgang mit S/H (Soll/Haben) Markierungen
- Dekriminalisierte Benennung (anonimisiert)

### Charakteristiken
- Python 3.7+ kompatibel
- Verwendet pdftotext für PDF-Verarbeitung
- Case-insensitive Textsuche
- Automatische Jahresextraktion aus Dateiename
- Fehlerbehandlung und Warnungen
