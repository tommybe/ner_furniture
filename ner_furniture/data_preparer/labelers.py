LABELS_LIST = ["0", "B-product", "I-product"]
LABELS_IDS = [0, 1, 2]


class WordLabeler:

    def label_loop(self, websites: dict) -> list:
        websites_labels = []
        for main_website, inner_websites in websites.items():
            website_labels = []
            for inner_website_name, inner_website_content in inner_websites.items():
                website_labels.extend(self._single_website_label(inner_website_name, inner_website_content))
            websites_labels.extend(website_labels)
        return websites_labels

    def _single_website_label(self, website_name: str, website_content: str) -> list:
        website_name_words = website_name.lower().split()
        # TODO -find better way get treat commas as separate words in website class
        website_content_words = [word.lower().replace(',', '') for word in website_content]

        labels = [LABELS_IDS[0]] * len((website_content_words))
        labels = self._mark_first_word(website_name_words, website_content_words, labels)
        labels = self._mark_inner_words(website_name_words, website_content_words, labels)
        return labels

    def _mark_first_word(self, website_name_words: str, website_content_words: str, labels: list) -> list:
        labels = [LABELS_IDS[1] if word in website_name_words else label for (label, word) in
                  zip(labels, website_content_words)]
        return labels

    # todo - possibility to make it faster through recurency on already non-zero labels
    def _mark_inner_words(self, website_name_words: str, website_content_words: str, labels: list) -> list:
        for i in range(1, len(labels)):
            if labels[i - 1] > 0 and website_content_words[i] in website_name_words:
                labels[i] = LABELS_IDS[2]
        return labels


class WordPieceLabeler:

    def label_loop(self, subword_tokens: list, word_labels: list) -> list:
        subword_labels = []
        for subwords, label in zip(subword_tokens, word_labels):
            if label > LABELS_IDS[0]:
                subword_labels.append(self._prepare_single_label(label, subwords))
            else:
                subword_labels.append([LABELS_IDS[0]] * len(subwords))

        return subword_labels

    def _prepare_single_label(self, label: int, subwords: str) -> list:
        subwords_labels = []
        if label == LABELS_IDS[1]:
            subwords_labels = [LABELS_IDS[1]] + [LABELS_IDS[2]] * (len(subwords) - 1)
        else:
            subwords_labels = [LABELS_IDS[2]] * len(subwords)
        return subwords_labels
