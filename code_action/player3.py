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

# convert thẻ điểm và normal
def dich_the(card):
    if "upgrade" not in card.keys():
        give = np.array(list(card["give_back"].values()))
        point = card['receive']
        rei = np.array([0,0,0,0])
        return give,rei,1,point
    receive = np.array(list(card["receive"].values()))
    give = np.array(list(card["give_back"].values()))
    times = card["times"]
    upgrade = card["upgrade"]
    return give,receive,times,upgrade


# từ 1 thẻ normal đến list mọi states có thể
def card_to_state(hand,the,score,turn):
    give,rei,times,upgrade = dich_the(the)
    # nếu là thẻ upgrade
    if upgrade > 0 and upgrade < 5:
        return full_upgrade(hand,upgrade)
    card = [give,rei]
    max = times
    states = []
    for idnl in range(4):
        if card[0][idnl] > 0:
            times = hand[idnl]//card[0][idnl]
            if times < max:
                max = times
    # nếu không phải thẻ upgrade
    score += upgrade
    for lan in range(max):
        state = hand - card[0]*(lan+1) + card[1]*(lan+1)
        while sum(state) > 10:
            thua = sum(state) - 10
            for idnl in range(4):
                state[idnl] -= min(thua,state[idnl])
        states.append(state)
    return states,score, turn + 1

# nâng cấp 1 lần
def state_to_states(state):
    states = []
    for idnl in range(3):
        s = state.copy()
        if s[idnl] > 0:
            s[idnl] -= 1
            s[idnl+1] += 1
            states.append(s)
    return states

# nâng cấp full
def full_upgrade(state,upgrade):
    states = [state]
    full = []
    while upgrade > 0:
        temp = []
        for state in states:
            temp += state_to_states(state)
        full += temp
        states = temp.copy()
        upgrade -=1
    return full

def action(player, board):
    hand = np.array(list(player.material.values()))
    for card in (player.card_close+board['card_normal']):
        print(card)
    return 'relax'

                 


            
