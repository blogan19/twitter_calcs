import random
import re
import pandas as pd


class Random_cream():
    def __init__(self):
        super().__init__()
        df = pd.read_csv('datasets/creams_list.csv')
        random_cream = df.iloc[random.randint(0,df.shape[0])]
        self.drug = random_cream['drug'].title()
        self.dose = random_cream['frequency_description']
        self.form = random_cream['c_form']
        self.strength = random_cream['c_strength']


class Random_tablet():
    def __init__(self):
        super().__init__()
        #Read csv and drop drugs that aren't PRN 
        df = pd.read_csv('datasets/tablet_list.csv')
        df = df[df['prn'] == "N"]
        random_tablet = df.iloc[random.randint(0,df.shape[0])]

        self.drug = random_tablet['drug'].title()
        self.tablet_strength = random_tablet['c_strength']
        self.dose = random_tablet['primary_dose']
        self.unit = random_tablet['primary_dose_description']
        self.tablet_strength_int = int(re.sub('\D','', random_tablet['c_strength']))
        self.route = random_tablet['route']
        self.frequency = random_tablet['frequency_description']
        self.pack_size = random_tablet['du_cont']
        self.bnf = random_tablet['name']