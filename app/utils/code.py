from random import SystemRandom
from random import randrange
from app.config import config

choice = SystemRandom().choice

def gen_code(symbols, size, specialSymbols = False):
    """Function for generating protection code

    :symbols: @todo
    :size: @todo
    :returns: @todo

    """
    code = ''
    # for _ in xrange(size):
    for _ in range(size):
        code += choice(symbols)
    if specialSymbols:
        position = randrange(1, size - 2)
        special_char = choice(config.PASSWORD_SYMBOLS_ALLOWED)
        code = code[:position] + special_char + code[position:]
    return code