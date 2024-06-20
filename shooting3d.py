import tkinter as tk
import random
import math as m

game = True #ゲーム続行フラグ
game_time = 0 #ゲームの経過時間

WINDOW_HEIGHT = 600  # ウィンドウの高さ
WINDOW_WIDTH = 600   # ウィンドウの幅

CANNON_X = 300       # 自機のx座標    初期位置
CANNON_Y = 550       # 自機のy座標
CANNON_Z = 50       # 自機のz座標
CANNON_RAD_W = 0       # 自機の水平角度
CANNON_RAD_H = 0        # 自機の垂直角度

CANNON_HEIGHT = 20  # 自機の縦幅
CANNON_WIDTH = 20    # 自機の横幅
CANNON_LENGTH = 20  #自機の長さ
ENEMY_HEIGHT = 20  # 敵の縦幅
ENEMY_WIDTH = 20    # 敵の横幅
ENEMY_LENGTH = 20  #敵の長さ

NUMBER_OF_ENEMY = 25    # 敵の数
ENEMY_SHOOT_INTERVAL = 400  # 敵がランダムに弾を打ってくる間隔

BULLET_HEIGHT = 4  # 弾の縦幅
BULLET_WIDTH = 4    # 弾の横幅
BULLET_LENGTH = 10  #玉の長さ
BULLET_SPEED = 15   # 弾のスピード(10 ms)
GAME_RATE = 16  #ゲームのフレームレート

TEXT_CONGRATULATIONS_SIZE = 50  # congratularionsのサイズ
TEXT_GAMECLEAR_SIZE = 60        # gameclearのサイズ
TEXT_GAMEOVER_SIZE = 90         # gameoverのサイズ

c_x = CANNON_X      #自機のグローバル関数
c_y = CANNON_Y
c_z = CANNON_Z
c_rad_w = CANNON_RAD_W
c_rad_h = CANNON_RAD_H

