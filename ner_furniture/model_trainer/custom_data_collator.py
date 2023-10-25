from transformers import DataCollatorForTokenClassification, AutoTokenizer, DataCollatorWithPadding

from ner_furniture.commons import BERTMODEL, DO_LOWER_CASE


class DataCollator:
    def create(self):
        tokenizer = AutoTokenizer.from_pretrained(BERTMODEL, do_lower_case=DO_LOWER_CASE)
        return DataCollatorWithPadding(tokenizer)
