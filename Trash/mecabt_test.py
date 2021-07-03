import MeCab
tagger = MeCab.Tagger()

def CMD():
    while True:
        sentence = input("> ")
        parsed_items = tagger.parse(sentence).split("\n")[:-2]
        for parse_item in parsed_items:
            token, positions = parse_item.split("\t")
            print(token + "\t" + "".join(positions))

if __name__=="__main__":
    CMD()