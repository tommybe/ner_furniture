from transformers import AutoTokenizer

from ner_furniture.commons import BERTMODEL, DO_LOWER_CASE

MAX_TOKEN_LENGTH = 64


class TokenEncoder:

    def create(self, tokens_set: dict, label_only_first_word=True):
        tokenizer = AutoTokenizer.from_pretrained(BERTMODEL, do_lower_case=DO_LOWER_CASE)
        tokens_set['tokens'] = tokenizer(tokens_set['tokens'], padding=True, truncation=True, max_length=64,
                                         is_split_into_words=True)
        tokens_set['labels'] = self._update_labels(tokens_set['tokens'], tokens_set['labels'], label_only_first_word)
        return tokens_set

    def _update_labels(self, encoded_tokens, old_labels, label_only_first_word):
        '''based on https://huggingface.co/docs/transformers/tasks/token_classification &
        https://www.freecodecamp.org/news/getting-started-with-ner-models-using-huggingface/
        primary token label passed to all subtokens'''
        total_adjusted_labels = []
        for k in range(0, len(encoded_tokens["input_ids"])):
            prev_word_id = -1
            word_ids_list = encoded_tokens.word_ids(batch_index=k)
            existing_label_ids = old_labels[k]
            adjusted_label_ids = []
            i = -1

            for word_id in word_ids_list:
                if (word_id is None):
                    adjusted_label_ids.append(-100)
                elif (word_id != prev_word_id):
                    i = i + 1
                    adjusted_label_ids.append(existing_label_ids[i])
                    prev_word_id = word_id
                else:
                    if label_only_first_word:
                        adjusted_label_ids.append(-100)
                    else:
                        adjusted_label_ids.append(existing_label_ids[i])

            total_adjusted_labels.append(adjusted_label_ids)

        return total_adjusted_labels
