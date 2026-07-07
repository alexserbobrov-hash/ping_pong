from pygame import *
init()

btn_continue = Rect(550, 300, 300, 60)
btn_speed_p = Rect(550, 400, 150, 60)
btn_speed_n = Rect(700, 400, 150, 60)
btn_reset = Rect(550, 400, 300, 60)
btn_quit = Rect(550, 500, 300, 60)

count_p = 0
paused = False

move_up1 = False
move_up2 = False

move_down1 = False
move_down2 = False

finished_p1 = False
finished_p2 = False

finished = False

game_over = False

speed_x = 3
speed_y = 5

score_1 = 0
score_2 = 0

back_color = (150, 150, 255)

window = display.set_mode((1400, 1000))

display.set_caption('Пинг-Понг')
display.set_icon(image.load('Media/ball.png'))

clock = time.Clock()

class Area():
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Picture(Area):
    def __init__(self, filename, x, y, width, height):
        Area.__init__(self, x, y, width, height)
        self.filename = image.load(filename)
    def draw(self):
        window.blit(self.filename, (self.rect.x, self.rect.y))

class Label(Area):
    def set_text(self, text, size, color = (20, 20, 20)):
        self.text = text
        self.image = font.SysFont('impact', size).render(text, True, color)
    def draw(self, shift_x, shift_y):
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y)) 

def reset():
    ball.rect.x = 200
    ball.rect.y = 240
    player1.rect.x = 60
    player1.rect.y = 500
    player2.rect.x = 1300
    player2.rect.y = 500

def draw_button(surface, rect, text, font, base_color, hover_color, mx, my):
    is_hover = rect.collidepoint(mx, my)
    if is_hover:
        color = hover_color
    else:
        color = base_color
    draw.rect(surface, color, rect)
    draw.rect(surface, (255, 255, 255), rect, 2)
    txt_surf = font.render(text, True, (255, 255, 255))
    txt_rect = txt_surf.get_rect()
    txt_rect.center = rect.center  # Автоматическое центрирование текста в кнопке
    surface.blit(txt_surf, txt_rect)
    return is_hover

ball = Picture('Media/ball.png', 200, 240, 50, 50)
player1 = Picture('Media/player_1.png', 60, 500, 50, 30)
player2 = Picture('Media/player_2.png', 1300, 500, 100, 30)

font.init()

font1 = font.Font(None, 108)
font2 = font.Font(None, 55)
font3 = font.Font(None, 35)

