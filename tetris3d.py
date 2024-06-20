from tkinter import *
from tkinter import messagebox as msgbox
from random import randint as rnd
import math as m

#グローバル変数
vertical = 20     #基盤の縦のマス数
side = 10     #基盤の横のマス数
depth = 10    #基盤の奥行きマス数
size = 30     #1マスの大きさ
mino_size = 4    #ミノの(縦横最大の)ブロック数
form = 0    #ミノの種類
nextform = [7,7,7,7,7]
mode = 0    #ミノの向き
y = -1     #ミノのy座標
x = 4     #ミノのx座標
z = 0
speed = 50     #落下速度
sita1 = m.pi*20/180  #横回転度数
sita2 = m.pi*20/180  #縦回転度数
#色の定義
colors = ["#00ffff", #I:0
          "#0000ff", #J:1
          "#ffa500", #L:2
          "#ffff00", #O:3
          "#008000", #S:4
          "#800080", #T:5
          "#ff0000", #Z:6
          "#202020", #foundation:7
          "#003333", #Iguide:8
          "#000033", #Jg:9
          "#332100", #Lg:10
          "#333300", #Og:11
          "#002000", #Sg:12
          "#200020", #Tg:13
          "#330000", #Zg:14
          "#404040", #foundationguide:15
          "#00aaaa", #Iguide2:16
          "#0000aa", #Jg2:17
          "#aa7800", #Lg2:18
          "#aaaa00", #Og2:19
          "#005a00", #Sg2:20
          "#5a005a", #Tg2:21
          "#aa0000", #Zg2:22
          "#161616"  #foundationguide2:23
          ] 

#ミノの移動と回転
y_data = [0, 0, 0, 0]
x_data = [0, 0, 0, 0]
z_data = [0, 0, 0, 0]
foundation_data = [7, 7, 7, 7]

#基盤
foundation = [[[7 for i in range(depth + 2)] for i in range(side + 2)] for j in range(vertical + 2)]
for i in range(vertical + 2):
    foundation[i][0], foundation[i][side + 1] = [8 for i in range(depth + 2)], [8 for i in range(depth + 2)]
    for j in range(side + 2):
        foundation[i][j][0], foundation[i][j][depth + 1] = 8,8
foundation[vertical + 1] = [[8 for i in range(depth + 2)] for j in range(side + 2)]

