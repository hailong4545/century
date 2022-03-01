'''
    Nghỉ Ngơi: return 'relax'
    Lấy thẻ có điểm: 'get_card_point', card
    Lấy thẻ không có điểm: 'get_card_normal', card, material_giveback, material_giveback2
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
from init_game import convert, check_get_card_point

def action(player, board):
    card_point = board['card_point']
    card_normal = board['card_normal']

    target = card_point[0]['give_back']
    total = sum(list(target.values()))
    #print(card_ponit[0])
    #print(player.material)

    if check_get_card_point(player.material, card_point[0]):
        return 'get_card_point', card_point[0]

    if sum(list(player.material.values())) < total:
        for card in player.card_close:
            if card['upgrade'] == 0:
                if total - sum(list(player.material.values())) == 1:
                    return 'card_get_material', card, convert('1-0-0-0')
                else:
                    return 'card_get_material', card, convert('0-0-0-0')

    else:
        for card in player.card_close:
            if card['upgrade'] > 0:
                for cl in player.material.keys():
                    if player.material[cl] > target[cl]:
                        if cl == 'yellow':
                            return 'card_update', card, convert('1-0-0-0'), convert('0-1-0-0')
                        elif cl == 'red':
                            return 'card_update', card, convert('0-1-0-0'), convert('0-0-1-0')
                        elif cl == 'green':
                            return 'card_update', card, convert('0-0-1-0'), convert('0-0-0-1')

                #return 'card_update', card, convert('0-0-0-0'),
    return 'relax'

                 


            
