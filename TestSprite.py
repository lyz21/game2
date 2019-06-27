"""
测试精灵类
"""
# -*- coding = utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
from random import randint

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640


# Player类 -- 继承自pygame.sprite.Sprite
# 两个主要属性：self.image 和 self.rect
# 一个重要方法 self.update, upodate函数是空的，里面的方法是需要自己完成的主要工作
class Player(pygame.sprite.Sprite):
    def __init__(self, initial_position):
        pygame.sprite.Sprite.__init__(self)  # ※ 父构造函数
        self.image = pygame.Surface([20, 10])  # ※ 精灵图片Surface(宽为20，高为10)
        self.image.fill((0, 0, 0))      # 颜色为黑色
        self.rect = self.image.get_rect()  # ※ 精灵图片的大小
        self.rect.topleft = initial_position  # ※ 精灵图片的位置

        self.speed = 6
    # 这里面需要写的才是最主要需要自己天机添加的内容
    # 当调用Group.update()方法时，会调用Group组内所有精灵的uodate方法
    def update(self):
        self.rect.left += self.speed    # 精灵左移
        if self.rect.left > SCREEN_WIDTH:   # 超出边界，将精灵从组内移除，回收资源
            self.kill()


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# 建立精灵组
group = pygame.sprite.Group()

while True:
    clock.tick(10)
    print(len(group.sprites()))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    # 绘制背景
    screen.fill((255, 255, 255))

    # 不断往精灵组中添加精灵
    # Player(pygame.sprite.Sprite)
    group.add(Player((randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))))

    # 将每个精灵更新后显示在Screen上
    group.update()
    group.draw(screen)

    pygame.display.update()