def draw_foundation():
    cv.create_rectangle(0, 0, 800, 800, fill="#101010")
    vd = 0      #vertical方向のマス数
    v1 = vd * size
    v2 = v1 + size * vertical
    sd = 0       #side方向のマス数
    s1 = sd * size
    s2 = s1 + size * side
    d = size * depth    #depth方向のマス数
    draw_x1,draw_x2,draw_x3,draw_x4= 300 + s1*m.cos(sita1), 300 + s2*m.cos(sita1), 300 + s2*m.cos(sita1), 300 + s1*m.cos(sita1),   #左上、右上、右下、左下
    draw_y1,draw_y2,draw_y3,draw_y4= 250 + (v1*m.cos(sita2)-s1*m.sin(sita1)), 250 + (v1*m.cos(sita2)-s2*m.sin(sita1)), 250 + (v2*m.cos(sita2)-s2*m.sin(sita1)), 250 + (v2*m.cos(sita2)-s1*m.sin(sita1))
    draw_x5,draw_x6,draw_x7,draw_x8= 300 + s1*m.cos(sita1)-d*m.sin(sita1), 300 + s2*m.cos(sita1)-d*m.sin(sita1), 300 + s2*m.cos(sita1)-d*m.sin(sita1), 300 + s1*m.cos(sita1)-d*m.sin(sita1)   #左上、右上、右下、左下
    draw_y5,draw_y6,draw_y7,draw_y8= 250 + (v1*m.cos(sita2)-s1*m.sin(sita1))-d*m.sin(sita2), 250 + (v1*m.cos(sita2)-s2*m.sin(sita1))-d*m.sin(sita2), 250 + (v2*m.cos(sita2)-s2*m.sin(sita1))-d*m.sin(sita2), 250 + (v2*m.cos(sita2)-s1*m.sin(sita1))-d*m.sin(sita2)
    cv.create_polygon(draw_x3,draw_y3,draw_x4,draw_y4,draw_x8,draw_y8,draw_x7,draw_y7,fill=colors[7])
    cv.create_polygon(draw_x5,draw_y5,draw_x6,draw_y6,draw_x7,draw_y7,draw_x8,draw_y8,fill=colors[23])
    for v in range(vertical):
        vd = vertical - v-1   #vertical方向のマス数
        v1 = vd * size
        v2 = v1 + size
        for s in range(side):
            sd = side - s-1      #side方向のマス数
            s1 = sd * size
            s2 = s1 + size
            for d in range(depth):
                dd = side - d-1    #depth方向のマス数
                d1 = dd * size
                d2 = d1 + size
                for c in range(len(colors)):
                    if foundation[vd + 1][sd + 1][dd + 1] == c and c != 7:
                        color = colors[c]
                        color2 = colors[c+16]                 
                        draw_x1,draw_x2,draw_x3,draw_x4= 300 + s1*m.cos(sita1)-d1*m.sin(sita1), 300 + s2*m.cos(sita1)-d1*m.sin(sita1), 300 + s2*m.cos(sita1)-d1*m.sin(sita1), 300 + s1*m.cos(sita1)-d1*m.sin(sita1)  #左上、右上、右下、左下
                        draw_y1,draw_y2,draw_y3,draw_y4= 250 + (v1*m.cos(sita2)-s1*m.sin(sita1))-d1*m.sin(sita1), 250 + (v1*m.cos(sita2)-s2*m.sin(sita1))-d1*m.sin(sita1), 250 + (v2*m.cos(sita2)-s2*m.sin(sita1))-d1*m.sin(sita1), 250 + (v2*m.cos(sita2)-s1*m.sin(sita1))-d1*m.sin(sita1)
                        draw_x5,draw_x6,draw_x7,draw_x8= 300 + s1*m.cos(sita1)-d2*m.sin(sita1), 300 + s2*m.cos(sita1)-d2*m.sin(sita1), 300 + s2*m.cos(sita1)-d2*m.sin(sita1), 300 + s1*m.cos(sita1)-d2*m.sin(sita1)   #左上、右上、右下、左下
                        draw_y5,draw_y6,draw_y7,draw_y8= 250 + (v1*m.cos(sita2)-s1*m.sin(sita1))-d2*m.sin(sita2), 250 + (v1*m.cos(sita2)-s2*m.sin(sita1))-d2*m.sin(sita2), 250 + (v2*m.cos(sita2)-s2*m.sin(sita1))-d2*m.sin(sita2), 250 + (v2*m.cos(sita2)-s1*m.sin(sita1))-d2*m.sin(sita2)
                        cv.create_polygon(draw_x1,draw_y1,draw_x2,draw_y2,draw_x3,draw_y3,draw_x4,draw_y4,fill=color)
                        cv.create_polygon(draw_x1,draw_y1,draw_x2,draw_y2,draw_x6,draw_y6,draw_x5,draw_y5,fill=color2)
                        cv.create_polygon(draw_x1,draw_y1,draw_x5,draw_y5,draw_x8,draw_y8,draw_x4,draw_y4,fill=color2)
                        #cv.create_rectangle(s1, v1, s2, v2, fill=color)
    draw_next()

def draw_next():
    for i in range(len(nextform)):
        for w in range(mino_size):
            mino_data[i][0][w]    
            v1 = 20 + 30*i + mino_data[nextform[i]][3][w][1]*size/5
            v2 = v1 + size/5
            s1 = 700 + 50 - mino_data[nextform[i]][3][w][0]*size/5
            s2 = s1 + size/5
            cv.create_rectangle(s1, v1, s2, v2, fill = colors[nextform[i]])


