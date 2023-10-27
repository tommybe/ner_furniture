import logging
from threading import Thread
from typing import NoReturn

import click
from flask import Flask
from transformers import AutoModelForTokenClassification, AutoTokenizer

from ner_furniture.commons import BERTMODEL, DO_LOWER_CASE
from ner_furniture.product_predictor.products_extractor import ProductsExtractor

flask_app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


def run_product_extractor(path_to_bert_model: str, flask_host: str = '0.0.0.0', flask_port: int = 5000) -> NoReturn:
    tokenizer = AutoTokenizer.from_pretrained(BERTMODEL, do_lower_case=DO_LOWER_CASE)
    bert_model = AutoModelForTokenClassification.from_pretrained(path_to_bert_model)

    questioner = ProductsExtractor(tokenizer, bert_model)

    flask_app.add_url_rule("/get_products/<path:url>", "get_products", questioner.get_products)
    Thread(target=flask_app.run, kwargs={"host": flask_host, "port": flask_port, "debug": False}).start()


@click.command(help="Flask server responsible for delivering products from website.")
@click.option("--path_to_bert_model", type=str, required=True, help="Path to directory with vector db")
@click.option("--flask_host", type=str, default='0.0.0.0', help="Host for questioning flask server.")
@click.option("--flask_port", type=int, default=5000, help="Port for questioning flask server.")
def run(path_to_bert_model: str, flask_host: str, flask_port: int) -> NoReturn:
    run_product_extractor(path_to_bert_model, flask_host, flask_port)


def main():
    run(auto_envvar_prefix="AWS_DOC_QUESTIONER")


if __name__ == "__main__":
    run()
