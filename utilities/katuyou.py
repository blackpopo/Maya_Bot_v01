from collections import defaultdict

import os

class Katuyou:
    def __init__(self, base_dir):
        self.base2te = defaultdict(str)
        self.te2base = defaultdict(str)
        self.base2renyou = defaultdict(str)
        self.renyou2base = defaultdict(str)
        self.meirei2base = defaultdict(str)
        self.base2meirei = defaultdict(str)
        self.base2mizen = defaultdict(str)
        self.mizen2base = defaultdict(str)
        self.base2u = defaultdict(str)
        self.u2base = defaultdict(str)
        self.base2ta = defaultdict(str)
        self.ta2base = defaultdict(str)
        self.files = os.listdir(base_dir)

        base_dict = {'base2te.txt':self.base2te, 'te2base.txt': self.te2base, 'base2renyou.txt': self.base2renyou,
                     'renyou2base.txt': self.renyou2base, 'base2meirei.txt': self.base2meirei, 'meirei2base.txt': self.meirei2base,
                     'mizen2base.txt': self.mizen2base, 'base2mizen.txt': self.base2mizen, 'base2u.txt': self.base2u,
                     'u2base.txt': self.u2base, 'base2ta.txt': self.base2ta, 'ta2base.txt': self.ta2base}
        for file in self.files:
            rev_file = '2'.join(reversed(str(file).rstrip('.txt').split('2'))) + '.txt'
            with open(os.path.join(base_dir, file), "r", encoding="utf-8") as f:
                lines = f.readlines()
            #2つkeyがある場合には下のほうが優先。
            for line in lines:
                key, value = line.rstrip('\n').split('\t')
                base_dict[file][key] = value
                base_dict[rev_file][value] = key
    ############ base ################################################

    def convert_base2te(self, tokens):
        return self.base2te[tokens] if tokens in self.base2te.keys() else tokens

    def convert_te2base(self, tokens):
        return self.te2base[tokens] if tokens in self.te2base.keys() else tokens

    def convert_base2renyou(self, tokens):
        return self.base2renyou[tokens] if tokens in self.base2renyou.keys() else tokens

    def convert_renyou2base(self, tokens):
        return self.renyou2base[tokens] if tokens in self.renyou2base.keys() else tokens

    def convert_base2meirei(self, tokens):
        return self.base2meirei[tokens] if tokens in self.base2meirei.keys() else tokens

    def convert_meirei2base(self, tokens):
        return self.base2renyou[tokens] if tokens in self.base2renyou.keys() else tokens

    def convert_base2mizen(self, tokens):
        return self.base2mizen[tokens] if tokens in self.base2mizen.keys() else tokens

    def convert_mizen2base(self, tokens):
        return self.mizen2base[tokens] if tokens in self.mizen2base.keys() else tokens

    def convert_u2base(self, tokens):
        return self.u2base[tokens] if tokens in self.u2base.keys() else tokens

    def convert_base2u(self, tokens):
        return self.base2u[tokens] if tokens in self.base2u.keys() else tokens

    def convert_base2ta(self, tokens):
        return self.base2ta[tokens] if tokens in self.base2ta.keys() else tokens

    def convert_ta2base(self, tokens):
        return self.ta2base[tokens] if tokens in self.ta2base.keys() else tokens

    ###############################################################################################3

    ############ mizen2 ##############################################
    def convert_mizen2renyou(self, tokens):
        return self.base2renyou[self.mizen2base[tokens]] if tokens in self.mizen2base.keys() else tokens

    def convert_mizen2u(self, tokens):
        return self.base2u[self.mizen2base[tokens]] if tokens in self.mizen2base.keys() else tokens

    def convert_mizen2te(self, tokens):
        return self.base2te[self.mizen2base[tokens]] if tokens in self.mizen2base.keys() else tokens

    def convert_mizen2meirei(self, tokens):
        return self.base2meirei[self.mizen2base[tokens]] if tokens in self.mizen2base.keys() else tokens

    def convert_mizen2ta(self, tokens):
        return self.base2ta[self.mizen2base[tokens]] if tokens in self.mizen2base.keys() else tokens

    ############ renyou2 ################################################
    def convert_renyou2meirei(self, tokens):
        return self.base2meirei[self.renyou2base[tokens]] if tokens in self.renyou2base.keys() else tokens

    def convert_renyou2mizen(self, tokens):
        return self.base2mizen[self.renyou2base[tokens]] if tokens in self.renyou2base.keys() else tokens

    def convert_renyou2u(self, tokens):
        return self.base2renyou[self.renyou2base[tokens]] if tokens in self.renyou2base.keys() else tokens

    def convert_renyou2te(self, tokens):
        return self.base2te[self.renyou2base[tokens]] if tokens in self.renyou2base.keys() else tokens

    def convert_renyou2ta(self, tokens):
        return self.base2ta[self.renyou2base[tokens]] if tokens in self.renyou2base.keys() else tokens

    ############ u2 ##############################################

    def convert_u2mizen(self, tokens):
        return self.base2mizen[self.u2base[tokens]] if tokens in self.u2base.keys() else tokens

    def covert_u2renyou(self, tokens):
        return self.base2renyou[self.u2base[tokens]] if tokens in self.u2base.keys() else tokens

    def convert_u2meirei(self, tokens):
        return self.base2meirei[self.u2base[tokens]] if tokens in self.u2base.keys() else tokens

    def convert_u2te(self, tokens):
        return self.base2te[self.u2base[tokens]] if tokens in self.u2base.keys() else tokens

    def convert_u2ta(self, tokens):
        return self.base2ta[self.u2base[tokens]] if tokens in self.u2base.keys() else tokens

    ############ te2 ################################################
    def convert_te2mizen(self, tokens):
        return self.base2mizen[self.te2base[tokens]] if tokens in self.te2base.keys() else tokens

    def convert_te2renyou(self, tokens):
        return self.base2renyou[self.te2base[tokens]] if tokens in self.te2base.keys() else tokens

    def convert_te2meirei(self, tokens):
        return self.base2meirei[self.te2base[tokens]] if tokens in self.te2base.keys() else tokens

    def convert_te2u(self, tokens):
        return self.base2u[self.te2base[tokens]] if tokens in self.te2base.keys() else tokens

    def convert_te2ta(self, tokens):
        return self.base2ta[self.te2base[tokens]] if tokens in self.te2base.keys() else tokens

    ############ ta2 ###################################################
    def convert_ta2mizen(self, tokens):
        return self.base2mizen[self.ta2base[tokens]] if tokens in self.ta2base.keys() else tokens

    def convert_ta2renyou(self, tokens):
        return self.base2renyou[self.ta2base[tokens]] if tokens in self.ta2base.keys() else tokens

    def convert_ta2meirei(self, tokens):
        return self.base2meirei[self.ta2base[tokens]] if tokens in self.ta2base.keys() else tokens

    def convert_ta2u(self, tokens):
        return self.base2u[self.ta2base[tokens]] if tokens in self.ta2base.keys() else tokens

    def convert_ta2te(self, tokens):
        return self.base2te[self.ta2base[tokens]] if tokens in self.ta2base.keys() else tokens

    ############ meirei2 ##############################################
    def convert_meirei2mizen(self, tokens):
        return self.base2mizen[self.meirei2base[tokens]] if tokens in self.meirei2base.keys() else tokens

    def convert_meirei2renyou(self, tokens):
        return self.base2renyou[self.meirei2base[tokens]] if tokens in self.meirei2base.keys() else tokens

    def convert_meirei2ta(self, tokens):
        return self.base2ta[self.meirei2base[tokens]] if tokens in self.meirei2base.keys() else tokens

    def convert_meirei2u(self, tokens):
        return self.base2u[self.meirei2base[tokens]] if tokens in self.meirei2base.keys() else tokens

    def convert_meirei2te(self, tokens):
        return self.base2te[self.meirei2base[tokens]] if tokens in self.meirei2base.keys() else tokens