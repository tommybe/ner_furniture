import csv
import logging
from typing import NoReturn, List
import os
from random import sample
import json

import click

from ner_furniture.data_preparer.websites_scrapper import Crawler
from ner_furniture.data_preparer.tokenizer import WordTokenizer, WordPieceTokenizer
from ner_furniture.commons import split_content_into_words

logging.basicConfig(level=logging.INFO)

PATH_TO_FURNITURES_TYPES = '/home/inquisitor/ner_furniture/furnitures_types.txt'
WEBSITES_SAMPLE_SIZE = 150
TOKENS_DATA_FILENAME = 'labeled_tokens_dataset.json'


def run_vdb_creator(list_of_websites: List[str], furnitures_types: List[str]) -> dict:
    websites_content = Crawler(list_of_websites, furnitures_types).run()

    # temp
    f = open('/home/inquisitor/ner_furniture/texts_150.json')
    websites_content = json.load(f)
    websites_content_by_words = split_content_into_words(websites_content)

    logging.info('Preparing tokens and labels on words')
    word_tokenizer = WordTokenizer(websites_content_by_words)
    content_word_tokens = word_tokenizer.tokenize()
    content_word_labels = word_tokenizer.labelize()

    logging.info('Preparing tokens and labels on subwords')
    subword_tokenizer = WordPieceTokenizer()
    content_subword_tokens = subword_tokenizer.tokenize(content_word_tokens)
    content_subword_labels = subword_tokenizer.labelize(content_subword_tokens, content_word_labels)

    return {'tokens': content_subword_tokens, 'labels': content_subword_labels}


@click.command(help="Script to prepare dataset for NER training")
@click.option("--path_to_csv_with_urls", type=str, required=True, help="Path to csv file with urls")
def run(path_to_csv_with_urls: str) -> NoReturn:
    file = open(path_to_csv_with_urls, "r")
    all_websites = [i[0] for i in list(csv.reader(file, delimiter=","))]
    # sample_of_websites = sample(all_websites, WEBSITES_SAMPLE_SIZE)
    file.close()

    file = open(PATH_TO_FURNITURES_TYPES, "r")
    furnitures_types = file.read().split("\n")
    file.close()

    token_data = run_vdb_creator(all_websites, furnitures_types)
    token_data_path = os.path.join(os.path.dirname(path_to_csv_with_urls), TOKENS_DATA_FILENAME)
    logging.info(f'Saving token dataset to {token_data_path}')
    with open(token_data_path, "w") as f:
        f.write(json.dumps(token_data))


def main():
    run(auto_envvar_prefix="AWS_DOC_SUPPORTER")


if __name__ == "__main__":
    run()
    # path_to_csv_with_urls='/home/inquisitor/ner_furniture/furniture_stores_pages.csv'
