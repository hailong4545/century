import pandas as pd
import numpy as np
from init_game import convert
from code_action import player1 as p1, player2 as p2, player3 as p3, player4 as p4, player5 as p5, player6 as p6, player7 as p7, player8 as p8, player9 as p9

p = [p1, p2, p3, p4, p5, p6, p7, p8, p9]

def creatCase():
    result = []
    for i in range(len(p)):
        for j in range(i+1,len(p)):
            for k in range(j+1,len(p)):
                for m in range(k+1,len(p)):
                    for n in range(m+1,len(p)):
                        result.append([p[i], p[j], p[k], p[m], p[n]])
                        result[-1] = np.random.choice(result[-1], len(result[-1]), replace=False)

    return result

def readDataGame():
    data = pd.read_excel('data_card/card_normal.xlsx', sheet_name='exchange', engine='openpyxl')
    data = dict(data)
    attribute = list(data.keys())

    data_card_normal = []
    for i in range(len(data['times'])):
        df_dict = {}

        for att in attribute:
            if att[0] in ['g', 'r']:
                df_dict[att] = convert(data[att][i])
            else:
                df_dict[att] = int(data[att][i])

        data_card_normal.append(df_dict.copy())

    data = pd.read_excel('data_card/card_point.xlsx', engine='openpyxl')

    data_card_point = [
        {'give_back': convert(data['card_point'][i]), 'receive': data['ponit'][i]}
        for i in range(len(data))
    ]

    return data_card_normal, data_card_point