"""Comprobador simple del CSV de eventos — no importa la aplicación ni módulos nativos.

Uso: python check_csv.py
"""
import csv
import os

csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eventos_sismicos.csv')
print(f"Buscando CSV en: {csv_path}")
if not os.path.exists(csv_path):
    print("Archivo no encontrado.")
    raise SystemExit(1)

with open(csv_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Filas encontradas: {len(rows)}")
if rows:
    print("Primer registro (campos):")
    for k, v in list(rows[0].items())[:10]:
        print(f"  {k}: {v}")
