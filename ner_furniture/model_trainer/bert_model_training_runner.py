import logging
from typing import NoReturn
import json
from datasets import load_dataset
from ner_furniture.model_trainer.dataset_creator import TransformerDataset
from ner_furniture.model_trainer.model_fine_tuner import ModelFineTuner

import click


from ner_furniture.commons import split_tokens_data_on_train_val_test, flatten_tokens_data

logging.basicConfig(level=logging.INFO)

PATH_TO_FURNITURES_TYPES = '/home/inquisitor/ner_furniture/furnitures_types.txt'
WEBSITES_SAMPLE_SIZE = 150


def run_bert_fine_tuning(tokens_data: dict) -> NoReturn:
    train_set, val_set, test_set = split_tokens_data_on_train_val_test(tokens_data)

    train_set = TransformerDataset(flatten_tokens_data(train_set))
    val_set = TransformerDataset(flatten_tokens_data(val_set))
    test_set = TransformerDataset(flatten_tokens_data(test_set))

    ModelFineTuner().train(train_set, val_set)

    print('!!!')




@click.command(help="Script to fine-tune BERT model for NER problem")
@click.option("--path_to_json_tokens_dataset", type=str, required=True, help="Path to json file with tokens and labels")
def run(path_to_json_tokens_dataset: str) -> NoReturn:
    f = open(path_to_json_tokens_dataset)
    tokens_data = json.load(f)

    # #TEST
    # dataset = load_dataset("wikiann", "bn", streaming=True)

    run_bert_fine_tuning(tokens_data)


def main():
    run(auto_envvar_prefix="AWS_DOC_SUPPORTER")


if __name__ == "__main__":
    run()
    #path_to_json_tokens_dataset='/home/inquisitor/ner_furniture/labeled_tokens_dataset.json'