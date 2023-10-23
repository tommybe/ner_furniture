import torch

class TransformerDataset(torch.utils.data.Dataset):
    #https://huggingface.co/transformers/v3.2.0/custom_datasets.html
    def __init__(self, raw_set:dict):
        self.tokens = raw_set['tokens']
        self.labels = raw_set['labels']

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.tokens.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)