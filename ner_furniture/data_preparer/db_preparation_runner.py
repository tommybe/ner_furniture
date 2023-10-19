import csv
import logging
from typing import NoReturn, List
import os

import click

from ner_furniture.data_preparer.websites_scrapper import Crawler

logging.basicConfig(level=logging.INFO)

PATH_TO_FURNITURES_TYPES = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())),'furnitures_types.txt')


def run_vdb_creator(list_of_websites: List[str], furnitures_types: List[str]) -> NoReturn:
    Crawler(list_of_websites, furnitures_types).run()


# @click.command(help="Script to prepare dataset for NER training")
# @click.option("--path_to_csv_with_urls", type=str, required=True, help="Path to csv file with urls")
def run(path_to_csv_with_urls: str) -> NoReturn:
    file = open(path_to_csv_with_urls, "r")
    list_of_websites = [i[0] for i in list(csv.reader(file, delimiter=","))]
    file.close()

    file = open(PATH_TO_FURNITURES_TYPES, "r")
    furnitures_types = file.read().split("\n")
    file.close()

    run_vdb_creator(list_of_websites, furnitures_types)


def main():
    run(auto_envvar_prefix="AWS_DOC_SUPPORTER")


if __name__ == "__main__":
    run(path_to_csv_with_urls='/home/inquisitor/ner_furniture/furniture_stores_pages.csv')
