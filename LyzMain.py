import pygame
from pygame.locals import *
from sys import exit

# 窗口分辨率
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
# 游戏速度
SPEED = 60
# 飞机大小
PLANE_WIDTH = 100
PLANE_HEIGHT = 128
# 飞机位置      40为偏移修正量，大概为飞机宽度的一半
PLANE_X = SCREEN_WIDTH / 2 - PLANE_WIDTH / 2
PLANE_Y = SCREEN_HEIGHT - PLANE_HEIGHT
# 计数
tick = 0

# 初始化游戏
# 初始化pygame
pygame.init()
# 初始化窗口
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# 设置窗口标题
pygame.display.set_caption('飞机大战')
# 按键状态 字典
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0, pygame.K_UP: 0, pygame.K_DOWN: 0}
# 载入图片
background = pygame.image.load('resources/images/background.png')
# 载入飞机图片
shoot_img = pygame.image.load('resources/images/plane1.png')
# 用subsurface剪切读入的图片
# 矩形剪切图片    图片 102*128 其中后面喷火部分高度为32，飞机大小98
# 矩形圈出飞机
hero1_rect = pygame.Rect(0, 0, 102, 96)
# 矩形圈出火焰
hero2_rect = pygame.Rect(0, 96, 102, 32)
# 剪出第一个矩形（飞机）
hero1 = shoot_img.subsurface(hero1_rect)
# 剪出第二个矩形（火焰）
hero2 = shoot_img.subsurface(hero2_rect)
# # 飞机位置
# hero_posplane = [PLANE_X, PLANE_Y]
# # 火焰1位置
# hero_pos1 = [hero_posplane[0], hero_posplane[1] + 95]
# # 火焰2位置
# hero_pos2 = [hero_pos1[0], hero_pos1[1] + 7]
# 事件循环
while True:
    # 绘制背景
    screen.blit(background, (0, 0))
    # 飞机位置
    hero_posplane = [PLANE_X, PLANE_Y]
    # 火焰1位置
    hero_pos1 = [hero_posplane[0], hero_posplane[1] + 95]
    # 火焰2位置
    hero_pos2 = [hero_pos1[0], hero_pos1[1] + 7]
    # 绘制飞机
    screen.blit(hero1, hero_posplane)
    if tick % 50 < 25:
        screen.blit(hero2, hero_pos1)
    else:
        screen.blit(hero2, hero_pos2)
    tick += 1
    # 控制游戏速度
    pygame.time.Clock().tick(SPEED)
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
                # 该方向移动值设为3
                offset[event.key] = 3
        # 键盘松开
        elif event.type == pygame.KEYUP:
            if event.key in offset:
                # 该方向移动值设为0
                offset[event.key] = 0
    # pygame.K_RIGHT和pygame.K_LEFT都为正且必有一个为0，最终结果便为右正左负。下面同理
    offset_x = offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
    offset_y = offset[pygame.K_DOWN] - offset[pygame.K_UP]
    # 到最左端
    if offset_x < 0 and PLANE_X <= 0:
        PLANE_X = 0
    else:
        PLANE_X = PLANE_X + offset_x
    # 到最右端
    if offset_x > 0 and PLANE_X >= SCREEN_WIDTH - PLANE_WIDTH:
        PLANE_X = SCREEN_WIDTH - PLANE_WIDTH
    else:
        PLANE_X = PLANE_X + offset_x
    # 到最下端
    if offset_y > 0 and PLANE_Y >= SCREEN_HEIGHT - PLANE_HEIGHT:
        PLANE_Y = SCREEN_HEIGHT - PLANE_HEIGHT
    else:
        PLANE_Y = PLANE_Y + offset_y
    # 到最上端
    if offset_y < 0 and PLANE_Y <= 0:
        PLANE_Y = 0
    else:
        PLANE_Y = PLANE_Y + offset_y
    # hero_posplane = [hero_posplane[0] + offset_x, hero_posplane[1] + offset_y]
