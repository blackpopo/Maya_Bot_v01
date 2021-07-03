from utilities.utilities import *
from utilities.katuyou import Katuyou

Open_Templates = ["どうすれば", "なんなん", "なんで", "どうして", "どうやって", "どうだろう", "なんだった", "何で", "どうなった", "何だろう", "何が"]

katuyou = Katuyou("./utilities/KatuyouCSVs")

def OpenQuestion(sentence, subject, conjunction, phrases, tokens, positions):
    apply = False
    statements = [is_completed(tokens, positions), is_question(tokens, positions)]
    res_sentence = ""
    if statements[0] == "uncompleted":
        if not conjunction and sentence.endswith('から.?。'):
            res_sentence = 'へー、そうなんだ。どうしてなの？'
        else:
            res_tokens, res_positions = uncompleted_builder(phrases)
            res_sentence = ''.join(res_tokens).replace('。', '？')
            #Todo change pronuoun
    elif not conjunction:
        res_sentence = is_opinion(phrases)
    else:
        pass
    if res_sentence != "":
        apply = True
    return sentence, apply, res_sentence

def is_opinion(phrases):
    statement = ""
    for j in range(len(phrases)):
        tokens, positions = phrases[j]
        for i, token, position in zip(range(len(tokens)), tokens, positions):
            if (position[0] == '形容詞' and position[6] in ['ほしい', '欲しい']):
                if (i + 1 < len(tokens) and positions[i+1][1] in ['格助詞', '並立助詞']) or (i + 2 < len(tokens) and positions[i+2][1] in ['格助詞', '並立助詞']):
                    pass
                else:
                    if j-1 >= 0 and (phrases[j-1][0][-1] in ["て", "で"] or phrases[j-1][1][0][0] == "名詞"):
                        if (j+1) < len(phrases):
                            tokens = tokens + phrases[j+1][0]
                            positions = positions + phrases[j+1][1]
                        flags = get_flags(tokens, positions, is_katuyou=True)
                        if flags['nai'] and flags['ta']:
                            statement = 'どうして、' + "".join(phrases[j-1][0]) + "ほしくなかったの？"
                        elif flags['nai']:
                            statement = 'どうして、' + "".join(phrases[j-1][0]) + "ほしくないの？"
                        elif flags['ta']:
                            statement = 'どうして、' + "".join(phrases[j-1][0]) + "ほしかったの？"
                        else:
                            statement = "どうして、" + "".join(phrases[j-1][0]) + "ほしいの？"
                        statement = statement.replace('ような', 'そんな')
                    else:
                        pass
            elif (position[0] == '動詞' and position[5] == '基本形' and  position[1] == '自立' and tokens not in ['ある', 'すぎる', 'なる', 'やる'] and i+1 < len(tokens) and tokens[i+1] == 'な'):
                if (i + 2 < len(tokens) and positions[i+2][1] in ['格助詞', '並立助詞']) or (i + 3 < len(tokens) and positions[i+3][1] in ['格助詞', '並立助詞']):
                    pass
                else:
                    base = katuyou.convert_base2te(token)
                    if base[-1] == "ん":
                        statement = 'どうして、' + base + 'ではいけないの？'
                    else:
                        statement = 'どうして、' + base + 'てはいけないの？'
            #今日は遊ぼう。
            elif position[0] == '助動詞' and token == 'う':
                if (i + 1 < len(tokens) and positions[i+1][1] in ['格助詞', '並立助詞']) or (i + 2 < len(tokens) and positions[i+2][1] in ['格助詞', '並立助詞']):
                    pass
                elif i - 1 >= 0 and tokens[i-1] in ['だろ', 'でしょ', 'あろ', 'なかろ']:
                    statement = 'どうして、そう思うの？'
                else:
                    if i - 1 >= 0 and tokens[i-1] != "しよ":
                        statement = 'いいね！それから？'
                    else:
                        pass
            #きっと、成功する信じている。
            elif (position[2] in ['引用', '連語'] or token in ['と', 'っと' ,'って'])  and j + 1 < len(phrases):
                if j + 1 < len(phrases):
                    post_tokens, post_positions = phrases[j+1]
                    bases = ['信じる', 'しんじる', '考える', 'かんがえる', '思う', 'おもう', '願う', 'ねがう']
                    tes = ['信じ', 'しんじ', '考え', 'かんがえ', '思っ', 'おもっ', '願っ', 'ねがっ']
                    for token,  position in zip(post_tokens, post_positions):
                        if position[6] in ['信じる', 'しんじる', '考える', 'かんがえる', '思う', 'おもう', '願う', 'ねがう']:
                            flags = get_flags(post_tokens, post_positions, is_katuyou=True)
                            if flags['reru']:
                                pass
                            elif flags['nai'] and flags['ta']:
                                statement = 'どうして、そう' + tes[bases.index(position[6])] + "てなかったの？"
                            elif flags['nai']:
                                statement = 'どうして、そう' + tes[bases.index(position[6])] + "てないの？"
                            elif flags['ta']:
                                statement = 'どうして、そう' + tes[bases.index(position[6])] + "てたの？"
                            else:
                                statement = "どうして、そう" + tes[bases.index(position[6])] + "てるの？"
                else:
                    pass

            #絶対に、あきらめまい。
            elif position[0] == '助動詞' and (position[4] == '特殊・タイ' or token == 'まい'):
                flags = get_flags(tokens, positions)
                if flags['nai'] and flags['ta']:
                    statement = "どうして、" + "".join(tokens[:i]) + 'たくなかったの？'
                elif flags['ta']:
                    statement = "どうして、" + "".join(tokens[:i]) + 'たかったの？'
                elif flags['nai']:
                    statement = "どうして、" + "".join(tokens[:i]) + 'たくないの？'
                else:
                    statement = "どうして、" + "".join(tokens[:i]) + 'たいの？'
            elif position[0] == '助動詞' and position[4] in ['特殊・ナイ', '特殊・ヌ']:
                if i+1 < len(tokens) and tokens[i+1] == 'ば':
                    if i + 3 < len(positions) and positions[i + 2][6] in ['なる', 'いく', 'なれる', 'いける'] and (
                            positions[i + 3][4] == '特殊・ナイ' or positions[i + 3][4] == '特殊・ヌ' or tokens[i + 3] == 'ませ'):
                        flags = get_flags(tokens, positions)
                        if flags['reru'] and flags['ta']:
                            statement = 'どうして、' + tokens[i-2] + 'れなければいけなかったの？'
                        elif flags['reru']:
                            statement = 'どうして、' + tokens[i-2] + 'れなければいけないの？'
                        elif flags['ta']:
                            statement = 'どうして、' + tokens[i-1] + 'ないといけなかったの？'
                        else:
                            statement = 'どうして、' + tokens[i-1] + 'ないといけないの？'
                else:
                    pass
            elif token in ['て', "で"]:
                #すぐに行動してくれよ。#Todo Write Template on User Demands
                if i+2 < len(tokens) and positions[i+1][6] in ['くださる', '下さる', 'くれる'] and tokens[i+2] in [ '？', 'ない', 'よ']:
                    statement = "ごめんね。できないんだ。"
                elif j+1 < len(phrases) and phrases[j+1][0][0] in ['ちょうだい', '頂戴']:
                    statement = "ごめんね。できないんだ。"
                #諦めてはいけない。
                elif i+1 < len(tokens) and tokens[i+1] == 'は':
                    if j + 1 < len(phrases) and phrases[j+ 1][1][0][6] in ['なる', 'いく', 'なれる', 'いける']:
                        post_tokens, post_positions = phrases[j+1]
                        flags = get_flags(post_tokens, post_positions)
                        if flags['ta']:
                            statement = "どうして、" +  "".join(tokens) + post_tokens[0] + "なかったの？"
                        else:
                            statement = "どうして、"+  "".join(tokens) + post_tokens[0] +  "ないの？"
                else:
                    statement = ""
            # 見なくちゃいけない。
            elif token == 'ちゃ' or token == 'じゃ':
                if i + 2 < len(positions) and positions[i+1][6] in ['なる', 'いく', 'いける', 'なれる'] and (positions[i + 2][4] == '特殊・ナイ' or positions[i + 2][4] == '特殊・ヌ' or tokens[i + 2] == 'ませ'):
                    flags = get_flags(tokens, positions)
                    if flags['ta']:
                        statement = "どうして、" +  "".join(tokens[:i+2]) + "なかったの？"
                    else:
                        statement = "どうして、"+  "".join(tokens[:i+2])  +  "ないの？"
                    statement = statement.replace('ちゃ', 'ては').replace('じゃ', 'では')
                else:
                    pass
            # #続けるべきだ。Todo wish
            elif position[0] == '動詞' and '命令' in position[5] and i + 1 < len(tokens) and tokens[i+1] == '。':
                if token in ['ください', '下さい']:
                    statement = 'もちろんだよ。'
                else:
                    statement = "ごめんね。できないんだ。"
            elif position[0] == '助動詞' and token in ['べき', 'べから'] and i + 1 < len(tokens):
                flags = get_flags(tokens, positions)
                if tokens[i+1] == 'で' and i+2 < len(tokens) and tokens[i+2] == 'は':
                    if flags['ta']:
                        statement = 'どうして、' + ''.join(tokens[:i+1]) + 'ではなかったの？'
                    else:
                        statement = 'どうして、' + ''.join(tokens[:i+1]) + 'ではないの？'
                else:
                    if flags['ta']:
                        statement = 'どうして、' + ''.join(tokens[:i+1]) + 'だったの？'
                    else:
                        statement = 'どうして、' + ''.join(tokens[:i+1]) + 'なの？'
            # #諦めることだけは出来ない。
            elif (j  == len(phrases) -1 or j == len(phrases) -2):
                if position[0] == '助詞' and token in ['こそ', 'さえ', 'しか', 'だって', 'のみ', 'ばかし', 'ばかり', 'ばっか', 'だけ', 'なんか', 'かも', 'だに', \
                                                'くらい', 'ばっかり', 'まで', '迄']:
                    statement = 'へぇー、そうなんだね。どうしてなの？'
                # #諦めないことは良いことだ。
                elif position[0] == '助動詞':
                    if position[6] == 'かもしれない':
                        statement = 'へぇー、そうなんだ。どうしてなの？'
                    elif  position[6] in ['いい', 'よい', '良い', 'わるい', '悪い', 'むずかしい', '難しい']:
                        statement = 'へぇー、そうなんだ。どんなところが？'
                    elif position[1] == '非自立' and position[6] in ['やすい', 'がたい', 'にくい', 'づらい', 'よい', 'イイ', '良い', '難い', 'いい']:
                        statement = 'へぇー、そうなんだ。どんなところが？'
                    else: #Judge in Emotional Recognition.
                        pass
                elif position[0] == '名詞':
                    if token in ['最高', '最良']:
                        statement = 'よかったね！どんなところが、' + token + 'だったの？'
                    elif token in ['最低', '最悪', 'ダメ', '駄目', 'だめ']:
                        statement = 'たいへんだね。どんなところが、' + token + 'だったの？'
                    else:
                        pass
                else:
                    pass
            else:
                pass
    return statement