#ミノ作成 y x z
mino_data = [[[[2, 0, 1], [2, 1, 1], [2, 2, 1], [2, 3, 1]], #I:0
              [[0, 1, 1], [1, 1, 1], [2, 1, 1], [3, 1, 1]],
              [[1, 0, 1], [1, 1, 1], [1, 2, 1], [1, 3, 1]],
              [[0, 2, 1], [1, 2, 1], [2, 2, 1], [3, 2, 1]]],
             [[[1, 0, 1], [2, 0, 1], [2, 1, 1], [2, 2, 1]], #J:1
              [[1, 1, 1], [1, 2, 1], [2, 1, 1], [3, 1, 1]],
              [[2, 0, 1], [2, 1, 1], [2, 2, 1], [3, 2, 1]],
              [[1, 1, 1], [2, 1, 1], [3, 0, 1], [3, 1, 1]]],
             [[[1, 2, 1], [2, 0, 1], [2, 1, 1], [2, 2, 1]], #L:2
              [[1, 1, 1], [2, 1, 1], [3, 1, 1], [3, 2, 1]],
              [[2, 0, 1], [2, 1, 1], [2, 2, 1], [3, 0, 1]],
              [[1, 0, 1], [1, 1, 1], [2, 1, 1], [3, 1, 1]]],
             [[[1, 1, 1], [1, 2, 1], [2, 1, 1], [2, 2, 1]], #O:3
              [[1, 1, 1], [1, 2, 1], [2, 1, 1], [2, 2, 1]],
              [[1, 1, 1], [1, 2, 1], [2, 1, 1], [2, 2, 1]],
              [[1, 1, 1], [1, 2, 1], [2, 1, 1], [2, 2, 1]]],
             [[[1, 1, 1], [1, 2, 1], [2, 0, 1], [2, 1, 1]], #S:4
              [[1, 1, 1], [2, 1, 1], [2, 2, 1], [3, 2, 1]],
              [[2, 1, 1], [2, 2, 1], [3, 0, 1], [3, 1, 1]],
              [[1, 0, 1], [2, 0, 1], [2, 1, 1], [3, 1, 1]]],
             [[[1, 1, 1], [2, 0, 1], [2, 1, 1], [2, 2, 1]], #T:5
              [[1, 1, 1], [2, 1, 1], [2, 2, 1], [3, 1, 1]],
              [[2, 0, 1], [2, 1, 1], [2, 2, 1], [3, 1, 1]],
              [[1, 1, 1], [2, 0, 1], [2, 1, 1], [3, 1, 1]]],
             [[[1, 0, 1], [1, 1, 1], [2, 1, 1], [2, 2, 1]], #Z:6
              [[1, 2, 1], [2, 1, 1], [2, 2, 1], [3, 1, 1]],
              [[2, 0, 1], [2, 1, 1], [3, 1, 1], [3, 2, 1]],
              [[1, 1, 1], [2, 0, 1], [2, 1, 1], [3, 0, 1]]]]
mino = [[[7 for i in range(mino_size)] for j in range(mino_size)] for k in range(mino_size)]


def create_mino():
    global form, nextform, mino
    for i in range(len(nextform)):
        if nextform[i] == 7:
            nextform[i] = rnd(0, 6)
    form = nextform[0]
    for i in range(len(nextform)):
        if i == len(nextform)-1:
            nextform[i] = rnd(0, 6)
        else:
            nextform[i] = nextform[i+1]
    for i in range(len(mino_data[form][mode % 4])):
        y = mino_data[form][mode % 4][i][0]
        x = mino_data[form][mode % 4][i][1]
        z = mino_data[form][mode % 4][i][2]
        mino[y][x][z] = form

