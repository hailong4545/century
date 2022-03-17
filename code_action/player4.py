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

def action(player, board):
    cards = []
    for card in player.card_close:
        card1 = card.copy()
        card1['bonus'] = 0
        cards.append(card1)
    for card in board['card_normal']:
        card1 = card.copy()
        card1['bonus'] = 0
        cards.append(card1)
    json_object = json.dumps(cards)
    with open("card_list.json", "w") as outfile:
        outfile.write(json_object)
    if len(board['card_normal']) > 0:
        return 'get_card_normal', board['card_normal'][0], convert('0-0-0-0'),convert('0-0-0-0')
    return "relax"
                 


            
