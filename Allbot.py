import telebot
import asyncio
#from googletrans import Translator
from telebot import types
import random


bot = telebot.TeleBot('7841264202:AAHvHOTMMevaQDePOPSmVdbraZTMAa77C14')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Числа фибоначи")
    btn2 = types.KeyboardButton("Casino")
    btn3 = types.KeyboardButton("Погода")
    btn4 = types.KeyboardButton("расписание")
    btn5 = types.KeyboardButton("Переводчик")
    btn6 = types.KeyboardButton("Music")
#   btn7 = types.KeyboardButtun("Time")
    markup.row(btn2)
    markup.add(btn1)
    bot.reply_to(message, f'привет, {message.from_user.first_name}', reply_markup=markup)





@bot.message_handler(func=lambda message: message.text =="Числа фибоначи")
def handler_message(message):
    bot.send_message(message.chat.id, "Введите ряд...")
    bot.register_next_step_handler(message, fibo)

def fibo(message):
    try:
        n = int(message.text)
        if n > 0:
            fib_seq = [0, 1]
            for i in range(2, n):
                fib_seq.append(fib_seq[i - 1] + fib_seq[i - 2])
            res = ''
            for i in str(fib_seq):
                res += i
            res = res[1:-2]
            bot.send_message(message.chat.id, f'Первые {n} чисел фибоначи, {res}')
        else:
            bot.send_message(message.chat.id, "Введите положительное число!")
            bot.register_next_step_handler(message, fibo)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число!")
        bot.register_next_step_handler(message, fibo)




@bot.message_handler(func=lambda message: message.text == "Casino")
def handler_casino(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Кости")
    btn2 = types.KeyboardButton("Казино")
    btn3 = types.KeyboardButton("Назад")
    markup.add(btn1, btn2)
    markup.row(btn3)
    bot.reply_to(message, "Выберите игру", reply_markup=markup)






@bot.message_handler(func=lambda message: message.text == "Кости")
def game_dice(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Бросить кости?", callback_data="roll_dice")
    markup.add(btn)
    bot.send_message(message.chat.id, "Ох, пойдет щас возня", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "roll_dice")
def callback_roll_dice(call):
    player_dice = bot.send_dice(call.message.chat.id, emoji='🎲')
    bot_dice = bot.send_dice(call.message.chat.id, emoji='🎲')
    player_value = player_dice.dice.value
    bot_value = bot_dice.dice.value
    determine_winner(call.message, player_value, bot_value)

def determine_winner(message, player_value, bot_value):
    if player_value > bot_value:
        bot.send_message(message.chat.id, f'Вы выиграли!\n<b>Ваше значение:</b> {player_value}\n<b>значение бота:</b> {bot_value}', parse_mode="html")
    elif player_value < bot_value:
        bot.send_message(message.chat.id, f'Вы проиграли.\n<b>Ваше значение:</b> {player_value}\n<b>значение бота:</b> {bot_value}', parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'Ничья!\n<b>Ваше значение:</b> {player_value}\n<b>значение бота:</b> {bot_value}', parse_mode='html')





@bot.message_handler(func=lambda message: message.text == "Казино")
def casino(message):
    slot_result = [random.choice(['🍒', '🍋', '🔔', '⭐', '🍉']) for _ in range(3)]

    if len(set(slot_result)) == 1:
        bot.send_message(message.chat.id, f'Поздравляю!\nВы выбили {slot_result} и <b>выиграли!</b>', parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'К сожалению, вы проиграли.\n<b>Ваши слоты:</b>\n{slot_result}', parse_mode='html')


@bot.message_handler(func=lambda message: message.text == "Назад")
def back(message):
    start(message)






































































bot.polling(none_stop=True)