class Wall:
    def __init__(self):
        
        self.x =0 #壁の座標初期化
        self.y =0
        self.z =0
          
        global c_x #自機座標読み込み
        global c_y
        global c_z
        global c_rad_w
        global c_rad_h
        self.set() #生成（壁）
        self.draw() #更新、描画

    def cal(self, x, y, z, cannon_x, cannon_y, cannon_z, p): #３次元座標を送信すると、スクリーン上の座標（二次元）を返す

        diff_x = x - cannon_x
        diff_y = y - cannon_y
        diff_z = z - cannon_z
        rad_w = m.atan2(-diff_x, -diff_y)
        rad_h = m.atan2(-diff_z, m.sqrt(diff_x**2 + diff_y**2))
        diff = m.sqrt(diff_x**2 + diff_y**2 + diff_z**2)
        diff_rad_w = rad_w - c_rad_w
        diff_rad_h = rad_h - c_rad_h

        if(diff_rad_h >= m.pi/2):
            diff_rad_h = m.pi/2
        elif(diff_rad_h <= -m.pi/2):
            diff_rad_h = -m.pi/2
        
        if(diff_rad_w > m.pi):
            diff_rad_w -= 2*m.pi
        elif(diff_rad_w <= -m.pi):
            diff_rad_w += 2*m.pi
        
        if(diff_rad_w > m.pi/2):
            diff_rad_w = m.pi/2
            if((diff_rad_h >= 0 and p == 1) or p == 0):
                diff_rad_h = m.pi/2
            if((diff_rad_h < 0 and p == 1) or p == 2) :
                diff_rad_h = -m.pi/2
        elif(diff_rad_w < -m.pi/2):
            diff_rad_w = -m.pi/2
            if((diff_rad_h >= 0 and p == 1) or p == 0):
                diff_rad_h = m.pi/2
            if((diff_rad_h < 0 and p == 1) or p == 2) :
                diff_rad_h = -m.pi/2

        if(diff_rad_h > m.pi/2):
            diff_rad_h = m.pi/2
        elif(diff_rad_h < -m.pi/2):
            diff_rad_h = -m.pi/2
        
        diff_x = -diff * m.sin(diff_rad_w) * m.cos(diff_rad_h)
        diff_y = -diff * m.cos(diff_rad_w) * m.cos(diff_rad_h)
        diff_z = -diff * m.sin(diff_rad_h)

        draw_poligon_pos_x = (WINDOW_WIDTH/2) - WINDOW_WIDTH * m.sin(diff_rad_w/2)
        draw_poligon_pos_y = (WINDOW_HEIGHT/2) - WINDOW_HEIGHT * m.sin(diff_rad_h/2)

        return draw_poligon_pos_x, draw_poligon_pos_y
    
    def cal2(self, bu0, bu1, bu2, bu3, p):#壁の平面４点（３次元）を送信すると、スクリーン上の座標（二次元）を返す
  
        pos_x = [0] * 400
        pos_y = [0] * 400
        draw_pos = [0] * 800

        for i in range(100):
            pos_x[i], pos_y[i] =  self.cal((bu1[0] * i  + bu0[0] * (100-i)) / 100,(bu1[1] * i  + bu0[1] * (100-i)) / 100,(bu1[2] * i  + bu0[2] * (100-i)) / 100, c_x, c_y, c_z, p)
        for i in range(100):
            pos_x[100+i], pos_y[100+i] =  self.cal((bu2[0] * i  + bu1[0] * (100-i)) / 100,(bu2[1] * i  + bu1[1] * (100-i)) / 100,(bu2[2] * i  + bu1[2] * (100-i)) / 100, c_x, c_y, c_z, p)
        for i in range(100):
            pos_x[200+i], pos_y[200+i] =  self.cal((bu3[0] * i  + bu2[0] * (100-i)) / 100,(bu3[1] * i  + bu2[1] * (100-i)) / 100,(bu3[2] * i  + bu2[2] * (100-i)) / 100, c_x, c_y, c_z, p)
        for i in range(100):
            pos_x[300+i], pos_y[300+i] =  self.cal((bu0[0] * i  + bu3[0] * (100-i)) / 100,(bu0[1] * i  + bu3[1] * (100-i)) / 100,(bu0[2] * i  + bu3[2] * (100-i)) / 100, c_x, c_y, c_z, p)

        for j in range(400):
                draw_pos[2*j], draw_pos[2*j+1]= pos_x[j], pos_y[j]
        return draw_pos
        
    def wall_poligon(self):#壁の座標を格納
        pos_0 = [0,0,0]#左上前
        pos_1 = [0,600,0]#左上後
        pos_2 = [600,600,0]#右上後
        pos_3 = [600,0,0]#右上前
        pos_4 = [0,0,100]#左下前
        pos_5 = [0,600,100]#左下後
        pos_6 = [600,600,100]#右下後
        pos_7 = [600,0,100]#右下前

        return [pos_0, pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7]

    def graphic_wall(self,wall_pos): #壁の描画
        
        if(self.graphic_vec(wall_pos[0], wall_pos[1], wall_pos[2], wall_pos[3])):
            self.id[0] = cv.create_polygon(self.cal2(wall_pos[0], wall_pos[1], wall_pos[2], wall_pos[3],0), fill="#e0e0f0")#up  
        if(self.graphic_vec(wall_pos[0], wall_pos[3], wall_pos[7], wall_pos[4])):
            self.id[1] = cv.create_polygon(self.cal2(wall_pos[0], wall_pos[3], wall_pos[7], wall_pos[4],0), fill="#c0c0e0")#front  
        if(self.graphic_vec(wall_pos[3], wall_pos[2], wall_pos[6], wall_pos[7])):
            self.id[2] = cv.create_polygon(self.cal2(wall_pos[3], wall_pos[2], wall_pos[6], wall_pos[7],0), fill="#c0c0e0")#right  
        if(self.graphic_vec(wall_pos[0], wall_pos[4], wall_pos[5], wall_pos[1])):
            self.id[3] = cv.create_polygon(self.cal2(wall_pos[0], wall_pos[4], wall_pos[5], wall_pos[1],0), fill="#c0c0e0")#left  
        if(self.graphic_vec(wall_pos[1], wall_pos[5], wall_pos[6], wall_pos[2])):
            self.id[4] = cv.create_polygon(self.cal2(wall_pos[1], wall_pos[5], wall_pos[6], wall_pos[2],0), fill="#c0c0e0")#back
        if(self.graphic_vec(wall_pos[4], wall_pos[7], wall_pos[6], wall_pos[5])):
            self.id[5] = cv.create_polygon(self.cal2(wall_pos[4], wall_pos[7], wall_pos[6], wall_pos[5],2), fill="#a0a0d0")#down

    def graphic_vec(self,pos0,pos1,pos2,pos3): #描画面のベクトル計算、裏から見えないようにする
        vec0 = [0] * 3
        vec1 = [0] * 3
        for i in range(3):
            vec0[i] = pos3[i]-pos0[i]
            vec1[i] = pos1[i]-pos0[i]
        gaiseki = vec0[1]*vec1[2] - vec0[2]*vec1[1], vec0[2]*vec1[0] - vec0[0]*vec1[2], vec0[0]*vec1[1] - vec0[1]*vec1[0]
        x = -m.sin(c_rad_w) * m.cos(c_rad_h)
        y = -m.cos(c_rad_w) * m.cos(c_rad_h)
        z = -m.sin(c_rad_h)
        if(x*gaiseki[0] + y*gaiseki[1] + z*gaiseki[2] > m.sqrt(x**2 + y**2 + z**2) + m.sqrt(gaiseki[0]**2 + gaiseki[1]**2 + gaiseki[2]**2) * m.sqrt(3) /2):
            return False
        else:
            return True

    def set(self):#アドレスを初期化
        self.id = [None, None, None, None, None, None]#上面,前面,右面,左面,後面,下面
        
    def draw(self): #更新、描画
        self.destroy() #いったん削除
        wall_pos = self.wall_poligon() #頂点座標を取得
        self.graphic_wall(wall_pos) #描画
        root.after(GAME_RATE, self.draw) #一定時間後にこの関数を再帰呼び出し

    def destroy(self): #削除
        for i in range(6):
            cv.delete(self.id[i])
        
