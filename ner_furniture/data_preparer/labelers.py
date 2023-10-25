from ner_furniture.commons import LABELS_IDS

class WordLabeler:

    def label_sentences(self, website_name: str, words_from_sentences: list) -> list:
        website_name_words = website_name.lower().split()
        all_labels = []

        for words_from_sentence in words_from_sentences:
            labels = [LABELS_IDS[0]] * len((words_from_sentence))
            labels = self._mark_first_word(website_name_words, words_from_sentence, labels)
            labels = self._mark_inner_words(website_name_words, words_from_sentence, labels)
            all_labels.append(labels)
        return all_labels

    def _mark_first_word(self, website_name_words: str, website_content_words: str, labels: list) -> list:
        labels = [LABELS_IDS[1] if word in website_name_words else label for (label, word) in
                  zip(labels, website_content_words)]
        return labels

    # todo - possibility to make it faster through reccurency on already non-zero labels
    def _mark_inner_words(self, website_name_words: str, website_content_words: str, labels: list) -> list:
        for i in range(1, len(labels)):
            if labels[i - 1] > 0 and website_content_words[i] in website_name_words:
                labels[i] = LABELS_IDS[2]
        return labels
