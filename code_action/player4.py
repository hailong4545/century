# '''
#     Nghỉ Ngơi: return 'relax'
#     Lấy thẻ có điểm: 'get_card_point', card
#     Lấy thẻ không có điểm: 'get_card_normal', card, material_giveback
#     Sử dụng thẻ:
#         - update: 'card_update', card, material_giveback, material_receive
#         - get_material: 'card_get_material', card, material_remove
#         - exchange: 'card_exchange', card, times, material_remove
#     Note:
#         - material_giveback: Nguyên liệu trả cho bàn chơi
#         - material_receive: Nguyên liệu nhận lại
#         - material_remove: Nguyên liệu bỏ đi khi tổng số nguyên liệu > 10
#         !IMPORTANT
#         - Tất cả các biến trên đều có dạng là một dict
#             các key là các màu của nguyên liệu(yellow,...)
#             value là số nguyên liệu tương ứng
# '''
# from init_game import convert
# import numpy as np
#
# name = '4'
#
# def getTypeCard(card):
#     if card['upgrade'] > 0:
#         return 'card_update'
#     elif sum(list(card['give_back'].values())) == 0:
#         return 'card_get_material'
#     else:
#         return 'card_exchange'
#
# def check(arr):
#     for i in range(len(arr)):
#         if arr[i] < 0:
#             return False
#
#     return True
#
# def useCard(state, card):
#     result = []
#     act = []
#     type_card = getTypeCard(card)
#     mate = np.array(state)
#     giveback = np.array(list(card['give_back'].values()))
#     receive = np.array(list(card['receive'].values()))
#     if type_card == 'card_update':
#         for i in range(3):
#             for j in range(i,3):
#                 if mate[i] > 0 and mate[j] > 0 :
#                     if (i == j and mate[i] >= 2) or i != j:
#                         result.append(mate.copy())
#                         act_giveback = [0, 0, 0, 0]
#                         act_receive = [0, 0, 0, 0]
#                         result[-1][i] -= 1
#                         result[-1][j] -= 1
#                         result[-1][i+1] += 1
#                         result[-1][j+1] += 1
#
#                         act_giveback[i] += 1
#                         act_giveback[j] += 1
#                         act_receive[i+1] += 1
#                         act_receive[j+1] += 1
#
#                         act_giveback = '-'.join(list(map(lambda x: str(x), act_giveback)))
#                         act_receive = '-'.join(list(map(lambda x: str(x), act_receive)))
#                         act.append((type_card, card, convert(act_giveback), convert(act_receive)))
#         for i in range(3):
#             result.append(mate.copy())
#             if result[-1][i] > 0:
#                 act_giveback = [0, 0, 0, 0]
#                 act_receive = [0, 0, 0, 0]
#                 result.append(mate.copy())
#                 result[-1][i] -= 1
#                 result[-1][i+1] += 1
#
#                 act_giveback[i] += 1
#                 act_receive[i+1] += 1
#
#                 act_giveback = '-'.join(list(map(lambda x: str(x), act_giveback)))
#                 act_receive = '-'.join(list(map(lambda x: str(x), act_receive)))
#                 act.append((type_card, card, convert(act_giveback), convert(act_receive)))
#             else:
#                 result.pop()
#         for i in range(2):
#             result.append(mate.copy())
#             if result[-1][i] > 0:
#                 act_giveback = [0, 0, 0, 0]
#                 act_receive = [0, 0, 0, 0]
#                 result.append(mate.copy())
#                 result[-1][i] -= 1
#                 result[-1][i+2] += 1
#
#                 act_giveback[i] += 1
#                 act_receive[i+2] += 1
#
#                 act_giveback = '-'.join(list(map(lambda x: str(x), act_giveback)))
#                 act_receive = '-'.join(list(map(lambda x: str(x), act_receive)))
#                 act.append((type_card, card, convert(act_giveback), convert(act_receive)))
#             else:
#                 result.pop()
#         return result, act
#     elif type_card == 'card_get_material':
#         result.append(mate)
#         result[-1] += receive
#         if sum(result[-1]) > 10:
#             return [], []
#
#         act.append((type_card, card, convert('0-0-0-0')))
#         return result, act
#
#     else:
#         t = 0
#         while True:
#             m = mate -(t+1) * giveback
#             if check(m):
#                 if sum(mate-(t+1)*giveback+(t+1)*receive) <= 10:
#                     result.append(mate-(t+1)*giveback+(t+1)*receive)
#                     act.append((type_card, card, t+1, convert('0-0-0-0')))
#                 else:
#                     break
#             else:
#                 break
#             t += 1
#
#         return result, act
#
# def createAction(player, board):
#     listAct = [player.card_close]
#     listAct[0] = list(map(lambda x: [x], listAct[0]))
#     listState = []
#     while len(listAct) < len(player.card_close):
#         listAct.append([])
#         for i in range(len(listAct[-2])):
#             for j in range(len(listAct[0])):
#                 if listAct[0][j][0] not in listAct[-2][i]:
#                     listAct[-1].append(listAct[-2][i]+listAct[0][j])
#
#     return listAct[-1]
#
# def stopLoop(state, card_point):
#     for card in card_point:
#         if check(state - np.array(list(card['give_back'].values()))):
#             return card
#     return ''
#
# def auto_code(actions, act, state, card_point):
#     global actFuture
#     if stopLoop(np.array(state), card_point) != '':
#         actFuture = act.copy()
#         raise Exception('...')
#     if len(act) != len(actions):
#         n = len(act)
#         listState, listAct = useCard(state, actions[n])
#         for i in range(len(listAct)):
#             act.append(listAct[i])
#             auto_code(actions, act, listState[i], card_point)
#             act.pop()
#
#
# actFuture = []
# flag = True
#
# def action(player, board):
#     global flag, actFuture
#     return 'relax'
#     print(list(player.material.values()))
#
#     if len(player.card_close) + len(player.card_open) < 7:
#         return 'get_card_normal', board['card_normal'][0], convert('0-0-0-0'), convert('0-0-0-0')
#
#     if flag == False:
#         listAct = createAction(player, board)
#         for act in listAct:
#             try:
#                 auto_code(act, [], list(player.material.values()), board['card_point'])
#             except:
#                 flag = True
#                 break
#
#     if len(actFuture) > 0:
#         act = actFuture[0]
#         actFuture.pop(0)
#         return act
#     else:
#         card = stopLoop(np.array(list(player.material.values())), board['card_point'])
#         if card != '':
#             print(card)
#             return 'get_card_point', card
#
#     flag = False
#     return 'relax'
#
#
#
#
#
#