class Cannon:  # 自機

    def __init__(self, x = CANNON_X, y=CANNON_Y, z=CANNON_Z, rad_w=CANNON_RAD_W, rad_h=CANNON_RAD_H): #初期設定
        self.x = x
        self.y = y
        self.z = z
        self.rad_w = rad_w
        self.rad_h = rad_h
        self.mouse_x = 0
        self.mouse_y = 0
        self.a = 0
        self.x_v = 0
        self.exist = True
        self.shot_triger = True
        self.bind() #出来るコマンド
        self.new_pos() #自機座標の更新

    def pos_show(self):#自機座標のグローバル変数化
        global c_x
        c_x = self.x
        global c_y
        c_y = self.y
        global c_z
        c_z = self.z
        global c_rad_w
        c_rad_w = self.rad_w
        global c_rad_h
        c_rad_h = self.rad_h

    def bind(self):#コマンド
        root.bind( "<KeyPress-a>", self.pressed_move_left)
        root.bind("<KeyPress-d>", self.pressed_move_right)
        root.bind( "<KeyRelease-a>", self.released_move)
        root.bind("<KeyRelease-d>", self.released_move)
        root.bind("<KeyPress-q>", self.reset)
        root.bind("<KeyPress-space>", self.pressed)
        root.bind("<KeyRelease-space>", self.released)
        root.bind("<Motion>", self.dragged)

    def pressed(self, event):#弾の発射
        if self.shot_triger:
            mybullet = MyBullet(self.x, self.y, self.z, self.rad_w, self.rad_h)#弾の生成
            mybullet.set()#弾の初期化
            mybullet.shoot()#弾の更新
            self.shot_triger = False
    def released(self, event):#弾の発射準備
        self.shot_triger = True

    def pressed_move_left(self, event):
        self.a = -1
    def pressed_move_right(self, event):
        self.a = 1
    def released_move(self, event):
        self.a = 0

    def dragged(self, event): #自機の向き検出
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.rad_w = (event.x - WINDOW_WIDTH/2) / -(WINDOW_WIDTH/2) * m.pi # -180 ~ 180
        self.rad_h = (event.y - WINDOW_HEIGHT/2) / -(WINDOW_HEIGHT/2) * m.pi / 2# -90 ~ 90
        
    def new_pos(self): #座標更新 GAME_RATE
        self.x_v += self.a
        if self.x_v > GAME_RATE/3:
            self.x_v = GAME_RATE/3
        if self.x_v < -GAME_RATE/3:
            self.x_v = -GAME_RATE/3

        self.x += self.x_v
        if (GAME_RATE/30 > self.x_v) and (-GAME_RATE/30 < self.x_v):
            self.x_v = 0
        if self.x_v > 0:
            self.x_v -= GAME_RATE/30
        if self.x_v < 0:
            self.x_v += GAME_RATE/30

        if self.x < 10:
            self.x = 10
        if self.x > 590:
            self.x = 590
        
        self.pos_show()#自機座標をグローバル化
        root.after(GAME_RATE, self.new_pos)#一定時間後にこの関数を再帰処理


    def reset(self,event):
        self.x = CANNON_X
        self.y = CANNON_Y
        self.x_v = 0
        self.a = 0

