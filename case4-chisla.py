import random
import time
import configparser
import datetime
import os

config = configparser.ConfigParser()

def save_game(diapazon, number_to_guess, attempts, start_time):
    # Чтение текущего значения statistics перед сохранением
    config.read('game.ini')
    statistics = config['Game'].get('statistics', 'off')
    
    config['Game'] = {
        'diapazon': str(diapazon),
        'number_to_guess': str(number_to_guess),
        'attempts': str(attempts),
        'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'statistics': statistics
    }
    
    with open('game.ini', 'w') as configfile:
        config.write(configfile)

def load_game():
    if not os.path.isfile('game.ini'):
        print("Файл game.ini не найден. Начнём новую игру.")
        return setup_new_game()

    config.read('game.ini')
    diapazon = int(config['Game']['diapazon'])
    number_to_guess = int(config['Game']['number_to_guess'])
    attempts = int(config['Game']['attempts'])
    start_time = datetime.datetime.strptime(config['Game']['start_time'], '%Y-%m-%d %H:%M:%S')
    return diapazon, number_to_guess, attempts, start_time

def toggle_statistics():
    # Создаем файл и секцию при их отсутствии
    if not os.path.isfile('game.ini'):
        config['Game'] = {'statistics': 'off'}
    else:
        config.read('game.ini')
        if not config.has_section('Game'):
            config.add_section('Game')
    
    # Получаем и меняем значение statistics
    current_status = config['Game'].get('statistics', 'off')
    new_status = 'off' if current_status == 'on' else 'on'
    config['Game']['statistics'] = new_status

    with open('game.ini', 'w') as configfile:
        config.write(configfile)
    print(f"Ведение статистики {'включено' if new_status == 'on' else 'отключено'}.")

def play_game():
    print("Добро пожаловать в игру 'Угадай число'!")
    time.sleep(2)
    print("Командные клавиши (действуют после начала раунда):")
    print("'с' - сохранить игру, 'з' - загрузить сохранение,")
    print("'о' - обновление статистики, 'в' - выход из игры.")
    time.sleep(2)
    
    if os.path.isfile('game.ini'):
        print("Нажмите 'з' для загрузки прогресса игры или любую другую клавишу для начала новой игры.")
        key = input()
        if key.lower() == "з":
            diapazon, number_to_guess, attempts, start_time = load_game()
        else:
            diapazon, number_to_guess, attempts, start_time = setup_new_game()
    else:
        diapazon, number_to_guess, attempts, start_time = setup_new_game()

    print(f"Я загадал число от 1 до {diapazon}. У вас есть {attempts} попыток, чтобы угадать.")
    print("Нажмите 'с' для сохранения прогресса игры, 'в' для выхода, ")
    print("или 'о' для включения/выключения статистики.")

    attempts_at_start = attempts

    # Проверка наличия секции 'Game' и параметра 'statistics'
    config.read('game.ini')
    if not config.has_section('Game'):
        config.add_section('Game')
    statistics = config['Game'].get('statistics', 'off')

    while attempts > 0:
        guess = input("Введите вашу догадку: ")

        if guess.lower() == "с":
            save_game(diapazon, number_to_guess, attempts, start_time)
            print("Прогресс игры сохранен.")
            continue
        
        if guess.lower() == "в":
            print("Выход...")
            exit(0)

        if guess.lower() == "о":
            toggle_statistics()
            statistics = config['Game']['statistics']
            continue

        if not guess.isdigit():
            print("Пожалуйста, введите целое число.")
            continue

        guess = int(guess)

        if guess < number_to_guess:
            print("Слишком маленькое число. Попробуйте еще раз.")
        elif guess > diapazon:
            print("Число выходит за рамки диапазона возможных чисел.")
        elif guess > number_to_guess:
            print("Слишком большое число. Попробуйте еще раз.")
        else:
            end_time = datetime.datetime.now()
            game_time = end_time - start_time
            print(f"Поздравляю! Вы угадали число {number_to_guess} за {attempts_at_start - attempts + 1} попыток(попытки) и за {game_time.seconds} секунд(ы).")

            # Если statistics равно on, записываем статистику в файл
            if statistics == 'on':
                with open('statistics.txt', 'a') as f:
                    f.write(f"Attempts: {attempts_at_start - attempts + 1}, Time: {game_time.seconds} seconds\n")
            break

        attempts -= 1
        print(f"Число оставшихся попыток: {attempts}")

    if attempts == 0:
        print(f"Игра окончена. Загаданное число было {number_to_guess}.")

    play_again = input('Хотите сыграть еще раз? (введите "да" для продолжения): ')
    if play_again.lower() == "да":
        play_game()
    else:
        print("Спасибо за игру! До свидания.")

def setup_new_game():
    print('Я загадаю число от 1 до... "Введите предельно возможное число:"')
    while True:
        try:
            diapazon = int(input())
            break
        except:
            print("Пожалуйста, введите целое число: ")

    number_to_guess = random.randint(1, diapazon)
    print('Введите желаемое количество попыток, доступное Вам: ')
    while True:
        try:
            attempts = int(input())
            break
        except:
            print("Пожалуйста, введите целое число: ")
    start_time = datetime.datetime.now()
    return diapazon, number_to_guess, attempts, start_time

play_game()
