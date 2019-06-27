import pygame
from pygame.locals import *
from sys import exit


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

    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        y = self.rect.top + offset[pygame.K_DOWN] - offset[pygame.K_UP]
        # 不超过最左端边界
        if x < 0:
            self.rect.left = 0
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
# 子弹速度
BULLET_SPEAD=10
# 按键状态 字典
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}

# 初始化游戏
# 初始化pygame
pygame.init()
# 初始化窗口
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# 设置窗口标题
pygame.display.set_caption('飞机大战')

# 载入图片
background = pygame.image.load('resources/images/background.png')
# 载入飞机图片
shoot_img = pygame.image.load('resources/images/plane1.png')
# 用subsurface剪切读入的图片
# 矩形剪切图片    图片 102*128 其中后面喷火部分高度为32，飞机大小98
# 矩形圈出飞机
hero1_rect = pygame.Rect(0, 0, 102, 96)
# 矩形圈出火焰
hero2_rect = pygame.Rect(0, 0, 102, 128)
# 剪出第一个矩形（飞机）
hero1 = shoot_img.subsurface(hero1_rect)
# 剪出第二个矩形（火焰）
hero2 = shoot_img.subsurface(hero2_rect)
# 子弹图片
bullet1_surface = pygame.image.load('resources/images/bullet.png')
# 用列表存储图像，网上代码有误，下面注释更改
hero_surface = []
hero_surface.append(hero1)
hero_surface.append(hero2)

hero_pos = [200, 500]
# 创建玩家
hero = Hero(hero_surface[0], hero_pos)

pygame.Surface([2, 5])
# 事件循环
while True:
    # 游戏帧率（速度）
    pygame.time.Clock().tick(SPEED)
    # 绘制背景
    screen.blit(background, (0, 0))
    # 绘制飞机
    screen.blit(hero.image, hero.rect)
    # 射击
    if tick % BULLET_SPEAD == 0:
        hero.single_shoot(bullet1_surface)
    # 子弹移动
    hero.bullets1.update()
    # 绘制子弹
    hero.bullets1.draw(screen)
    # 改变飞机制造动画
    if tick >= ANIMATE_CYCLE:
        tick = 0
    hero.image = hero_surface[tick // (ANIMATE_CYCLE // 2)]
    tick += 1

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
