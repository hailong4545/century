'''
    Nghỉ Ngơi: return 'relax'
    Lấy thẻ có điểm: 'get_card_point', card
    Lấy thẻ không có điểm: 'get_card_normal', card, material_giveback
    Sử dụng thẻ:
        - update: 'card_update', card, material_giveback, material_receive
        - get_material: 'card_get_material', card, material_remove
        - exchange: 'card_exchange', card, times, material_remove
    Note:
        - material_giveback: Nguyên liệu trả cho bàn chơi
        - material_receive: Nguyên liệu nhận lại
        - material_remove: Nguyên liệu bỏ đi khi tổng số nguyên liệu > 10
        !IMPORTANT
        - Tất cả các biến trên đều có dạng là một dict
            các key là các màu của nguyên liệu(yellow,...)
            value là số nguyên liệu tương ứng
'''
from init_game import convert
import numpy as np

name = '3'

def checkMate(arr):
    for i in arr:
        if i > 5:
            return False
    return True

def getTypeCard(card):
    if card['upgrade'] > 0:
        return 'card_update'
    elif sum(list(card['give_back'].values())) == 0:
        return 'card_get_material'
    else:
        return 'card_exchange'

def check(arr):
    for i in range(len(arr)):
        if arr[i] < 0:
            return False

    return True

def useCard(state, card):
    result = []
    act = []
    type_card = getTypeCard(card)
    mate = np.array(state)
    giveback = np.array(list(card['give_back'].values()))
    receive = np.array(list(card['receive'].values()))
    if type_card == 'card_update':
        for i in range(3):
            for j in range(i,3):
                if mate[i] > 0 and mate[j] > 0 :
                    if (i == j and mate[i] >= 2) or i != j:
                        result.append(mate.copy())
                        act_giveback = [0, 0, 0, 0]
                        act_receive = [0, 0, 0, 0]
                        result[-1][i] -= 1
                        result[-1][j] -= 1
                        result[-1][i+1] += 1
                        result[-1][j+1] += 1

                        act_giveback[i] += 1
                        act_giveback[j] += 1
                        act_receive[i+1] += 1
                        act_receive[j+1] += 1

                        act_giveback = '-'.join(list(map(lambda x: str(x), act_giveback)))
                        act_receive = '-'.join(list(map(lambda x: str(x), act_receive)))
                        act.append((type_card, card, convert(act_giveback), convert(act_receive)))
        for i in range(3):
            result.append(mate.copy())
            if result[-1][i] > 0:
                act_giveback = [0, 0, 0, 0]
                act_receive = [0, 0, 0, 0]
                result.append(mate.copy())
                result[-1][i] -= 1
                result[-1][i+1] += 1

                act_giveback[i] += 1
                act_receive[i+1] += 1

                act_giveback = '-'.join(list(map(lambda x: str(x), act_giveback)))
                act_receive = '-'.join(list(map(lambda x: str(x), act_receive)))
                act.append((type_card, card, convert(act_giveback), convert(act_receive)))
            else:
                result.pop()
        for i in range(2):
            result.append(mate.copy())
            if result[-1][i] > 0:
                act_giveback = [0, 0, 0, 0]
                act_receive = [0, 0, 0, 0]
                result.append(mate.copy())
                result[-1][i] -= 1
                result[-1][i+2] += 1

                act_giveback[i] += 1
                act_receive[i+2] += 1

                act_giveback = '-'.join(list(map(lambda x: str(x), act_giveback)))
                act_receive = '-'.join(list(map(lambda x: str(x), act_receive)))
                act.append((type_card, card, convert(act_giveback), convert(act_receive)))
            else:
                result.pop()
        return result, act
    elif type_card == 'card_get_material':
        result.append(mate)
        result[-1] += receive
        if sum(result[-1]) > 10:
            return [], []

        act.append((type_card, card, convert('0-0-0-0')))
        return result, act

    else:
        t = 0
        while True:
            m = mate -(t+1) * giveback
            if check(m):
                if sum(mate-(t+1)*giveback+(t+1)*receive) <= 10 and checkMate(mate-(t+1)*giveback+(t+1)*receive):
                    result.append(mate-(t+1)*giveback+(t+1)*receive)
                    act.append((type_card, card, t+1, convert('0-0-0-0')))
                else:
                    break
            else:
                break
            t += 1

        return result, act

def createAction(player):
    listAct = [player.card_close]
    listAct[0] = list(map(lambda x: [x], listAct[0]))
    while len(listAct) < len(player.card_close):
        listAct.append([])
        for i in range(len(listAct[-2])):
            for j in range(len(listAct[0])):
                if listAct[0][j][0] not in listAct[-2][i]:
                    listAct[-1].append(listAct[-2][i]+listAct[0][j])

    return listAct[-1]

def stopLoop(state, card_point):
    for card in card_point:
        if check(state - np.array(list(card['give_back'].values()))):
            return card
    return ''

def auto_code(actions, act, state):
    global actFuture, stateFuture
    if len(act) != len(actions):
        n = len(act)
        listState, listAct = useCard(state, actions[n])
        if len(listAct) == 0 and len(act) != 0:
            actFuture.append(act.copy())
            stateFuture.append(state.copy())
        else:
            for i in range(len(listAct)):
                act.append(listAct[i])
                auto_code(actions, act, listState[i])
                act.pop()

def points(a, b):
    total = 0
    for i in range(len(a)):
        total += (b[0] - a[0]) * (i+1)
    return total

def actionNext(state):
    global actFuture, stateFuture
    m = 0
    index = 0
    for i in range(len(actFuture)):
        a = np.array(stateFuture[i])
        p = points(state, a)
        if len(actFuture[i]) != 0:
            if float(p)/len(actFuture[i]) > m:
                m = float(p)/len(actFuture[i])
                index = i
    return actFuture[index][0]


actFuture = []
flag = True
stateFuture = []

def action(player, board):
    global flag, actFuture,stateFuture
    print(list(player.material.values()))

    if len(player.card_close) + len(player.card_open) < 6:
        return 'get_card_normal', board['card_normal'][0], convert('0-0-0-0'), convert('0-0-0-0')

    card = stopLoop(np.array(list(player.material.values())), board['card_point'])
    if card != '':
        print(card)
        return 'get_card_point', card

    listAct = createAction(player)
    for act in listAct:
        auto_code(act, [], list(player.material.values()))
    if len(actFuture) != 0:
        actNext = actionNext(list(player.material.values()))
        actFuture = []
        stateFuture = []
        return actNext
    else:
        return 'relax'

    return 'relax'






