from ner_furniture.data_preparer.labelers import WordLabeler


class WordSplitter:
    """
    Class responsible for creating words and labels from dict with scrappered website data.
    Stricly related from returns from Crawler class.
    """

    def __init__(self, websites: dict):
        self.websites = websites
        self.labeler = WordLabeler()

    def run(self) -> list:
        all_sentences = []
        all_labels = []
        for inner_website in self.websites.values():
            for website_name, sentences in inner_website.items():
                sentences_by_words = [sentence.lower().split(' ') for sentence in sentences]
                all_sentences.extend(sentences_by_words)
                sentence_by_labels = self.labeler.label_sentences(website_name, sentences_by_words)
                all_labels.extend(sentence_by_labels)

        return all_sentences, all_labels

    def labelize(self) -> list:
        return self.labeler.label_loop(self.websites)

    def _extract_sentences(self, websites: dict) -> list:
        all_sentences = []
        for inner_website in websites.values():
            for sentences in inner_website.values():
                all_sentences.extend(sentences)
        return all_sentences
