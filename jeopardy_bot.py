import os
import telebot
from question_handling import *
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

formas_de_decir_que_si = ["yes", "si", "sí", "yes!", "si!", "sí!", "¡si!", "¡sí!", "shoot", "go on", "sabelo", "de una", "obvio", "mas bien", "claro", "más bien", "por favor", "you bet", "definitely", "obviously", "naturally", "of course", "ask", "i'm ready", "ready", "bueno", "sip", "porfi"]
formas_de_decir_que_no = ["no", "No", "no!", "¡no!"]

# online flag // modified by bot_start
online_flag = False

@bot.message_handler(commands = ['start', 'hello', 'hi'])
def bot_start(message):
    global online_flag
    online_flag = True
    bot.send_message(message.chat.id, "Hello. Type /ask for a question. then, answer it or type /info to know more about the question you got")

# GET methods //////////////////////////////////////////////////////////////////////////
def get_question():
    global index
    index = random.randint(0, len(questions))
    # print(index)
    return questions.iloc[index].category, questions.iloc[index].question
def get_info():

    question_air_date = questions.iloc[index].air_date
    question_round = questions.iloc[index].game_round
    question_value = questions.iloc[index].value
    info = "This question was featured in the episode aired on {date}. The round was {round} and it was worth {value}".format(
        date=question_air_date, round=question_round, value=question_value)
    return info

@bot.message_handler(commands=['ask', 'shoot', 'play', 'Play', 'Ask'], func=lambda message: online_flag)
def ask_question(message):
    chosen_question = get_question()
    question_send = "Category: {cat}\n\n{q}".format(cat=chosen_question[0], q=chosen_question[1])
    print(questions.iloc[index].answer) # print the answer to the console to test bc i don't usually get them right unaided
    sent_msg = bot.send_message(message.chat.id, question_send, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, check_answer)

@bot.message_handler(func=lambda message: online_flag and not message.text.startswith('/'))
def other_messages(message):
    bot.send_message(message.chat.id, "Type /play to get a random Jeopardy question :)")

@bot.message_handler(commands = ['info'], func=lambda message: online_flag)
def send_info(message):
    info_msg = get_info()
    bot.reply_to(message, info_msg)
@bot.message_handler(func=lambda message: online_flag and not message.text.startswith('/'))
def check_answer(message):

    answer_full = questions.iloc[index].answer
    prefixes = ['the', 'a', 'The', 'A']
    for prefix in prefixes:
        if answer_full.startswith(prefix):
            answer = answer_full[len(prefix)+1:].lower()
        else:
            answer = answer_full.lower()
## check this
    # right_answer = questions.iloc[index].answer.lower()
    if message.text.lower() == answer:
        sent_msg = bot.reply_to(message, 'Your answer "{}" is correct!\n\nDo you want to /play again?'.format(message.text))
    elif message.text.lower() != answer and message.text.lower() in answer:
        sent_msg = bot.reply_to(message, 'Close! Your answer "{}" is almost correct. The right answer was "{}".\n\n/Play one more time?'.format(message.text, answer_full))
    elif message.text.lower() == 'info':
        send_info(message)
    else:
        sent_msg = bot.reply_to(message, 'Your answer "{wrong}" is wrong :(\n\nThe correct answer was "{right}"\n\nCare to /play again?'.format(wrong=message.text, right=answer_full))
    bot.register_next_step_handler(sent_msg, loop)

@bot.message_handler(commands=['stop', 'bye'])
def stop(message):
    global online_flag
    online_flag = False
    bot.reply_to(message, "Bye! I'm going offline. Type /start to play again. :)")

def loop(message):
    if message.text.lower() in formas_de_decir_que_si:
        ask_question(message)
    elif message.text.lower() in formas_de_decir_que_no:
        stop(message)
    elif 'info' in message.text.lower():
        send_info(message)
    else:
        other_messages()

bot.infinity_polling()