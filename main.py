import random
import math
from typing import Optional
from patients import patient
from random_drugs import Random_cream, Random_tablet
from fastapi import FastAPI
from pydantic import BaseModel

# converts a frequency to text frequency and integer
def frequency_convert(freq):
    frequency_conversions = {
        'QDS': ("four times daily",4),
        '6H': ("6 hourly",4),
        "OM": ("each morning",1),
        "ON": ("each night",1),
        "BD": ("twice daily",2),
        "3H": ("three hourly",8),
        "4H": ("four hourly",6),
        "TDS": ("three times daily",3),
        "OD": ("once daily",1),
        "8H": ("eight hourly",3),
        "12H": ("twelve hourly",2),
        "Five times a day": ("five times daily",5),
        "Six times a day": ("six time daily",6),
        "2H": ("2 hourly",12)
    }
    dose = frequency_conversions.get(freq)
    if dose != None:
        return(dose)
    else:
        return(freq)

#Get a random amount of drug 
class randomAmount:
    # takes a unit and if None it returns a random unitype
    def __init__(self, unit, min, max, interval):
        self.min = min
        self.max = max
        self.interval = interval
        self.unit = unit       
    def generate_volume(self):
        #returns a random volume
        if self.unit == '': 
            self.unit = random.choice(['ml','L'])
        return (random.randrange(self.min,self.max,self.interval),self.unit)
    def generate_amount(self):
        #returns an amount
        if self.unit == '': 
            self.unit = random.choice(['microgram','mg','g'])
        return (random.randrange(self.min,self.max,self.interval),self.unit)


class ConcentrationConversion:
    drug_volume = randomAmount('ml',50,2500,50).generate_volume()
    #If random choice in - then question is in mg
    if random.choice([0,1]) == 0:        
        drug_amount = randomAmount('mg',10,2500,10).generate_amount()
        answer = (round((drug_amount[0]/drug_volume[0])/10,3),'%')
    else:
        drug_amount = randomAmount('g',10,2500,10).generate_amount()
        answer = (round(((drug_amount[0]/drug_volume[0])/10)*1000,2),'%')
    
    synonyms = random.choice(['You are asked to prepare a preparation that contains','A colleague hands you a solution containing', 'You are handed a prescription for'])
    question = f'{synonyms} {str(drug_amount[0]) + drug_amount[1]} drug of x dissolved in {str(drug_volume[0]) + drug_volume[1]} of water. What is the concentration expressed as %w/v?',answer


class AmountStrengths:
    drug_amount = randomAmount('mg',10,200,1).generate_amount()
    volume = randomAmount('ml',10,300,1).generate_volume()    
    answer = ({round((drug_amount[0] * volume[0])/10000,2)},'g')
    question = f'How many grams of drug are contained in a {volume[0]/10}{volume[1]} bottle of {drug_amount[0]}{drug_amount[1]}/mL concentration?'


class c1v2:
    drug_amount = randomAmount('g',10,100,5).generate_amount()
    volume = randomAmount('ml',50,950,50).generate_volume() 
    answer = (round(((drug_amount[0]/volume[0])*5)*1000,2),'mg')
    question = f'If a {volume[0]}ml bottle of a product contains {drug_amount[0]}g of ingredient A. How many milligrams of drug will be contained in one 5ml spoonful?'

class CreamDilution:
    cream = Random_cream()
    synonym1 = random.choice(['A formula','A prescription','A prescription for a patient'])
    synonym2 = random.choice(['calls for', 'requires','asks for'])
    drug_amount = randomAmount('mg',5,100,5).generate_amount()
    vehicle_amount = randomAmount('ml',5,250,5).generate_volume()
    answer = (round(((cream.strength/100) * drug_amount[0] / (drug_amount[0] + vehicle_amount[0]))*100,3),'%')
    question =  f'{synonym1} {synonym2} {drug_amount[0]}g of a {cream.strength}% {cream.drug} {cream.form} to be diluted with {vehicle_amount[0]}g of a vehicle. What is the resulting concentration %w/w?',answer

