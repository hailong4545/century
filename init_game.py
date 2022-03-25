import numpy as np

def initGame(data_card_normal, data_card_point):
    Random = lambda x: np.random.choice(x, len(x), replace=False)
    data_card_normal = Random(data_card_normal)
    data_card_point = Random(data_card_point)
    for i in range(len(data_card_point)):
        data_card_point[i]['bonus'] = 0

    for i in range(len(data_card_normal)):
        data_card_normal[i]['bonus'] = convert('0-0-0-0')

    return list(data_card_normal), list(data_card_point)
#
# def setBonus(data_card_point, conis):
#     if conis['gold'] == 0:
#         data_card_point[-1]['bonus'] = 1
#     else:
#         data_card_point[-1]['bonus'] = 3
#         data_card_point[-2]['bonus'] = 1
#
#     return data_card_point


def setBonus(data_card_point, conis):
    if conis['gold'] != 0 and conis['silver'] != 0:
        data_card_point[-1]['bonus'] = 3
        data_card_point[-2]['bonus'] = 1
    elif conis['gold'] == 0 and conis['silver'] == 0:
        pass
    elif conis['gold'] != 0:
        data_card_point[-1]['bonus'] = 3
    elif conis['silver'] != 0:
        data_card_point[-1]['bonus'] = 1

    return data_card_point

def setDefault():
    card_normal = [
        {'give_back': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0},
         'receive': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0}, 'upgrade': 2, 'times': 1, 'bonus': convert('0-0-0-0')},
         {'give_back': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0},
         'receive': {'yellow': 2, 'red': 0, 'green': 0, 'brown': 0}, 'upgrade': 0, 'times': 1, 'bonus': convert('0-0-0-0')}
    ]

    return card_normal


def convert(string):
    value_card = list(map(lambda x: int(x), string.split('-')))

    return {
        'yellow': value_card[0],
        'red' : value_card[1],
        'green' : value_card[2],
        'brown' : value_card[3]
    }

def stop_game(players):
    for player in players:
        if player.count_card == 5:
            return True
    
    return False

def check_player_win(players):
    id_win = 1
    max_point = players[0].count_point + sum(list(players[0].material.values())[1:])

    for i in range(1, len(players)):
        if players[i].count_point + sum(list(players[i].material.values())[1:]) >= max_point:
            max_point = players[i].count_point + sum(list(players[i].material.values())[1:])
            id_win = i + 1

    return id_win

def show_point_players(players, id):
    # for i in range(len(players)):
        # print(f'NGƯỜI CHƠI {i+1} CÓ {players[i].count_point + sum(list(players[i].material.values())[1:])} ĐIỂM')

    print(f'NGƯỜI CHƠI THỨ {id} CHIẾN THẮNG')


def check_dict(dt):
    color = ['yellow', 'red', 'green', 'brown']

    for cl in color:
        try:
            k = dt[cl]
        except:
            return False

    if len(list(dt.keys())) != 4:
        return False

    return True

def check_card(card):
    if list(card.keys()) == ['give_back', 'receive', 'upgrade', 'times', 'bonus']:
        return "card_normal"

    if list(card.keys()) == ['give_back', 'receive', 'bonus']:
        return 'card_point'

    return ''

def check_action(action):
    if len(action) == 1 and action[0] == 'relax':
        return True

    if len(action) == 2 and action[0] == 'get_card_point' and check_card(action[1]) == 'card_point':
        return True

    if len(action) == 3 and action[0] == 'card_get_material' and check_card(action[1]) == 'card_normal' and check_dict((action[2])):
        return True

    if len(action) == 4 and action[0] == 'card_update' and check_card(action[1]) == 'card_normal' and check_dict(action[2]) and check_dict(action[3]):
        return True

    if len(action) == 4 and action[0] == 'card_exchange' and check_card(action[1]) == 'card_normal' and type(action[2]) == type(int(1)) and check_dict(action[3]):
        return True

    if len(action) == 4 and action[0] == 'get_card_normal' and check_card(action[1]) == 'card_normal' and check_dict(action[2]) and check_dict(action[3]):
        return True
    return False

def check_get_card_point(m, card):
    card = card['give_back']
    for cl in m.keys():
        if m[cl] < card[cl]:
            return False

    return True