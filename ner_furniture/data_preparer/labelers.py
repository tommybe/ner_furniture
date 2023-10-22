from transformers import AutoTokenizer
import re

LABELS_LIST = ["0", "B-product", "I-product"]
LABELS_IDS = [0, 1, 2]


class WordLabeler:

    def label_loop(self, websites: dict) -> list:
        websites_labels = {}
        for main_website, inner_websites in websites.items():
            websites_labels[main_website] = {}
            for inner_website_name, inner_website_content in inner_websites.items():
                websites_labels[main_website][inner_website_name] = self._single_website_label(inner_website_name,
                                                                                               inner_website_content)
        return websites_labels

    def _single_website_label(self, website_name: str, website_content: str) -> list:
        website_name_words = website_name.lower().split()
        website_content_words = [word.lower().split() for word in website_content]

        labels = [LABELS_IDS[0]] * len((website_content_words))
        labels = self._mark_first_word(website_name_words, website_content_words, labels)
        labels = self._mark_inner_words(website_name_words, website_content_words, labels)
        return labels

    def _mark_first_word(self, website_name_words: str, website_content_words: str, labels: list) -> list:
        first_product_word = website_name_words[0]
        labels = [LABELS_IDS[1] if word == first_product_word else label for (label, word) in
                  zip(labels, website_content_words)]
        return labels

    # todo - possibility to make it faster through recurency on already non-zero labels
    def _mark_inner_words(self, website_name_words: str, website_content_words: str, labels: list) -> list:
        inner_product_word = website_name_words[1:]
        for i in range(1, len(labels)):
            if labels[i - 1] > 0 and website_content_words[i] in inner_product_word:
                labels[i] = LABELS_IDS[2]
        return labels


class WordPieceLabeler:

    def label_loop(self, subword_tokens: list, word_labels: list) -> list:
        subword_labels = []

        return subword_labels

    # def _single_website_label(self, website_name: str, website_content: str) -> list:
    #     website_name_words = website_name.lower().split()
    #     website_content_words = [word.lower().split() for word in website_content]
    #
    #     labels = [LABELS_IDS[0]] * len((website_content_words))
    #     labels = self._mark_first_word(website_name_words, website_content_words, labels)
    #     labels = self._mark_inner_words(website_name_words, website_content_words, labels)
    #     return labels
    #
    # def _mark_first_word(self, website_name_words: str, website_content_words: str, labels: list) -> list:
    #     first_product_word = website_name_words[0]
    #     labels = [LABELS_IDS[1] if word == first_product_word else label for (label, word) in
    #               zip(labels, website_content_words)]
    #     return labels
    #
    # # todo - possibility to make it faster through recurency on already non-zero labels
    # def _mark_inner_words(self, website_name_words: str, website_content_words: str, labels: list) -> list:
    #     inner_product_word = website_name_words[1:]
    #     for i in range(1, len(labels)):
    #         if labels[i - 1] > 0 and website_content_words[i] in inner_product_word:
    #             labels[i] = LABELS_IDS[2]
    #     return labels
