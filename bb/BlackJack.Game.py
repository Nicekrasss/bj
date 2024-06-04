import pygame
import sys
import copy
import random

# создает объект часов, который будет использоваться для контроля частоты кадров в игре
mainClock = pygame.time.Clock()
# инициализирует все модули pygame
pygame.init()
# устанавливает заголовок окна игры
pygame.display.set_caption('MyGame')
# создает окно игры размером 700x700 пикселей
screen = pygame.display.set_mode((700, 700), 0, 32)
# создает объект шрифта для использования в игре
font = pygame.font.SysFont(None, 30)
font_2 = pygame.font.SysFont(None, 100)

# рисует текст на экране игры,
# text - текст, который нужно отрисовать, font - шрифт,
# color - цвет текста, surface - поверхность, на которой отрисовывается текст,
# x и y - координаты верхнего левого угла текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# переменная, которая используется для отслеживания состояния клика мыши
click = False

# функция, которая управляет меню игры,
# она заполняет экран синим цветом и выводит название меню
def main_menu():
    # Включение фоновой музыки для главного меню
    pygame.mixer.music.load('fon.mp3')
    pygame.mixer.music.play(-1)
    while True:
        screen.fill((205, 181, 205))
        draw_text('BlackJack', font_2, (0, 0, 0), screen, 190, 150)
        # здесь мы получаем текущие координаты мыши
        mx, my = pygame.mouse.get_pos()
        # создание кнопок, а pygame.Rect создает прямоугольник, который будет использоваться в качестве кнопки
        button_1 = pygame.Rect(250, 500, 200, 50)
        button_2 = pygame.Rect(250, 580, 200, 50)
        # этот блок кода проверяет, находится ли мышь над кнопкой и был ли произведен клик
        # если да, то вызывается соответствующая функция
        if button_1.collidepoint((mx, my)):
            if click:
                play_game()
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        # здесь мы рисуем кнопки на экране (цвет)
        pygame.draw.rect(screen, (132, 112, 255), button_1)
        pygame.draw.rect(screen, (132, 112, 255), button_2)
        # текст на кнопках
        draw_text('Играть', font, (255, 230, 201), screen, 315, 515)
        draw_text('Выход', font, (255, 230, 201), screen, 315, 595)
        # сбрасывает состояние клика перед началом нового цикла обработки событий
        click = False
        # этот блок кода обрабатывает события в игре
        # если игрок нажал на кнопку мыши, то click становится True
        # если игрок нажал на клавишу Esc или закрыл окно, то игра завершается
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        # эти две строки обновляют экран и ограничивают частоту кадров до 60 кадров в секунду
        pygame.display.update()
        mainClock.tick(60)

# музыка
pygame.mixer.init()
pygame.mixer.music.load('fon.mp3')
pygame.mixer.music.play(-1)
s = pygame.mixer.Sound('knopki.mp3')

