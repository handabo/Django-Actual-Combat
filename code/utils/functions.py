import random


def get_ticket():
    ticket = ''
    s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    for i in range(100):
        ticket += random.choice(s)
    return ticket