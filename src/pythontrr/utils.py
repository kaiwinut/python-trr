import os
import random
from datetime import date


def set_esc_delay(delay = 25):
	os.environ.setdefault('ESCDELAY', str(delay))


def fix_text(text):
	text = text.replace('”', '"')
	text = text.replace('“', '"')
	text = text.replace("’", "'")
	text = text.replace("‘", "'")
	text = text.replace('—', '-')
	text = text.replace("æ", 'e')
	text = text.replace("é", 'e')
	text = text.replace("à", 'a')

	return text


def generate_text(word_count = 300):
	# Read text from the texts folder
	files = os.listdir(os.path.join(os.path.dirname(__file__), 'data', 'texts'))
	file = random.choice(files)

	with open(os.path.join(os.path.dirname(__file__), 'data', 'texts', file), 'r') as f:
		try:
			content = f.read()
		except ValueError as e:
			raise Exception('Can not read %s' % file) from e

	text_list = content.split()
	i = random.randint(0, len(text_list) - 1)
	text = text_list[i]
	l = i - 1
	r = i + 1

	while len(text) < word_count:
		if r < len(text_list):
			text += ' ' + text_list[r]
			r += 1

		elif l >= 0:
			text = text_list[l] + ' ' + text
			l -= 1

	text = fix_text(text)
	title = file[:-4].replace('-', ' ').title()

	return title, text.encode('ascii', 'replace').decode()


def modify_text(text, window_width):
	for i in range(window_width):
		if len(text) <= window_width:
			break
		if text[window_width - i - 2] == ' ':
			# print(text)
			text = text[:window_width - i - 1] + '\n\n' + modify_text(text[window_width - i - 1:], window_width)
			break
	return text


def save_result(stage, target, record, tries):
	result = f'Stage: {stage}\nTarget: {target}\nRecord: {record}\nTries: {tries}'
	with open(os.path.join(os.path.dirname(__file__), 'data', 'logs', 'result.txt'), 'w') as f:
		f.write(result)


def load_result():
	with open(os.path.join(os.path.dirname(__file__), 'data', 'logs', 'result.txt'), 'r') as f:
		stage = f.readline()[7:]
		target = f.readline()[8:]
		record = f.readline()[8:]
		tries = f.readline()[7:]

		if stage == '' or record == '' or tries == '':
			stage = 1
			record = 0
			tries = 0

	return int(stage), int(record), int(tries)


def reset_results():
	with open(os.path.join(os.path.dirname(__file__), 'data', 'logs', 'result.txt'), 'w') as f:
		f.write('')	


def save_history(stage, score, tries):
	file = os.path.join(os.path.dirname(__file__), 'data', 'logs', 'history.txt')
	new_history = ' '*4 + str(stage).rjust(2) + ' '*4 + str(score).rjust(3) + ' '*5 + str(tries).rjust(2) + ' '*5 + date.today().strftime('%y/%m/%d')
	with open(file, 'r') as f:
		f.seek(0)
		history = f.read()
		if history != '':
			new_history = str(int(history[:3])+1).rjust(3) + ': ' + new_history + '\n' + history

		else:
			new_history = '  1: ' + new_history

	with open(file, 'w') as f:	
		f.write(new_history)


def load_history(entries = 3):
	file = os.path.join(os.path.dirname(__file__), 'data', 'logs', 'history.txt')
	with open(file, 'r') as f:
		history = f.readlines()

	if len(history) < entries:
		return history
	else:
		return history[:entries]


def reset_history():
	with open(os.path.join(os.path.dirname(__file__), 'data', 'logs', 'history.txt'), 'w') as f:
		f.write('')


def convert_score_to_y(s):
	return 9 - int(s) // 50


def save_config(config):
	file = os.path.join(os.path.dirname(__file__), 'data', 'logs', 'config.txt')
	with open(file, 'w') as f:	
		f.write(config)


def load_config(l):
	file = os.path.join(os.path.dirname(__file__), 'data', 'logs', 'config.txt')
	if not os.path.exists(file):
		return [0] * l
	with open(file, 'r') as f:
		config = f.read()
	return [int(s) for s in config]