from transformers import AutoTokenizer

from ner_furniture.data_preparer.labelers import WordLabeler

BERTMODEL = 'bert-base-uncased'  # to check distilbert-base-uncased, https://huggingface.co/docs/transformers/tasks/token_classification
MIN_NO_OF_LETTERS_IN_SENTENCE = 5


class WordTokenizer:
    """
    Class responsible for creating words tokens and labels from dict with scrappered website data.
    Stricly related from returns from Crawler class.
    """

    def __init__(self, websites: dict):
        self.tokenizer = AutoTokenizer.from_pretrained(BERTMODEL, do_lower_case=True)
        self.websites = websites
        self.is_split_into_words = False
        self.labeler = WordLabeler()

    def tokenize(self) -> list:
        sentences = self._extract_sentences(self.websites)
        tokens = [self.tokenizer.tokenize(s, is_split_into_words=self.is_split_into_words) for s in sentences]
        return tokens

    def labelize(self) -> list:
        return self.labeler.label_loop(self.websites)

    def _extract_sentences(self, websites: dict) -> list:
        just_sentences = []
        for inner_website in websites.values():
            for sentences in inner_website.values():
                just_sentences.extend(sentences)
        return just_sentences


class WordPieceTokenizer:
    """
    Class responsible for creating subwords tokens and labels from already existing words tokens and labels.
    Stricly related from returns from WordTokenizer class.
    """

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(BERTMODEL, do_lower_case=True)
        self.is_split_into_words = True
        self.labeler = WordLabeler()

    def tokenize(self, word_tokens: list) -> list:
        subword_tokens = [self.tokenizer.tokenize(s, is_split_into_words=self.is_split_into_words) for s in word_tokens]
        return subword_tokens

    def labelize(self, subword_tokens:list, word_labels:list) -> list:
        return self.labeler.label_loop(subword_tokens, word_labels)

    def _extract_sentences(self, websites: dict) -> list:
        just_sentences = []
        for inner_website in websites.values():
            for sentences in inner_website.values():
                just_sentences.extend(sentences)
        return just_sentences