class MyBullet:  # 自分の弾

    def __init__(self, x, y, z, rad_w, rad_h):#弾の初期化
        self.x = x + 5 * m.cos(rad_w) - 5 * m.sin(rad_w) - 5 * m.sin(rad_h) * m.sin(rad_w)
        self.y = y - 5 * m.sin(rad_w) - 5 * m.cos(rad_w) - 5 * m.sin(rad_h) * m.cos(rad_w) 
        self.z = z - 5 * m.sin(rad_h) + 5 * m.cos(rad_h)
        self.rad_w = rad_w
        self.rad_h = rad_h
        self.exist = True

    def cal(self, x, y, z, cannon_x, cannon_y, cannon_z):#描画座標への変換
        diff_x = x - cannon_x
        diff_y = y - cannon_y
        diff_z = z - cannon_z
        rad_w = m.atan2(-diff_x, -diff_y)
        rad_h = m.atan2(-diff_z , m.sqrt(diff_x**2 + diff_y**2))
        diff = m.sqrt(diff_x**2 + diff_y**2+ diff_z**2)
        diff_rad_w = rad_w - c_rad_w #角度算出
        diff_rad_h = rad_h - c_rad_h

        if(diff_rad_h >= m.pi/2):
            diff_rad_h = m.pi/2
        elif(diff_rad_h <= -m.pi/2):
            diff_rad_h = -m.pi/2
        
        if(diff_rad_w > m.pi):
            diff_rad_w -= 2*m.pi
        elif(diff_rad_w <= -m.pi):
            diff_rad_w += 2*m.pi

        draw_poligon_pos_x = (WINDOW_WIDTH/2) - WINDOW_WIDTH * m.sin((diff_rad_w/2))
        draw_poligon_pos_y = (WINDOW_HEIGHT/2) - WINDOW_HEIGHT * m.sin((diff_rad_h/2))

        return draw_poligon_pos_x, draw_poligon_pos_y

    def cal2(self, bu0, bu1, bu2, bu3):#内部座標-->描画座標の変換
    
        pos_x1, pos_y1 = self.cal(bu0[0], bu0[1], bu0[2], c_x, c_y, c_z)
        pos_x2, pos_y2 = self.cal(bu1[0], bu1[1], bu1[2], c_x, c_y, c_z)
        pos_x3, pos_y3 = self.cal(bu2[0], bu2[1], bu2[2], c_x, c_y, c_z)
        pos_x4, pos_y4 = self.cal(bu3[0], bu3[1], bu3[2], c_x, c_y, c_z)
        return pos_x1, pos_y1, pos_x2, pos_y2, pos_x3, pos_y3, pos_x4, pos_y4

    def bullet_poligon(self, x, y, z):#弾の座標計算

        pos = [0] * 8
        for i in range(8):
            if (i % 4 == 0 or i % 4 == 1):
                width = -1/2
            else:
                width = 1/2

            if (i % 4 == 1 or i % 4 == 2):
                length = 1
            else:
                length = 0

            if (i < 4):
                height = -1/2
            else:
                height = 1/2
            
            diff_x = width * BULLET_WIDTH * m.cos(self.rad_w) + length * BULLET_LENGTH * m.sin(self.rad_w) - height * BULLET_HEIGHT * m.sin(self.rad_h) * m.sin(self.rad_w)
            diff_y = - width * BULLET_WIDTH * m.sin(self.rad_w) + length * BULLET_LENGTH * m.cos(self.rad_w) * m.cos(self.rad_h)  - height * BULLET_HEIGHT * m.sin(self.rad_h) * m.cos(self.rad_w) 
            diff_z = length * BULLET_LENGTH * m.sin(self.rad_h) + height * BULLET_HEIGHT * m.cos(self.rad_h)


            pos[i] = [x+diff_x, y+diff_y, z+diff_z]
        return pos

    def graphic_bullet(self,bu_pos):#弾の描画
            
        self.id[0] = cv.create_polygon(self.cal2(bu_pos[0], bu_pos[1], bu_pos[2], bu_pos[3]), fill="#8080f0")#up
        self.id[1] = cv.create_polygon(self.cal2(bu_pos[0], bu_pos[3], bu_pos[7], bu_pos[4]), fill="#6060f0")#front
        self.id[2] = cv.create_polygon(self.cal2(bu_pos[3], bu_pos[2], bu_pos[6], bu_pos[7]), fill="#6060f0")#right
        self.id[3] = cv.create_polygon(self.cal2(bu_pos[0], bu_pos[4], bu_pos[5], bu_pos[1]), fill="#6060f0")#left
        self.id[4] = cv.create_polygon(self.cal2(bu_pos[1], bu_pos[5], bu_pos[6], bu_pos[2]), fill="#6060f0")#back
        self.id[5] = cv.create_polygon(self.cal2(bu_pos[4], bu_pos[7], bu_pos[6], bu_pos[5]), fill="#4040f0")#down

    def graphic_bullet_shadow(self,bu_pos):#弾の影の描画
            
        bu_s_pos = [0] * 8
        for i in range(8):
            bu_s_pos[i] = [bu_pos[i][0], bu_pos[i][1], 100]
        
        if self.rad_h >= 0:
            self.id2[0] = cv.create_polygon(self.cal2(bu_s_pos[0], bu_s_pos[3], bu_s_pos[7], bu_s_pos[4]), fill="#404080")#front
            self.id2[1] = cv.create_polygon(self.cal2(bu_s_pos[4], bu_s_pos[7], bu_s_pos[6], bu_s_pos[5]), fill="#404080")#down  
        else:
            self.id2[0] = cv.create_polygon(self.cal2(bu_s_pos[1], bu_s_pos[5], bu_s_pos[6], bu_s_pos[2]), fill="#404080")#back
            self.id2[1] = cv.create_polygon(self.cal2(bu_s_pos[4], bu_s_pos[7], bu_s_pos[6], bu_s_pos[5]), fill="#404080")#down

    def set(self):#弾のアドレス初期化
        self.id = [None, None, None, None, None, None]#up,front,right,left,back,down
        self.id2 = [None, None]#shadow front_or_back down
  
    def shoot(self):#弾の更新
        self.destroy()
        if (self.x >= 0 and self.x <= 600) and (self.y >= 0 and self.y <= 600) and (self.z >= 0 and self.z <= 100) and self.exist and game:
            self.x += -BULLET_SPEED * m.sin(self.rad_w) * m.cos(self.rad_h)
            self.y += -BULLET_SPEED * m.cos(self.rad_w) * m.cos(self.rad_h)
            self.z += -BULLET_SPEED * m.sin(self.rad_h)

            bu_pos = self.bullet_poligon(self.x, self.y, self.z)
            self.graphic_bullet(bu_pos)
            self.graphic_bullet_shadow(bu_pos)

            self.defeat()
            root.after(GAME_RATE, self.shoot)

    def defeat(self):#敵が弾に当たったら敵を消す、玉も消える
        for enemy in enemies:
            if (abs(self.x-enemy.x) < ENEMY_WIDTH/2) and (abs(self.y-enemy.y) < ENEMY_LENGTH/2) and (abs(self.z-enemy.z) < ENEMY_HEIGHT/2):
                enemy.exist = False
                self.exist = False
                enemy.destroy()

    def destroy(self):#初期化
        for i in range(6):
            cv.delete(self.id[i])
        for i in range(2):
            cv.delete(self.id2[i])

