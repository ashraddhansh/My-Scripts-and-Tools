#! /usr/bin/env python3
from html.parser import HTMLParser
import csv

class TableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_tbody = False
        self.in_thead = False
        self.in_td = False
        self.in_th = False
        self.current_row = []
        self.current_cell = ""
        self.headers = []
        self.rows = []
        self.capture_href = False
        self.last_href = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "thead":
            self.in_thead = True
        elif tag == "tbody":
            self.in_tbody = True
        elif tag == "tr":
            self.current_row = []
        elif tag == "th":
            self.in_th = True
            self.current_cell = ""
        elif tag == "td":
            self.in_td = True
            self.current_cell = ""
            self.last_href = None
        elif tag == "a" and "href" in attrs:
            self.last_href = attrs["href"]

    def handle_endtag(self, tag):
        if tag == "thead":
            self.in_thead = False
        elif tag == "tbody":
            self.in_tbody = False
        elif tag == "th":
            self.in_th = False
            self.headers.append(self.current_cell.strip())
        elif tag == "td":
            self.in_td = False
            # If this cell had a link, store the href instead of text
            if self.last_href:
                self.current_row.append(self.last_href.strip())
            else:
                self.current_row.append(self.current_cell.strip())
        elif tag == "tr":
            if self.current_row:
                self.rows.append(self.current_row)

    def handle_data(self, data):
        if self.in_th:
            self.current_cell += data
        elif self.in_td:
            self.current_cell += data


def html_table_to_csv(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    parser = TableParser()
    parser.feed(html_content)

    # Replace the last header "View" with "Link" to reflect content change
    if parser.headers and parser.headers[-1].strip() == "View":
        parser.headers[-1] = "Link"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if parser.headers:
            writer.writerow(parser.headers)
        writer.writerows(parser.rows)

    print(f"Done! Saved {len(parser.rows)} rows to '{output_file}'")


if __name__ == "__main__":
    html_table_to_csv("table.html", "output.csv")
