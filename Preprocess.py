from utilities.utilities import *
from utilities.phrase_utilitie import split_parts

import re
last_sentence = re.compile("^[。？！].+?[。？！]")

adjunct_particles = ["からには", "から", "ので", "さかい", "んで"]

adjunct_conjunctions = ["なので", "だから", "ですから", "だからこそ", "ゆえに", "故に", "そやさかい", "よって", "従って", "したがって", "んで"]

ends = re.compile("[。？！]$")

def Preprocess(sentence):
    if not ends.search(sentence):
        sentence = sentence + '。'
    apply = False
    sentence = sentence[::-1] + "。"
    re_sentence = last_sentence.search(sentence)
    sentence = re_sentence.group()
    sentence = sentence[::-1][1:]
    tokens, positions = mecab_parse(sentence)
    conjunction, hearsay, tokens, positions = sentence_extractor(tokens, positions) #重要そうな部分の抜き出し
    if hearsay:
        apply = True
        sentence = 'へぇー、そうなんだ。それから？'
    phrases = phrase_separator(tokens, positions) #文節分け
    subject  = subject_extractor(phrases) #主語の抜き出し
    return sentence, apply, subject, conjunction, phrases, tokens, positions

def phrase_separator(tokens, positions):
    phrases = split_parts(tokens, positions)
    return phrases

def subject_extractor(phrases):
    subject = ""
    for i, phrase in enumerate(phrases):
        phrase_tokens, phrase_positions = phrase
        for j, token, position in zip(range(len(phrase_tokens)), phrase_tokens, phrase_positions):
            if token == "は"or (token == "が" and position[1] == "格助詞"):
                if j > 0 and phrase_positions[j-1][0] in ["助詞", "助動詞"]:
                    subject = "".join(phrases[i][0][:j-1])
                else:
                    subject = "".join(phrases[i][0][:j])

    return subject

def sentence_extractor(tokens, positions):
    conjunction = False #順接かどうか？
    independent_flag = False #接続助詞のあとに文があるがどうか
    start_position = 0 #抜き出すときのスタートのインデックス。
    pre_start_position = 0
    is_shifted = False #切断するかどうか。
    hearsay_flag = False

    if (len(tokens) > 1 and tokens[-2] in ["から", "っと", "って"]) or (len(tokens) > 2 and tokens[-3] in ["から", "っと", "って"]):
        hearsay_flag = True
        return conjunction, hearsay_flag, tokens, positions


    for i, token, position in zip(range(len(tokens)), tokens, positions):
        if position[6] in ['よう', 'そう', 'みたい', 'らしい'] and (position[0] in ['名詞', '助動詞']):
            hearsay_flag = True
            start_position = i + 1; independent_flag = False; is_shifted = True
        elif position[0] == "接続詞":
            start_position = i + 1; independent_flag = False; is_shifted = True
            if token in adjunct_conjunctions:
                conjunction = True
            else:
                pass
        elif (token in ["て", "で"] or (position[0] == "動詞" and position[5] == "連用形")) and i + 1 < len(tokens) and tokens[i + 1] in ["、", 'は', "も"]:
            if (i + 2) < len(tokens) and positions[i+2][1] != '自立':
                pass
            else:
                start_position = i + 1; independent_flag = False; is_shifted = True
        elif position[1] == "接続助詞":
            if i + 1 < len(tokens) and positions[i + 1][4] in ["特殊・ダ", "特殊・デス"]:
                pass
            elif token in adjunct_particles:
                start_position = i + 1; independent_flag = False; is_shifted = True
                conjunction = True
            else:
                if token  in ["て", "で", 'ば', 'ちゃ', 'じゃ']:
                    pass
                elif token == 'と' and i + 1 < len(tokens) and positions[i+1][6] in ['なる', 'いく', 'なれる', 'いける']:
                    pass
                else:
                    start_position = i + 1; independent_flag = False; is_shifted = True
        elif position[0] == '助動詞' and (token == 'たら' or token == 'だら' or token == 'なら') and i + 1 < len(tokens) and tokens[i+1] not in ["。", "ば"]:
             start_position = i + 1; independent_flag = False; is_shifted = True
        elif token in ["ため", "為"]:
            if i + 1 < len(tokens) and tokens[i + 1] == 'の':
                pass
            else:
                conjunction = True
                start_position = i + 1; independent_flag = False; is_shifted = True

        else:
            if is_shifted:
                if position[0] == '助詞' or position[0] == '記号' or position[0] == '助動詞' or \
                                       (position[0] == '名詞' and (token == 'の' or token == 'ん')): #切る位置をずらす場合。
                    start_position = start_position + 1; independent_flag = False
                else:
                    independent_flag = True
                    hearsay_flag = False
                    pre_start_position = start_position
                    is_shifted = False
            else:
                hearsay_flag = False
                independent_flag = True
                is_shifted = False

    if independent_flag:
        res_tokens, res_positions = tokens[start_position:], positions[start_position:]
    else:
        res_tokens, res_positions = tokens[pre_start_position:], positions[pre_start_position:]

    return conjunction, hearsay_flag, res_tokens, res_positions

if __name__=="__main__":
    # sentences = read_lines()
    sentences = ["高校に入ってからだ。", ]
    for sentence in sentences:
        print(Preprocess(sentence))

    # sentences = ["高校生からだし。", "殿下を誑し込む為だろうが。"]
    # for sentence in sentences:
    #     tokens, positions = mecab_parse(sentence)
    #     conjunction, tokens, positions = sentence_extractor(tokens, positions) #重要そうな部分の抜き出し
    #     print(tokens)

