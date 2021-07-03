from utilities.utilities import *
from Greeting import GreetingClass
from FixedPhrase import FixedPhraseClass
from Preprocess import Preprocess
from Repeating import Repeating
from EmotionalSummary import EmotionClass
from OpenQuestion import OpenQuestion
from Aizuchi import Aizuchi

def main(sentence = "", greeting=True, fixed_phrase=True, preprocess=True, repeating=True, emotional_summary=True,  open_question=True):
    Greeting = GreetingClass()
    FixedPhrase = FixedPhraseClass()
    Emotion = EmotionClass('utilities/FEELINGS', 'utilities/feelings2line.csv')

    while(True):
        if sentence == "":
            sentence = input('YOU : ')
        apply = False
        if not apply and preprocess:
            sentence, apply, subject, conjunction, phrases, tokens, positions = Preprocess(sentence)
        if not apply and  greeting:
            sentence, apply = Greeting.Greeting(sentence)
        if not apply and  fixed_phrase:
            sentence, apply = FixedPhrase.FixedPhrase(sentence)
        if not apply and  open_question:
            sentence, apply, res_sentence = OpenQuestion(sentence, subject, conjunction, phrases, tokens, positions)
        if not apply and  emotional_summary:
            res_sentence, apply = Emotion.Emotion(phrases)
        if not apply and repeating:
            sentence, apply = Repeating(sentence, apply, subject, conjunction, phrases, tokens, positions)
        if not apply:
            sentence = Aizuchi(sentence) #あいづちは必要最低限
        print('OUKA : ' + sentence)
        sentence = ""

def test():
    lines = read_lines()
    Greeting = GreetingClass()
    FixedPhrase = FixedPhraseClass()
    Emotion = EmotionClass('utilities/FEELINGS', 'utilities/feelings2line.csv')
    cnt = 0
    for sentence in lines:
        sentence, apply, subject, conjunction, phrases, tokens, positions = Preprocess(sentence)
        if not apply:
            sentence, apply = Greeting.Greeting(sentence)
        if not apply:
            sentence, apply = FixedPhrase.FixedPhrase(sentence)
        if not apply:
            sentence, apply, res_sentence = OpenQuestion(sentence, subject, conjunction, phrases, tokens, positions)
        if not apply:
            res_sentence, apply = Emotion.Emotion(phrases)
        if not apply:
            sentence, apply = Repeating(sentence, apply, subject, conjunction, phrases, tokens, positions)
            cnt += 1
        if not apply:
            sentence = Aizuchi(sentence) #あいづちは必要最低限
    print("{} % sentence is failed".format(cnt/ len(lines) * 100))



if __name__=="__main__":
    main("こんにちは。")
    # test()


