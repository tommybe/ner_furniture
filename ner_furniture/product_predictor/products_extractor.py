import logging
from re import split

from ner_furniture.data_preparer.websites_scrapper import Scrapper
from ner_furniture.data_preparer.words_splitter import WordSplitter


class ProductsExtractor:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def get_products(self, url: str):
        website_content = Scrapper(url).get_content()
        all_sentences = split('[\n|\.]', website_content)
        sentences_by_words = WordSplitter().extract_words_from_sentence(all_sentences)

        tokens_set = self.tokenizer(sentences_by_words, padding=True, truncation=True, max_length=64,
                                    is_split_into_words=True)

        logging.info(f'Products on {url} websites:: {tokens_set}')
        return tokens_set
