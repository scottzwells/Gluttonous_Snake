import pygame
from pygame.locals import *
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))  # 创建屏幕
pygame.display.set_caption('贪吃蛇')           # 设置标题
pygame.mixer.init()                          # 初始化音效
eat_sound = pygame.mixer.Sound('coin.mp3')
bgm = pygame.mixer.Sound('bgm.mp3')
settlement_bgm = pygame.mixer.Sound('settlement.mp3')

class Snake:
    def __init__(self):
        self.x = 300     # 初始位置
        self.y = 300
        self.direction = 'right'    # 初始方向
        self.location = [(self.x, self.y)]   # 蛇每节身体的位置

    def update(self):
        # 根据方向更新蛇的位置
        if self.direction == 'up':
            self.y -= 10
        elif self.direction == 'down':
            self.y += 10
        elif self.direction == 'left':
            self.x -= 10
        elif self.direction == 'right':
            self.x += 10

        if self.x > 790:  self.x = 0
        if self.x < 0  :  self.x = 790
        if self.y > 590:  self.y = 0
        if self.y < 0  :  self.y = 590
        self.location.append((self.x, self.y))           # 将新的位置添加到蛇身体，蛇头在末尾
        self.location = self.location[-1 * (scoreboard.score+1):]    # 保持蛇的长度

    def draw(self):
        """绘制蛇身的同时判断是否撞到自己"""
        for (x, y) in self.location:
            if screen.get_at((x,y)) == (255, 0, 0) or screen.get_at((x,y)) == (0,255,0):
                return False
            pygame.draw.rect(screen, (255,0,0), (x, y, 10, 10))
        return True

class Food:
    def __init__(self,num):
        self.location = []  # 随机初始位置
        self.num = num      # 初始化食物个数
        for i in range(self.num):
            self.location.append((random.randint(1, 78) * 10 , random.randint(1, 58) * 10))

    def update(self, index):
         self.location[index] = (random.randint(1, 78) * 10, random.randint(1, 58) * 10)

    def draw(self):
        # 绘制食物
        for i in self.location:
           pygame.draw.rect(screen, (0, 0, 255), (i[0], i[1], 10, 10))

class Scoreboard:
    """显示当前分数与最高分数的计分板"""
    def __init__(self,h_score=0):
        self.score = 0
        self.h_score = h_score

    def increase_score(self):
        self.score += 1
        if int(self.h_score) < self.score:
            self.h_score = self.score

    def draw(self):
        font = pygame.font.Font(None, 36)
        text1 = font.render("Score: " + str(self.score), True, (0, 0, 0))
        text2 = font.render("HighScore: " + str(self.h_score), True, (0, 0, 0))
        screen.blit(text1, (10, 10))                         # 当前分数的绘制
        screen.blit(text2, (600, 10))                        # 最高分的绘制


def border():
    pygame.draw.rect(screen,(0,255,0),pygame.Rect(0,0,800,600),10)

def opening_manu():
    """开始菜单"""
    screen.fill((255, 255, 255))
    screen.blit(pygame.image.load("./title.png"), (150, 100))
    screen.blit(pygame.image.load("./startbutton.png"), (300, 400))
    pygame.display.update()

    start = True
    while start:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 468 and 400 <= mouse_pos[1] <= 494:
                    # 当检测到鼠标按下开始按钮时游戏开始
                    start = False
                    return True


def rank_selc():
    """难度选择界面"""
    screen.fill((255, 255, 255))
    screen.blit(pygame.image.load("./rankbutton.png"), (300, 100))
    screen.blit(pygame.image.load("./rankbutton.png"), (300, 250))
    screen.blit(pygame.image.load("./rankbutton.png"), (300, 400))
    font = pygame.font.SysFont("calibri",50)
    text1 = font.render("Easy", True, (55, 209, 55))
    text2 = font.render("Normal", True, (55, 154, 250))
    text3 = font.render("Hard", True, (250, 78, 65))
    screen.blit(text1,(342, 120))
    screen.blit(text2, (309, 272))
    screen.blit(text3, (336, 422))
    title_font = pygame.font.Font(None,75)
    title = title_font.render("Rank  Selection",True,(0,0,0))
    screen.blit(title,(200,10))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 468:
                    if 100 <= mouse_pos[1] <= 194:
                        return 1
                    elif 250 <= mouse_pos[1] <= 344:
                        return 2
                    elif 400 <= mouse_pos[1] <= 494:
                        return 3


