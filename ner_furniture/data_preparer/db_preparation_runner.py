import csv
import logging
from typing import NoReturn, List
import os
from random import sample
import json

import click

from ner_furniture.data_preparer.websites_scrapper import Crawler
from ner_furniture.data_preparer.tokenizer import WordTokenizer, WordPieceTokenizer
from ner_furniture.data_preparer.labelers import WordLabeler
from ner_furniture.commons import split_websites_on_train_test, split_content_into_words

logging.basicConfig(level=logging.INFO)

PATH_TO_FURNITURES_TYPES = '/home/inquisitor/ner_furniture/furnitures_types.txt'
WEBSITES_SAMPLE_SIZE = 150


def run_vdb_creator(list_of_websites: List[str], furnitures_types: List[str]) -> NoReturn:
    # websites_content = Crawler(list_of_websites, furnitures_types).run()

    #temp
    f = open('/home/inquisitor/ner_furniture/texts_test.json')
    websites_content = json.load(f)


    websites_content_by_words = split_content_into_words(websites_content)
    content_word_tokens = WordTokenizer.tokenize(websites_content_by_words)
    websites_content_by_words_labels = WordLabeler().label_loop(websites_content_by_words)


    #TODO - add label to train test split
    train_websites, test_websites = split_websites_on_train_test(websites_content_by_words)

    train_tokens = BasicTokenizer().tokenize(train_websites)
    test_tokens = BasicTokenizer().tokenize(test_websites)

    print('!!!')




# @click.command(help="Script to prepare dataset for NER training")
# @click.option("--path_to_csv_with_urls", type=str, required=True, help="Path to csv file with urls")
def run(path_to_csv_with_urls: str) -> NoReturn:
    file = open(path_to_csv_with_urls, "r")
    all_websites = [i[0] for i in list(csv.reader(file, delimiter=","))]
    sample_of_websites = sample(all_websites, WEBSITES_SAMPLE_SIZE)
    file.close()

    file = open(PATH_TO_FURNITURES_TYPES, "r")
    furnitures_types = file.read().split("\n")
    file.close()

    run_vdb_creator(sample_of_websites, furnitures_types)


def main():
    run(auto_envvar_prefix="AWS_DOC_SUPPORTER")


if __name__ == "__main__":
    run(path_to_csv_with_urls='/home/inquisitor/ner_furniture/furniture_stores_pages.csv')