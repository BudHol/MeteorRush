import pygame 
from random import randint, uniform
from os.path import join

pygame.init() 

#setting up display
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 
pygame.display.set_caption('Meteor Rush')

#making sprites for game components
class Player(pygame.sprite.Sprite): 
    def __init__(self,groups):
        super().__init__(groups) 
        self.image = pygame.image.load('images\SpaceShip1.png') 
        width_player = self.image.get_rect().width
        height_player = self.image.get_rect().height
        self.image = pygame.transform.scale(self.image,(int(width_player*0.2),(height_player*0.2)))  
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2 , WINDOW_HEIGHT/2)) 
        self.direction = pygame.math.Vector2()
        self.speed = 300 

        self.can_shoot = True 
        self.laser_shoot_time = 0 
        self.cooldown = 300

        self.mask = pygame.mask.from_surface(self.image)

    def laser_timer(self): 
        if not self.can_shoot: 
            current_item = pygame.time.get_ticks() 
            if current_item - self.laser_shoot_time >= self.cooldown: 
                self.can_shoot=True

    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) 
        self.direction = self.direction.normalize() if self.direction else self.direction 
        self.rect.center += self.direction * self.speed * dt 
        
        recent_keys = pygame.key.get_just_pressed() 
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_Surf, self.rect.midtop, (all_sprites,laser_sprites))  
            laser_sound.play()
            self.can_shoot = False 
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer() 

class Laser(pygame.sprite.Sprite): 
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(midbottom=pos) 
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt): 
        self.rect.centery -= 400*dt
        if self.rect.bottom < 0:
            self.kill()

class Stars(pygame.sprite.Sprite): 
    def __init__(self, groups, surf):
        super().__init__(groups) 
        self.image = surf
        self.rect = self.image.get_frect(center = (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT))) 
        self.mask = pygame.mask.from_surface(self.image)

class Meteor(pygame.sprite.Sprite): 
    def __init__(self, groups,surf,pos):
        super().__init__(groups) 
        self.original_surf = surf
        self.image = surf 
        self.rect = self.image.get_frect(center = pos)   
        self.start_time = pygame.time.get_ticks() 
        self.lifetime = 3000  
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,500) 
        self.mask = pygame.mask.from_surface(self.image) 
        self.rotation_speed = randint(40,60) 
        self.rotation = 0
    
    def update(self,dt): 
        self.rect.center += self.direction * self.speed * dt 
        if pygame.time.get_ticks() - self.start_time >= self.lifetime: 
            self.kill() 
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf,self.rotation,1) 
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite): 
    def __init__(self,frames,pos,groups):
        super().__init__(groups) 
        self.frames = frames 
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self,dt): 
        self.frame_index += 20 * dt  
        if self.frame_index < len(self.frames): 
            self.image = self.frames[int(self.frame_index)] 
        else: 
            self.kill()

# class Meteor(pygame.sprite.Sprite):
def display_score():  
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time),True,'white') 
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH/2,WINDOW_HEIGHT - 50)) 
    display_surface.blit(text_surf,text_rect) 
    pygame.draw.rect(display_surface,'white',text_rect.inflate(20,15),5,10) 

#declaring sprites
all_sprites = pygame.sprite.Group()  
meteor_sprites = pygame.sprite.Group() 
laser_sprites = pygame.sprite.Group()


#surfaces
star_surf = pygame.image.load('images\star.png')
meteor_surf = pygame.image.load('images\meteor.png') 
laser_Surf = pygame.image.load('images\laser.png') 

#adjusting surfaces width and height to scale of the game
width_meteor = meteor_surf.get_rect().width 
height_meteor =meteor_surf.get_rect().height 
meteor_surf = pygame.transform.scale(meteor_surf,(int(width_meteor*0.3),(height_meteor*0.3)))

width_laser = laser_Surf.get_frect().width 
height_laser = laser_Surf.get_frect().height
laser_Surf = pygame.transform.scale(laser_Surf,(int(width_laser*0.1), (height_laser*0.1))) 

for i in range(20): 
    Stars(all_sprites,star_surf)
player = Player(all_sprites) 

#initialising system clock
clock = pygame.time.Clock()

#font
font = pygame.font.Font('images\Pixellettersfull-BnJ5.ttf', 60)  

#explosion
explosion_frames = [pygame.image.load(join('images','explosions',f'{i}.png')).convert_alpha() for i in range(21)]

#Audio files
laser_sound = pygame.mixer.Sound('audio\laser.wav') 
laser_sound.set_volume(0.4) 
explosion_sound=pygame.mixer.Sound('audio\explosion.wav') 
damage_sound = pygame.mixer.Sound('audio\damage.ogg') 
gameplay_music = pygame.mixer.Sound('audio\game_music.wav')   
gameplay_music.play() 
gameplay_music.set_volume(0.2)


meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 150)

running = True 

# num_collisions = 1

#displaying the screen indefinitely 
while running: 
    dt = clock.tick() / 1000
    #allowing user to close the window 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        if event.type == meteor_event: 
            x,y = randint(0,WINDOW_WIDTH), randint(-200,-100)
            Meteor((all_sprites, meteor_sprites),meteor_surf,(x,y))

    all_sprites.update(dt)
    
    #managing lives
    collision_Sprites = pygame.sprite.spritecollide(player, meteor_sprites,  True, pygame.sprite.collide_mask)  
    if collision_Sprites: 
        # num_collisions -= 1  
        damage_sound.play() 
    # if num_collisions == 0: 
    #     damage_sound.play()
        running = False  
        
    
    #collision detecting
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True) 
        if collided_sprites: 
            laser.kill()   
            explosion_sound.play() 
            AnimatedExplosion(explosion_frames,laser.rect.midtop,all_sprites)

    display_surface.fill('#2E2B4E')  

    display_score() 
    all_sprites.draw(display_surface)

    pygame.display.update() 

pygame.quit() 