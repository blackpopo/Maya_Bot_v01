################### SPLIT PARTS #######################################################################################333
def parts_apply(pos, token, position, phrase_tokens, phrase_positions, res_list): #pos == none のときはtokenを保存せずに文節を保存。
    assert pos == 'pre' or pos == 'post' or pos == 'none', 'Parts Apply Position Incorrect at {}'.format(pos)
    if pos == 'pre': #単語のリストに入れて,文節のリストに保存。
        phrase_tokens.append(token)
        phrase_positions.append(position)
    if phrase_tokens != []:
        res_list.append((phrase_tokens, phrase_positions))
    phrase_tokens, phrase_positions = list(), list() #文節のリストの初期化
    if pos == 'post': #単語のリストに保存
        phrase_tokens.append(token)
        phrase_positions.append(position)
    return res_list, phrase_tokens, phrase_positions


def verb_check(i, token, position, tokens, positions):
    if position[0] == '動詞' or position[0] == '副詞'or position[0] == '助詞' or position[0] == '助動詞' or position[0] == '記号' \
            or (position[0] == '名詞' and (token[0] == 'の' or token[0] == 'ん')) \
            or (i + 1 < len(tokens) and position[0] == '接頭詞' and positions[i + 1][0] == '動詞'):
        return True
    else:
        return False


def adj_check(i, token, position, tokens, positions):
    if position[0] == '形容詞' or position[0] == '副詞' or position[0] == '助詞' or position[0] == '助動詞' or position[0] == '記号' \
            or (position[0] == '名詞' and (position[0] in ['接尾', '非自立'])) \
            or (i + 1 < len(tokens) and position[0] == '接頭詞' and positions[i + 1][0] == '形容詞') \
            or (i + 1 < len(tokens) and position[0] == '動詞' and positions[i + 1][1] == '非自立'):
        return True
    else:
        return False


def noun_check(i, token, position, tokens, positions):
    if position[0] == '名詞' or position[0] == '連体詞' or position[0] == '副詞' or position[0] == '助詞'  or position[
        0] == '助動詞' or position[0] == '記号' \
            or (i + 1 < len(tokens) and position[0] == '接頭詞' and positions[i + 1][0] == '名詞'):
        return True
    else:
        return False


def append_each_part(type, i, tokens, positions, phrase_tokens, phrase_positions, res_list): #形容詞・動詞・名詞の文節に分解する
    assert type == 'verb' or type == 'adj' or type == 'noun', 'Incorrect Type at {}'.format(type)
    if type == 'verb':
        flag_func = verb_check
    elif type == 'adj':
        flag_func = adj_check
    else:
        flag_func = noun_check
    token, position = tokens[i], positions[i]
    if phrase_tokens != []:
        res_list, phrase_tokens, phrase_positions = parts_apply('post', token, position, phrase_tokens,
                                                                phrase_positions, res_list)
        i += 1
    while i < len(tokens):
        token, position = tokens[i], positions[i]
        if flag_func(i, token, position, tokens, positions):
            if '終助詞' in position[1]:
                i, phrase_tokens, phrase_positions = split_end_particles(tokens, positions, i, phrase_tokens,
                                                                         phrase_positions)
            elif token == "は" or (position[1] == "格助詞" and positions[i+1][0] != "助詞"):
                if (i+1 < len(tokens) and positions[i+1][0] == "記号"): #ex)機能は、ありません。
                    phrase_tokens.append(token)
                    phrase_positions.append(position)
                    res_list, phrase_tokens, phrase_positions = parts_apply('pre', tokens[i+1], positions[i+1], phrase_tokens,
                                                                            phrase_positions, res_list)
                    i += 2
                else: #機能はありません。
                    res_list, phrase_tokens, phrase_positions = parts_apply('pre', token, position, phrase_tokens,
                                                                            phrase_positions, res_list)
                    i += 1
            elif position[0] == '記号':
                res_list, phrase_tokens, phrase_positions = parts_apply('pre', token, position, phrase_tokens,
                                                                        phrase_positions, res_list)
                i += 1
                break
            elif position[1] == "接続助詞" and type == "verb":
                if i + 2 < len(positions) and positions[i+1][0] == "助詞" and positions[i+2][1] == "自立":
                    phrase_tokens.append(token)
                    phrase_positions.append(position)
                    res_list, phrase_tokens, phrase_positions = parts_apply('pre', tokens[i+1], positions[i+1], phrase_tokens, phrase_positions, res_list)
                    i+=2
                elif  i + 1 < len(positions) and positions[i+1][1] == "自立":
                    res_list, phrase_tokens, phrase_positions = parts_apply('pre', token, position, phrase_tokens, phrase_positions, res_list)
                    i+=1
                else:
                    phrase_tokens.append(token)
                    phrase_positions.append(position)
                    i += 1
            else:
                phrase_tokens.append(token)
                phrase_positions.append(position)
                i += 1
        else:
            res_list, phrase_tokens, phrase_positions = parts_apply('none', token, position, phrase_tokens,
                                                                    phrase_positions, res_list)
            break
    return i, phrase_tokens, phrase_positions, res_list