# m_give : material_give_back : Trả lại nguyên liệu khi lấy thẻ normal
# m_give2 : material_give_back2 : Nguyên liệu trả lại khi lấy thẻ và nhận bonus > 10
from init_game import convert
import numpy as np

name = 4

def action(player, board):
    # print(player.material)
    # print(taget_card_max_point(player, board))
    # print(player.count_point)
    # for card in board['card_normal']:
    #     print(dich_the(card), board['card_normal'].index(card))
    # for card in board['card_point']:
    #     print(dich_the(card))
    # for card in player.card_close:
    #     print(dich_the(card))
    return Hanhdongchinh(player, board)

def Hanhdongchinh(player, board):
    #Lấy thẻ Normal
    if Laythe(player, board) != None and len(player.card_close + player.card_open) < 10:
        if board['turn'] < 15:
            # print(Laythe(player, board))
            return Laythe(player, board)

    #lấy thẻ có điểm ở trên bàn chơi
    if Laythediem(player, board) != None:
        # print('Lay the diem')
        # print(Laythediem(player, board))
        return Laythediem(player, board)

    if card_taget_2(player, board['card_normal'], board['card_point']) != None:
        return card_taget_2(player, board['card_normal'], board['card_point'])
    hand = np.array(list(player.material.values()))
    #update
    for card in player.card_close:
        give, rei, time_use, time, bonus = dich_the(card)
        if sum(give) > 0 and sum(rei) > 0 and get_card_exchange(player, board, card) != None:
            # print(get_card_exchange(player, board, card))
            return get_card_exchange(player, board, card)
        if sum(give) == 0 and sum(rei) > 0 and get_material(player, board, card) != None:
            # print(get_material(player, board, card))
            return get_material(player, board, card)
        if sum(give) > 0 and sum(rei) > 0:
            time = 1
            hand1 = np.array(list(player.material.values()))
            hand1 -= time*give
            hand1 += time*rei
            nhan = rei - give
            if min(hand1) >= 0:
                if sum(nhan) + sum(hand1) <= 10:
                    # print('card_exchange',card)
                    return 'card_exchange', card,time, convert('0-0-0-0')
        if sum(give) == 0 and (sum(rei) > 0) and (sum(hand) + sum(rei) <= 10):
            # print('card_get_material', card)
            return 'card_get_material', card, convert('0-0-0-0')
        if card['upgrade'] > 0 and upgrade(player, board, card) != None:
            # print(upgrade(player, board, card))
            return upgrade(player, board, card)

    # print('relax')
    return 'relax'

