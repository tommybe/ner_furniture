import json
import logging
from typing import List

import requests
import trafilatura
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import urllib.request
from urllib.parse import urljoin

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


class Crawler:
    def __init__(self, basic_urls: List[str], furnitures_types: List[str]):
        self.basic_urls = basic_urls
        self.furnitures_types = furnitures_types
        self.results = {}

    def run(self):
        for url in tqdm(self.basic_urls):
            try:
                all_furnitures_urls = self._get_all_linked_furnitures_websites(url)
                self._single_website_run(all_furnitures_urls, url)
            except:
                logging.error(f'Website {url} doesn\'t work')
        return self.results

    def _get_all_linked_furnitures_websites(self, url: str):
        all_furnitures_urls = [url]
        r = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(r, 'lxml')
        all_urls = soup.find_all('a')
        for connected_url in all_urls:
            clear_url = urljoin(url, connected_url.get('href'))
            if any([furniture_type in clear_url for furniture_type in self.furnitures_types]):
                all_furnitures_urls.append(clear_url)
        logging.debug(f'{len(all_furnitures_urls)} of {len(all_urls)} was about furnitures')
        return all_furnitures_urls

    def _single_website_run(self, all_inner_websites: List[str], website: str):
        inner_results = {}
        for inner_website in all_inner_websites:
            try:
                scrapper = Scrapper(inner_website)
                inner_results[scrapper.get_title()] = scrapper.get_content()
                del scrapper
            except:
                logging.error(f'Error during scraping {inner_website}.')
        if inner_results:
            self.results[website] = inner_results
        self._dump()

    # TEMPORARY
    def _dump(self):
        with open('/home/inquisitor/ner_furniture/texts_150.json', "w") as file:
            json.dump(self.results, file)


class Scrapper:
    def __init__(self, url: str):
        self.url = url
        logging.debug(f"Initialize {type(self).__name__} class.")

    def get_title(self) -> str:
        r = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(r.content)
        website_title = self.remove_multiple_whitespaces(soup.find('title').string)
        return website_title

    def get_content(self) -> str:
        downloaded = trafilatura.fetch_url(self.url)
        content = self.remove_multiple_whitespaces(trafilatura.extract(downloaded, include_comments=False))
        return content

    def remove_multiple_whitespaces(self, text: str):
        return re.sub(r"\s+", " ", text)
