name = '7'
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

name = '7'

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
def card_to_state(hand,the,score):
    give,rei,times,upgrade = dich_the(the)
    # nếu là thẻ upgrade
    if upgrade > 0 and upgrade < 5:
        return full_upgrade(hand,upgrade),score
    card = [give,rei]
    max = times
    states = []
    for idnl in range(4):
        if card[0][idnl] > 0:
            times = hand[idnl]//card[0][idnl]
            if times < max:
                max = times
    # nếu không phải thẻ upgrade
    if np.min(hand-give) <0:
        return [],0
    score += upgrade
    for lan in range(max):
        state = hand - card[0]*(lan+1) + card[1]*(lan+1)
        while sum(state) > 10:
            thua = sum(state) - 10
            for idnl in range(4):
                state[idnl] -= min(thua,state[idnl])
        states.append(state)
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
    while upgrade > 0:
        temp = []
        for state in states:
            temp += state_to_states(state)
        full += temp
        states = temp.copy()
        upgrade -=1
    return full


def future(start_items,turn,terminate,max_score,start_score,full_hand):
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
                    states, new_score = card_to_state(f,the,point)
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
    return future(items,turn + 1,terminate,max_score,start_score,full_hand)

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

# Convert
def convert_card(card):
    if 'upgrade' not in card.keys():
        giveback = np.array(list(card['give_back'].values()))
        receive = np.array([0,0,0,0])
        point = card['receive'] + card['bonus']

        return giveback, receive, point, 1

    giveback = np.array(list(card['give_back'].values()))
    receive = np.array(list(card['receive'].values()))
    upgrade = card['upgrade']
    times = card['times']

# def fill_combo(player, board):
def fill_combo(player, board):
    input_need = np.array([2,2,2,2])
    output_need = np.array([3,3,3,3])

    list_card_normal = player.card_open + player.card_close

    list_card_normal.remove({
        'give_back': convert('0-0-0-0'),
        'receive': convert('2-0-0-0'),
        'times': 1,
        'upgrade': 0,
        'bonus': convert('0-0-0-0')
    })

    for card_normal in list_card_normal:
        give, receive, times, upgrade = dich_the(card_normal)

        for i in range(4):
            if give[i] != 0:
                input_need[i] -= 1
            if receive[i] != 0:
                if sum(receive != [0,0,0,0]) == 1 and sum(give) != 0:
                    output_need[i] -= 2
                else:
                    output_need[i] -= 1

    return input_need, output_need

# Type card normal
def get_card_normal_type(card):
    giveback, receive, times, upgrade = dich_the(card)

    if upgrade != 0:
        return 'upgrade'

    if times == 1:
        return 'get_material'

    return 'exchange'



def card_normal_rating(card):
    if get_card_normal_type(card) == 'upgrade':
        return 10

    give, receive, times, upgrade = dich_the(card)

    if get_card_normal_type(card) == 'get_material':
        return sum(receive * [1,2,3,4]) + 0.5

    n = max(sum(give), sum(receive))

    input_list = [2,3,4,5]
    output_list = [3,2,1,1]

    m = output_list[input_list.index(n)]

    return m * sum(receive * [1,2,3,4] - give * [1,2,3,4])


# Lấy thẻ normal
def get_card_normal_setup(card_target, board, my_hand):
    index_target = board['card_normal'].index(card_target)
    bonus_material = np.array(list(card_target['bonus'].values()))

    my_hand_after = my_hand - np.array([index_target,0,0,0]) + bonus_material

    give2 = np.array([0,0,0,0])

    if sum(my_hand_after) > 10:
        n = sum(my_hand_after) - 10
        while n > 0:
            for i in range(4):
                n -= min(n, my_hand_after[i])

    return convert(f'{index_target}-0-0-0'), convert(f'{give2[0]}-{give2[1]}-{give2[2]}-{give2[3]}')



