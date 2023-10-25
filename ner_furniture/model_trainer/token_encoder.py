from transformers import AutoTokenizer

from ner_furniture.commons import BERTMODEL, DO_LOWER_CASE


class TokenEncoder:

    def create(self, tokens_set: dict):
        tokenizer = AutoTokenizer.from_pretrained(BERTMODEL, do_lower_case=DO_LOWER_CASE)
        tokens_set['tokens'] = tokenizer(tokens_set['tokens'], padding=True, truncation=True)
        tokens_set['labels'] = self._update_labels(tokens_set['tokens'], tokens_set['labels'])
        return tokens_set

    def _update_labels(self, encoded_tokens, old_labels):
        '''based on https://www.freecodecamp.org/news/getting-started-with-ner-models-using-huggingface/'''
        total_adjusted_labels = []
        for k in range(0, len(encoded_tokens["input_ids"])):
            prev_wid = -1
            word_ids_list = encoded_tokens.word_ids(batch_index=k)
            existing_label_ids = old_labels[k]
            adjusted_label_ids = []

            for wid in word_ids_list:
                if (wid is None):
                    adjusted_label_ids.append(-100)
                elif (wid != prev_wid):
                    adjusted_label_ids.append(existing_label_ids)
                    prev_wid = wid
                else:
                    adjusted_label_ids.append(existing_label_ids)

            total_adjusted_labels.append(adjusted_label_ids)
        return total_adjusted_labels