def get_result():
    """开始结算分数"""
    with open("./highest score.txt", "w", encoding="utf-8") as file:
        file.write(str(scoreboard.h_score))
        file.close()
    screen.blit(pygame.image.load("./gameover.png"),(200,200))
    final_font1 = pygame.font.SysFont("calibri",50)
    final_text1 = final_font1.render("Your final score is  " + str(scoreboard.score) + ".",True,(118, 104, 174))
    final_font2 = pygame.font.SysFont("calibri", 36)
    final_text2 = final_font2.render("(Press Enter to restart or Esc to rank selection)",True,(118, 104, 174))
    screen.blit(final_text1,((175,300)))
    screen.blit(final_text2,((75,360)))



"""游戏主程序"""
with open("./highest score.txt", "r", encoding="utf-8") as file:
    """读取最高分"""
    h_score = file.read()
    file.close()
if h_score.isdigit():
    h_score = int(h_score)
else:
    h_score = 0
bgm.play(-1)
running = opening_manu()    # 打开主界面
rank = 0
if running:
    rank = rank_selc()  # 游戏难度

snake = Snake()
food = Food(13 - rank * 3)
scoreboard = Scoreboard(h_score)     # 初始化各对象
life = True
clock = pygame.time.Clock()

while running and rank:
    """游戏进行中"""
    screen.fill((255, 255, 255))      # 填充游戏画面为白色（同时抹去上一轮所绘的蛇身）
    border()

    snake.update()
    life = snake.draw()
    food.draw()

    scoreboard.draw()         # 即时绘制更新画面

    if snake.location[-1] in food.location:          # 当贪吃蛇吃到豆时加分
        scoreboard.increase_score()
        index = food.location.index(snake.location[-1])
        if scoreboard.score in range(rank*5,50-(rank-2)*(rank-3)*10,rank*5):   # 当分数达到一定值时减少食物数量
                                                                               # 简单难度每5分减一个，至少5个
                                                                               # 普通难度每10分减1个，至少3个
                                                                               # 困难难度每15分减1个，至少1个
            del food.location[index]
        else: food.update(index)
        eat_sound.play()


    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:             # 当按下esc键时游戏退出
                running = False
                # 按下上下左右键改变贪吃蛇方向
            elif event.key == K_UP and snake.direction != 'down':
                snake.direction = 'up'
            elif event.key == K_DOWN and snake.direction != 'up':
                snake.direction = 'down'
            elif event.key == K_LEFT and snake.direction != 'right':
                snake.direction = 'left'
            elif event.key == K_RIGHT and snake.direction != 'left':
                snake.direction = 'right'

    pygame.display.update()              # 更新画面
    clock.tick(10+rank*5)                       # 停顿小段时间，稳定小蛇速度

    if life == False:
        """判断小蛇是否存活"""
        bgm.stop()
        settlement_bgm.play(-1)
        get_result()
        pygame.display.update()
        flag = 1
        while flag:
            for event in pygame.event.get():
                if event.type == QUIT:
                    flag = False
                    running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:    # 当按下Escape键时退回难度选择界面
                        settlement_bgm.stop()
                        bgm.play(-1)
                        rank = rank_selc()
                        snake = Snake()
                        food = Food(13 - rank * 3)
                        scoreboard = Scoreboard(scoreboard.h_score)  # 重新初始化各对象
                        flag = False
                    elif event.key == K_RETURN:  # 当按下Enter键时重新开始游戏
                        snake = Snake()
                        food = Food(13 - rank * 3)
                        scoreboard = Scoreboard(scoreboard.h_score)  # 重新初始化各对象
                        settlement_bgm.stop()
                        bgm.play(-1)
                        flag = False

pygame.quit()