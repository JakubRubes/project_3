# Election Results Scraper – Czech Parliament 2017

This project was created as the third assignment for the Engeto Online Python Academy.

The script downloads official election results for the 2017 elections to the Chamber of Deputies of the Czech Republic from the public website volby.cz.  
It collects results for all municipalities within a selected district and saves them into a CSV file.

---

## What does the script do?

The script performs the following steps:

1. Loads a list of all municipalities for a selected district  
2. For each municipality:
   - opens the municipality detail page
   - extracts basic voting statistics
   - extracts vote counts for all political parties  
3. Saves all collected data into a single CSV file

---

## Output data

Each row in the resulting CSV file represents one municipality and contains:

- `code` – municipality code (e.g. 554499)
- `location` – municipality name (e.g. Brandýs nad Labem)
- `registered` – number of registered voters
- `envelopes` – number of issued envelopes
- `valid` – number of valid votes
- one column per political party or movement  
  (party names are taken directly from the website and sorted alphabetically)

The CSV file is encoded in UTF-8 and can be opened in spreadsheet software.

---

## Requirements

- Python 3.6+
- External libraries:
  - requests
  - beautifulsoup4

---

## Installation

Install required libraries using:

```bash
pip install -r requirements.txt
```
---

## Example requirements.txt:

requests
beautifulsoup4

---

##How to run the script

Run the script with two command-line arguments: the district URL and the output CSV file.

```bash
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109" praha_vychod.csv
```

After successful execution, the file praha_vychod.csv will be created in the current directory.

---

##Tested environment

Python 3.13.3
Operating system: Windows 
Example district: Praha-východ (Central Bohemian Region)

---

##Notes

The script relies on the current HTML structure of volby.cz.
Party names and column headers are taken directly from the source website.
URLs must be enclosed in quotes when running the script due to special characters.

---

##Author
Jakub Rubes
Created as part of the Engeto Online Python Academy.