def dich_the(card):
    if "upgrade" not in card.keys():
        give = np.array(list(card["give_back"].values()))
        point = card['receive']
        rei = np.array([0,0,0,0])
        return give,rei,1,point, card['bonus']
    receive = np.array(list(card["receive"].values()))
    give = np.array(list(card["give_back"].values()))
    bonus = np.array(list(card["bonus"].values()))
    times = card["times"]
    upgrade = card["upgrade"]
    return give,receive,times,upgrade, bonus

def Danhgiathe(card, m_give, m_give2):
    give,receive,times,upgrade, bonus = dich_the(card)
    list_give_and_bonus = bonus - m_give - m_give2
    list_con = receive - give
    danhgia = 0
    for i in range(len(list_con)):
        danhgia += (i+1)*list_con[i] + list_give_and_bonus[i]*0.2*(i+1)
    danhgia += upgrade*1.5
    return danhgia

def give_back_soNL(player, soNL, card):
    give_back = convert('0-0-0-0')
    for color in player.material:
        if player.material[color] < soNL:
            give_back[color] = player.material[color]
            soNL -= give_back[color]
        else:
            give_back[color] = soNL
            break
    return give_back

def give_back_soNL2(player, soNL, card):
    give_back = convert('0-0-0-0')
    for color in player.material:
        if player.material[color] + card['bonus'][color] < soNL:
            give_back[color] = player.material[color] + card['bonus'][color]
            soNL -= give_back[color]
        else:
            give_back[color] = soNL
            break
    return give_back

def material_give_back2(player, card):
    if (sum(list(player.material.values())) + sum(list(card['bonus'].values()))) - 10 <= 0:
        return '0-0-0-0'
    else:
        soNL = (sum(list(player.material.values())) + sum(list(card['bonus'].values()))) - 10
        give_back = give_back_soNL2(player, soNL, card)
        return str(give_back['yellow']) + '-' + str(give_back['red']) + '-' + str(give_back['green']) + '-' + str(give_back['brown'])

def material_give_back(player, soNL, card):
    give_back = give_back_soNL(player, soNL, card)
    if soNL <= (player.material['yellow']+player.material['red']) and soNL > 0:
        if give_back['green'] == 0 and give_back['brown'] == 0:
            return str(give_back['yellow']) + '-' + str(give_back['red']) + '-' + str(give_back['green']) + '-' + str(give_back['brown'])
    else:
        return '0-0-0-0'

def Laythe(player,board):
    for danhgia in np.arange(4.5, 2.5, -0.1):
        for card in board['card_normal']:
            soNL = board['card_normal'].index(card)
            if (material_give_back(player, soNL, card) != None) and (player.material['yellow'] + player.material['red'] >= soNL):
                m_give = np.array(list(convert(material_give_back(player, soNL, card)).values()))
                m_give2 = np.array(list(convert(material_give_back2(player, card)).values()))
                if Danhgiathe(card, m_give, m_give2) > danhgia:
                    # print(board['card_normal'].index(card))
                    return 'get_card_normal', card, list_to_str(m_give), list_to_str(m_give2)
    return None

def Laythediem(player, board):
    for card in board['card_point']:
        check = True
        for cl in player.material.keys():
            if player.material[cl] < card['give_back'][cl]:
                check = False
        if check == True:
            return 'get_card_point', card

def list_to_str(a):
    return convert(str(a[0]) +'-'+ str(a[1]) +'-'+ str(a[2]) +'-'+ str(a[3]))

def taget_card_max_point(player, board):
    card_taget = board['card_point'][0]
    for card in board['card_point']:
        if card['receive'] + card['bonus']  > card_taget['receive'] + card_taget['bonus']:
            card_taget = card     # Taget thẻ nhiều điểm nhất trong bàn
    nguyenlieudangco = np.array(list(player.material.values()))
    give,rei,time,point,bonus = dich_the(card_taget)
    nguyenlieucan = give - nguyenlieudangco
    return nguyenlieucan

# def Time_to_get_point(player, card):

