import MeCab
mecab = MeCab.Tagger()
import random
import os

def isquote(sentence):
    res_tokens, res_positions = mecab_parse(sentence)
    for i, token, position in zip(range(len(res_tokens)), res_positions, res_positions):
        if position[1] == "格助詞" and token in ["って", "と"]:
            return True
    return False

def mecab_parse(line):
    res_tokens, res_positions = list(), list()
    tokens_positions = mecab.parse(line).splitlines()
    for token_position in tokens_positions[:-1]:
        token, positions = token_position.split('\t')
        position = positions.split(',')
        res_tokens.append(token)
        res_positions.append(position)
    return res_tokens, res_positions

def read_lines():
    res_lines = list()
    src_dir = 'C://Users/Atsuya/Documents/Modern_Renai_Tanpen_norm1_mecab2'
    files = os.listdir(src_dir)
    files = random.choices(files, k=int(len(files)/15))
    for i, file in enumerate(files):
        print('{} % is finished...'.format(i/len(files)))
        with open(os.path.join(src_dir, file), 'r', encoding="utf-8") as f:
            lines = f.readlines()
        lines = [line.rstrip('\n') for line in lines]
        res_lines.extend(lines)
    random.shuffle(res_lines)
    return res_lines

def pre_suru(res_tokens, res_positions, res_list_element):
    tokens, positions = res_list_element
    if (positions[-1][0] == "名詞" and positions[-1][1] in ["一般","サ変接続"]) or positions[-1][0] == "副詞":
        res_tokens = [tokens[-1]] + res_tokens
        res_positions = [positions[-1]] + res_positions
    else:
        pass
    return res_tokens, res_positions


#非自立名詞の前はカオスだからソノで誤魔化す。
def pre_independent_noun(res_tokens, res_positions):
    noun = res_tokens[0]
    if noun in ['後', 'よう', '点', 'ため', '為']:
        res_tokens.insert(0, 'その')
        res_positions.insert(0, ['連体詞', '*', '*', '*', '*', '*', 'その', 'ソノ', 'ソノ'])
    elif noun in ["さ", "そう", 'の', 'ん']:
        pass
    else:
        res_tokens.insert(0, 'そういう')
        res_positions.insert(0, ['連体詞', '*', '*', '*', '*', '*', 'そういう', 'ソウイウ', 'ソウイウ'])
    return res_tokens, res_positions

#引前のブロックはpre_positions
def inyou_replacer(res_tokens, res_positions):
    verb_list = ['話す', 'はなす', 'いう', '言う', 'おっしゃる', 'おもう', '思う', '考える', 'かんがえる', 'しんじる', '信じる', 'する']
    if res_positions[0][6] in verb_list:
        res_tokens.insert(0, 'そう')
        res_positions.insert(0, ['副詞','助詞類接続','*','*','*','*','そう','ソウ','ソー'])
    return res_tokens, res_positions

def pre_zyosi_hukusi(res_tokens, res_positions, pre_list_element): #Repeat時の詳細
    tokens, positions = pre_list_element
    if positions[0][0] in ['助詞', '助動詞']:
        res_tokens.insert(0, 'そう')
        res_positions.insert(0, ['副詞', '助詞類接続', '*', '*', '*', '*', 'そう', 'ソウ', 'ソー'])
    elif positions[0][0] in ['副詞']:
        core_i = 0
        for i, token, position in zip(range(len(tokens)), tokens, positions):
            if position[0] == '副詞':
                core_i = i
            else:
                pass
        res_tokens = tokens[core_i:] + res_tokens
        res_positions = positions[core_i] + res_positions
    else:
        pass
    return res_tokens, res_positions

def pre_adder(res_list, level, res_tokens, res_positions, is_cut=False): #前の文節を付け足す。
    if len(res_list) > level and not is_cut:
        if res_positions[0][4] == 'サ変・スル' or res_positions[0][0] == '形容詞' and res_positions[0][6] in ['ない', '無い']:
            res_tokens, res_positions = pre_suru(res_tokens, res_positions, res_list[-level - 1])
        elif res_positions[0][6] in ['なさる', 'いたす', 'ちゃう', 'じゃう', 'くださる', 'しまう', 'やすい'
                                                                                '下さる',
                                     'なる', 'ほしい', 'いる', 'よる', 'しれる', 'ある']:
            pass
        else:
            pass
    if res_positions[0][0] == '名詞' and res_positions[0][1] in ['非自立', '接尾'] or res_tokens[0]=='よう':
        res_tokens, res_positions = pre_independent_noun(res_tokens, res_positions)
    if res_positions[0][0] == "動詞":
        res_tokens, res_positions = inyou_replacer(res_tokens, res_positions)
    if res_positions[0][0] == '動詞' and len(res_list) > level and not is_cut:
        res_tokens, res_positions = pre_zyosi_hukusi(res_tokens, res_positions, res_list[-level-1])
    else:
        pass
    return res_tokens, res_positions


