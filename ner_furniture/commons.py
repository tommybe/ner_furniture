from random import sample
from re import split
from typing import Tuple

TRAIN_WEBSITES_SHARE = 0.7
BERTMODEL = 'bert-base-uncased'  # to check distilbert-base-uncased, https://huggingface.co/docs/transformers/tasks/token_classification
DO_LOWER_CASE = True
TRAIN_VAL_TEST_SHARES = [0.7,0.2,0.1]


def split_content_into_words(tokens_data: dict) -> dict:
    for main_website, inner_websites in websites.items():
        for inner_website_name, inner_website_content in inner_websites.items():
            websites[main_website][inner_website_name] = split('\s', inner_website_content)
    return websites


def split_websites_on_train_val_test(tokens_data: dict) -> Tuple[dict, dict]:
    websites_names = list(websites.keys())
    training_websites_names = sample(websites_names, int(len(websites_names) * TRAIN_WEBSITES_SHARE))
    training_websites = dict((k, websites[k]) for k in training_websites_names)
    testing_websites = dict((k, websites[k]) for k in [x for x in websites_names if x not in training_websites_names])
    return training_websites, testing_websites
