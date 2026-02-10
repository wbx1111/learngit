import pygame
import random
#定义操作
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
#屏幕画布大小
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#玩家位置
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self,pressed_key):
        # 控制移动方向
        if pressed_key[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_key[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(5, 0)
        #定义边界线
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
#敌人
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        #敌人位置为屏幕的外面
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0,SCREEN_HEIGHT)
            )
        )
        #速度区间为5,20
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
#初始化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = Player()

enemies = pygame.sprite.Group() #专门管理敌人的精灵组
all_sprites = pygame.sprite.Group() #管理所有精灵的总组
all_sprites.add(player) #把玩家添加到总精灵组

#自定义事件:每隔一段时间生成敌人
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250) #每250ms生成一个敌人

running = True
#事件处理
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:   #检查是否为事件
            if event.key == K_ESCAPE:  #如果为esc键则退出
                running = False
        elif event.type == QUIT:  #如果点击关闭则退出
            running = False

        elif event.type == ADDENEMY: #处理生成敌人事件
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    #获取按键状态
    pressed_keys = pygame.key.get_pressed()
    #更新玩家位置
    player.update(pressed_keys)
    #更新所有精灵状态
    enemies.update()

    screen.fill((0,0,0))#黑色背景

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    #碰撞试验
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
    #区块转移,将创建好的玩家显示到屏幕上
    screen.blit(player.surf,player.rect)
    pygame.display.flip()
    clock.tick(60)
