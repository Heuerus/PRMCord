from random import randint

pool = 10
chance = randint(1, pool)
for i in range(1, 10): 
    chance = randint(1, pool)
    print(chance)