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


def run_bert_fine_tuning(list_of_websites: List[str], furnitures_types: List[str]) -> NoReturn:
    # websites_content = Crawler(list_of_websites, furnitures_types).run()

    #temp
    f = open('/home/inquisitor/ner_furniture/texts_test.json')
    websites_content = json.load(f)


    websites_content_by_words = split_content_into_words(websites_content)
    content_word_tokens = WordTokenizer(websites_content_by_words).tokenize()
    content_word_labels = WordTokenizer(websites_content_by_words).labelize()

    content_subword_tokens = WordPieceTokenizer().tokenize(content_word_tokens)
    print('#TODO')

    #TODO - add label to train test split
    train_websites, test_websites = split_websites_on_train_test(websites_content_by_words)

    train_tokens = BasicTokenizer().tokenize(train_websites)
    test_tokens = BasicTokenizer().tokenize(test_websites)

    print('!!!')




# @click.command(help="Script to fine-tune BERT model for NER problem")
# @click.option("--path_to_json_tokens_dataset", type=str, required=True, help="Path to json file with tokens and labels")
def run(path_to_json_tokens_dataset: str) -> NoReturn:
    # Opening JSON file
    f = open(path_to_json_tokens_dataset)
    tokens_data = json.load(f)

    run_bert_fine_tuning(tokens_data)


def main():
    run(auto_envvar_prefix="AWS_DOC_SUPPORTER")


if __name__ == "__main__":
    run(path_to_csv_with_urls='/home/inquisitor/ner_furniture/furniture_stores_pages.csv')