def cutter(tokens, positions, is_katuyou):
    is_cut = False
    cut_i = len(tokens)
    if is_katuyou: #動詞 or 形容詞
        pass
    else:  #名詞
        noun_flag = False
        for i, token, position in zip(range(len(tokens) - 1, -1, -1), tokens[::-1], positions[::-1]):
            if position[0] == '名詞' and token not in ['の', 'ん']:
                noun_flag = True
            elif not noun_flag and position[0] in ['記号', '助詞', '助動詞']:
                pass
            elif noun_flag and token in ['の', 'な']:
                noun_flag = False
            elif noun_flag and position[0] in ['助詞', '助動詞']:
                cut_i = i
                break
            else:
                pass
    if cut_i < len(tokens): #文節の途中で区切ったかどうか。区切った場合は is_cut = True
        tokens = tokens[cut_i + 1:]
        positions = positions[cut_i + 1:]
        is_cut = True
    else:
        pass
    return is_cut, tokens, positions

def get_flags(tokens, positions, is_katuyou=True): #否定と過去の状態確認
    flags = {'nai': False, 'ta': False, 'reru': False}
    if is_katuyou:
        #じゃないは肯定
        for i, token, position in zip(range(len(tokens)), tokens, positions):
            if position[0] == '助動詞' and (position[4] in ['特殊・ナイ', '特殊・ヌ'] or token=='まい' or token=='へん' or token=='ん'):
                flags['nai'] = not flags['nai']
            elif token == 'ん' and i-1 >= 0 and (positions[i-1][0] == '動詞' or tokens[i-1] == 'な'):
                flags['nai'] = not flags['nai']
            elif (position[0] == '助詞' and token == 'じゃ' and i+1 < len(positions) and positions[i+1][4] in ['特殊・ナイ'])or \
                    (token == 'で' and i+1 < len(tokens) and tokens[i+1]== 'は'and
                     i+2 < len(positions) and positions[i+2][4] in ['特殊・ナイ'] and i+3 < len(tokens) and tokens[i+3] in ['か', 'の']):
                flags['nai'] = not flags['nai']
            elif position[4] == '特殊・タ' and position[5] == '基本形':
                flags['ta'] = True
            elif position[6] in ["ない", "無い"]:
                flags['nai'] = not flags['nai']
            elif position[6] in ['れる', 'られる']:
                flags['reru'] = True
            elif position[0] in ['助詞', '助動詞'] and i+1 < len(tokens) and positions[i+1][0] in ['形容詞', '動詞']:
                flags = {'nai': False, 'ta': False, 'reru': flags['reru']}
            else:
                pass
    else:
        double_not = False
        for i ,token ,position in zip(range(len(tokens)-1, -1, -1), tokens[::-1], positions[::-1]):
            if position[0] in ['名詞', '連体詞']:
                if token in ['の', 'ん']:
                    pass
                elif position[1] == '非自立' and i-1 >= 0 and positions[i-1][5] == '基本形':
                    pass
                else:
                    if i-1 >= 0 and positions[i-1][0] == '助動詞' and (positions[i-1][4] in ['特殊・ナイ', '特殊・ヌ'] or tokens[i-1]=='まい' or tokens[i-1]=='へん' or tokens[i-1]=='ん') and double_not:
                        flags['nai'] = True
                    break
            elif position[0] == '助動詞' and (position[4] in ['特殊・ナイ', '特殊・ヌ'] or token=='まい' or token=='へん' or token=='ん'):
                flags['nai'] = not flags['nai']
                double_not = True
            elif position[4] == '特殊・タ' and position[5] == '基本形':
                flags['ta'] = True
            elif (position[0] == '助詞' and token == 'じゃ' and i + 1 < len(positions) and positions[i + 1][4] in [
                '特殊・ナイ']) or (token == 'で' and i + 1 < len(tokens) and tokens[i + 1] == 'は' and
                              i + 2 < len(positions) and positions[i + 2][4] in ['特殊・ナイ']):
                flags['nai'] = not flags['nai']
                double_not = True
            elif position[6] in ["ない", "無い"]:
                flags['nai'] = not flags['nai']
            elif position[6] in ['れる', 'られる']:
                flags['reru'] = True
            elif position[0] in ['助詞', '助動詞'] and i+1 < len(tokens) and (positions[i+1][0] == '名詞' and positions[i+1][1] not in ['非自立']):
                flags = {'nai': False, 'ta': False, 'reru': flags['reru']}
            else:
                pass
    return  flags

