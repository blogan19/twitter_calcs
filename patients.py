import names
import random
class patient: 
    def __init__(self):
        self.gender = random.choice(['male','female'])
        self.age = random.randint(18,100)
        self.weight = random.randint(40,100)
        self.name = names.get_first_name(gender=self.gender)
        self.creatinine = random.randint(40,300)
    
        if self.gender == 'male':
            self.possesive_pronoun = 'his'
            self.pronoun = 'he'
            self.noun = 'man'
        else:
            self.possesive_pronoun = 'her'
            self.pronoun = 'she'
            self.noun = 'woman'

class obese(patient):
    def __init__(self):
        super().__init__()
        self.weight = random.randint(100,200)

class child(patient):
    def __init__(self):
        super().__init__()
        self.age = random.randint(0,20)
        genders = ['male','female'] 
        g = random.choice([genders])
        self.gender = g