class SubstituteQuantities:
    perc1 = random.randrange(1,30,1)
    perc2 = random.randrange(1,10,1)
    volume = randomAmount('ml',50,500,50).generate_volume()
    answer = (round((perc2 * volume[0]/100) / (perc1/100),2),'ml')
    question = f'How much of a {perc1}% solution is required to manufacture {volume[0]}ml of a {perc2}% solution?'

class ConcentratedWaters:
    volume = randomAmount('ml',100,500,10).generate_volume()
    c = random.choice([1,2,3])
    answer =''
    if c == 1:
        question = f'How much concentrated chloroform (mls) is required to produce {volume[0]}ml of single strengh chlorform water?'
        answer = ( 1/40 * volume[0],'ml')
    elif c == 2:
        volume = volume[0]/100
        answer = (round(1/20 * volume*1000,2),'ml')
        question = f'How much concentrated chloroform (mls) is required to produce {volume}L of double strength chloroform water?'
    elif c == 3:
        answer  = (volume[0]/10 * 39,'ml')
        question = f'How much water needs to be added to a {round(volume[0]/10,0)}ml solution of concentration chloroform water to produce a single strength chloroform water?'

class dilution: 
    volume = randomAmount('ml',100,300,50).generate_volume()
    percentage = random.randrange(11,20,1)
    percentagePost = random.randrange(1,10,1)
    answer = (((percentage * volume[0])/percentagePost) - volume[0], 'ml')
    question = f'How much water needs to be added to {volume[0]}ml of a {percentage}% v/v solution to reduce it to a {percentagePost}% v/v solution?'

class formulations:
    ingredientA = randomAmount('g',5,300,5).generate_amount()
    ingredientB = randomAmount('g',5,300,5).generate_amount()
    ingredientC = randomAmount('%',50,500,5).generate_amount()
    ingredientD = randomAmount('g',5,300,5).generate_amount()
    ingredientE = randomAmount('mg',5,300,3).generate_amount()
    waterto = randomAmount('ml',5,500,5).generate_volume()
    totalAmount = randomAmount('ml',5,1500,5).generate_volume()

    ingredientChoice = random.choice(['Ingredient A','Ingredient B','Ingredient C','Ingredient D','Ingredient E'])
    
    answer = None
    if ingredientChoice == 'Ingredient A':
        answer = round((ingredientA[0]/waterto[0])*totalAmount[0],2)
        answer = (answer,'g')
    elif ingredientChoice == 'Ingredient B':
        answer = round((ingredientB[0]/waterto[0])*totalAmount[0],2)
        answer = (answer,'g')
    elif ingredientChoice == 'Ingredient C':
        #NEED TO CALCULATE ANSWER TO THIS
        answer = (ingredientC[0]/100) * totalAmount[0]
    elif ingredientChoice == 'Ingredient D':
        answer = round((ingredientD[0]/waterto[0])*totalAmount[0],2)
        answer = (answer,'g')
    elif ingredientChoice == 'Ingredient E':        
        answer = round(((ingredientE[0]/waterto[0])*totalAmount[0]),2)
        answer = (answer,'mg')
    question = f'You have a formula for a solution:\nIngredient A:{ingredientA[0]}{ingredientA[1]} \nIngredient B:{ingredientB[0]}{ingredientB[1]}\nIngredient C: {ingredientC[0]/10}{ingredientC[1]}\nIngredient D:{ingredientD[0]}{ingredientD[1]}\nIngredient E:{ingredientE[0]}{ingredientE[1]}\nWater to {waterto[0]}{waterto[1]}\nHow much of {ingredientChoice} is required to make {totalAmount[0]}{totalAmount[1]} of the solution?'

