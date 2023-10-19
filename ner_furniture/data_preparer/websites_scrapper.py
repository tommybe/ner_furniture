import requests
from bs4 import BeautifulSoup
import logging
import os
from typing import NoReturn, List
import json

import trafilatura
from tqdm import tqdm
from trafilatura.sitemaps import sitemap_search

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Crawler:
    def __init__(self, basic_urls: List[str], furnitures_types: List[str]):
        self.basic_urls = basic_urls
        self.furnitures_types = furnitures_types
        self.results = {}

    def run(self):
        for url in tqdm(self.basic_urls):
            sitemap_urls = sitemap_search(url)


            logging.info(f"Scrapping {url} and {len(sitemap_urls)} connected sites.")
            self._single_website_run(all_urls, url)

    def _get_all_linked_websites(self, url: str):
        for link in soup.find_all('a'):
            print(link.get('href'))

    def _single_website_run(self, all_inner_websites: List[str], website: str):
        inner_results = {}
        for inner_website in all_inner_websites:
            try:
                scrapper = Scrapper(inner_website)
                inner_results[scrapper.get_title()] = scrapper.get_content()
                del scrapper
            except:
                logging.error(f'Error during scraping {inner_website}.')
        self.results[website] = inner_results
        self._dump()

    # TEMPORARY
    def _dump(self):
        with open('/home/inquisitor/ner_furniture/texts3.json', "w") as file:
            json.dump(self.results, file)


class Scrapper:
    def __init__(self, url: str):
        self.url = url
        logging.debug(f"Initialize {type(self).__name__} class.")

    def get_title(self) -> str:
        r = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(r.content)
        return soup.find('title').string.strip()

    def get_content(self) -> str:
        downloaded = trafilatura.fetch_url(self.url)
        return trafilatura.extract(downloaded, include_comments=False).strip()
