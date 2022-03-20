from read_data_game import *
from init_game import *
from Player import *
from copy import deepcopy


class Century():

    def __init__(self):
        self.coins = {'gold': 10, 'silver': 10}
        self.all_card_normal, self.all_card_point = initGame(*readDataGame())
        self.card_point_close = self.all_card_point[5:]
        self.card_normal_close = self.all_card_normal[6:]
        self.card_normal_open = self.all_card_normal[:6]
        self.card_point_open = setBonus(self.all_card_point[:5], self.coins)
        self.turn = 1

    @property
    def run(self):
        data_player = []
        for id in range(1, 6):
            data_player.append(Player(id))

        while not stop_game(data_player):
            print("Turn: ", self.turn)
            for player in data_player:
                card_normal = self.card_normal_open.copy()
                card_point = self.card_point_open.copy()
                coins = self.coins.copy()

                ps_players = []
                for p in data_player:
                    if player.id != p.id:
                        ps_players.append(deepcopy(p))
                        ps_players[-1].card_close = []

                board_game = {'turn': self.turn, 'coins': self.coins, 'card_normal': self.card_normal_open.copy(),
                              'card_point': self.card_point_open.copy(), 'players': ps_players}


                action_player = player.action(board_game)
                # print(action_player)

                if type(action_player) == type('string'):
                    action_player = [action_player]

                if not check_action(action_player):
                    print(action_player)
                    raise Exception(f'NGƯỜI CHƠI {player.id} OUTPUT RA SAI SỬA ĐI')
                else:
                    print(action_player)


                if action_player[0] == "relax":
                    player.relax

                elif action_player[0] == "get_card_point":
                    player.get_card_point(action_player[1].copy())

                    if action_player[1]['bonus'] == 1:
                        self.coins['silver'] -= 1

                    if action_player[1]['bonus'] == 3:
                        self.coins['gold'] -= 1

                    self.card_point_open.remove(action_player[1])
                    self.card_point_open += [self.card_point_close[0]]+self.card_point_open
                    self.card_point_close.pop(0)

                    self.card_point_open = setBonus(self.card_point_open, self.coins)

                elif action_player[0] == "get_card_normal":
                    if len(self.card_normal_open) == 0:
                        raise Exception(f"DÙ ĐÃ HẾT THẺ NORMAL NHƯNG NGƯỜI CHƠI {player.id} VẪN ACTION LẤY THẺ")

                    card = action_player[1].copy()
                    material_giveback = action_player[2].copy()
                    material_giveback2 = action_player[3].copy()
                    all_card = self.card_normal_open.copy()
                    pos = self.card_normal_open.index(card)

                    player.get_card_normal(card, material_giveback, material_giveback2, all_card, pos)

                    if pos != 0:
                        color = ['yellow', 'red', 'green', 'brown']
                        st = 0
                        ps_pos = 0
                        while ps_pos < pos:
                            if material_giveback[color[st]] != 0:
                                self.card_normal_open[ps_pos]['bonus'][color[st]] += 1
                                material_giveback[color[st]] -= 1
                                ps_pos += 1
                            else:
                                st += 1


                    self.card_normal_open.remove(card)

                    if len(self.card_normal_close) != 0:
                        self.card_normal_open.append(self.card_normal_close[0])
                        self.card_normal_close.pop(0)

                elif action_player[0] == "card_update":
                    card = action_player[1].copy()
                    material_giveback = action_player[2].copy()
                    material_recevie = action_player[3].copy()

                    player.use_card_upgrade(card, material_giveback, material_recevie)

                elif action_player[0] == "card_get_material":
                    card = action_player[1].copy()
                    material_remove = action_player[2].copy()

                    player.use_card_get_material(card, material_remove)

                elif action_player[0] == "card_exchange":
                    card = action_player[1].copy()
                    times = action_player[2]
                    material_remove = action_player[3].copy()

                    player.use_card_exchange(card, times, material_remove)

                else:
                    raise Exception(
                        'Không có action nào để đọc'
                    )
            self.turn += 1

            # if self.turn == 2:
            #     data_player[0].count_card = 5
            #     data_player[0].count_point = 40

        id_win = check_player_win(data_player)
        show_point_players(data_player, id_win)
        # print(data_player[2].material)


game = Century()
game.run