def draw_mino():
    global x, y, z,foundation, mino, mode
    global x_data, y_data, z_data, foundation_data
    guide_flag = True
    dy = 0
    while(guide_flag):
        for i in range(len(mino_data[form][mode % 4])):
            y_data[i] = mino_data[form][(mode) % 4][i][0] + y
            x_data[i] = mino_data[form][(mode) % 4][i][1] + x
            z_data[i] = mino_data[form][(mode) % 4][i][2] + z
            foundation_data[i] = foundation[y_data[i] + 1][x_data[i]][z_data[i]]
        if foundation_data == [7, 7, 7, 7]:
            dy += 1
            y += 1
        if foundation_data != [7, 7, 7, 7]:
            guide_flag = False

    for v in range(mino_size):
        vd = mino_size - v-1
        v1 = (vd + y - 1) * size
        v2 = v1 + size
        for s in range(mino_size):
            sd = mino_size - s-1
            s1 = (sd + x - 1) * size
            s2 = s1 + size
            for d in range(mino_size):
                dd = mino_size - d-1
                d1 = (dd + z - 1) * size
                d2 = d1 + size
                if mino[vd][sd][dd] == form:
                    color = colors[form+16]               
                    draw_x1,draw_x2,draw_x3,draw_x4= 300 + s1*m.cos(sita1)-d1*m.sin(sita1), 300 + s2*m.cos(sita1)-d1*m.sin(sita1), 300 + s2*m.cos(sita1)-d1*m.sin(sita1), 300 + s1*m.cos(sita1)-d1*m.sin(sita1)  #左上、右上、右下、左下
                    draw_y1,draw_y2,draw_y3,draw_y4= 250 + (v1*m.cos(sita2)-s1*m.sin(sita1))-d1*m.sin(sita1), 250 + (v1*m.cos(sita2)-s2*m.sin(sita1))-d1*m.sin(sita1), 250 + (v2*m.cos(sita2)-s2*m.sin(sita1))-d1*m.sin(sita1), 250 + (v2*m.cos(sita2)-s1*m.sin(sita1))-d1*m.sin(sita1)
                    draw_x5,draw_x6,draw_x7,draw_x8= 300 + s1*m.cos(sita1)-d2*m.sin(sita1), 300 + s2*m.cos(sita1)-d2*m.sin(sita1), 300 + s2*m.cos(sita1)-d2*m.sin(sita1), 300 + s1*m.cos(sita1)-d2*m.sin(sita1)   #左上、右上、右下、左下
                    draw_y5,draw_y6,draw_y7,draw_y8= 250 + (v1*m.cos(sita2)-s1*m.sin(sita1))-d2*m.sin(sita2), 250 + (v1*m.cos(sita2)-s2*m.sin(sita1))-d2*m.sin(sita2), 250 + (v2*m.cos(sita2)-s2*m.sin(sita1))-d2*m.sin(sita2), 250 + (v2*m.cos(sita2)-s1*m.sin(sita1))-d2*m.sin(sita2)
                    cv.create_polygon(draw_x1,draw_y1,draw_x2,draw_y2,draw_x3,draw_y3,draw_x4,draw_y4,fill=colors[23],width = 1, outline = color)
                    cv.create_polygon(draw_x1,draw_y1,draw_x2,draw_y2,draw_x6,draw_y6,draw_x5,draw_y5,fill=colors[23],width = 1, outline = color)
                    cv.create_polygon(draw_x1,draw_y1,draw_x5,draw_y5,draw_x8,draw_y8,draw_x4,draw_y4,fill=colors[23],width = 1, outline = color)
    y -= dy
    for v in range(mino_size):
        vd = mino_size - v-1
        v1 = (vd + y - 1) * size
        v2 = v1 + size
        for s in range(mino_size):
            sd = mino_size - s-1
            s1 = (sd + x - 1) * size
            s2 = s1 + size
            for d in range(mino_size):
                dd = mino_size - d-1
                d1 = (dd + z - 1) * size
                d2 = d1 + size
                if mino[vd][sd][dd] == form:
                    color = colors[form]
                    color2 = colors[form+16]               
                    draw_x1,draw_x2,draw_x3,draw_x4= 300 + s1*m.cos(sita1)-d1*m.sin(sita1), 300 + s2*m.cos(sita1)-d1*m.sin(sita1), 300 + s2*m.cos(sita1)-d1*m.sin(sita1), 300 + s1*m.cos(sita1)-d1*m.sin(sita1)  #左上、右上、右下、左下
                    draw_y1,draw_y2,draw_y3,draw_y4= 250 + (v1*m.cos(sita2)-s1*m.sin(sita1))-d1*m.sin(sita1), 250 + (v1*m.cos(sita2)-s2*m.sin(sita1))-d1*m.sin(sita1), 250 + (v2*m.cos(sita2)-s2*m.sin(sita1))-d1*m.sin(sita1), 250 + (v2*m.cos(sita2)-s1*m.sin(sita1))-d1*m.sin(sita1)
                    draw_x5,draw_x6,draw_x7,draw_x8= 300 + s1*m.cos(sita1)-d2*m.sin(sita1), 300 + s2*m.cos(sita1)-d2*m.sin(sita1), 300 + s2*m.cos(sita1)-d2*m.sin(sita1), 300 + s1*m.cos(sita1)-d2*m.sin(sita1)   #左上、右上、右下、左下
                    draw_y5,draw_y6,draw_y7,draw_y8= 250 + (v1*m.cos(sita2)-s1*m.sin(sita1))-d2*m.sin(sita2), 250 + (v1*m.cos(sita2)-s2*m.sin(sita1))-d2*m.sin(sita2), 250 + (v2*m.cos(sita2)-s2*m.sin(sita1))-d2*m.sin(sita2), 250 + (v2*m.cos(sita2)-s1*m.sin(sita1))-d2*m.sin(sita2)
                    cv.create_polygon(draw_x1,draw_y1,draw_x2,draw_y2,draw_x3,draw_y3,draw_x4,draw_y4,fill=color)
                    cv.create_polygon(draw_x1,draw_y1,draw_x2,draw_y2,draw_x6,draw_y6,draw_x5,draw_y5,fill=color2)
                    cv.create_polygon(draw_x1,draw_y1,draw_x5,draw_y5,draw_x8,draw_y8,draw_x4,draw_y4,fill=color2)