def action(player, board):
    # level = 10
    hand = np.array(list(player.material.values()))

    input_need, output_need = fill_combo(player, board)

    # Lấy thẻ normal
    if max(output_need) >= 2:
        list_card_normal_can_buy = []
        for card_normal in board['card_normal']:
            if hand[0] > board['card_normal'].index(card_normal):
                give, receive, times, upgrade = dich_the(card_normal)

                if upgrade != 0:
                    list_card_normal_can_buy.append(card_normal)
                    continue

                if not max((give > 0) * (input_need <= 0)) and not max((receive > 0) * (output_need <= 0)):
                    list_card_normal_can_buy.append(card_normal)

            else:
                break

        if len(list_card_normal_can_buy) != 0:
            list_card_rating = []
            for card_normal in list_card_normal_can_buy:
                list_card_rating.append(card_normal_rating(card_normal))

            indexx = list_card_rating.index(max(list_card_rating))
            card_target = list_card_normal_can_buy[indexx]
            give1, give2 = get_card_normal_setup(card_target, board, hand)

            return 'get_card_normal', card_target, give1, give2


    # if len(player.card_close + player.card_open) <level:
    #     for card_normal in board['card_normal']:
    #         id_card = board['card_normal'].index(card_normal)
    #         give, rei, times,upgrade = dich_the(card_normal)
    #         if rei[0] > 0 and sum(give) == 1 and hand[0] >= id_card:
    #             print("thẻ sinh vàng")
    #             return 'get_card_normal', card_normal, convert(str(id_card) + "-0-0-0"),convert("0-0-0-0")
    #         if sum(give) == 0 and hand[0] >= id_card:
    #             print("lấy thẻ free")
    #             return 'get_card_normal', card_normal, convert(str(id_card) + "-0-0-0"),convert("0-0-0-0")
    #         if give[0] > 0 and sum(give*np.array([0,1,1,1])) == 0 and hand[0] >= id_card:
    #             print("thẻ đổi vàng")
    #             return 'get_card_normal', card_normal, convert(str(id_card) + "-0-0-0"),convert("0-0-0-0")


    rest = {'give_back': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0}, 'receive': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0}, 'upgrade': 0, 'times': 100, 'bonus': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0}}
    full_hand = player.card_close + player.card_open + board['card_point'] + [rest]
    cards = player.card_close+board['card_point'] + [rest]
    score_max = 0
    card_use = None
    start_score = sum(hand*np.array([1,2,3,4]))
    ter = 5
    target_state = None

    list_card_normal_can_buy = []

    for i in range(0, hand[0]+1, 1):
        #print(len(board['card_normal'][i]))
        if i >= len(board['card_normal']):
            break
        list_card_normal_can_buy.append(board['card_normal'][i])

    for card in list_card_normal_can_buy:
        give1_, give2_ = get_card_normal_setup(card, board, hand)

        give1 = np.array(list(give1_.values()))
        give2 = np.array(list(give2_.values()))

        bonus_material = np.array(list(card['bonus'].values()))

        new_hand = hand - give1 - give2 + bonus_material
        new_cards = cards + [card]
        new_full_hand = full_hand + [card]
        new_start_score = sum(new_hand * np.array([1,2,3,4]))
        item = [[new_hand], new_full_hand, 0]

        item = [[new_hand], new_cards, 0]

        value, b, c = future([item], 1, ter, 0, start_score, new_full_hand)

        if value > score_max:
            score_max = value
            card_use = card
            target_state = new_hand


    for card in cards:
        if "times" in card.keys() and card["times"] == 100:
            item = [[hand],full_hand,0]
            evaluate,b,c = future([item],1,ter,0,start_score,full_hand)
            if evaluate > score_max:
                score_max = evaluate
                card_use = card
                target_state = hand
        states, diem  = card_to_state(hand,card,0)
        new_cards = [car for car in cards if car != card]
        for state in states:
            item = [[state],new_cards,diem]
            evaluate,b,c = future([item],1,ter,0,start_score,full_hand)
            if evaluate > score_max:
                score_max = evaluate
                card_use = card
                target_state = state
    if score_max < 1:
        return "relax"
    # print(score_max,target_state,dich_the(card_use))
    give, rei, times,upgrade = dich_the(card_use)
    # nếu target thẻ nghỉ
    if times == 100:
        return "relax"

    # Lấy thẻ thường ở bàn
    if card_use in board['card_normal']:
        give1, give2 = get_card_normal_setup(card_use, board, hand)

        return 'get_card_normal', card_use, give1, give2
    # nếu target thẻ điểm
    if upgrade > 5:
        return 'get_card_point', card_use
    # nếu target thẻ normal
    else:
        if upgrade > 0:
            tra,lay = hand_to_target(hand,target_state)
            return 'card_update', card_use, convert(tra), convert(lay)
        if sum(give) == 0:
            tra = the_lay_free(hand,target_state,give,rei)
            return 'card_get_material', card_use, convert(tra)
        else:
            lan,tra_ve = the_doi_nl(hand,target_state,give,rei)
            return 'card_exchange', card_use, lan, convert(tra_ve)