def split_parts(tokens, positions): #大まかな文節分け
    i = 0
    res_list = list()
    phrase_tokens, phrase_positions = list(), list()

    while i < len(tokens):
        token, position = tokens[i], positions[i]
        if (position[0] == "動詞" and position[1] == "非自立" and i-1 > 0 and positions[i-1][0] != "動詞") or position[0] == '動詞' or (i + 1 < len(tokens) and position[0] == '接頭詞' and positions[i + 1][0] == '動詞'):
            i, phrase_tokens, phrase_positions, res_list = append_each_part('verb', i, tokens, positions, phrase_tokens,
                                                                            phrase_positions, res_list)
        elif position[0] == '形容詞' or (i + 1 < len(tokens) and position[0] == '接頭詞' and positions[i + 1][0] == '形容詞'):
            i, phrase_tokens, phrase_positions, res_list = append_each_part('adj', i, tokens, positions, phrase_tokens,
                                                                            phrase_positions, res_list)
        elif (position[0] == '名詞' and token not in ['の', 'ん']) or position[0] == '連体詞' or (i + 1 < len(tokens) and position[0] == '接頭詞' and positions[i + 1][0] == '名詞'):
            i, phrase_tokens, phrase_positions, res_list = append_each_part('noun', i, tokens, positions, phrase_tokens,
                                                                            phrase_positions, res_list)
        else:
            if '終助詞' in position[1]:
                i, phrase_tokens, phrase_positions = split_end_particles(tokens,
                                                                         positions, i,
                                                                         phrase_tokens,
                                                                         phrase_positions)
            elif position[0] == '記号':
                res_list, phrase_tokens, phrase_positions = parts_apply('pre', token,
                                                                        position,
                                                                        phrase_tokens,
                                                                        phrase_positions,
                                                                        res_list)
                i += 1
            else:
                phrase_tokens.append(token)
                phrase_positions.append(position)
                i += 1
    return res_list

def split_end_particles(tokens, positions, i, phrase_tokens, phrase_positions): #終助詞のところを整える
    token, position = tokens[i], positions[i]
    if 'か' in token:
        phrase_tokens.append('か')
        phrase_positions.append(['助詞', '副助詞／並立助詞／終助詞', '*', '*', '*', '*', 'か', 'カ', 'カ'])
        i += 1
    elif 'な' == token and i - 1 > 0 and positions[i - 1][0] == '動詞' and positions[i - 1][5] == '基本形':
        phrase_tokens.append(token)
        phrase_positions.append(position)
        i += 1
    else:
        while i < len(tokens):
            token, position = tokens[i], positions[i]
            if '終助詞' in position[1]:
                i += 1
                if token == 'な' or token == 'ね':
                    phrase_tokens.append(token)
                    phrase_positions.append(position)
                    break
            else:
                if (position[0] == '助詞' and position[2] != '引用') or position[0] == '助動詞':
                    i += 1
                else:
                    break
    return i, phrase_tokens, phrase_positions

if __name__=="__main__":
    from utilities import *
    test_line = "なぜならば。"
    tokens, positions = mecab_parse(test_line)
    print(split_parts(tokens, positions))