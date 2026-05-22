#! /usr/bin/env python3

import csv
import argparse
import os

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Convert CSV to HTML table rows.")
parser.add_argument("input", help="Path to the input CSV file")
parser.add_argument("-o", "--output", required=True, help="Path to the output HTML file")
args = parser.parse_args()

# Expand user (~) in file paths
input_path = os.path.expanduser(args.input)
output_path = os.path.expanduser(args.output)

# Read CSV and write HTML output
with open(input_path, newline='', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    for row in reader:
        outfile.write('    <tr>\n')
        for field in row:
            outfile.write(f'        <td>{field.strip()}</td>\n')
        outfile.write('    </tr>\n')

print(f"HTML output saved to {output_path}")
