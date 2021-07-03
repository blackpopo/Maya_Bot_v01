import os
import csv
from utilities.utilities import *
from utilities.katuyou import Katuyou
from collections import defaultdict


class EmotionClass:
    def __init__(self, feeling_folder_path, line_file_path):
        self.feeling_foloder_path = feeling_folder_path
        self.line_file_path = line_file_path
        files = os.listdir(feeling_folder_path)
        self.feeling_dict = defaultdict(list) #key is file name, value is feelings
        self.line_dict = defaultdict(list) #key is file name, value is line
        self.katuyou = Katuyou('./utilities/KatuyouCSVs')
        for file in files:
            name = file.split('.')[0]
            with open(os.path.join(self.feeling_foloder_path, file), 'r', encoding="utf-8") as f:
                feelings = f.readlines()
            for feeling in feelings:
                feeling = feeling.rstrip('\n')
                if feeling.startswith('#') or feeling.startswith('-'):
                    pass
                else:
                    self.feeling_dict[name].append(feeling)

        with open(self.line_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            reader = csv.reader(lines)
            for row in reader:
                assert row[0] in self.feeling_dict.keys(), 'Not found file name at {}'.format(row[0])
                self.line_dict[row[0]] = row[1:]

    def current2past(self, current):
        escape_words = ['さすが', '流石', '立派', '知的', '頭', 'どうして', '素敵', '大丈夫', 'お疲れ様']
        for word in escape_words:
            if word in current:
                return current
        if 'がない' in current:
            current = current.replace('がない', 'がなかった')
        elif 'が無い' in current:
            current = current.replace('が無い', 'が無かった')
        elif 'なんだ' in current:
            current = current.replace('なんだ', 'だったんだ')
        elif 'いいん' in current:
            current = current.replace('いいん', 'よかったん')
        elif 'いん' in current:
            current = current.replace('いん', 'かったん')
        elif 'いね' in current:
            current = current.replace('いね', 'かったね')
        else:
            current = self._verb_cur2past(current)
        return current

    def _verb_cur2past(self, line): #動詞のやつを過去形に変換。
        tokens, positions = mecab_parse(line)
        res_line = ''
        for i, token, position in zip(range(len(tokens)-1, -1, -1), tokens[::-1], positions[::-1]):
            if position[0] == '助動詞' and i -1 >= 0 and (positions[i-1][0] not in ['動詞', '形容詞'] and tokens[i-1] not in ['ん']):
                token = self.katuyou.convert_base2ta(token)
                res_line = ''.join(tokens[:i]) + token  + 'たんだ' + res_line
                break
            elif position[0] in ['形容詞', '動詞']:
                token = self.katuyou.convert_base2ta(token)
                res_line = ''.join(tokens[:i]) + token + 'た' + res_line
                break
            else:
                res_line = token + res_line
        return res_line

    def Emotion(self, phrases):
        statement = ''
        apply = False
        if len(phrases) > 2:
            tokens = phrases[-3][0] + phrases[-2][0] + phrases[-1][0]
            positions = phrases[-3][1] + phrases[-2][1] + phrases[-1][1]
        elif len(phrases) == 2:
            tokens = phrases[-2][0] + phrases[-1][0]
            positions = phrases[-2][1] + phrases[-1][1]
        else:
            tokens, positions = phrases[-1]

        for i, token, position in zip(range(len(tokens)-1, -1, -1), tokens[::-1], positions[::-1]):
            if position[-1] in self.line_dict.keys():
                flag = get_flags(tokens[i:], positions[i:])
                if not flag['nai'] and not flag['reru']:
                    apply = True
                    statement = random.choice(self.line_dict[position[-1]])
                    if flag['ta']:
                        statement = self.current2past(statement)
                else:
                    pass
                break
        return statement, apply


    def passive_checker(self, tokens, positions):
        for i, token, position in zip(range(len(tokens)), tokens, positions):
            if position[0] == '動詞' and i + 2 < len(positions) and tokens[i + 1] in ['て', 'で'] \
                    and positions[i + 2][-3] in ['くださる', 'もらえる', 'くれる', 'もらう', '下さる']:
                return True
            elif position[0] == '動詞' and i + 1 < len(positions) and positions[i + 1][-3] in ['れる', 'られる', 'せる']:
                return True
            elif token in ['を'] and i + 1 < len(positions) and positions[i + 1][-3] in ['受ける', '迎える']:
                return True
            elif position[0] == '名詞' and position[1] not in ['非自立', '接尾']:
                return False
            return False

if __name__=='__main__':
    emotion = EmotionClass('utilities/FEELINGS', 'utilities/feelings2line.csv')
    from Preprocess import Preprocess
    sentences = read_lines()
    sentences = ['好きな男だった。']
    for sentence in sentences:
        sentence, apply, subject, conjunction, phrases, tokens, positions = Preprocess(sentence)
        print(phrases)
        print(emotion.Emotion(phrases))