def is_question(tokens, positions):
    question_flag = False
    open_flag = False
    open_tokens = ['なに', '何故', '何', '何故', 'どうして', 'どう', 'どういう', 'なにゆえ', '誰', '何処',
                   'どこ', 'いくつ', 'いつ', 'どちら', '何時', 'なんで', '何で', '如何', 'なん', '何か', "なぜ"]
    for i, token, position in zip(range(len(tokens)-1, 0, -1), tokens[::-1], positions[::-1]):
        if token == '？':
            question_flag = True
        elif token in ["かぁ", "かい", "かも", "かしら", "かな"]: #かしら・かな・かも
            question_flag = True
        elif position[0] == '終助詞' or token in ["。"]:
            pass
        else:
            break

    for i, token, position in zip(range(len(tokens)), tokens, positions):
        if token in open_tokens:
            open_flag = True
        elif open_flag and token == 'も':
            open_flag = False
        else:
            pass

    if open_flag:
        return "open"
    elif question_flag:
        return "close"
    else:
        return 'affirmative'

def is_completed(tokens, positions):
    if len(positions) > 1 and positions[-2][0] == "助詞" and positions[-2][1] not in  ["終助詞", "副助詞／並立助詞／終助詞", "副助詞"]:
        return 'uncompleted'
    return 'completed'

