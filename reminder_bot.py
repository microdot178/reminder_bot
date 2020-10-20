import telebot
from threading import Thread
import time
from time import strftime, gmtime
import json

do = True

<<<<<<< HEAD
bot = telebot.TeleBot('');

def send_message(message):
	bot.send_message(, message)
=======
bot = telebot.TeleBot('tokentokentokentokentokentokentokentokentokentokentoken');

def send_message(message):
	bot.send_message(idididid, message)
>>>>>>> 1f889181394dfd089a990c36cbb0baf70099c006

def listen_messages(): #слушает сообщения пользователя

	@bot.message_handler(content_types=['text'])

	def start(message):

		if message.text == '/help':
			bot.send_message(message.chat.id, '''/add daily - добавить ежедневное сообщение\n
/add once - добавить разовое сообщение\n/show dailys - покаказь ежедневные сообщения\n
/show onces - показать разовые сообщения\n/del daily - удалить ежедневное сообщение\n
/del once - удалить разовое сообщение\n/del all - удалить все сообщения''')

		elif message.text == '/add daily': #добавить ежедневную задачу
			bot.register_next_step_handler(message, dailymsg);
			bot.send_message(message.chat.id, 'введите время в формате hh:mm:ss')

		elif message.text == '/add once': #добавить разовую задачу
			bot.register_next_step_handler(message, oncemsg);
			bot.send_message(message.chat.id, 'введите время в формате hh:mm:ss')

		elif message.text == '/show dailys':
			with open('data.json') as f:
				data = json.load(f)
			daily = data['daily']
			showdailys = ''
			for i in daily:
				showdailys += i + ' - ' + daily[i] + '\n'
			if len(showdailys) == 0:
				bot.send_message(message.chat.id, 'нет сообщений')
			else:
				bot.send_message(message.chat.id, showdailys)

		elif message.text == '/show onces':
			with open('data.json') as f:
				data = json.load(f)
			once = data['once']
			showonces = ''
			for i in once:
				showonces += i + ' - ' + once[i] + '\n'
			if len(showonces) == 0:
				bot.send_message(message.chat.id, 'нет сообщений')
			else:
				bot.send_message(message.chat.id, showonces)

		elif message.text == '/del daily':
			bot.register_next_step_handler(message, del_daily);
			bot.send_message(message.chat.id, 'время сообщения?')

		elif message.text == '/del once':
			bot.register_next_step_handler(message, del_once);
			bot.send_message(message.chat.id, 'время сообщения?')
		elif message.text == '/del all':
			once = {}
			daily = {}
			data = {'once': once, 'daily': daily}
			with open('data.json', 'w') as f:
				f.write(json.dumps(data))
		else:
			bot.send_message(message.chat.id, '/help - справка')

	def del_once(message):
		with open('data.json') as f:
			data = json.load(f)

		once = data['once']
		daily = data['daily']
		try:
			del once[message.text]
			data = {'once': once, 'daily': daily}
			with open('data.json', 'w') as f:
				f.write(json.dumps(data))
		except:
			send_message('сообщения на это время небыло назначено')

	def del_daily(message):
		with open('data.json') as f:
			data = json.load(f)

		once = data['once']
		daily = data['daily']
		try:
			del daily[message.text]
			data = {'once': once, 'daily': daily}
			with open('data.json', 'w') as f:
				f.write(json.dumps(data))
		except:
			send_message('сообщения на это время небыло назначено')

	def dailymsg(message):
		global dailymsg_time
		dailymsg_time = message.text
		bot.register_next_step_handler(message, save_dailymsg);
		bot.send_message(message.chat.id, 'введите текст сообщения')

	def save_dailymsg(message):
		dailymsg_text = message.text
		to_save = {dailymsg_time : dailymsg_text}
		with open('data.json') as f:
			data = json.load(f)
		once = data['once']
		daily = data['daily']
		daily.update(to_save)
		data = {'once': once, 'daily': daily}
		with open('data.json', 'w') as f:
			f.write(json.dumps(data))

	def oncemsg(message):
		global oncemsg_time
		oncemsg_time = message.text
		bot.register_next_step_handler(message, save_oncemsg);
		bot.send_message(message.chat.id, 'введите текст сообщения')

	def save_oncemsg(message):
		oncemsg_text = message.text
		to_save = {oncemsg_time : oncemsg_text}
		with open('data.json') as f:
			data = json.load(f)
		once = data['once']
		daily = data['daily']
		once.update(to_save)
		data = {'once': once, 'daily': daily}
		with open('data.json', 'w') as f:
			f.write(json.dumps(data))

	bot.polling(none_stop = True, interval=0)

def read_data(): #читает data.json

	while do:
		try:
			with open('data.json') as f:
				data = json.load(f)

			once = data['once']
			daily = data['daily']
			for i in once:
				if i == strftime("%H:%M:%S", gmtime()):
					send_message(once[i])
					del once[i]
					data = {'once': once, 'daily': daily}
					with open('data.json', 'w') as f:
						f.write(json.dumps(data))

			for i in daily:
				if i == strftime("%H:%M:%S", gmtime()):
					send_message(daily[i])
					time.sleep(1)

		except:
			None

th_1, th_2 = Thread(target=listen_messages), Thread(target = read_data)

if __name__ == '__main__':
	th_1.start(), th_2.start()
	th_1.join(), th_2.join()