#メイン関数を定義
def main():
    global win, cv
    win = Tk()     #ウィンドウの作成
    cv = Canvas(win, width=800, height=800)     #キャンバスの作成
    cv.pack()    #オブジェクト配置のオプション
    create_mino()
    draw_foundation()
    draw_mino()
  

    left = Move_mino(0, -1, 0, 0)
    right = Move_mino(0, 1, 0, 0)
    back = Move_mino(0, 0, 1, 0)
    front = Move_mino(0, 0, -1, 0)
    under = Move_mino(1, 0, 0, 0)
    harddrop = Move_mino(1, 0, 0, 0)
    left_spin = Move_mino(0, 0, 0, -1)
    right_spin = Move_mino(0, 0, 0, 1)

    win.bind("<Left>", left.move_mino)     #左キーが押されたら左に移動
    win.bind("<Right>", right.move_mino)     #右キーが押されたら右に移動
    win.bind("<w>", back.move_mino)     #wキーが押されたら奥に移動
    win.bind("<s>", front.move_mino)     #sキーが押されたら手前に移動
    win.bind("<Down>", under.move_mino)          #下キーが押されたら下に移動
    win.bind("<Up>", harddrop.hard_move_mino)        #上キーが押されたら即落下  
    win.bind("<a>", right_spin.spin_mino)     #aキーが押されたら右回転
    win.bind("<d>", left_spin.spin_mino)     #dキーが押されたら左回転
    under.drop_mino()
    win.mainloop()     #記載済

  