def uncompleted_builder(res_list):
    tokens, positions = res_list[-1] #最後の文節
    if (positions[0][0] == '名詞' and tokens[0] not in ['の', 'ん']) or positions[0][0] == '連体詞' \
            or (1 < len(tokens) and positions[0][0] == '接頭詞' and positions[1][0] == '名詞'):
        is_cut, tokens, positions = cutter(tokens, positions, False)
    elif positions[0][0] == '動詞' or (
            1 < len(tokens) and positions[0][0] == '接頭詞' and positions[1][0] == '動詞'):
        is_cut, tokens, positions = cutter(tokens, positions, True)
    elif positions[0][0] == '形容詞' or (
            1 < len(tokens) and positions[0][0] == '接頭詞' and positions[1][0] == '形容詞'):
        is_cut, tokens, positions = cutter(tokens, positions, True)
    else:
        is_cut = False
    res_tokens, res_positions = pre_adder(res_list, 1, tokens, positions, is_cut)
    return res_tokens, res_positions

if __name__=="__main__":
    from Preprocess import Preprocess
    sentences = read_lines()
    for sentence in sentences:
        sentence, apply, subject, conjunction, phrases, tokens, positions = Preprocess(sentence)
        OpenQuestion(sentence, apply, conjunction, phrases, tokens, positions)
