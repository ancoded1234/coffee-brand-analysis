"""Replay reviewed source URLs using cache; failed requests remain visible in logs."""
import csv
from collect import R,scrape
with (R/'data/sources.csv').open(encoding='utf-8-sig',newline='') as f:
    for row in csv.DictReader(f):
        slug=row['원문파일'].split('/')[-1].removesuffix('.md')
        scrape(row['출처URL'],slug)
