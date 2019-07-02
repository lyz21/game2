import pygame
from pygame.locals import *
from sys import exit
from random import randint


# 例：返回整数N ，a<= N <=b
# N=randint(a,b)


# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_surface, enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = FLAG_SPEED
        # 爆炸动画的索引
        self.down_index = 0

    def update(self):
        self.rect.top = self.rect.top + self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_surface, bullet_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = bullet_init_pos
        self.speed = 8

    # 控制子弹移动
    def update(self):
        self.rect.top -= self.speed
        if self.rect.top <= -self.rect.height:
            self.kill()


# 玩家类
class Hero(pygame.sprite.Sprite):
    def __init__(self, hero_surface, hero_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_surface
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_pos
        self.speed = 6
        # 建立子弹精灵组
        self.bullets1 = pygame.sprite.Group()
        self.is_hit = False
        self.down_index = 0

    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        # 不超过最左端边界
        if x < -10:
            self.rect.left = -10
        # 不超过最右端边界（将要设定的位置如果大于边界-宽度即最右端值，设定为最右端值）
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x
        if y < 0:
            self.rect.top = 0
        elif y > SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top = y

    def single_shoot(self, bullet1_surface):
        bullet1 = Bullet(bullet1_surface, self.rect.midtop)
        self.bullets1.add(bullet1)


# 窗口分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
# 画面帧率
SPEED = 60
# 动画周期（帧数）
ANIMATE_CYCLE = 30
# 计数
tick = 0
# 子弹出现速度
BULLET_SPEED = 15
# 敌机出现速度
ENEMY_SPEED = 30
# 敌机飞行速度
FLAG_SPEED=2
# 爆炸速度
BOOM_SPEED = 5
# 按键状态 字典
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}

# 初始化游戏
# 初始化pygame
pygame.init()
# 初始化窗口
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# 设置窗口标题
pygame.display.set_caption('飞机大战')
# 文字surface
# print(pygame.font.get_fonts())    # 打印可用字体
font = pygame.font.SysFont("方正小标宋简体", 20)
score = 0
# 标志位，标志是否为刚进行过加速
flag = -1
# 载入图片
background = pygame.image.load('resources/images/background.png')
# 载入飞机图片
# 己方战斗机
shoot_img = pygame.image.load('resources/images/feiji.png')
# 敌机
enemy_img = pygame.image.load('resources/images/enemy.png')
# 敌机爆炸图片
enemy_boom_img = pygame.image.load('resources/images/boom.png')
enemy_down_surface = []
enemy_down_surface.append(enemy_boom_img.subsurface(pygame.Rect(0, 0, 71, 85)))
enemy_down_surface.append(enemy_boom_img.subsurface(pygame.Rect(66, 0, 71, 85)))
enemy_down_surface.append(enemy_boom_img.subsurface(pygame.Rect(131, 0, 71, 85)))
enemy_down_surface.append(enemy_boom_img.subsurface(pygame.Rect(206, 0, 80, 85)))
# 用subsurface剪切读入的图片
# 矩形剪切图片    图片 102*128 其中后面喷火部分高度为32，飞机大小98
#   feiji.png 102*109  飞机部分：102*89;火焰部分：102*20
'''
plane.png
# 矩形圈出飞机
hero1_rect = pygame.Rect(0, 0, 102, 96)
# 矩形圈出火焰
hero2_rect = pygame.Rect(0, 0, 102, 128)
'''
# 矩形圈出飞机 feiji.png
hero1_rect = pygame.Rect(0, 0, 102, 89)
# 矩形圈出火焰
hero2_rect = pygame.Rect(0, 0, 102, 109)
# 剪出第一个矩形（飞机）
hero1 = shoot_img.subsurface(hero1_rect)
# 剪出第二个矩形（火焰）
hero2 = shoot_img.subsurface(hero2_rect)
# 子弹图片
bullet1_surface = pygame.image.load('resources/images/bullet.png')
# 游戏结束图片
gameover = pygame.image.load('resources/images/fail.png')
# 用列表存储图像，网上代码有误，下面注释更改
hero_surface = []
hero_surface.append(hero1)
hero_surface.append(hero2)