class Enemy:  # 敵

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.rad_w = m.pi
        self.rad_h = 0
        self.exist = True
        self.set()#敵の初期化

    def enemies_poligon(self, x, y, z):#敵の座標取得
        pos = [0] * 8

        for i in range(8):
            if (i % 4 == 0 or i % 4 == 1):
                width = -1/2
            else:
                width = 1/2

            if (i % 4 == 1 or i % 4 == 2):
                length = 1/2
            else:
                length = -1/2

            if (i < 4):
                height = -1/2
            else:
                height = 1/2
            
            diff_x = width * ENEMY_WIDTH * m.cos(self.rad_w) + length * ENEMY_LENGTH * m.sin(self.rad_w) - height * ENEMY_HEIGHT * m.sin(self.rad_h) * m.sin(self.rad_w)
            diff_y = - width * ENEMY_WIDTH * m.sin(self.rad_w) + length * ENEMY_LENGTH * m.cos(self.rad_w) * m.cos(self.rad_h)  - height * ENEMY_HEIGHT * m.sin(self.rad_h) * m.cos(self.rad_w) 
            diff_z = length * ENEMY_LENGTH * m.sin(self.rad_h) + height * ENEMY_HEIGHT * m.cos(self.rad_h)


            pos[i] = [x+diff_x, y+diff_y, z+diff_z]
        return pos

    def graphic_enemies(self,ene_pos):#敵の描画
        diff_x = self.x - c_x
        diff_y = self.y - c_y
        diff_z = self.z - c_z
        rad_w = m.atan2(-diff_x, -diff_y)
        rad_h = m.atan2(-diff_z , m.sqrt(diff_x**2 + diff_y**2))
        diff = m.sqrt(diff_x**2 + diff_y**2+ diff_z**2)
        diff_rad_w = rad_w - c_rad_w #角度算出
        diff_rad_h = rad_h - c_rad_h
        if m.cos(diff_rad_w) > 0.5 and m.cos(diff_rad_h) > 0.5:
            self.id[0] = cv.create_polygon(self.cal2(ene_pos[0], ene_pos[1], ene_pos[2], ene_pos[3]), fill="#a00000")#up
            self.id[1] = cv.create_polygon(self.cal2(ene_pos[0], ene_pos[3], ene_pos[7], ene_pos[4]), fill="#800000")#front
            self.id[2] = cv.create_polygon(self.cal2(ene_pos[3], ene_pos[2], ene_pos[6], ene_pos[7]), fill="#800000")#right
            self.id[3] = cv.create_polygon(self.cal2(ene_pos[0], ene_pos[4], ene_pos[5], ene_pos[1]), fill="#800000")#left
            self.id[4] = cv.create_polygon(self.cal2(ene_pos[1], ene_pos[5], ene_pos[6], ene_pos[2]), fill="#800000")#back
            self.id[5] = cv.create_polygon(self.cal2(ene_pos[4], ene_pos[7], ene_pos[6], ene_pos[5]), fill="#600000")#down

    def cal(self, x, y, z, cannon_x, cannon_y, cannon_z):#内部座標から描画座標へ
        diff_x = x - cannon_x
        diff_y = y - cannon_y
        diff_z = z - cannon_z
        rad_w = m.atan2(-diff_x, -diff_y)
        rad_h = m.atan2(-diff_z , m.sqrt(diff_x**2 + diff_y**2))
        diff = m.sqrt(diff_x**2 + diff_y**2+ diff_z**2)
        diff_rad_w = rad_w - c_rad_w #角度算出
        diff_rad_h = rad_h - c_rad_h

        if(diff_rad_h >= m.pi/2):
            diff_rad_h = m.pi/2
        elif(diff_rad_h <= -m.pi/2):
            diff_rad_h = -m.pi/2
        
        if(diff_rad_w > m.pi):
            diff_rad_w -= 2*m.pi
        elif(diff_rad_w <= -m.pi):
            diff_rad_w += 2*m.pi

        draw_poligon_pos_x = (WINDOW_WIDTH/2) - WINDOW_WIDTH * m.sin((diff_rad_w/2))
        draw_poligon_pos_y = (WINDOW_HEIGHT/2) - WINDOW_HEIGHT * m.sin((diff_rad_h/2))

        return draw_poligon_pos_x, draw_poligon_pos_y

    def cal2(self, bu0, bu1, bu2, bu3):#内部座標から描画座標へ
    
        pos_x1, pos_y1 = self.cal(bu0[0], bu0[1], bu0[2], c_x, c_y, c_z)
        pos_x2, pos_y2 = self.cal(bu1[0], bu1[1], bu1[2], c_x, c_y, c_z)
        pos_x3, pos_y3 = self.cal(bu2[0], bu2[1], bu2[2], c_x, c_y, c_z)
        pos_x4, pos_y4 = self.cal(bu3[0], bu3[1], bu3[2], c_x, c_y, c_z)
        return pos_x1, pos_y1, pos_x2, pos_y2, pos_x3, pos_y3, pos_x4, pos_y4

    def graphic_enemies_shadow(self,ene_pos):#敵の影の描画
        diff_x = self.x - c_x
        diff_y = self.y - c_y
        diff_z = self.z - c_z
        rad_w = m.atan2(-diff_x, -diff_y)
        rad_h = m.atan2(-diff_z , m.sqrt(diff_x**2 + diff_y**2))
        diff = m.sqrt(diff_x**2 + diff_y**2+ diff_z**2)
        diff_rad_w = rad_w - c_rad_w #角度算出
        diff_rad_h = rad_h - c_rad_h
        if m.cos(diff_rad_w) > 0.5 and m.cos(diff_rad_h) > 0.5:
            ene_s_pos = [0] * 8
            for i in range(8):
                ene_s_pos[i] = [ene_pos[i][0], ene_pos[i][1], 100]
        
            if self.rad_h >= 0:
                self.id2[0] = cv.create_polygon(self.cal2(ene_s_pos[0], ene_s_pos[3], ene_s_pos[7], ene_s_pos[4]), fill="#400000")#front
                self.id2[1] = cv.create_polygon(self.cal2(ene_s_pos[4], ene_s_pos[7], ene_s_pos[6], ene_s_pos[5]), fill="#400000")#down  
            else:
                self.id2[0] = cv.create_polygon(self.cal2(ene_s_pos[1], ene_s_pos[5], ene_s_pos[6], ene_s_pos[2]), fill="#400000")#back
                self.id2[1] = cv.create_polygon(self.cal2(ene_s_pos[4], ene_s_pos[7], ene_s_pos[6], ene_s_pos[5]), fill="#400000")#down

    def set(self):#敵のアドレス初期化
        self.id = [None, None, None, None, None, None]#up,front,right,left,back,down
        self.id2 = [None, None]#shadow front_or_back down
        self.draw()#描画

    def draw(self):#敵の描画
        self.destroy()#敵の初期化
        if self.exist:
            ene_pos = self.enemies_poligon(self.x, self.y, self.z)#敵の座標取得
            self.graphic_enemies(ene_pos)#敵を描画
            self.graphic_enemies_shadow(ene_pos)#敵の影を描画

            root.after(GAME_RATE, self.draw)#一定時間後にこの関数を再帰処理

    def enemy_shoot(self):#弾生成
        if self.exist:
            enemybullet = EnemyBullet(self.x, self.y, self.z)#弾生成
            enemybullet.set()#弾初期化
            enemybullet.shoot()#弾更新
        
    def destroy(self):#初期化
        for i in range(6):
            cv.delete(self.id[i])
        for i in range(2):
            cv.delete(self.id2[i])

