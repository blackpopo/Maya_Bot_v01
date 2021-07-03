from utilities.utilities import *
import csv

class GreetingClass:
    def __init__(self):
        self.file_name = 'utilities/CSV/Greeting.csv'
        csv_file = open(self.file_name, "r", encoding="utf-8")
        self.reader = list(csv.reader(csv_file))

    def Greeting(self, sentence):
        apply = False
        if isquote(sentence):
            return sentence, apply
        for row in self.reader:
            if len(row) != 2:
                raise ValueError("Incorrect CSV format in Greeting.csv at {}".format(" ".join(row)))
            word, response = row[0], row[1]
            if word in sentence:
                sentence = response
                apply = True
                break
        return sentence, apply

if __name__=='__main__':
    sentence = 'こんにちは。'
    Greeting = GreetingClass()
    print(Greeting.Greeting(sentence))