class Move_mino:
    def __init__(self, next_y, next_x, next_z, next_mode):
        self.next_y = next_y
        self.next_x = next_x
        self.next_z = next_z
        self.next_mode = next_mode

    def reference(self):
        global x_data, y_data, z_data, foundation_data
        for i in range(len(mino_data[form][mode % 4])):
             y_data[i] = mino_data[form][(mode + self.next_mode) % 4][i][0] + y
             x_data[i] = mino_data[form][(mode + self.next_mode) % 4][i][1] + x
             z_data[i] = mino_data[form][(mode + self.next_mode) % 4][i][2] + z
             foundation_data[i] = foundation[y_data[i] + self.next_y][x_data[i] + self.next_x][z_data[i] + self.next_z]

    def move_mino(self, e):
         global x, y, z, foundation_data, mino, mode
         self.reference()
         if foundation_data == [7, 7, 7, 7]:
          y += 1 * self.next_y
          x += 1 * self.next_x
          z += 1 * self.next_z
         if self.next_y == 1 and foundation_data != [7, 7, 7, 7]:
            for i in range(len(y_data)):
                 foundation[y_data[i]][x_data[i]][z_data[i]] = form
            delete()
            game_over()
            mode = 0
            y = -1
            x = 4
            z = 0
            mino = [[[7 for i in range(mino_size)] for j in range(mino_size)] for k in range(mino_size)]
            create_mino()
         cv.delete("all")
         draw_foundation()
         draw_mino()
         
    def hard_move_mino(self, e):
        hard_flag = True
        while(hard_flag):
            global x, y, z, foundation_data, mino, mode
            self.reference()
            if foundation_data == [7, 7, 7, 7]:
                y += 1 * self.next_y
                x += 1 * self.next_x
                z += 1 * self.next_z
            if self.next_y == 1 and foundation_data != [7, 7, 7, 7]:
                hard_flag = False
                for i in range(len(y_data)):
                    foundation[y_data[i]][x_data[i]][z_data[i]] = form
                delete()
                game_over()
                mode = 0
                y = -1
                x = 4
                z = 0
                mino = [[[7 for i in range(mino_size)] for j in range(mino_size)] for k in range(mino_size)]
                create_mino()
            cv.delete("all")
            draw_foundation()
            draw_mino()

    def drop_mino(self):
        global speed
        self.move_mino(Event)
        #if speed > 200:
        #  speed
        cv.delete("all")
        draw_foundation()
        draw_mino()
        win.after(speed *20, self.drop_mino)
        


    def spin_mino(self, e):
       self.reference()
       global mode, mino
       if foundation_data == [7, 7, 7, 7]:
         mode += 1 * self.next_mode
         mino = [[[7 for i in range(mino_size)] for j in range(mino_size)] for k in range(mino_size)]
         for i in range(len(mino_data[form][mode % 4])):
            y = mino_data[form][mode % 4][i][0]
            x = mino_data[form][mode % 4][i][1]
            z = mino_data[form][mode % 4][i][2]
            mino[y][x][z] = form
         cv.delete("all")
         draw_foundation()
         draw_mino()

def delete():#foundation[v][s][d]    #foundation[v][s]
    for v in range(vertical):
        for d in range(depth):
            s_del =[1 for i in range(depth)]
            for s in range(side):
                if foundation[v+1][s+1][d+1] == 7:
                    s_del[s] = 0

            if(0 in s_del) == False:
                for i in range(side):
                    for j in range(v):
                        if j == v-1:
                            foundation[v+1-j][i+1][d+1] = 7
                        else:
                            foundation[v+1-j][i+1][d+1] = foundation[v-j][i+1][d+1]
"""
def delete():#foundation[v][s][d]    #foundation[v][s]
    for v in range(len(foundation)):

        if (7 in foundation[v]) == False and foundation[v] != [8 for i in range(side + 2)]:
            del foundation[v]
            add_foundation = [7 for i in range(side + 2)]
            add_foundation[0], add_foundation[side + 1] = 8, 8
            foundation.insert(0, add_foundation)
"""
def game_over():
    top_foundation = [[7 for i in range(depth + 2)] for j in range(side + 2)]
    top_foundation[0], top_foundation[side + 1] = [8 for i in range(depth + 2)], [8 for i in range(depth + 2)]
    for i in range(side+2):
        top_foundation[i][0], top_foundation[i][depth+1] = 8,8
    if foundation[1] != top_foundation:
        msgbox.showinfo(message = "Game Over")     #メッセージの表示
        quit()     #プログラムの終了

if __name__ == "__main__":
    main()