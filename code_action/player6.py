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

name = '6'

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
def card_to_state(hand,the,score,da_mua):
    give,rei,times,upgrade = dich_the(the)
    # nếu là thẻ upgrade
    if upgrade > 0 and upgrade < 5:
        return full_upgrade(hand,upgrade),score
    card = [give,rei]
    max = times
    states = []
    # nếu không phải thẻ upgrade
    if np.min(hand-give) <0:
        return [],0
    score += upgrade
    if da_mua == 4:
        score += upgrade*1000
    for time in range(times):
        hand = hand - give + rei
        if min(hand) < 0:
            break
        if sum(hand) > 10:
            thua = sum(hand) - 10
            while thua > 0:
                for idnl in range(3):
                    if hand[idnl] > 0:
                        hand[idnl] -= 1
                        thua -= 1
                        break
            states.append(hand)
            break
        states.append(hand)
    return states,score

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
    for time in range(upgrade):
        for state in states:
            add = state_to_states(state)
            for ad in add:
                if True not in list(map(lambda x: np.array_equal(x, ad), full)):
                    full.append(ad)
        states = add.copy()
    return full


def future(start_items,turn,terminate,max_score,start_score,full_hand,da_mua):
    # print(turn,max_score)
    if turn == terminate:
        return max_score,turn,start_score
    items = []
    for it in start_items:
        fn = it[0]
        cards = it[1]
        point = it[2]
        for f in fn:
            for the in cards:
                if "times" in the.keys() and the["times"] == 100:
                    states = [f]
                    new_cards = full_hand
                    item = [states,new_cards,point]
                    items.append(item)
                else:
                    states, new_score = card_to_state(f,the,point,da_mua)
                    if len(states) == 0:
                        a = 0
                    else:
                        for state in states:
                            eval_score = (sum(state*np.array([1,2,3,4])) + point- start_score)/turn
                            if eval_score > max_score:
                                max_score = eval_score
                        new_cards = [car for car in cards if car != the]
                        item = [states,new_cards,point + new_score]
                        items.append(item)
    return future(items,turn + 1,terminate,max_score,start_score,full_hand,da_mua)

def hand_to_target(hand,target):
    x = target-hand
    give = x*(x<0)*-1
    give = "-".join([str(a) for a in give])
    rei = x*(x>0)
    rei = "-".join([str(a) for a in rei])
    return give,rei

def the_doi_nl(hand,target,giv,re):
    x = target-hand
    give = x*(x<0)*-1
        # give = "-".join([str(a) for a in give])
    rei = x*(x>0)
        # rei = "-".join([str(a) for a in rei])

    times = int(max(give)/max(giv))
    hand += times*(re)
    hand -= times*(giv)
    tra_ve = hand - target
    tra_ve = "-".join([str(a) for a in tra_ve])
    return times,tra_ve

def the_lay_free(hand,target,giv,re):
    x = target-hand
    tra_ve = re - x
    tra_ve = "-".join([str(a) for a in tra_ve])
    return tra_ve

def action(player, board):
    level = 10
    hand = np.array(list(player.material.values()))
    if len(player.card_close + player.card_open) <level:
        for card_normal in board['card_normal']:
            id_card = board['card_normal'].index(card_normal)
            give, rei, times,upgrade = dich_the(card_normal)
            tra_ve = (sum(card_normal['bonus'].values()) + sum(hand)) - 10
            if tra_ve < 0:
                tra_ve = 0
            if sum(give) == 0 and hand[0] >= id_card:
                # print("lấy thẻ free")
                return 'get_card_normal', card_normal, convert(str(id_card) + "-0-0-0"),convert(str(tra_ve) + "-0-0-0")
            if rei[0] > 0 and sum(give) == 1 and hand[0] >= id_card:
                # print("thẻ sinh vàng")
                return 'get_card_normal', card_normal, convert(str(id_card) + "-0-0-0"),convert(str(tra_ve) + "-0-0-0")
            if give[0] > 0 and sum(give*np.array([0,1,1,1])) == 0 and hand[0] >= id_card:
                # print("thẻ đổi vàng")
                return 'get_card_normal', card_normal, convert(str(id_card) + "-0-0-0"),convert(str(tra_ve) + "-0-0-0")
    rest = {'give_back': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0}, 'receive': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0}, 'upgrade': 0, 'times': 100, 'bonus': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0}}
    full_hand = player.card_close + player.card_open + board['card_point'] + [rest]
    cards = player.card_close+board['card_point'] + [rest]
    da_mua = 0
    score_max = 0
    card_use = None
    start_score = sum(hand*np.array([1,2,3,4]))
    ter = 4
    target_state = None
    for card in cards:
        if "times" in card.keys() and card["times"] == 100:
            item = [[hand],full_hand,0]
            evaluate,b,c = future([item],1,ter,0,start_score,full_hand,da_mua)
            if evaluate > score_max:
                score_max = evaluate
                card_use = card
                target_state = hand
        states, diem  = card_to_state(hand,card,0,da_mua)
        new_cards = [car for car in cards if car != card]
        for state in states:
            item = [[state],new_cards,diem]
            evaluate,b,c = future([item],1,ter,0,start_score,full_hand,da_mua)
            if evaluate > score_max:
                score_max = evaluate
                card_use = card
                target_state = state
    if score_max < 1:
        # print("nghỉ 1",score_max)
        return "relax"
    # print(score_max,target_state,dich_the(card_use))
    give, rei, times,upgrade = dich_the(card_use)
    # nếu target thẻ nghỉ
    if times == 100:
        # print("nghỉ 4",score_max)
        return "relax"
    # nếu target thẻ điểm
    if upgrade > 5:
        # print("mua thẻ điểm",score_max)
        return 'get_card_point', card_use
    # nếu target thẻ normal
    else:
        if upgrade > 0:
            tra,lay = hand_to_target(hand,target_state)
            # print("nâng cấp " + str(upgrade) + " lần",score_max)
            return 'card_update', card_use, convert(tra), convert(lay)
        if sum(give) == 0:
            # print("lấy free",score_max)
            tra = the_lay_free(hand,target_state,give,rei)
            return 'card_get_material', card_use, convert(tra)
        else:
            # print("đổi nguyên liệu",score_max)
            lan,tra_ve = the_doi_nl(hand,target_state,give,rei)
            return 'card_exchange', card_use, lan, convert(tra_ve)
    if len(player.card_close) == 0:
        # print("nghỉ 2",score_max)
        return "relax"
    # print(future([[[hand],cards,0,0]],1,len(cards)+1,0,start_score))
    # print("nghỉ 3",score_max)
    return 'relax'

                 


            
