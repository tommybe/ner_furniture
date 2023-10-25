from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer
from ner_furniture.commons import BERTMODEL, DO_LOWER_CASE
from ner_furniture.model_trainer.custom_data_collator import DataCollator
from ner_furniture.commons import LABELS_IDS
from ner_furniture.model_trainer.evaluation_metrics import compute_metrics
from ner_furniture.model_trainer.dataset_creator import TransformerDataset

TRAINING_ARGS = TrainingArguments(
    output_dir="../../fine_tune_bert_models/fine_tune_bert",
    evaluation_strategy="steps",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_steps = 0.05,
)


class ModelFineTuner:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(BERTMODEL, do_lower_case=DO_LOWER_CASE)
        self.data_collator = DataCollator().create()
        self.model = AutoModelForTokenClassification.from_pretrained(BERTMODEL, num_labels=len(LABELS_IDS))

    def train(self, train_set: TransformerDataset, eval_set: TransformerDataset):
        trainer = Trainer(
            model=self.model,
            args=TRAINING_ARGS,
            train_dataset=train_set,
            eval_dataset=eval_set,
            data_collator=self.data_collator,
            tokenizer=self.tokenizer,
            compute_metrics=compute_metrics
        )
        trainer.train()
        return trainer