while not game_over:
    mx, my = mouse.get_pos()
    for events in event.get():
        if events.type == QUIT:
            game_over = True
        elif events.type == KEYDOWN:
            if events.key == K_w:  
                move_up1 = True
            if events.key == K_s:
                move_down1 = True
            if events.key == K_UP:  
                move_up2 = True
            if events.key == K_DOWN:
                move_down2 = True
            if events.key == K_ESCAPE and not finished:
                paused = not paused
        elif events.type == KEYUP:
            if events.key == K_w:  
                move_up1 = False
            if events.key == K_s:
                move_down1 = False
            if events.key == K_UP:  
                move_up2 = False
            if events.key == K_DOWN:
                move_down2 = False
        elif events.type == MOUSEBUTTONDOWN and paused:
            if btn_continue.collidepoint(events.pos):
                paused = False
            elif btn_speed_n.collidepoint(events.pos):
                if abs(speed_x) > 2:
                    if speed_x > 0:
                        speed_x -= 2
                    elif speed_x < 0:
                        speed_x += 2
            elif btn_speed_p.collidepoint(events.pos):
                if abs(speed_x) < 18:
                    if speed_x > 0:
                        speed_x += 2
                    elif speed_x < 0:
                        speed_x -= 2 
            elif btn_quit.collidepoint(events.pos):
                game_over = True
        elif events.type == MOUSEBUTTONDOWN and finished:
            if btn_reset.collidepoint(events.pos):
                paused, finished, finished_p1, finished_p2 = False, False, False, False
                speed_x = 3
                reset()
            elif btn_quit.collidepoint(events.pos):
                game_over = True

    speed_text = font2.render(f'Текущая скорость: {abs(speed_x)}', True, (0, 0, 0))

    window.fill(back_color)

    ball.draw()
    player1.draw()
    player2.draw()

    window.blit(speed_text, (20, 20))

    if not finished and not paused:
        count_p = 0
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        #speed_text = font2.render(f'Текущая скорость: {abs(speed_x)}', True, (0, 0, 0))

        if ball.rect.right >= 1400:
            finished = True
            finished_p1 = True
        
        if ball.rect.left <= 0:
            finished = True
            finished_p2 = True

        if ball.rect.top <= 0 or ball.rect.bottom >= 1000:
            speed_y *= -1

        if ball.rect.left <= player1.rect.right and speed_x < 0 and ball.colliderect(player1.rect):
            speed_x *= -1
        
        if ball.rect.right >= player2.rect.left - 5 and speed_x > 0 and ball.colliderect(player2.rect):
            speed_x *= -1
        
        if ball.rect.bottom >= player1.rect.top and speed_y > 0 and ball.colliderect(player1.rect):
            speed_y *= -1
        
        if ball.rect.top >= player1.rect.bottom and speed_y < 0 and ball.colliderect(player1.rect):
            speed_y *= -1
        
        if ball.rect.bottom >= player2.rect.top and speed_y > 0 and ball.colliderect(player2.rect):
            speed_y *= -1

        if ball.rect.top >= player2.rect.bottom and speed_y < 0 and ball.colliderect(player2.rect):
            speed_y *= -1
        

        '''
        for events in event.get():
            if events.type == QUIT:
                game_over = True
            elif events.type == KEYDOWN:
                if events.key == K_w:  
                    move_up1 = True
                if events.key == K_s:
                    move_down1 = True
                if events.key == K_UP:  
                    move_up2 = True
                if events.key == K_DOWN:
                    move_down2 = True
            elif events.type == KEYUP:
                if events.key == K_w:  
                    move_up1 = False
                if events.key == K_s:
                    move_down1 = False
                if events.key == K_UP:  
                    move_up2 = False
                if events.key == K_DOWN:
                    move_down2 = False

        ball.fill()
        player1.fill()
        player1.fill()
        '''
    
        if move_up1 and player1.rect.y > 3:
            player1.rect.y -= 7
        if move_down1 and player1.rect.y < 926:
            player1.rect.y += 7
        if move_up2 and player2.rect.y > 3:
            player2.rect.y -= 7
        if move_down2 and player2.rect.y < 926:
            player2.rect.y += 7

        #window.fill(back_color)

        #ball.draw()
        #player1.draw()
        #player2.draw()

        #window.blit(speed_text, (20, 20))

    if paused:
        overlay = Surface(window.get_size(), SRCALPHA)
        overlay.fill((0, 0, 0, 75))
        window.blit(overlay, (0, 0))

        #speed_text = font2.render(f'Текущая скорость: {abs(speed_x)}', True, (0, 0, 0))
        pause_text = font1.render(f'Остановлено', True, (255, 255, 255))
        #window.blit(speed_text, (20, 20))
        window.blit(pause_text, (455, 900))
        draw_button(window, btn_continue, 'Продолжить', font2, (70, 130, 180), (100, 180, 230), mx, my)
        draw_button(window, btn_speed_n, "- скорость", font3, (70, 130, 180), (100, 180, 230), mx, my)
        draw_button(window, btn_speed_p, "+ скорость", font3, (70, 130, 180), (100, 180, 230), mx, my)
        draw_button(window, btn_quit, "Выйти", font2, (70, 130, 180), (100, 180, 230), mx, my)

    if finished:

        if finished_p1:
            End_Label = Label(470, 90, 100, 50) 
            End_Label.set_text('Игрок 1 победил!', 60, (0, 0, 0))
            End_Label.draw(20, 20)

        elif finished_p2:
            End_Label = Label(470, 90, 100, 50) 
            End_Label.set_text('Игрок 2 победил!', 60, (0, 0, 0))
            End_Label.draw(20, 20)

        overlay = Surface(window.get_size(), SRCALPHA)
        overlay.fill((0, 0, 0, 75))
        window.blit(overlay, (0, 0))

        #speed_text = font2.render(f'Текущая скорость: {abs(speed_x)}', True, (0, 0, 0))
        pause_text = font1.render(f'Остановлено', True, (255, 255, 255))
        #window.blit(speed_text, (20, 20))
        window.blit(pause_text, (455, 900))
        draw_button(window, btn_reset, 'Заново', font2, (70, 130, 180), (100, 180, 230), mx, my)
        draw_button(window, btn_quit, "Выйти", font2, (70, 130, 180), (100, 180, 230), mx, my)

    clock.tick(60)
    display.update()
    