class EnemyBullet:#敵の弾

    def __init__(self, x, y, z):#初期設定
        diff_x = x - c_x
        diff_y = y - c_y
        diff_z = z - c_z
        self.rad_w = m.atan2(diff_x, diff_y) + 0.2* (random.random()-0.5)
        self.rad_h = m.atan2((diff_z-8) , m.sqrt(diff_x**2 + diff_y**2))
        self.x = x
        self.y = y
        self.z = z

    def cal(self, x, y, z, cannon_x, cannon_y, cannon_z):#内部座標から描画座標へ
        diff_x = x - cannon_x
        diff_y = y - cannon_y
        diff_z = z - cannon_z
        rad_w = m.atan2(-diff_x, -diff_y)
        rad_h = m.atan2(-diff_z , m.sqrt(diff_x**2 + diff_y**2))
        diff = m.sqrt(diff_x**2 + diff_y**2+ diff_z**2)
        diff_rad_w = rad_w - c_rad_w #角度算出
        diff_rad_h = rad_h - c_rad_h

        if(diff_rad_h >= m.pi/2):
            diff_rad_h = m.pi/2
        elif(diff_rad_h <= -m.pi/2):
            diff_rad_h = -m.pi/2
        
        if(diff_rad_w > m.pi):
            diff_rad_w -= 2*m.pi
        elif(diff_rad_w <= -m.pi):
            diff_rad_w += 2*m.pi

        draw_poligon_pos_x = (WINDOW_WIDTH/2) - WINDOW_WIDTH * m.sin((diff_rad_w/2))
        draw_poligon_pos_y = (WINDOW_HEIGHT/2) - WINDOW_HEIGHT * m.sin((diff_rad_h/2))

        return draw_poligon_pos_x, draw_poligon_pos_y

    def cal2(self, bu0, bu1, bu2, bu3):#内部座標から描画座標へ
    
        pos_x1, pos_y1 = self.cal(bu0[0], bu0[1], bu0[2], c_x, c_y, c_z)
        pos_x2, pos_y2 = self.cal(bu1[0], bu1[1], bu1[2], c_x, c_y, c_z)
        pos_x3, pos_y3 = self.cal(bu2[0], bu2[1], bu2[2], c_x, c_y, c_z)
        pos_x4, pos_y4 = self.cal(bu3[0], bu3[1], bu3[2], c_x, c_y, c_z)
        return pos_x1, pos_y1, pos_x2, pos_y2, pos_x3, pos_y3, pos_x4, pos_y4

    def bullet_poligon(self, x, y, z):#敵の弾の座標取得
        pos = [0] * 8

        for i in range(8):
            if (i % 4 == 0 or i % 4 == 1):
                width = -1/2
            else:
                width = 1/2

            if (i % 4 == 1 or i % 4 == 2):
                length = 1
            else:
                length = 0

            if (i < 4):
                height = -1/2
            else:
                height = 1/2
            
            diff_x = width * BULLET_WIDTH * m.cos(self.rad_w) + length * BULLET_LENGTH * m.sin(self.rad_w) - height * BULLET_HEIGHT * m.sin(self.rad_h) * m.sin(self.rad_w)
            diff_y = - width * BULLET_WIDTH * m.sin(self.rad_w) + length * BULLET_LENGTH * m.cos(self.rad_w) * m.cos(self.rad_h)  - height * BULLET_HEIGHT * m.sin(self.rad_h) * m.cos(self.rad_w) 
            diff_z = length * BULLET_LENGTH * m.sin(self.rad_h) + height * BULLET_HEIGHT * m.cos(self.rad_h)


            pos[i] = [x+diff_x, y+diff_y, z+diff_z]
        return pos

    def graphic_bullet(self,bu_pos):#敵の玉描画
        
        diff_x = self.x - c_x
        diff_y = self.y - c_y
        diff_z = self.z - c_z
        rad_w = m.atan2(-diff_x, -diff_y)
        rad_h = m.atan2(-diff_z , m.sqrt(diff_x**2 + diff_y**2))
        diff = m.sqrt(diff_x**2 + diff_y**2+ diff_z**2)
        diff_rad_w = rad_w - c_rad_w #角度算出
        diff_rad_h = rad_h - c_rad_h
        if m.cos(diff_rad_w) > 0.5 and m.cos(diff_rad_h) > 0.5:
            self.id[0] = cv.create_polygon(self.cal2(bu_pos[0], bu_pos[1], bu_pos[2], bu_pos[3]), fill="#f08080")#up
            self.id[1] = cv.create_polygon(self.cal2(bu_pos[0], bu_pos[3], bu_pos[7], bu_pos[4]), fill="#f06060")#front
            self.id[2] = cv.create_polygon(self.cal2(bu_pos[3], bu_pos[2], bu_pos[6], bu_pos[7]), fill="#f06060")#right
            self.id[3] = cv.create_polygon(self.cal2(bu_pos[0], bu_pos[4], bu_pos[5], bu_pos[1]), fill="#f06060")#left
            self.id[4] = cv.create_polygon(self.cal2(bu_pos[1], bu_pos[5], bu_pos[6], bu_pos[2]), fill="#f06060")#back
            self.id[5] = cv.create_polygon(self.cal2(bu_pos[4], bu_pos[7], bu_pos[6], bu_pos[5]), fill="#f04040")#down

    def graphic_bullet_shadow(self,bu_pos):#敵の玉の影の描画
        diff_x = self.x - c_x
        diff_y = self.y - c_y
        diff_z = self.z - c_z
        rad_w = m.atan2(-diff_x, -diff_y)
        rad_h = m.atan2(-diff_z , m.sqrt(diff_x**2 + diff_y**2))
        diff = m.sqrt(diff_x**2 + diff_y**2+ diff_z**2)
        diff_rad_w = rad_w - c_rad_w #角度算出
        diff_rad_h = rad_h - c_rad_h
        if m.cos(diff_rad_w) > 0.5 and m.cos(diff_rad_h) > 0.5:
            bu_s_pos = [0] * 8
            for i in range(8):
                bu_s_pos[i] = [bu_pos[i][0], bu_pos[i][1], 100]
        
            if self.rad_h >= 0:
                self.id2[0] = cv.create_polygon(self.cal2(bu_s_pos[0], bu_s_pos[3], bu_s_pos[7], bu_s_pos[4]), fill="#804040")#front
                self.id2[1] = cv.create_polygon(self.cal2(bu_s_pos[4], bu_s_pos[7], bu_s_pos[6], bu_s_pos[5]), fill="#804040")#down  
            else:
                self.id2[0] = cv.create_polygon(self.cal2(bu_s_pos[1], bu_s_pos[5], bu_s_pos[6], bu_s_pos[2]), fill="#804040")#back
                self.id2[1] = cv.create_polygon(self.cal2(bu_s_pos[4], bu_s_pos[7], bu_s_pos[6], bu_s_pos[5]), fill="#804040")#down

    def set(self):#敵の弾のアドレス初期化
        self.id = [None, None, None, None, None, None]#up,front,right,left,back,down
        self.id2 = [None, None]#shadow front_or_back down
  
    def shoot(self):#敵の玉の更新
        self.destroy()
        if (self.x >= 0 and self.x <= 600) and (self.y >= 0 and self.y <= 600) and (self.z >= 0 and self.z <= 100) and game:
            self.x += -BULLET_SPEED * m.sin(self.rad_w) * m.cos(self.rad_h)
            self.y += -BULLET_SPEED * m.cos(self.rad_w) * m.cos(self.rad_h)
            self.z += -BULLET_SPEED * m.sin(self.rad_h)

            bu_pos = self.bullet_poligon(self.x, self.y, self.z)#弾の頂点を取得
            self.graphic_bullet(bu_pos)#弾の描画
            self.graphic_bullet_shadow(bu_pos)#弾の影描画

            self.collision()#衝突判定
            root.after(GAME_RATE, self.shoot)#一定時間後にこの関数を再帰処理

    def collision(self):#敵の弾が自機に当たったら自機を消す
        if (abs(self.x-c_x) < CANNON_WIDTH/2) and (abs(self.y-c_y) < CANNON_LENGTH/2) and (abs(self.z-c_z) < CANNON_HEIGHT/2):
            cannon.exist = False

    def destroy(self):#初期化
        for i in range(6):
            cv.delete(self.id[i])
        for i in range(2):
            cv.delete(self.id2[i])

