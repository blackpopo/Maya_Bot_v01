from collections import defaultdict
import os
import csv
from utilities import mecab_parse

def get_dir(katuyou_folder):
    file_names = ['Adj.csv', 'Auxil.csv', 'Verb.csv']
    adj_dic = defaultdict(list)
    auxil_dic = defaultdict(list)
    verb_dic = defaultdict(list)
    dicts = [adj_dic, auxil_dic, verb_dic]
    for file, dic in zip(file_names, dicts):
        with open(os.path.join(katuyou_folder, file), 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            temp_list = list()
            for i,  row in enumerate(rows):
                if i == len(rows) -1 or row[10] != rows[i+1][10]:
                    temp_list.append(row)
                    dic[row[10]] = temp_list
                    temp_list = list()
                else:
                    temp_list.append(row)
    return adj_dic, auxil_dic, verb_dic

def build_csv(feeling_dict, dicts):
    adj_dic, auxil_dic, verb_dic = dicts
    files = os.listdir(feeling_dict)
    res_lines = list()
    for file in files:
        name = file.split('.')[0]
        with open(os.path.join(feeling_dict, file), 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('-') or line.startswith('#'):
                    continue
                line = line.rstrip('\n')
                temp_token = ''
                temp_base_token = ''
                temp_kana_token = ''
                tokens, positions = mecab_parse(line)
                for i, token, position in zip(range(len(tokens)), tokens, positions):
                    if i == len(tokens) -1:
                        if position[0] in ['助動詞', '動詞', '形容詞']:
                            key = position[6]
                            katuyou_list = list()
                            if position[0] == '助動詞':
                                if key in auxil_dic.keys():
                                    katuyou_list = auxil_dic[key]
                            elif position[0] == '動詞':
                                if key in verb_dic.keys():
                                    katuyou_list = verb_dic[key]
                            elif position[0] == '形容詞':
                                if key in adj_dic.keys():
                                    katuyou_list = adj_dic[key]
                            else:
                                pass
                            for i, item in enumerate(katuyou_list): #item is csv row format token, pre_id, pos_id, ..., base, katagana, feeling 12 cols
                                item_copy = item.copy()
                                if item[10] in ['ない', '無い']:
                                    item_copy[4] = '形容詞'
                                    item_copy[5] = '自立'
                                    item_copy[8] = '形容詞・アウオ段'
                                elif item[10] in ['れる', 'られる']:
                                    item_copy[5] = '自立'
                                else:
                                    pass
                                item_copy[0] = temp_token + item[0]
                                item_copy[10] = temp_base_token + item[10]
                                item_copy[11] = temp_kana_token + item[11]
                                item_copy[12] = name
                                if int(item[3]) > 1000:
                                    item_copy[3] = 1000
                                res_lines.append(item_copy)
                                if key == 'する' or (key == 'れる' and temp_token[-1] == 'さ'):
                                    item_copy2 = item.copy()
                                    if item[10] in ['ない', '無い']:
                                        item_copy2[4] = '形容詞'
                                        item_copy2[5] = '自立'
                                        item_copy2[8] = '形容詞・アウオ段'
                                    elif item[10] in ['れる', 'られる']:
                                        item_copy2[5] = '自立'
                                    else:
                                        pass
                                    if key == 'する':
                                        temp_token2 = temp_token + 'を'
                                        temp_base_token2 = temp_base_token + 'を'
                                        temp_kana_token2 = temp_kana_token + 'ヲ'
                                    else:
                                        temp_token2 = temp_token[:-1] + 'をさ'
                                        temp_base_token2 = temp_base_token[:-1] + 'をさ'
                                        temp_kana_token2 = temp_kana_token[:-1] + 'ヲサ'
                                    item_copy2[0] = temp_token2 + item[0]
                                    item_copy2[10] = temp_base_token2 + item[10]
                                    item_copy2[11] = temp_kana_token2 + item[11]
                                    item_copy2[12] = name
                                    if int(item[3]) > 1000:
                                        item_copy2[3] = 1000
                                    res_lines.append(item_copy2)
                            temp_token, temp_base_token, temp_kana_token = '', '', ''

                        else:

                            temp_token += token
                            '''
                            名詞:一般:1285, 1285, 3000
                            名詞:サ変接続: ?
                            名詞:形容動詞互換:1287, 1287, 300
                            '''

                            if len(position) == 7: #1285, 1285, 3000
                                temp_base_token += token
                                temp_kana_token += token
                            else:
                                temp_base_token += position[-3]
                                temp_kana_token += position[-2]

                            item = [temp_token, 1287, 1287, 3000, '名詞', '形容動詞語幹', '*', '*', '*', '*', temp_base_token, temp_kana_token, name]
                            res_lines.append(item)
                            temp_token, temp_base_token, temp_kana_token = '', '', ''

                    else:
                        temp_token += token
                        temp_base_token += token
                        if len(position) == 7:
                            # temp_base_token += token
                            temp_kana_token += token
                        else:
                            # temp_base_token += position[-3]
                            temp_kana_token += position[-2]
    return res_lines


def main():
    katuyou_folder = 'C:/Users/Atsuya/PycharmProjects/Maya_v01_Development/utilities/Katuyou_Resource'
    dicts = get_dir(katuyou_folder)
    feelings_folder = 'C:/Users/Atsuya/PycharmProjects/Maya_v01_Development/utilities/FEELINGS'
    lines = build_csv(feelings_folder, dicts)
    with open('Katuyou_Resource/feeling.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for line in lines:
            assert len(line) == 13, ValueError('Invalid Line format at {} is {}'.format(','.join(line), len(line)))
            writer.writerow(line)


if __name__=='__main__':
    main()
