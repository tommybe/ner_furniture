import json
import logging
from typing import NoReturn

import click

from ner_furniture.commons import split_tokens_data_on_train_val_test
from ner_furniture.model_trainer.dataset_creator import TransformerDataset
from ner_furniture.model_trainer.model_fine_tuner import ModelFineTuner
from ner_furniture.model_trainer.token_encoder import TokenEncoder

logging.basicConfig(level=logging.INFO)


def run_bert_fine_tuning(tokens_data: dict) -> NoReturn:
    logging.info('Create train, val and test sets')
    train_set, val_set, test_set = split_tokens_data_on_train_val_test(tokens_data)

    logging.info('Tokenize train, val and test sets')
    train_set = TokenEncoder().create(train_set, label_only_first_word=False)
    val_set = TokenEncoder().create(val_set, label_only_first_word=False)

    logging.info('Create train, val and test Dataset class')
    train_set = TransformerDataset(train_set)
    val_set = TransformerDataset(val_set)

    logging.info('Start of model fine-tuning')
    ModelFineTuner().train(train_set, val_set)


@click.command(help="Script to fine-tune BERT model for NER problem")
@click.option("--path_to_json_tokens_dataset", type=str, required=True, help="Path to json file with tokens and labels")
def run(path_to_json_tokens_dataset: str) -> NoReturn:
    f = open(path_to_json_tokens_dataset)
    tokens_data = json.load(f)

    run_bert_fine_tuning(tokens_data)


def main():
    run(auto_envvar_prefix="AWS_DOC_SUPPORTER")


if __name__ == "__main__":
    run()