class halfLives:
    halfLife = random.randrange(1,8,1)
    plasmaConc = randomAmount('mg/L',50,5000,5).generate_amount()
    timeElapsed = random.randrange(12,72,1)
    #half lives elapsed 
    halfLivesElapsed = timeElapsed//halfLife

    #conc after closest half lives 
    conc1 = plasmaConc[0]/ 2**halfLivesElapsed
    conc2 = plasmaConc[0] / 2**(halfLivesElapsed+1)

    answer = (round(conc1 - ((conc1-conc2) * (timeElapsed - halfLivesElapsed*halfLife)/halfLife),2),'mg/L')    
    question = f'Drug X has a half life of {halfLife} hours. If the initial plasma level of drug is {plasmaConc[0]}mg/L. What will its plasma level be after {timeElapsed} hours?'

class increasingPercentageSolution:
    initialVolume = randomAmount('ml',50,250,25).generate_volume()
    percentage1 = random.randrange(20,100,5)/10
    percentage2 = random.randrange(150,300,5)/10
    answer = (round(((100-percentage1) * initialVolume[0]) / (100-percentage2),2),'ml')
    question = f'How much of ingredient A should be added to {initialVolume[0]}ml of a {percentage1}% solution v/v to increased its strength to {percentage2}%v/v?'


class mixingConcentrations: 
    volumeA = randomAmount('ml',50,250,25).generate_volume()   
    volumeB = randomAmount('ml',50,250,25).generate_volume()   
    percentage1 = random.randrange(2,300,5)/10
    percentage2 = random.randrange(2,300,5)/10

    answer = (round(((percentage1/100)*volumeA[0] + (percentage2/100)*volumeB[0]) / (volumeA[0] + volumeB[0]) * 100,2),'ml')
    question = f'{volumeA[0]}{volumeA[1]} of a {percentage1}% solution is mixed with {volumeB[0]}{volumeB[1]} of {percentage2}% solution. What is the resulting strength % v/v?'

class multipleDilutions:
    volumeA = randomAmount('ml',3000,20000,125).generate_volume()   
    volumeB = randomAmount('ml',20,290,10).generate_volume()
    volumeC = randomAmount('ml',300,1500,25).generate_volume()   
    concentration =  random.randrange(10,100,5)/10
    answer = (round((((concentration/100)*volumeC[0]) * volumeA[0] )/ volumeB[0],2),'ml')
    question = f'What amount of substance is required to make {volumeA[0]/10}ml of a product so that {volumeB[0]}ml diluted to {volumeC[0]}ml will give a {concentration}% v/v concentration?'

class percentageStrengths:
    volumeA = randomAmount('ml',1500,20000,50).generate_volume() 
    percentage = random.randrange(10,40,1)/10
    answer = (round((percentage/100) * (volumeA[0]/10),2),'g')
    question = f'How much grams of drug x is contained in {volumeA[0]/10}{volumeA[1]} of a {percentage} v/v concentration?'

class prescriptions:
    drug = Random_tablet()
    frequency = frequency_convert(drug.frequency)
    course_length = random.choice([28, 56, 84, 112, 30, 32,21])
    dose = drug.dose.replace(",","")    
    answer = (int((float(dose)/drug.tablet_strength_int) * frequency[1] * course_length),'tablets')
    question = f'{drug.drug} is prescribed at a dose of {dose}{drug.unit} {frequency[0]}. How many {drug.tablet_strength} tablets will need to be supplied to cover a period of {course_length} days'

