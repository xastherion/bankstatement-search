#!/usr/bin/env python3
"""
Skript zum Suchen von Text in PDF-Kontoauszügen und Extrahieren von Transaktionen.
Verwendung: python3 bankstatement_search.py "Suchtext"

Dieses Skript wurde für deutsche Bankauszüge entwickelt und kann Transaktionen
nach Suchtext durchsuchen und relevante Daten exportieren.
"""

import os
import re
import sys
import subprocess
import csv
from pathlib import Path

def extract_year_from_filename(filename):
    """Extrahiert das Jahr aus dem PDF-Dateinamen."""
    match = re.search(r'(\d{4})_Nr\.\d{3}', filename)
    if match:
        return match.group(1)
    return None

def pdf_to_text(pdf_path):
    """Konvertiert PDF zu Text mit erhaltener Formatierung."""
    try:
        result = subprocess.run(
            ['pdftotext', '-layout', str(pdf_path), '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.returncode == 0 else None
    except Exception as e:
        print(f"Fehler beim Verarbeiten von {pdf_path}: {e}", file=sys.stderr)
        return None

def search_in_pdf(text, search_text, year):
    """
    Sucht Text in PDF und extrahiert Datum, Betrag und Jahr.
    
    Unterstützt zwei Formate:
    - Ältere PDFs: Beträge in nachfolgenden Zeilen (rechte Spalte)
    - Neuere PDFs: Beträge in gleicher Zeile (rechte Spalte)
    """
    results = []
    lines = text.split('\n')
    
    transaction_starts = []
    for i, line in enumerate(lines):
        if re.match(r'^\d{2}\.\d{2}\.', line.strip()):
            transaction_starts.append(i)
    
    for idx, start_line in enumerate(transaction_starts):
        if idx + 1 < len(transaction_starts):
            end_line = transaction_starts[idx + 1]
        else:
            end_line = len(lines)
        
        transaction_block = '\n'.join(lines[start_line:end_line])
        
        if search_text.lower() not in transaction_block.lower():
            continue
        
        date_match = re.match(r'^(\d{2}\.\d{2}\.)', lines[start_line].strip())
        if not date_match:
            continue
        date_part = date_match.group(1)
        
        amount = None
        first_line = lines[start_line]
        amount_match = re.search(r'(\d+,\d{2})\s+([SH])\s*$', first_line)
        if amount_match:
            amount = amount_match.group(1) + ' ' + amount_match.group(2)
        
        if not amount:
            for j in range(start_line, min(start_line + 20, end_line)):
                match = re.search(r'(\d+,\d{2})\s+([SH])\s*$', lines[j].rstrip())
                if match:
                    amount = match.group(1) + ' ' + match.group(2)
                    break
        
        if not amount:
            inline_match = re.search(r'(\d+,\d{2})\s+([SH])', first_line)
            if inline_match:
                amount = inline_match.group(1) + ' ' + inline_match.group(2)
        
        if amount:
            full_date = f"{date_part}{year}"
            parts = amount.split()
            valor = parts[0]
            tipo = parts[1] if len(parts) > 1 else "S"
            
            if tipo == "H":
                valor = "-" + valor
            
            results.append({
                'datum': full_date,
                'suchtext': search_text,
                'betrag': valor
            })
    
    return results

def search_in_pdfs(search_text, output_file='ergebnisse.csv'):
    """
    Sucht in allen PDFs des aktuellen Verzeichnisses.
    """
    results = []
    pdf_files = sorted(Path('.').glob('*.pdf'))
    
    if not pdf_files:
        print("Keine PDF-Dateien im aktuellen Verzeichnis gefunden.", file=sys.stderr)
        return
    
    print(f"Verarbeite {len(pdf_files)} PDF-Dateien...", file=sys.stderr)
    
    for pdf_path in pdf_files:
        year = extract_year_from_filename(pdf_path.name)
        if not year:
            print(f"Warnung: Konnte Jahr nicht aus {pdf_path.name} extrahieren", file=sys.stderr)
            continue
        
        text = pdf_to_text(pdf_path)
        if not text:
            continue
        
        hits = search_in_pdf(text, search_text, year)
        results.extend(hits)
    
    if results:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['datum', 'suchtext', 'betrag'], delimiter='|')
            writer.writeheader()
            writer.writerows(results)
        print(f"\n✓ {len(results)} Ergebnisse gefunden.")
        print(f"✓ Gespeichert in: {output_file}")
    else:
        print(f"\nKeine Ergebnisse für '{search_text}' gefunden.", file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Verwendung: python3 bankstatement_search.py 'Suchtext'", file=sys.stderr)
        sys.exit(1)
    
    search_text = sys.argv[1]
    search_in_pdfs(search_text)