def upgrade(player, board, card):
    give, rei, time_use, time, bonus = dich_the(card)
    taget_card = taget_card_max_point(player, board)
    sl = 0
    if max(taget_card) > 0 and min(taget_card) < 0:
        while time > 0 or sl < 10:
            for i in range(len(taget_card) - 1):
                for j in range(time, 0, -1):
                    if i+j < len(taget_card):
                        if((taget_card[i] < 0) and (taget_card[i+j] > 0)) or (i+j < len(taget_card) and (taget_card[i] < 0) and(taget_card[i+j] > 0)):
                            time -= j
                            taget_card[i] += 1
                            give[i] += 1
                            taget_card[i+j] -= 1
                            rei[i+j] += 1
                        if time == 0:
                            break
            sl += 1
            if sl > 3:
                time -= 1
        return 'card_update', card, list_to_str(give), list_to_str(rei)

def get_material(player,board, card):
    give, rei, time_use, time, bonus = dich_the(card)
    taget_card = taget_card_max_point(player, board)
    hand = np.array(list(player.material.values()))
    for i in range(len(taget_card)):
        check = True
        for j in range(len(taget_card)):
            if taget_card[j] > 0 and rei[j] > 0:
                check = False
        if check == True:
            soNL = sum(hand) - sum(give) + sum(rei) - 10
            m_give = material_give_back(player, soNL, card)
            return 'card_get_material', card, convert(m_give)
        if sum(hand) + sum(rei) <= 12:
            if taget_card[j] > 0:
                soNL = sum(hand) + sum(rei) - 10
                m_give = material_give_back(player, soNL, card)
                return 'card_get_material', card, convert(m_give)



def get_card_exchange(player, board, card):
    give, rei, time_use, time, bonus = dich_the(card)
    taget_card = taget_card_max_point(player, board)
    nhan = rei - give
    hand = np.array(list(player.material.values()))

    for i in range(len(nhan)):
        # if hand[i] >= give[i]:
        time = 1
        if taget_card[i] < 0:
            check = True
            for j in range(len(nhan)):
                if nhan[j] > 0 and taget_card[j] > 0:
                    check = False
            if check == True:
                hand -= time*give
                hand += time*rei
                if min(hand) >= 0:
                    soNL = sum(hand) - sum(give) + sum(rei) - 10
                    m_give = material_give_back(player, soNL, card)
                    return 'card_exchange', card,time, convert(m_give)
        if taget_card[i] < 0:
            hand -= time*give
            hand += time*rei
            if min(hand) >= 0:
                if sum(nhan) + sum(hand) <= 12:
                    soNL = sum(hand) - sum(give) + sum(rei) - 10
                    m_give = material_give_back(player, soNL, card)
                    return 'card_exchange', card,time, convert(m_give)

