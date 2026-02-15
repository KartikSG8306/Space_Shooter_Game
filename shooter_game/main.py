import pygame
from pygame import *
import random
from player import Player , Bullet
from enemy import Enemy , Particle


width , height = 1000,800
fps=60

black = (10 ,10 ,15)
neon_green = (50 , 255 ,50)
yellow = (255,255,0)
white = (255,255,255)
neon_red = (255, 50, 50)

player_friction = 0.98
recoil_force = 5.0
player_speed_limit = 10.0
enemy_speed = 2
bullet_speed = 15.0

pygame.init()
screen = display.set_mode((width , height))
display.set_caption("Space Shooter Game")
clock = time.Clock()
font_score = font.SysFont("Orbitron", 24)
font_title = font.SysFont("Impact",80)
font_sub = font.SysFont("Consolas",30)


def main():

    game_active = False

    player = Player()
    bullets = []
    enemies = []
    particles = []

    score =0
    shake_timer=0

    last_spawn_time = time.get_ticks()

    running = True
    while running:
        clock.tick(fps)
        current_time = time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == MOUSEBUTTONDOWN:
                if game_active :
                    if event.button == 1:
                        bullets.append(player.shoot())
                        shake_timer = 5
                else :
                    game_active = True
                    player = Player()
                    bullets = []
                    enemies = []
                    particles = []
                    score = 0
                    last_spawn_time = current_time
        if game_active:
            spawn_delay = max(300, 1000 - (score // 200) * 50)

            if current_time - last_spawn_time > spawn_delay:
                enemies.append(Enemy())
                last_spawn_time = current_time

            player.update()

            for p in particles:
                p.update()
                if p.timer <= 0:
                    particles.remove(p)

            for b in bullets:
                b.update()
                if not (0 <= b.pos.x <= width and 0<= b.pos.y <= height):
                    bullets.remove(b)

            for e in enemies:
                e.update(player.pos)

                if e.pos.distance_to(player.pos) < e.radius + player.radius:
                    game_active = False

                    for _ in range(50):
                        particles.append(Particle(player.pos.x , player.pos.y , neon_green))
                for b in bullets:
                    if e.pos.distance_to(b.pos) < e.radius + b.radius:
                        enemies.remove(e)
                        bullets.remove(b)
                        score+= 100
                        for _ in range(10):
                            particles.append(Particle(e.pos.x,e.pos.y,neon_red))
                        break

        screen.fill(black)

        offset = [0,0]
        if shake_timer > 0:
            shake_timer -= 1
            offset = [random.randint(-3 , 3) , random.randint(-3,3)]

        for x in range(0 , width ,50):
            draw.line(screen ,(20,20,30), (x + offset[0],0),(x+offset[0] , height))
        for y in range(0 , height , 50):
            draw.line(screen , (20 ,20 ,30), (0,y+offset[1]),(width , y+offset[1]))

        if game_active:
            player.draw(screen , offset)
            for b in bullets:
                b.draw(screen , offset)
            for e in enemies:
                e.draw(screen , offset)
            for p in particles:
                p.draw(screen , offset)
            
            score_text = font_score.render(f"SCORE : {score}" , True , white)
            screen.blit(score_text , (10 ,10))
        else :

            title_text = font_title.render("SPACE SHOOTER", True, (0,255,255))
            title_rect = title_text.get_rect(center=(width // 2, height // 2 - 50))
            screen.blit(title_text, title_rect)


            if score > 0:
                sub_text = font_sub.render(f"GAME OVER! Score: {score}", True, neon_red)
            else:
                sub_text = font_sub.render("Aim to Shoot. Shoot to Move.", True, white)

            sub_rect = sub_text.get_rect(center=(width // 2, height // 2 + 20))
            screen.blit(sub_text, sub_rect)

            prompt_text = font_score.render("[ CLICK MOUSE TO START ]", True, neon_green)
            prompt_rect = prompt_text.get_rect(center=(width // 2, height // 2 + 80))


            if (pygame.time.get_ticks() // 500) % 2 == 0:
                screen.blit(prompt_text, prompt_rect)


            for p in particles:
                p.update()
                p.draw(screen, offset)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()












