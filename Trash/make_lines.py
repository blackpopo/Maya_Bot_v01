import os

def make_lines():
    dir = '../utilities/FEELINGS'
    files = os.listdir(dir)
    with open('../utilities/feelings2line.csv', 'w') as f:
        for file in files:
            f.write(file.split('.')[0] + '\n')

if __name__=='__main__':
    make_lines()