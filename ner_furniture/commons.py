from re import split
from typing import Tuple

BERTMODEL = 'distilbert-base-uncased'  # to check bert-base-uncased, https://huggingface.co/docs/transformers/tasks/token_classification
DO_LOWER_CASE = True
TRAIN_VAL_TEST_SHARES = [0.7, 0.2, 0.1]

LABELS_LIST = ['O', 'B-PRODUCT', 'I-PRODUCT']
LABELS_IDS = [0, 1, 2]
MIN_NO_OF_LETTERS_IN_SENTENCE = 8
MAX_NO_OF_LETTERS_IN_SENTENCE = 256

def split_content_into_sentences(websites: dict) -> dict:
    for main_website, inner_websites in websites.items():
        for inner_website_name, inner_website_content in inner_websites.items():
            all_sentences = split('[\n|\.]', inner_website_content)
            sentences_with_suff_len = [sentence[:MAX_NO_OF_LETTERS_IN_SENTENCE] for sentence in all_sentences if
                                       len(sentence) > MIN_NO_OF_LETTERS_IN_SENTENCE]
            websites[main_website][inner_website_name] = sentences_with_suff_len
    return websites


def split_tokens_data_on_train_val_test(tokens_data: dict) -> Tuple[dict, dict, dict]:
    no_of_words = len(tokens_data['labels'])
    split_points = [0,
                    int(no_of_words * TRAIN_VAL_TEST_SHARES[0]),
                    int(no_of_words * (TRAIN_VAL_TEST_SHARES[0] + TRAIN_VAL_TEST_SHARES[0])),
                    no_of_words + 1
                    ]
    train_set = {'tokens': tokens_data['tokens'][split_points[0]:split_points[1]],
                 'labels': tokens_data['labels'][split_points[0]:split_points[1]]}
    val_set = {'tokens': tokens_data['tokens'][split_points[1]:split_points[2]],
               'labels': tokens_data['labels'][split_points[1]:split_points[2]]}
    test_set = {'tokens': tokens_data['tokens'][split_points[2]:split_points[3]],
                'labels': tokens_data['labels'][split_points[2]:split_points[3]]}
    return train_set, val_set, test_set


def flatten_tokens_data(tokens_data: dict) -> dict:
    tokens_data['tokens'] = [subword for word in tokens_data['tokens'] for subword in word]
    tokens_data['labels'] = [sublabel for label in tokens_data['labels'] for sublabel in label]
    return tokens_data