def gameclear():  # ゲームクリア判定
    winflag = 0
    for enemy in enemies:
        if enemy.exist == False:
            winflag += 1
    if winflag == NUMBER_OF_ENEMY:
        global game
        game = False  #ゲーム続行不可
        cv.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2-80, text="Congratulations!",
                       fill="lime", font=("System", TEXT_CONGRATULATIONS_SIZE))
        cv.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2+20, text="GAME CLEAR!",
                       fill="lime", font=("System", TEXT_GAMECLEAR_SIZE))
    root.after(GAME_RATE, gameclear)#一定時間後に繰り返し

def gameover():  # ゲームオーバー判定
    loseflag = 0
    if cannon.exist == False:
            loseflag += 1
    if loseflag == 1:
        global game
        game = False  #ゲーム続行不可
        cv.create_rectangle(0, 0, WINDOW_HEIGHT, WINDOW_WIDTH, fill="#f0f0f0")
        cv.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, text="GAME OVER",
                       fill="red", font=("System", TEXT_GAMEOVER_SIZE))
    root.after(GAME_RATE, gameover)#一定時間後に繰り返し

def enemy_randomshoot():  # ランダムに敵の弾が発射
    global game_time
    game_time += 1#ゲーム時間を進める
    if game_time > 5:#最初の敵の玉は出さない
        enemy = random.choice(enemies)
        enemy.enemy_shoot()
    root.after(ENEMY_SHOOT_INTERVAL, enemy_randomshoot)#繰り返し

