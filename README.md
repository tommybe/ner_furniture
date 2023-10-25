# ner_furniture
NER model set on data from furnitures shop websites

## data_preparer
Module responsible for: 
 - scrapping websites from list
 - scrapping all websites connected (by link) with website from list which is about furniture
 - tokenize their content as words and subwords (WordPiece)
 - label it automatically based on website name. 
Result is json with tokens and labels, which is dumped to the the same directory as csv.
To run, use click command. Example:
```
python path_to/db_preparation_runner.py
--path_to_csv_with_urls='path to csv file with list of furniture websites'
```

## model_trainer
Module responsible for: 
 - loading results of data_preparer
 - split dataset into training, validation and testing sets
 - prepare datasets as Torch Dataset object
 - fine-tune BERT model. 
Result model dumped as fine_tune_bert.
To run, use click command. Example:
```
python path_to/bert_model_training_runner.py
--path_to_json_tokens_dataset='path to json file with tokens and labels'
```
Additionally, there is Colab notebook with dump to wandb (hard c&paste from classes in model_trainer directory).

## TODO
- got to parent site if basic site returns 404
- remove facebook, twitter, etc from scrapping pages
- find better way to filter out websites about furnitures (now it is based on furnitures_types.txt)
- deal with Trainer training_args
- add analysis of test dataset
- -stronger use commons.py in ProductExtractor
- -test model fine-tuned on label_only_first_word=False