hero_pos = [200, 500]
# 创建玩家
hero = Hero(hero_surface[0], hero_pos)

pygame.Surface([2, 5])
# 敌机组
enemy_group = pygame.sprite.Group()
# 击毁组
enemy_down_group = pygame.sprite.Group()

# 事件循环
while True:
    # 游戏帧率（速度）
    pygame.time.Clock().tick(SPEED)
    # 绘制背景
    screen.blit(background, (0, 0))
    # 绘制文字
    # 分数

    score_text = '成绩:' + str(score)
    text_surface = font.render(score_text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))
    # 绘制飞机
    screen.blit(hero.image, hero.rect)
    # 绘制敌机
    # enemy = Enemy(enemy_img, [100, 100])
    # 敌机宽50，高49
    if tick % ENEMY_SPEED == 0:
        enemy = Enemy(enemy_img, [randint(0, SCREEN_WIDTH - 50), -49])
        enemy_group.add(enemy)
    # 敌机运动
    enemy_group.update()
    # 绘制敌机
    enemy_group.draw(screen)
    # 射击
    if tick % BULLET_SPEED == 0:
        hero.single_shoot(bullet1_surface)
    # 子弹移动
    hero.bullets1.update()
    # 绘制子弹
    hero.bullets1.draw(screen)
    # 敌机与玩家发生碰撞
    list1 = pygame.sprite.spritecollide(hero, enemy_group, True)
    if len(list1) > 0:
        enemy_down_group.add(list1)  # 将敌机销毁
        hero.is_hit = True
    # 销毁玩家
    if hero.is_hit:
        if tick % BOOM_SPEED == 0 and hero.down_index < 4:
            hero.image = enemy_down_surface[hero.down_index]
            hero.down_index += 1
        if hero.down_index >= 4:
            # screen.blit(gameover, (0, 0))
            # screen.blit(text_surface, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            break
    else:
        # 改变飞机制造动画
        if tick >= ANIMATE_CYCLE:
            tick = 0
        hero.image = hero_surface[tick // (ANIMATE_CYCLE // 2)]
    tick += 1
    # 敌机与子弹碰撞
    enemy_down_list = pygame.sprite.groupcollide(enemy_group, hero.bullets1, True, True)  # 检测group与group之间的碰撞
    if len(enemy_down_list) > 0:
        score += 1  # 得分+1
        flag = 1  # 表示可进行加速
        enemy_down_group.add(enemy_down_list)

    # 爆炸
    # screen.blit(enemy_down_surface[0], [200,200])
    # print('enemy_down_surface:',enemy_down_surface[0])
    for enemy_down in enemy_down_group:
        screen.blit(enemy_down_surface[enemy_down.down_index], enemy_down.rect)
        if tick % BOOM_SPEED == 0:
            if enemy_down.down_index < 3:
                enemy_down.down_index += 1
            else:
                enemy_down_group.remove(enemy_down)
    # 加快敌机速度与子弹出现速度与敌机飞行速度
    if score % 10 == 0 and flag == 1:
        ENEMY_SPEED = ENEMY_SPEED - 2
        BULLET_SPEED = BULLET_SPEED - 1
        FLAG_SPEED=FLAG_SPEED+0.3   # 增加敌机飞行速度
        flag = -1  # 刚进行过加速，不可再加速
        if ENEMY_SPEED <= 10:
            ENEMY_SPEED = 10
        if BULLET_SPEED <= 10 or ENEMY_SPEED == 10:
            BULLET_SPEED = 10

    # 更新屏幕
    pygame.display.update()

    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # 控制方向
        # 键盘是否按下
        if event.type == pygame.KEYDOWN:
            # 键盘按下并且是offset字典中的键
            if event.key in offset:
                # 该方向移动值设为hero.speed,默认为6
                offset[event.key] = hero.speed
        # 键盘松开
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                # 该方向移动值设为0
                offset[event.key] = 0
    hero.move(offset)
screen.blit(gameover, (0, 0))
screen.blit(text_surface, (10, 10))
pygame.display.update()
while True:
    # 处理游戏退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
