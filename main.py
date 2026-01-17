"""
projekt_3.py: Third project, web scraping

author: Jakub Rubes
email: rubes.jakub@email.cz
"""
import sys
import csv
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


WHITESPACE_REGEX = r"\s+"
PARTY_HEADER_TEXT = "Strana"


def fetch_soup(url: str) -> BeautifulSoup:
    """Download page and return parsed HTML."""
    response = requests.get(url)
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def clean_number(text: str) -> str:
    """Remove all whitespace from numeric text."""
    return re.sub(WHITESPACE_REGEX, "", text)


def parse_municipality_list(url: str) -> list:
    """Get list of municipalities from main page."""
    base_url = "https://volby.cz/pls/ps2017nss/"
    soup = fetch_soup(url)

    municipalities = []
    tables = soup.find_all("table")

    for table in tables:
        for row in table.find_all("tr")[2:]:
            cells = row.find_all("td")
            if len(cells) < 3:
                continue

            name = cells[1].get_text(strip=True)
            link = cells[0].find("a")

            if not link:
                print(f"Warning: municipality '{name}' has no link, skipping.")
                continue

            href = link.get("href")
            full_url = urljoin(base_url, href)

            match = re.search(r"xobec=(\d+)", href)
            code = match.group(1) if match else ""

            municipalities.append((code, name, full_url))

    return municipalities


def parse_municipality_results(code: str, name: str, url: str) -> dict:
    """Parse election results for one municipality."""
    soup = fetch_soup(url)
    results = {
        "code": code,
        "location": name
    }

    # voter statistics
    # columns: 3 = registered, 4 = envelopes, 7 = valid votes
    table = soup.find("table", id="ps311_t1")
    if table:
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 8:
                continue

            results["registered"] = clean_number(cells[3].get_text())
            results["envelopes"] = clean_number(cells[4].get_text())
            results["valid"] = clean_number(cells[7].get_text())

    # party results
    tables = soup.find_all("table")
    for table in tables:
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        if not any(PARTY_HEADER_TEXT in h for h in headers):
            continue

        for row in table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 3:
                continue

            party = cols[1].get_text(strip=True)
            votes = clean_number(cols[2].get_text())

            if party:
                results[party] = votes

    return results


def main() -> None:
    """Main program entry point."""
    if len(sys.argv) != 3:
        print("Usage: python script.py <URL> <output.csv>")
        return

    input_url = sys.argv[1]
    output_file = sys.argv[2]

    print(f"Loading municipalities from {input_url}")
    municipalities = parse_municipality_list(input_url)

    if not municipalities:
        print("No municipalities found. Check the URL.")
        return

    all_results = []

    for code, name, detail_url in municipalities:
        print(f"Processing {name} ({code})")
        data = parse_municipality_results(code, name, detail_url)
        all_results.append(data)

    priority = ["code", "location", "registered", "envelopes", "valid"]
    all_keys = {key for row in all_results for key in row}
    other_keys = sorted(k for k in all_keys if k not in priority)
    fieldnames = priority + other_keys

    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)

    print(f"Done. Results saved to {output_file}")


if __name__ == "__main__":
    main()