class prescriptionDoseTitration:
    #calculate number of tablets needed for a titrating course 
    drug = Random_tablet()
    days_interval = random.choice([7, 14, 21, 28])
    dose = drug.dose.replace(",","") 
    dose = float(dose)

    frequency = frequency_convert(drug.frequency)
    
    answer = int((float(dose)/drug.tablet_strength_int) * frequency[1] * days_interval)
    answer2 = int((float(dose*2)/drug.tablet_strength_int) * frequency[1] * days_interval)
    answer3 = int((float(dose*4)/drug.tablet_strength_int) * frequency[1] * days_interval)
    answer = (answer + answer2 + answer3,'tablets')
    question = f'Drug x is prescribed as {dose}{drug.unit} {frequency_convert(frequency[0])}. After {days_interval} days the dose is increased to {dose*2}{drug.unit} {frequency[0]}. After another {days_interval} days the dose is increased to {dose *4}{drug.unit} to be reviewed in {days_interval}. How many {drug.tablet_strength} tablets need to be supplied to provide cover for the entire course?'


class eyeDrops:
    drop_no = random.choice([2,3,4])
    frequency = random.choice(['2H','BD','TDS','QDS','6H','Five times a day','Six times a day'])
    container_size = random.choice([2.5,3,5,8,10,15])
    course_length = random.choice([28, 56, 84, 112, 30, 32,21])
    question = f'A course of eye drops is prescribed at a dose of {drop_no} drops {frequency_convert(frequency)[0]}. Each bottle contains {container_size}ml. How many bottles are required to provide cover for {course_length} days? (assuming 1 drop = 20ml)'
    answer = (math.ceil(((drop_no * frequency_convert(frequency)[1])/20) * course_length / container_size),'bottles')
    
class ratioStrengths:
    part = random.randrange(50,500,50)
    volume = randomAmount('ml',50,500,25).generate_volume()
    question = f'How many grams of sodium chloride are in {volume[0]}{volume[1]} of a 1 part in {part} w/v concentration?'
    answer = (round(1/part * volume[0],2),'g')

#Driver class to create a question either randomly or predefined
class Calculation:
    def __init__(self, random_selected):
        #dictiontary contains question objects
        question_types = {
            "concentration_Conversion":ConcentrationConversion(),
            "cream_dilution": CreamDilution(),
            "amount_strengths": AmountStrengths(),
            "c1v2": c1v2(),
            "substitute_quantities": SubstituteQuantities(),
            "concentrated_waters": ConcentratedWaters(),
            "dilution": dilution(),
            "formulations": formulations(),
            "half_lives": halfLives(),
            "increasing_percentage_solution": increasingPercentageSolution(),
            "mixing_concentrations": mixingConcentrations(),
            "multiple_dilutions": multipleDilutions(),
            "percentage_strengths":percentageStrengths(),
            "prescriptions": prescriptions(),
            "prescriptionDoseTitration": prescriptionDoseTitration(),
            "eyeDrops": eyeDrops(),
            "ratioStrengths": ratioStrengths()
        }
        #self.questionType = list(question_types.values())
        if random_selected == 'random':
            self.questionType = random.choice(list(question_types))
            self.question = question_types[self.questionType]
        else:
            self.question = question_types[random_selected]
            self.questionType = random_selected
    def generate_question(self): 
    
        q_json = {
            "question_type": self.questionType,
            "question": self.question.question,
            "answer": self.question.answer[0],
            "answer_unit": self.question.answer[1],
            "length": len(self.question.question)

        }         
        return (q_json)




# app = FastAPI()

# @app.get('/question/', status_code=200)
# async def question_type(q_type: Optional[str] = None):
#     if q_type == None:
#         q_type = 'random'
#         print(q_type)
    
#     calculation = Calculation(q_type)
#     question = calculation.generate_question()
#     return question

'''
@app.get("/question/{q_type}", status_code=200)
async def read_question(*, q_type) -> dict:
    calculation = Calculation(q_type)
    question = calculation.generate_question()

    return  question
#https://realpython.com/fastapi-python-web-apis/#path-parameters-get-an-item-by-id
# to run : uvicorn main:app --reload
'''


'''if __name__ == '__main__':
    calculation = Calculation('ratioStrengths')
    question = calculation.generate_question()
    print(question)
    print(f'Tweet length: {len(question[2])}')
'''