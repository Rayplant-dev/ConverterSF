import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_command(message: telebot.types.Message):
    text = (
        "Чтобы узнать цену на определённое количество валюты, отправьте сообщение в формате:\n"
        "<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n"
        "Пример: eur usd 100\n"
        "Доступные команды:\n"
        "/start или /help - Показать эту подсказку\n"
        "/values - Показать список доступных валют"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    text = "Доступные валюты: евро(eur), доллар(usd), рубль(rub) и другие (введите ISO-код валюты)"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException("Неверное количество параметров. Введите /help для просмотра формата отправки валют.")

        base, quote, amount = values
        result = CurrencyConverter.get_price(base.lower(), quote.lower(), amount)
        text = f"Цена {amount} {base.upper()} в {quote.upper()} составляет {result:.2f}."

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка.\n{e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Не удалось обработать команду.\n{e}")
    else:
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