def card_taget_2(player, card_normal, card_point):
    for cardpoint in card_point:
        dict_NL_can = convert('0-0-0-0')
        for color in player.material:
            dict_NL_can[color] = cardpoint['give_back'][color] - player.material[color]
        for card in player.card_close:
            if card['upgrade'] == 3:
                for color in dict_NL_can.keys():
                    if dict_NL_can[color] >= 2:
                        if color == 'red' and dict_NL_can['yellow'] <= -3:
                            if check_get_card_point(player, cardpoint, '3-0-0-0', '0-3-0-0') == True:
                                return 'card_update', card, convert('3-0-0-0'), convert('0-3-0-0')
                        if color == 'green' and dict_NL_can['red'] <= -3:
                            if check_get_card_point(player, cardpoint, '0-3-0-0', '0-0-3-0') == True:
                                return 'card_update', card, convert('0-3-0-0'), convert('0-0-3-0')
                        if color == 'brown' and dict_NL_can['green'] <= -3:
                            if check_get_card_point(player, cardpoint, '0-0-3-0', '0-0-0-3') == True:
                                return 'card_update', card, convert('0-0-3-0'), convert('0-0-0-3')
                    if dict_NL_can[color] >= 1:
                        if color == 'red' and dict_NL_can['green'] >= 1:
                            if dict_NL_can['yellow'] <= -2:
                                if check_get_card_point(player, cardpoint, '2-0-0-0', '0-1-1-0') == True:
                                    return 'card_update', card, convert('2-0-0-0'), convert('0-1-1-0')
                        if color == 'green' and dict_NL_can['brown'] >= 1:
                            if dict_NL_can['red'] <= -2:
                                if check_get_card_point(player, cardpoint, '0-2-0-0', '0-0-1-1') == True:
                                    return 'card_update', card, convert('0-2-0-0'), convert('0-0-1-1')
                        if color == 'brown' and dict_NL_can['yellow'] <= -1:
                            if check_get_card_point(player, cardpoint, '1-0-0-0', '0-0-0-1') == True:
                                return 'card_update', card, convert('1-0-0-0'), convert('0-0-0-1')
            elif card['upgrade'] == 2:
                for color in dict_NL_can.keys():
                    if dict_NL_can[color] >= 1:
                        if color == 'red' and dict_NL_can['yellow'] <= -2:
                            if check_get_card_point(player, cardpoint, '2-0-0-0', '0-2-0-0') == True:
                                return 'card_update', card, convert('2-0-0-0'), convert('0-2-0-0')
                        if color == 'green' and dict_NL_can['red'] <= -2:
                            if check_get_card_point(player, cardpoint, '0-2-0-0', '0-0-2-0') == True:
                                return 'card_update', card, convert('0-2-0-0'), convert('0-0-2-0')
                        if color == 'brown' and dict_NL_can['green'] <= -2:
                            if check_get_card_point(player, cardpoint, '0-0-2-0', '0-0-0-2') == True:
                                return 'card_update', card, convert('0-0-2-0'), convert('0-0-0-2')
                    if dict_NL_can[color] >= 1:
                        if color == 'green' and dict_NL_can['yellow'] <= -1:
                            if check_get_card_point(player, cardpoint, '1-0-0-0', '0-0-1-0') == True:
                                return 'card_update', card, convert('1-0-0-0'), convert('0-0-1-0')
                        if color == 'brown' and dict_NL_can['red'] <= -1:
                            if check_get_card_point(player, cardpoint, '0-1-0-0', '0-0-0-1') == True:
                                return 'card_update', card, convert('0-1-0-0'), convert('0-0-0-1')
                        if color == 'brown' and dict_NL_can['yellow'] <= -1:
                            if check_get_card_point(player, cardpoint, '1-0-0-0', '0-0-1-0') == True:
                                return 'card_update', card, convert('1-0-0-0'), convert('0-0-1-0')
            elif sum(list(card['give_back'].values())) == 0 and sum(list(card['receive'].values())) > 0:
                if sum(list(card['receive'].values())) <= (10 - sum(list(player.material.values()))):
                    str_receive = str(card['receive']['yellow']) + '-' + str(card['receive']['red']) + '-' + str(card['receive']['green']) + '-' + str(card['receive']['brown'])
                    if check_get_card_point(player, cardpoint, '0-0-0-0', str_receive) == True:
                        return 'card_get_material', card, convert('0-0-0-0')
            elif sum(list(card['give_back'].values())) > 0 and sum(list(card['receive'].values())) > 0:
                for color1 in player.material:
                    for color2 in player.material:
                        if card['give_back'][color1] > 0 and card['receive'][color2] > 0:
                            if card['give_back'][color1] + dict_NL_can[color1] <= 0 and dict_NL_can[color2] > 0:
                                check = True
                                for color in player.material:
                                    if player.material[color] < card['give_back'][color]:
                                        check = False
                                if check == True:
                                    soNL2 = sum(list(player.material.values())) - sum(list(card['give_back'].values())) + sum(list(card['receive'].values())) - 10
                                    str_give_back = str(card['give_back']['yellow']) + '-' + str(card['give_back']['red']) + '-' + str(card['give_back']['green']) + '-' + str(card['give_back']['brown'])
                                    str_receive = str(card['receive']['yellow']) + '-' + str(card['receive']['red']) + '-' + str(card['receive']['green']) + '-' + str(card['receive']['brown'])
                                    if soNL2 < 0:
                                        if check_get_card_point(player, cardpoint, str_give_back, str_receive) == True:
                                            return 'card_exchange', card, 1, convert('0-0-0-0')
                                    else:
                                        give_back = give_back_soNL(player, soNL2, card)
                                        if check_get_card_point(player, cardpoint, str_give_back, str_receive) == True:
                                            return 'card_exchange', card, 1, convert(str(give_back['yellow']) + '-' + str(give_back['red']) + '-' + str(give_back['green']) + '-' + str(give_back['brown']))
    return None

def check_get_card_point(player, cardpoint, str_give_back, str_receive):
    give_back = convert(str_give_back)
    receive = convert(str_receive)
    check = True
    for color in player.material:
        if (- give_back[color] + receive[color] + player.material[color]) < cardpoint['give_back'][color]:
            check = False
    return check

