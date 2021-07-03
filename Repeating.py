def Repeating(sentence, apply, subject, conjunction, phrases, tokens, positions):
    apply = False
    tokens, positions = phrases[-1]
    start_position = -1
    end_position = -1
    for i, token, position in zip(range(len(tokens)), tokens, positions):
        if start_position >= 0 and (position[0] in ['名詞', '副詞'] or (position[0] == '助詞' and position[1] not in ['副助詞', '係助詞'])):
            end_position += 1
        elif start_position >= 0:
            end_position += 1
            if position[1] in ['係助詞']:
                start_position = -1
            break
        elif position[1] == '形容動詞語幹' and i + 1 < len(tokens) and tokens[i+1] == 'な':
            start_position = i
            end_position = i
        elif position[0] in ['名詞', '副詞', '連体詞', '接頭詞'] and position[1] not in ['非自立', '形容動詞語幹', '代名詞', '助詞類接続']:
            start_position = i
            end_position = i
        else:
            pass
    if start_position >= 0:
        apply = True
        sentence = ''.join(tokens[start_position: end_position])
    return sentence, apply

if __name__=='__main__':
    sentence = '黒髪の男子生徒。'
    from Preprocess import Preprocess
    sentence, apply, subject, conjunction, phrases, tokens, positions = Preprocess(sentence)
    print(tokens)
    Repeating(sentence, apply, subject, conjunction, phrases, tokens, positions)