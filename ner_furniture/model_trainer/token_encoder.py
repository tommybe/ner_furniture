from transformers import AutoTokenizer

from ner_furniture.commons import BERTMODEL, DO_LOWER_CASE


class TokenEncoder:

    def create(self, tokens_set: dict):
        tokenizer = AutoTokenizer.from_pretrained(BERTMODEL, do_lower_case=DO_LOWER_CASE)
        tokens_set['tokens'] = tokenizer(tokens_set['tokens'], padding=True, truncation=True,
                                         return_offsets_mapping=True)
        tokens_set['labels'] = self._update_labels(tokens_set['tokens'], tokens_set['labels'])
        return tokens_set

    def _update_labels(self, encoded_tokens, old_labels, label_only_first_word=True):
        '''based on https://huggingface.co/docs/transformers/tasks/token_classification &
        https://www.freecodecamp.org/news/getting-started-with-ner-models-using-huggingface/
        primary token label passed to all subtokens'''
        total_adjusted_labels = []
        for k in range(0, len(encoded_tokens["input_ids"])):
            prev_word_id = -1
            word_ids_list = encoded_tokens.word_ids(batch_index=k)
            existing_label_ids = old_labels[k]
            adjusted_label_ids = []

            for word_id in word_ids_list:
                if (word_id is None):
                    adjusted_label_ids.append(-100)
                elif (word_id != prev_word_id):
                    adjusted_label_ids.append(existing_label_ids)
                    prev_word_id = word_id
                else:
                    adjusted_label_ids.append(existing_label_ids)

            total_adjusted_labels.append(adjusted_label_ids)
        return total_adjusted_labels
