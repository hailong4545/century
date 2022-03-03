from read_data_game import convert
from init_game import setDefault
from code_action import player6 as p1, player2 as p2, player3 as p3, player4 as p4, player5 as p5
from copy import deepcopy

class Player():

    def __init__(self, id):
        self.id = id
        if id == 1:
            self.material = convert('3-0-0-0')
        elif id == 4 or id == 5:
            self.material = convert('3-1-0-0')
        else:
            self.material = convert('4-0-0-0')
        
        self.card_open = []
        self.card_close = setDefault()
        self.card_point = []
        self.count_card = 0
        self.count_point = 0
    
    @property
    def relax(self):
        self.card_close += self.card_open
        self.card_open = []
    
    def get_card_normal(self, card, material_giveback, material_giveback2, all_card, pos):
        if card not in all_card:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: LẤY THẺ KHÔNG CÓ TRÊN BÀN')
        
        if sum(list(material_giveback.values())) > pos:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: NGUYÊN LIỆU TRẢ LẠI BÀN CHƠI THỪA ĐỂ LẤY THẺ')
        
        if sum(list(material_giveback.values())) < pos:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: NGUYÊN LIỆU TRẢ LẠI BÀN CHƠI KO ĐỦ ĐỂ LẤY THẺ') 
        
        for cl in self.material.keys():
            if self.material[cl] < material_giveback[cl]:
                raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: KHÔNG CÓ ĐỦ NGUYÊN LIỆU ĐỂ LẤY THẺ')

        for cl in self.material.keys():
            self.material[cl] += card['bonus'][cl] - material_giveback2[cl]- material_giveback[cl]

        if sum(list(self.material.values())) > 10:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: Nguyên liệu vượt quá 10')

        self.card_close.append(card)
    
    def get_card_point(self, card):
        # if card not in self.card_close:
        #     raise Exception("CODE BOT LỖI KHI LẤY THẺ")

        self.card_point.append(card)
        self.count_card += 1
        self.count_point += int(card['receive']) + int(card['bonus'])

        for cl in self.material.keys():
            self.material[cl] -= card['give_back'][cl]
    
    def use_card_exchange(self, card, times, material_remove):
        if card not in self.card_close:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: SỬ DỤNG THẺ ĐÃ SỬ DỤNG')

        for cl in self.material.keys():
            if self.material[cl] < times * card['give_back'][cl]:
                raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: KHÔNG ĐỦ NGUYÊN LIỆU ĐỂ TRAO ĐỔI')
        
        for cl in self.material.keys():
            self.material[cl] += times * (card['receive'][cl] - card['give_back'][cl])

        for cl in self.material.keys():
            self.material[cl] -= material_remove[cl]

        if sum(list(self.material.values())) > 10:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: THỪA NGUYÊN LIỆU')

        self.card_close.remove(card)
        self.card_open.append(card)
            
    def use_card_upgrade(self, card, material_giveback, material_recevie):
        if card not in self.card_close:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: SỬ DỤNG THẺ ĐÃ SỬ DỤNG')
        
        if sum(list(material_giveback.values())) > card['upgrade']:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: SỬ DỤNG THẺ UPDATE QUÁ MỨC CHO PHÉP')

        if sum(list(material_giveback.values())) != sum(list(material_recevie.values())):
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: NGUYÊN LIỆU UPDATE KHÔNG ĐỒNG ĐỀU')

        for cl in self.material.keys():
            if self.material[cl] < material_giveback[cl]:
                raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: KHÔNG ĐỦ NGUYÊN LIỆU ĐỂ TRAO ĐỔI')
        
        color = {'yellow': 1, 'red': 2, 'green': 3, 'brown': 4}

        for cl in color.keys():
            if material_giveback[cl] > material_recevie[cl]:
                break
            elif material_giveback[cl] < material_recevie[cl]:
                raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: ĐỔI NGUYÊN LIỆU KHÔNG HỢP LỆ')
            else:
                continue

        count_upgrade = 0
        for cl in color.keys():
            count_upgrade += (material_recevie[cl] - material_giveback[cl]) * color[cl]
        
        if count_upgrade < 0 or count_upgrade > card['upgrade']:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: ĐỔI NGUYÊN LIỆU KHÔNG HỢP LỆ')
        
        for cl in color.keys():
            self.material[cl] += material_recevie[cl] - material_giveback[cl]
        
        self.card_close.remove(card)
        self.card_open.append(card)
    
    def use_card_get_material(self, card, material_remove):
        if card not in self.card_close:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: SỬ DỤNG THẺ ĐÃ SỬ DỤNG')
        
        for cl in self.material.keys():
            self.material[cl] += card['receive'][cl] - material_remove[cl]
        
        if sum(list(self.material.values())) > 10:
            raise Exception(f'NGƯỜI CHƠI {self.id} CODE BOT LỖI: THỪA NGUYÊN LIỆU')
        
        self.card_close.remove(card)
        self.card_open.append(card)
    

    def action(self, board):
        if self.id == 1:
            return p1.action(deepcopy(self), board)
        elif self.id == 2:
            return p2.action(deepcopy(self), board)
        elif self.id == 3:
            return p3.action(deepcopy(self), board)
        elif self.id == 4:
            return p4.action(deepcopy(self), board)
        elif self.id == 5:
            return p5.action(deepcopy(self), board)

        

    
    


        


            

        
        


        
    
