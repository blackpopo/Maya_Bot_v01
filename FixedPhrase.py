import csv

from utilities.utilities import *
import re


class FixedPhraseClass():
    def __init__(self):
        self.file_names = ['utilities/CSV/Personal.csv']
        csv_files = [open(file_name, "r", encoding="utf-8") for file_name in self.file_names]
        readers = [list(csv.reader(csv_file)) for csv_file in csv_files]
        self.fixed_phrases = list()
        for csv_name, reader in zip(self.file_names, readers):
            for row in reader:
                if len(row) != 2:
                    raise ValueError("Incorrect CSV format in {} at {}".format(csv_name, " ".join(row)))
                self.fixed_phrases.append([re.compile(row[0]), row[1]])


    def FixedPhrase(self, sentence):
        apply = False
        if isquote(sentence):
            return sentence, apply
        for word, response in self.fixed_phrases:
            if word.search(sentence):
                sentence = response
                apply = True
        return sentence, apply