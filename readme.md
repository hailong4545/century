Player:
  - id: ID của người chơi
  - material: Nguyên liệu hiện có (dict)
  - card_open: Các thẻ đã sử dụng
  - card_close: Các thẻ chưa sử dụng
  - card_point: Các thẻ có điểm đã mua
  - count_card: Số lượng thẻ có điểm đã mua
  - count_point: Tổng điểm hiện có
 
 board:
  - turn: Lượt chơi hiện tại (1, 2, 3....)
  - coins: Số đồng vàng đồng bạc
  - card_normal: Thẻ không có điểm đang ở trên bàn
  - card_point: Thẻ có điểm đang ở trên bàn
  - players: Thông tin của các người chơi còn lại(là một array mỗi phần tử là một người chơi truy cập vào thuộc tính tương tự Player)
 
 card: Chia thành 2 loại
  - Thẻ không có điểm: {'give_back': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 1}, 'receive': {'yellow': 3, 'red': 0, 'green': 1, 'brown': 0}, 'upgrade': 0, 'times': 10, 'bonus': {'yellow': 0, 'red': 0, 'green': 0, 'brown': 0}}
      - give_back: số nguyên liệu người chơi trả cho bàn chơi
      - receive: số nguyên liệu người chơi nhận lại từ bàn chơi
      - upgrade: Số lần nâng cấp (chỉ có thẻ nâng cấp thì upgrade khác 0)
      - times: Số lần sử dụng tối đa trong 1 turn
      - bonus: Số nguyên liệu các người chơi trước đã rải
      
  - Thẻ có điểm: {'give_back': {'yellow': 2, 'red': 2, 'green': 0, 'brown': 2}, 'receive': 15, 'bonus': 0}
      - give_back: số nguyên liệu người chơi trả cho bàn chơi
      - receive: số điểm người chơi nhận lại từ bàn chơi chưa tính bonus
      - bonus: Số điểm được cộng thêm từ các đồng xu, đồng vàng
  
  
 

- Nghỉ Ngơi: return 'relax'
- Lấy thẻ có điểm: 'get_card_point', card
- Lấy thẻ không có điểm: 'get_card_normal', card, material_giveback, material_giveback2 (1)
- Sử dụng thẻ:
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


Chú ý với phần lấy thẻ không có điểm (1) thì:
  - material_giveback: nguyên liệu rải ra bàn chơi để lấy thẻ
  - material_giveback2: nguyên liệu trả lại bàn chơi nếu có thừa 10 nguyên liệu (phải thêm tham số này cho đầu ra vì vừa sửa các thẻ normal có thêm thuộc tính bonus là các nguyên liệu các người chơi rải ra nên có thể sau khi lấy thẻ thì tổng số nguyên liệu của người chơi lớn hơn 10)
