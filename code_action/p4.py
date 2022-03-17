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
import json
import random
from code_action.player1 import action as act_after

def action(player, board):
    hand = np.array(list(player.material.values()))
    act = None
    if len(player.card_close + player.card_open) < 5:
        with open('card_list.json', 'r') as openfile:
            card_list = json.load(openfile)
        score_table = np.zeros(46)
        card_observed = player.card_close + player.card_open
        for card in card_observed:
            card1 = card.copy()
            card1['bonus'] = 0
            index = card_list.index(card1)
            with open('RL/card'+ str(index) + '.json', 'r') as openfile:
                matrix = np.array(json.load(openfile))
            score_table += matrix
        so_card = len(card_observed)
        with open('RL/hand'+ str(so_card) + '.json', 'r') as openfile:
            matrix = np.array(json.load(openfile))
        score_table += matrix 
        action_available = []
        matrix_available = []
        for id_card in range(len(board['card_normal'])):
            if hand[0] >= id_card:
                action_available.append(board['card_normal'][id_card])
                card1 = card.copy()
                card1['bonus'] = 0
                index = card_list.index(card1)
                matrix_available.append(score_table[index])
        action_available.append(None)
        matrix_available.append(score_table[-1])
        act = random.choices(action_available,weights = matrix_available)[0]
        if act == None:
            id_act = -1
        else:
            card1 = act.copy()
            card1['bonus'] = 0
            id_act = card_list.index(card1)
        with open("p4learning.json") as openfile:
            action_dict = json.load(openfile)
        for card in card_observed:
            card1 = card.copy()
            card1['bonus'] = 0
            index = str(card_list.index(card1))
            if index not in action_dict.keys():
                action_dict[index] = [id_act]
            else:
                action_dict[index].append(id_act)
        index = "hand" + str(so_card)
        if index not in action_dict.keys():
            action_dict[index] = [id_act]
        else:
            action_dict[index].append(id_act)
        # print(action_dict)
        a = json.dumps(action_dict)
        with open("p4learning.json", "w") as outfile:
            outfile.write(a)
    if act == None:
        return act_after(player,board)
    else:
        for idcard in range(len(board['card_normal'])):
            if act == board['card_normal'][idcard]:
                rei = sum(act['bonus'].values())
                in_hand = sum(hand)
                total = (rei + in_hand)
                back = (total - 10)*(total > 10)
                return 'get_card_normal', act, convert(str(idcard)+"-0-0-0"), convert(str(back) + "-0-0-0")
    return "relax"
                 


            
