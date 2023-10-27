import logging
from re import split

from transformers import pipeline

from ner_furniture.data_preparer.websites_scrapper import Scrapper


class ProductsExtractor:
    def __init__(self, tokenizer, bert_model):
        self.nlp = pipeline("ner", model=bert_model, tokenizer=tokenizer, aggregation_strategy="first")

    def get_products(self, url: str):
        print(url)
        website_content = Scrapper(url).get_content()
        website_content = website_content.lower()
        all_sentences = split('[\n|\.]', website_content)

        all_entities = []
        for sentence in all_sentences:
            predictions = self.nlp(sentence)
            all_entities.extend(self._extract_entities(predictions))

        unique_entities = list(set(all_entities))
        logging.info(f'Products on {url} websites: {unique_entities}')
        return unique_entities

    def _extract_entities(self, predictions):
        all_entities = []
        this_entity = []
        for prediction in predictions:
            if (prediction['entity_group'] == 'LABEL_2' and len(this_entity) > 0) or \
                    prediction['entity_group'] == 'LABEL_1':
                this_entity.append(prediction['word'])
            if prediction['entity_group'] == 'LABEL_0':
                if len(this_entity) > 1:
                    all_entities.append(' '.join(this_entity))
                this_entity = []
        return all_entities
