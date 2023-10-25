from flask import Flask
import click
import logging
from typing import NoReturn
from threading import Thread
from ner_furniture.product_predictor.products_extractor import ProductsExtractor
from transformers import AutoModelForTokenClassification

flask_app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


def run_product_extractor(path_to_bert_model: str, flask_host: str = '0.0.0.0', flask_port: int = 5000) -> NoReturn:
    tokenizer = AutoModelForTokenClassification.from_pretrained(path_to_bert_model, local_files_only=True)

    questioner = ProductsExtractor(tokenizer)

    flask_app.add_url_rule("/get_products/<url>", "get_products", questioner.get_products)
    Thread(target=flask_app.run, kwargs={"host": flask_host, "port": flask_port, "debug": False}).start()


@click.command(help="Flask server responsible for delivering products from website.")
@click.option("--path_to_bert_model", type=str, required=True, help="Path to directory with vector db")
@click.option("--flask_host", type=str, required=False, help="Host for questioning flask server.")
@click.option("--flask_port", type=int, required=False, help="Port for questioning flask server.")
def run(path_to_bert_model: str, flask_host: str, flask_port: int) -> NoReturn:
    run_product_extractor(path_to_bert_model, flask_host, flask_port)


def main():
    run(auto_envvar_prefix="AWS_DOC_QUESTIONER")


if __name__ == "__main__":
    run()
