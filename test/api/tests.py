from django.test import TestCase

# Create your tests here.


class brave:
    def __init__(self,name,level=1,strength=4,patient=4,maxhp=10):
        self.name = name
        self.level = level
        self.strength = strength
        self.patient = patient
        self.maxhp = maxhp
        self.hp = maxhp
    เงินเดือน = 500
p1 = brave('ไก่กา',1,5,5,12)

dict = p1.__dict__

print(p1.__dict__)
print(type(dict))