import random

import send

def code():

    code_list = []

    for i in range(10):
        code_list.append(str(i))
    r = random.sample(code_list, 6)
    m = ''.join(r)

    #cd = str({"code": m})

    return m

if __name__ == "__main__":
    m = code()
    print(m)
