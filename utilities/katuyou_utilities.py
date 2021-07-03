import os
import csv

base2meirei, base2mizen, base2renyou, base2ta, base2te, base2u = list(), list(), list(), list(), list(), list()

def read_files(base_dir):
    files = os.listdir(base_dir)
    return [os.path.join(base_dir, file) for file in files]

def convert_base2katuyou(files):
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            temp_list = list()
            index_list = list()
            for i,  row in enumerate(rows):
                if i == len(rows) -1 or row[10] != rows[i+1][10]:
                    temp_list.append(row)
                    index_list.append(row[9])
                    assert len(temp_list) == len(index_list)
                    list_katuyou(temp_list, index_list)
                    temp_list = list()
                    index_list  = list()
                else:
                    temp_list.append(row)
                    index_list.append(row[9])

def list_katuyou(temp_list, index_list):
    base = temp_list[0][10]
    if '未然形' in index_list or '未然ウ接続' in index_list:
        if '未然ウ接続' in index_list:
            base2u.append(base + '\t' + temp_list[index_list.index('未然ウ接続')][0])
        else:
            base2u.append(base + '\t' + temp_list[index_list.index('未然形')][0])
        if '未然形' in index_list:
            base2mizen.append(base + '\t' + temp_list[index_list.index('未然形')][0])
        else:
            base2mizen.append(base + '\t' + temp_list[index_list.index('未然ウ接続')][0])

    if '連用形' in index_list or '連用タ接続' in index_list or '連用テ接続' in index_list:
        if '連用タ接続' in index_list:
            base2ta.append(base + '\t' + temp_list[index_list.index('連用タ接続')][0])
        else:
            if '連用テ接続' in index_list:
                base2ta.append(base + '\t' + temp_list[index_list.index('連用テ接続')][0])
            elif '連用形' in index_list:
                base2ta.append(base + '\t' + temp_list[index_list.index('連用形')][0])
            else:
                pass
        if '連用テ接続' in index_list:
            base2te.append(base + '\t' + temp_list[index_list.index('連用テ接続')][0])
        else:
            if '連用タ接続' in index_list:
                base2te.append(base + '\t' + temp_list[index_list.index('連用タ接続')][0])
            elif '連用形' in index_list:
                base2te.append(base + '\t' + temp_list[index_list.index('連用形')][0])
            else:
                pass
        if '連用形' in index_list:
            base2renyou.append(base + '\t' + temp_list[index_list.index('連用形')][0])
        else:
            if '連用タ接続' in index_list:
                base2renyou.append(base + '\t' + temp_list[index_list.index('連用タ接続')][0])
            elif '連用テ接続' in index_list:
                base2renyou.append(base + '\t' + temp_list[index_list.index('連用テ接続')][0])
            else:
                pass

    if '命令ｅ' in index_list or '命令ｒｏ' in index_list:
        if '命令ｅ' in index_list:
            base2meirei.append(base + '\t' + temp_list[index_list.index('命令ｅ')][0])
        else:
            base2meirei.append(base + '\t' + temp_list[index_list.index('命令ｒｏ')][0])

def save_files(save_dir):
    list_name = [base2u, base2mizen, base2ta, base2te, base2renyou, base2meirei]
    name = ['base2u', 'base2mizen', 'base2ta', 'base2te', 'base2renyou', 'base2meirei']
    for name, lists in zip(name, list_name):
        with open(os.path.join(save_dir, name + '.txt'), 'w', encoding='utf-8') as f:
            print('file: {} is written'.format(name + '.txt'))
            f.write('\n'.join(lists))

def main():
    files = read_files('Katuyou_Resource')
    convert_base2katuyou(files)
    save_files('C:/Users/Atsuya/PycharmProjects/Maya_v01_Development/utilities/KatuyouCSVs')

if __name__=='__main__':
    main()