def marker(): #画面の真ん中の標準を描画
    cv.create_polygon(WINDOW_HEIGHT/2 -2, WINDOW_WIDTH/2 -10,
                      WINDOW_HEIGHT/2 -2, WINDOW_WIDTH/2 +10,
                      WINDOW_HEIGHT/2 +2, WINDOW_WIDTH/2 +10,
                      WINDOW_HEIGHT/2 +2, WINDOW_WIDTH/2 -10, fill="white")
    cv.create_polygon(WINDOW_HEIGHT/2 -10, WINDOW_WIDTH/2 -2,
                      WINDOW_HEIGHT/2 -10, WINDOW_WIDTH/2 +2,
                      WINDOW_HEIGHT/2 +10, WINDOW_WIDTH/2 +2,
                      WINDOW_HEIGHT/2 +10, WINDOW_WIDTH/2 -2, fill="white")
    root.after(GAME_RATE, marker)#繰り返せ

def clear():#描画物を定期的に消して、動作が重くなることを防ぐ
    cv.delete('all')
    cv.create_rectangle(0, 0, WINDOW_HEIGHT, WINDOW_WIDTH, fill="#d0d0e0")
    root.after(GAME_RATE*300, clear)#繰り返し（スパン長め）

if __name__ == "__main__":
    # 初期描画
    root = tk.Tk()
    root.title("invader")
    cv = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
    cv.pack()

    # メニューバー
    menubar = tk.Menu(root)
    root.configure(menu=menubar)
    menubar.add_command(label="QUIT", underline=0, command=root.quit)

    # インスタンス生成
    wall = Wall()#壁
    cannon = Cannon(CANNON_X, CANNON_Y, CANNON_Z ,CANNON_RAD_W, CANNON_RAD_W)#自機
    enemies = []
    for i in range(NUMBER_OF_ENEMY):#敵（座標ランダム）
        ENEMY_SPACE_X = 50 + 500 * random.random()
        ENEMY_SPACE_Y = 50 + 250 * random.random()
        ENEMY_SPACE_Z = 10 + 80 * random.random()
        enemy_i = Enemy(ENEMY_SPACE_X, ENEMY_SPACE_Y, ENEMY_SPACE_Z)
        enemies.append(enemy_i)

    enemy_randomshoot()
    marker()

    gameover()#ゲーム終了判定
    gameclear()

    clear()#描画を消して動作軽量化

    root.mainloop()#game continue