# функция, которая запускает игру
def play_game():
    global s
    # Остановка музыки главного меню и включение фоновой музыки для игры
    pygame.mixer.music.stop()
    pygame.mixer.music.load('fonn.mp3')
    pygame.mixer.music.play(-1)

    s.play()

    # игровые вариации
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    one_deck = 4 * cards
    decks = 4
    WIDTH = 700
    HEIGHT = 700
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Blackjack')
    fps = 60
    timer = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font(None, 44)
    smaller_font = pygame.font.Font(None, 25)
    active = False
    # игровые данные (победы, проигрыши, ничья)
    records = [0, 0, 0]
    player_score = 0
    dealer_score = 0
    initial_deal = False
    my_hand = []
    dealer_hand = []
    outcome = 0
    reveal_dealer = False
    hand_active = False
    outcome = 0
    add_score = False
    results = ['', 'Ты перебрал! o_O', 'Победа! :)', 'Победа дилера :(', 'Ничья...']

    # карты дилера, которые выбираются рандомно по 1 карте за раз
    def deal_cards(current_hand, current_deck):
        card = random.randint(0, len(current_deck))
        current_hand.append(current_deck[card - 1])
        current_deck.pop(card - 1)
        return current_hand, current_deck

    # чтобы нарисовать очки дилера и игрока на экране
    def draw_scores(player, dealer):
        screen.blit(font.render(f'Очки[{player}]', True, 'white'), (350, 443))
        if reveal_dealer:
            screen.blit(font.render(f'Очки[{dealer}]', True, 'white'), (450, 100))

    # отрисовка карт
    def draw_cards(player, dealer, reveal):
        for i in range(len(player)):
            pygame.draw.rect(screen, 'white', [70 + (70 * i), 460 + (5 * i), 120, 220], 0, 5)
            screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 465 + 5 * i))
            screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 635 + 5 * i))
            pygame.draw.rect(screen, 'red', [70 + (70 * i), 460 + (5 * i), 120, 220], 5, 5)

        # если игрок не закончил ход, дилер спрячет одну карту
        for i in range(len(dealer)):
            pygame.draw.rect(screen, 'white', [70 + (70 * i), 160 + (5 * i), 120, 220], 0, 5)
            if i != 0 or reveal:
                screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
                screen.blit(font.render(dealer[i], True, 'black'), (75 + 70 * i, 335 + 5 * i))
            else:
                screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
                screen.blit(font.render('???', True, 'black'), (75 + 70 * i, 335 + 5 * i))
            pygame.draw.rect(screen, 'blue', [70 + (70 * i), 160 + (5 * i), 120, 220], 5, 5)

    # пас в руке диллера или игрока и возможность получить лучший результат
    def calculate_score(hand):
        # вычисляем новый счет руки каждый раз и проверяем сколько у нас тузов
        hand_score = 0
        aces_count = hand.count('A')
        for i in range(len(hand)):
            # для 1-9 просто добавить число
            for j in range(8):
                if hand[i] == cards[j]:
                    hand_score += int(hand[i])
            # для 10 и выше добавить 10
            if hand[i] in ['10', 'J', 'Q', 'K']:
                hand_score += 10
            # для тузов добавить 11
            elif hand[i] == 'A':
                hand_score += 11
        # определяем сколько тузов должно быть 1 вместо 11, чтобы получить меньше 21
        if hand_score > 21 and aces_count > 0:
            for i in range(aces_count):
                if hand_score > 21:
                    hand_score -= 10
        return hand_score

    # изображение
    background_image_path = 'TABLE.png'
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.scale(background_image, (700, 700))

    # отрисовка кнопок и игровых настроек
    def draw_game(act, record, result):
        button_list = []
        # единственный вариант - раздать новую руку
        if not act:
            deal = pygame.draw.rect(screen, 'white', [275, 650, 150, 50], 0, 5)
            pygame.draw.rect(screen, 'green', [275, 650, 150, 50], 3, 5)
            deal_text = font.render('Раздать', True, 'black')
            screen.blit(deal_text, (290, 665))
            button_list.append(deal)
        # жмать кнопки "раздать" и "взять", а также записи о выигрыше/проигрыше
        else:
            hit = pygame.draw.rect(screen, 'white', [200, 650, 150, 50], 0, 5)
            pygame.draw.rect(screen, 'green', [200, 650, 150, 50], 3, 5)
            hit_text = font.render('Взять', True, 'black')
            screen.blit(hit_text, (235, 665))
            button_list.append(hit)
            stand = pygame.draw.rect(screen, 'white', [350, 650, 150, 50], 0, 5)
            pygame.draw.rect(screen, 'green', [350, 650, 150, 50], 3, 5)
            stand_text = font.render('Хватит', True, 'black')
            screen.blit(stand_text, (380, 665))
            button_list.append(stand)
            score_text = smaller_font.render(f'Победа: {record[0]} Проигрыш: {record[1]} Ничья: {record[2]}', True, 'white')
            screen.blit(score_text, (15, 20))
        # отображение кнопки перезапуска
        if result != 0:
            screen.blit(font.render(results[result], True, 'white'), (15, 45))
            deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
            pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
            pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
            deal_text = font.render('Новая рука', True, 'black')
            screen.blit(deal_text, (165, 250))
            button_list.append(deal)
        return button_list

    # функция проверки условий конца игры
    def check_endgame(hand_act, deal_score, play_score, result, totals, add):
        # проверка сценариев конца игры
        # результат 1- перебрал, 2-победа, 3-поражение, 4-пуш
        if not hand_act and deal_score >= 17:
            if play_score > 21:
                result = 1
            elif deal_score < play_score <= 21 or deal_score > 21:
                result = 2
            elif play_score < deal_score <= 21:
                result = 3
            else:
                result = 4
            if add:
                if result == 1 or result == 3:
                    totals[1] += 1
                elif result == 2:
                    totals[0] += 1
                else:
                    totals[2] += 1
                add = False
        return result, totals, add

    # игровой цикл
    run = True
    while run:
        # фон и фпс
        timer.tick(fps)
        screen.blit(background_image, (0, 0))
        # инициализация руки игрока и дилера
        if initial_deal:
            for i in range(2):
                my_hand, game_deck = deal_cards(my_hand, game_deck)
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            initial_deal = False
        # счет очков и показ карт
        if active:
            player_score = calculate_score(my_hand)
            draw_cards(my_hand, dealer_hand, reveal_dealer)
            if reveal_dealer:
                dealer_score = calculate_score(dealer_hand)
                if dealer_score < 17:
                    dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            draw_scores(player_score, dealer_score)
        buttons = draw_game(active, records, outcome)

        # обработка событий, если нажать кнопку выхода, то выйти из игры
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                if not active:
                    if buttons[0].collidepoint(event.pos):
                        s.play()
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                else:
                    # если игрок хочет взять карту, то ее надо нарисовать
                    if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                        s.play()
                        my_hand, game_deck = deal_cards(my_hand, game_deck)
                    # позволить игроку завершить ход
                    elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                        s.play()
                        reveal_dealer = True
                        hand_active = False
                    elif len(buttons) == 3:
                        if buttons[2].collidepoint(event.pos):
                            s.play()
                            active = True
                            initial_deal = True
                            game_deck = copy.deepcopy(decks * one_deck)
                            my_hand = []
                            dealer_hand = []
                            outcome = 0
                            hand_active = True
                            reveal_dealer = False
                            outcome = 0
                            add_score = True
                            dealer_score = 0
                            player_score = 0

        # если игрок перебрал, ход автоматически завершается
        if hand_active and player_score >= 21:
            hand_active = False
            reveal_dealer = True

        outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

        pygame.display.flip()
    pygame.quit()
    main_menu()

# запуск основного меню при старте игры
main_menu()

