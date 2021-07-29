import pygame
import math
import os
from settings import PATH, PATH2

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))

class Enemy:
    """
    為了 Bonus 多了一個 path 的參數
    正常運作時的前三隻都會走左邊
    只有呼叫在 EnemyGroup 當中的 change 才會改變到 path 的值，讓第二波攻擊從右邊來
    """
    def __init__(self, path):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        # Bonus:
        #   self.path 決定現在是第幾波攻擊
        self.path = path
        self.path_pos = 0
        self.move_count = 0
        # 我讓他跑快一點 所以改2
        self.stride = 2
        self.x, self.y = self.path[0]

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        red = 255, 0, 0
        green = 0, 255, 0
        # 決定一格血的間隔多寬
        # 間隔 = 寬度 / 總共幾格血
        gap = self.width / self.max_health

        # 血量的位置會隨著 Enemy 的 (x, y) 座標跟著改變
        x_pos = self.x - self.width/2
        y_pos = self.y - 30

        # 把血量一格一格印出來
        for i in range(self.max_health):
            """
            殘餘血量用綠色
            扣除血量用紅色
            """
            if i < self.health:
                pygame.draw.rect(win, green, [x_pos + i*gap, y_pos, gap, 5])
            else :
                pygame.draw.rect(win, red, [x_pos + i*gap, y_pos, gap, 5])

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """

        """
        啊我都抄助教給的 所以相信大家看得懂 :D

        取法是 p_A, p_B 為 Enemy 的原點跟新點，新點就是PATH中下一個點
        PATH 當中有幾個點，總共就有幾個點
        至於為何判斷式要 < path長度-1 是因為沒有-1的話，最後一個讀取時，會超過陣列長度
        """
        
        if self.path_pos < (len(self.path)-1):
            p_A = self.path[self.path_pos]
            p_B = self.path[self.path_pos + 1]
            ax, ay = p_A  # x, y position of point A
            bx, by = p_B
            distance_A_B = math.sqrt((ax - bx)**2 + (ay - by)**2)
            max_count = int(distance_A_B / self.stride)  # total footsteps that needed from A to B
            if self.move_count < max_count:
                unit_vector_x = (bx - ax) / distance_A_B
                unit_vector_y = (by - ay) / distance_A_B
                delta_x = unit_vector_x * self.stride
                delta_y = unit_vector_y * self.stride

                # update the coordinate and the counter
                self.x += delta_x
                self.y += delta_y
                self.move_count += 1
            else:
                # 這裡 self.path_pos += 1 是因為要跑完PATH裡面的所有點
                # 跑完第一個之後要 +1 才能到下一個點繼續跑
                self.move_count = 0
                self.path_pos += 1

class EnemyGroup:
    def __init__(self):
        self.gen_count = 0
        self.gen_period = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = []  # don't change this line until you do the EX.3 

        # Bonus:
        # 第一波攻擊的路線為 PATH
        # 第二波攻擊的路線為 PATH2
        # 我多寫了兩個函數在最下方，分別為 is_clean 和 change
        self.path = PATH

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # 每呼叫一次 campaign 則代表過了一幀，self.gen_count 是在計算過了幾幀
        # 因為每過 120 幀，就要派出一個 Enemy ，而 self.gen_period 的單位就是幀數
        # 因此如果是 self.gen_period 的倍數，且同時 self.reserved_members 裡面有 Enemy 準備出擊，則將其派出
        self.gen_count += 1
        if (self.gen_count % self.gen_period == 0) and (not self.is_empty()):
            self.expedition.append(self.reserved_members.pop())

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        # num 為要讓幾個 Enemy 準備出擊
        # 因為知道準備派幾個，所以用 for 來將其加入
        for i in range(num):
            self.reserved_members.append(Enemy(self.path))

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)
    
    # 以下是我為了 Bonus 多寫的兩個函數
    def is_clean(self):
        """
        Check the enemies in a wave are all clean
        """
        # 檢查 self.expedition 是不是空的
        # 換句話說，就是檢查場上有沒有 Enemy
        # 換句話說，如果你的眼睛現在有看到任何一個 Enemy ，那就回傳 True，沒有就 False
        return False if self.expedition else True
    
    def change(self):
        """
        If first wave is over
        Change the attack path
        """
        # 啊就是要變成第二次出擊時候，把路線改成 PATH2
        self.path = PATH2


