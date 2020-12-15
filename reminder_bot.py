import telebot
from threading import Thread
import time
from time import strftime, gmtime
import json

do = True

bot = telebot.TeleBot('tokentokentokentokentokentoken');

def send_message(id ,message): 
	bot.send_message(id, message)

def check_id_in_json(id): #если id нету, то добавляет его в json
		
	with open('data.json') as f:
		data = json.load(f)
		check = str(id) in data.keys()
		if check == False:
			data[str(id)] = {'once': {}, 'daily': {}}
			with open('data.json', 'w') as f:
				f.write(json.dumps(data))
				print(id, ' добавлен в базу')

def listen_messages(): #слушает сообщения пользователя

	@bot.message_handler(content_types=['text'])

	def start(message):
		
		check_id_in_json(message.chat.id)

		if message.text == '/help': #показать список команд
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

		elif message.text == '/show dailys': #показать ежедневные сообщения
			with open('data.json') as f:
				data = json.load(f)
			id = data[str(message.chat.id)]
			daily = id['daily']
			showdailys = ''
			for i in daily:
				showdailys += i + ' - ' + daily[i] + '\n'
			if len(showdailys) == 0:
				bot.send_message(message.chat.id, 'нет сообщений')
			else:
				bot.send_message(message.chat.id, showdailys)

		elif message.text == '/show onces': #показать разовые сообщения
			with open('data.json') as f:
				data = json.load(f)
			id = data[str(message.chat.id)]
			once = id['once']
			showonces = ''
			for i in once:
				showonces += i + ' - ' + once[i] + '\n'
			if len(showonces) == 0:
				bot.send_message(message.chat.id, 'нет сообщений')
			else:
				bot.send_message(message.chat.id, showonces)

		elif message.text == '/del daily': #удалить ежедневное сообщение
			bot.register_next_step_handler(message, del_daily);
			bot.send_message(message.chat.id, 'время сообщения?')

		elif message.text == '/del once': #удалить разовое сообщение
			bot.register_next_step_handler(message, del_once);
			bot.send_message(message.chat.id, 'время сообщения?')
		elif message.text == '/del all': #удалить вообще все сообщения
			with open('data.json',) as f:
				data = json.load(f)
			data[str(message.chat.id)] = {"once": {}, "daily": {}}
			with open('data.json', 'w') as f:
				f.write(json.dumps(data))
		else:
			bot.send_message(message.chat.id, '/help - справка')

	def del_once(message): #удаляет разовое сообщение
		with open('data.json') as f:
			data = json.load(f)
		id = data[str(message.chat.id)]
		once = id['once']
		daily = id['daily']
		try:
			del once[message.text]
			data[str(message.chat.id)] = {'once': once, 'daily': daily}
			with open('data.json', 'w') as f:
				f.write(json.dumps(data))
		except:
			send_message('сообщения на это время небыло назначено')

	def del_daily(message): #удаляет ежедневное сообщение
		with open('data.json') as f:
			data = json.load(f)
		id = data[str(message.chat.id)]
		once = id['once']
		daily = id['daily']
		try:
			del daily[message.text]
			data[str(message.chat.id)] = {'once': once, 'daily': daily}
			with open('data.json', 'w') as f:
				f.write(json.dumps(data))
		except:
			send_message('сообщения на это время небыло назначено')

	def dailymsg(message): #добавляет ежедневное сообщение
		global dailymsg_time
		dailymsg_time = message.text
		bot.register_next_step_handler(message, save_dailymsg);
		bot.send_message(message.chat.id, 'введите текст сообщения')

	def save_dailymsg(message): #сохраняет ежедневное сообщение в json
		dailymsg_text = message.text
		to_save = {dailymsg_time : dailymsg_text}
		with open('data.json') as f:
			data = json.load(f)
		id = data[str(message.chat.id)]
		once = id['once']
		daily = id['daily']
		daily.update(to_save)
		data[str(message.chat.id)] = {'once': once, 'daily': daily}
		with open('data.json', 'w') as f:
			f.write(json.dumps(data))

	def oncemsg(message): #добавляет разовое сообщение
		global oncemsg_time
		oncemsg_time = message.text
		bot.register_next_step_handler(message, save_oncemsg);
		bot.send_message(message.chat.id, 'введите текст сообщения')

	def save_oncemsg(message): #сохраняет разовое сообщение в json
		oncemsg_text = message.text
		to_save = {oncemsg_time : oncemsg_text}
		with open('data.json') as f:
			data = json.load(f)
		id = data[str(message.chat.id)]
		once = id['once']
		daily = id['daily']
		once.update(to_save)
		data[str(message.chat.id)] = {'once': once, 'daily': daily}
		with open('data.json', 'w') as f:
			f.write(json.dumps(data))

	bot.polling(none_stop = True, interval=0)

def read_data(): #читает data.json

	while do:
		try:
			with open('data.json') as f:
				data = json.load(f)

			for user_id in data:

				id = data[user_id]
				once = id['once']
				daily = id['daily']
				
				for i in once:
					if i == strftime("%H:%M:%S", gmtime()): # если время разового сообщения совпадает с gmtime
						send_message(user_id, once[i])		# отправляет сообщение и 
						del once[i]							# удаляет его из data.json
						data[str(user_id)] = {'once': once, 'daily': daily}
						with open('data.json', 'w') as f:
							f.write(json.dumps(data))

				for i in daily:
					if i == strftime("%H:%M:%S", gmtime()):	# тоже самое для ежедневных сообщений
						send_message(user_id, daily[i])		# только без удаления
						time.sleep(1)

		except:
			None

th_1, th_2 = Thread(target=listen_messages), Thread(target = read_data)

if __name__ == '__main__':
	th_1.start(), th_2.start()
	th_1.join(), th_2.join()