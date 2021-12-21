import time
import curses
from .utils import *
from .config import *


#######################
#					  #
#    Define styles    #
#					  #
#######################

class Styles:
	def __init__(self):
		curses.start_color()

	@property
	def title(self):
		curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
		return curses.color_pair(1)	

	@property
	def correct_text(self):
		curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
		return curses.color_pair(2)	

	@property
	def incorrect_text(self):
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
		return curses.color_pair(3)

	@property
	def selected_option(self):
		curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
		return curses.color_pair(4)


#######################
#					  #
#    Define blocks    #
#					  #
#######################

class Block:
	def __init__(self, *inputs):
		self.window = curses.newwin(*inputs)


class TaskBlock(Block):
	def __init__(self, stdscr, styles):
		self.height = TEXT_BLOCK_HEIGHT
		self.width = curses.COLS
		self.pos_y = 1
		self.pos_x = 0

		super(TaskBlock, self).__init__(self.height, self.width, self.pos_y, self.pos_x)
		
		self.stdscr, self.styles = stdscr, styles
		self.window.nodelay(True)
		self.cursor_y, self.cursor_x = 0, 0

	def init_ui(self):
		self.update()

	def update(self):
		self.window.clear()
		title, self.original_text = generate_text(word_count = WORD_COUNT)

		text_banner = ' Task' + ' ' * (curses.COLS - 5)
		self.text_banner = text_banner[:-len(title)-1] + title + ' '

		self.modified_text = modify_text(self.original_text, self.width)
		self.target_text = self.modified_text

		self.stdscr.addstr(0, 0, self.text_banner, curses.A_BOLD | self.styles.title)
		self.window.addstr(0, 0, self.modified_text, curses.A_DIM)
		self.window.move(0, 0)
		self.window.addstr(1, 0, '^', curses.A_NORMAL)

	def handle_correct_input(self):
		self.window.clear()
		self.window.addstr(0, 0, self.modified_text, curses.A_NORMAL | self.styles.correct_text)

		if len(self.target_text) == 1:
			return True

		self.target_text = self.target_text[1:]

		if self.target_text[0] == '\n':
			self.target_text = self.target_text[2:]
			self.cursor_y += 2
			self.cursor_x = 0
		else:
			self.cursor_x += 1
		self.window.addstr(self.cursor_y, self.cursor_x, self.target_text, curses.A_DIM)
		self.window.move(self.cursor_y, self.cursor_x)
		self.window.addstr(self.cursor_y + 1, self.cursor_x, '^', curses.A_NORMAL)

	def handle_incorrect_input(self, key):
		self.window.clear()
		self.window.addstr(0, 0, self.modified_text, curses.A_NORMAL | self.styles.correct_text)
		self.window.addstr(self.cursor_y, self.cursor_x, self.target_text, curses.A_DIM)
		self.window.addstr(self.cursor_y, self.cursor_x, self.target_text[0], curses.A_UNDERLINE | curses.A_BOLD | self.styles.incorrect_text)
		self.window.move(self.cursor_y, self.cursor_x)
		self.window.addstr(self.cursor_y + 1, self.cursor_x, chr(key), curses.A_NORMAL | self.styles.incorrect_text)

	def restore_state(self):
		self.window.clear()
		self.stdscr.addstr(0, 0, self.text_banner, curses.A_BOLD | self.styles.title)
		self.window.addstr(0, 0, self.modified_text, curses.A_NORMAL | self.styles.correct_text)
		self.window.addstr(self.cursor_y, self.cursor_x, self.target_text, curses.A_DIM)
		# self.window.addstr(self.cursor_y, self.cursor_x, self.target_text[0], curses.A_UNDERLINE | curses.A_BOLD | self.styles.incorrect_text)
		self.window.move(self.cursor_y, self.cursor_x)
		self.window.addstr(self.cursor_y + 1, self.cursor_x, '^', curses.A_NORMAL)

	def reset_cursor(self):
		self.cursor_y, self.cursor_x = 0, 0


class ScoreBlock(Block):
	def __init__(self, stdscr, styles):
		self.height = SCORE_BLOCK_HEIGHT
		self.width = SCORE_BLOCK_WIDTH
		self.pos_y = TEXT_BLOCK_HEIGHT + 2
		self.pos_x = 0

		super(ScoreBlock, self).__init__(self.height, self.width, self.pos_y, self.pos_x)

		self.stdscr, self.styles = stdscr, styles
		self.start_time = time.time()
		self.correct_count = 0
		self.error_count = 0

		self.passed_time = 0.0
		self.error_rate = 0.0
		self.kpm = 0
		self.score = 0

		self.already_passed_time = None

	def init_ui(self):
		score_banner = ' Score' + ' ' * (SCORE_BLOCK_WIDTH - 7)
		self.stdscr.addstr(TEXT_BLOCK_HEIGHT + 1, 0, score_banner, curses.A_BOLD | self.styles.title)

	def update(self):
		# Time updates every SCORE_UPDATE_TIME_STEP seconds
		self.passed_time = (time.time() - self.start_time) // SCORE_UPDATE_TIME_STEP * SCORE_UPDATE_TIME_STEP
		self.error_rate = self.error_count / (self.correct_count + self.error_count) if self.correct_count + self.error_count > 0 else 0.0
		self.kpm = int(self.correct_count * 60 / self.passed_time) if self.passed_time > 0 else 0
		self.score = int(self.kpm * (1 - self.error_rate))

		passed_time = f'  Time:     {str(int(self.passed_time)).rjust(3)} s'
		error_rate = f'  Error:  {"{:.1f}".format(self.error_rate * 100).rjust(5)} %'
		kpm = f'  KPM:        {str(self.kpm).rjust(3)}'
		score = f'  Score:      {str(self.score).rjust(3)}'
		self.window.clear()
		self.window.addstr(1, 0, passed_time, curses.A_BOLD)
		self.window.addstr(2, 0, error_rate, curses.A_BOLD)
		self.window.addstr(3, 0, kpm, curses.A_BOLD)
		self.window.addstr(4, 0, score, curses.A_BOLD)

	def reset(self):
		self.start_time = time.time()
		self.correct_count = 0
		self.error_count = 0
		self.passed_time = 0.0
		self.error_rate = 0.0
		self.kpm = 0
		self.score = 0

	def pause(self):
		self.already_passed_time = self.passed_time

	def restore_state(self):
		assert self.already_passed_time is not None
		self.start_time = time.time() - self.already_passed_time


class ResultBlock(Block):

	stage_to_score = list(range(0, 500, 20))

	def __init__(self, stdscr, styles):
		self.height = SCORE_BLOCK_HEIGHT
		self.width = SCORE_BLOCK_WIDTH
		self.pos_y = TEXT_BLOCK_HEIGHT + 2
		self.pos_x = SCORE_BLOCK_WIDTH

		super(ResultBlock, self).__init__(self.height, self.width, self.pos_y, self.pos_x)

		self.stdscr, self.styles = stdscr, styles
		if not READ_RESULT_FROM_HISTORY:
			reset_results()
		self.stage, self.record, self.tries = load_result()

	def init_ui(self):
		result_banner = ' Result' + ' ' * (SCORE_BLOCK_WIDTH - 8)
		self.stdscr.addstr(TEXT_BLOCK_HEIGHT + 1, SCORE_BLOCK_WIDTH, result_banner, curses.A_BOLD | self.styles.title)

		stage = f'  Stage:      {str(self.stage).rjust(3)}'
		target = f'  Target:     {str(self.stage_to_score[self.stage]).rjust(3)}'
		record = f'  Record:     {str(self.record).rjust(3)}'
		tries = f'  Tries:      {str(self.tries).rjust(3)}'

		self.window.addstr(1, 0, stage, curses.A_BOLD)
		self.window.addstr(2, 0, target, curses.A_BOLD)
		self.window.addstr(3, 0, record, curses.A_BOLD)
		self.window.addstr(4, 0, tries, curses.A_BOLD)

	def update(self, score):
		if score >= self.stage_to_score[self.stage]:
			self.stage += 1
			self.tries = 0
		else:
			self.tries += 1

		if score > self.record:
			self.record = score

		stage = f'  Stage:      {str(self.stage).rjust(3)}'
		target = f'  Target:     {str(self.stage_to_score[self.stage]).rjust(3)}'
		record = f'  Record:     {str(self.record).rjust(3)}'
		tries = f'  Tries:      {str(self.tries).rjust(3)}'
		self.window.clear()
		self.window.addstr(1, 0, stage, curses.A_BOLD)
		self.window.addstr(2, 0, target, curses.A_BOLD)
		self.window.addstr(3, 0, record, curses.A_BOLD)
		self.window.addstr(4, 0, tries, curses.A_BOLD)


class HistoryBlock(Block):
	def __init__(self, stdscr, styles):
		self.height = HISTORY_BLOCK_HEIGHT
		self.width = HISTORY_BLOCK_WIDTH
		self.pos_y = TEXT_BLOCK_HEIGHT + SCORE_BLOCK_HEIGHT + 4
		self.pos_x = 0

		super(HistoryBlock, self).__init__(self.height, self.width, self.pos_y, self.pos_x)

		self.stdscr, self.styles = stdscr, styles
		if not READ_HISTORY:
			reset_history()

	def init_ui(self):
		history_banner_1 = ' History' + ' ' * (HISTORY_BLOCK_WIDTH - 9)
		history_banner_2 = ' No.  Stage  Score  Tries' + ' ' * (HISTORY_BLOCK_WIDTH - 31) + 'Date '

		self.stdscr.addstr(TEXT_BLOCK_HEIGHT + SCORE_BLOCK_HEIGHT + 2, 0, history_banner_1, curses.A_BOLD | self.styles.title)
		self.stdscr.addstr(TEXT_BLOCK_HEIGHT + SCORE_BLOCK_HEIGHT + 3, 0, history_banner_2, curses.A_BOLD | self.styles.title)

		self.update()

	def update(self):
		for i, h in enumerate(load_history(HISTORY_ENTRIES)):
			self.window.addstr(i, 0, h.strip('\n'), curses.A_BOLD)


class GraphBlock(Block):

	y_to_score = {(2 * i + 1): str(400 - i * 100).rjust(3) for i in range(5)}
	x_step = 6 if GRAPH_ENTRIES == 5 else 3
	x_to_index = {(6 + (i + 1) * (6 if GRAPH_ENTRIES == 5 else 3)): str(i + 1) for i in range(GRAPH_ENTRIES)}

	def __init__(self, stdscr, styles):
		self.height = GRAPH_BLOCK_HEIGHT
		self.width = GRAPH_BLOCK_WIDTH
		self.pos_y = TEXT_BLOCK_HEIGHT + 2
		self.pos_x = HISTORY_BLOCK_WIDTH

		super(GraphBlock, self).__init__(self.height, self.width, self.pos_y, self.pos_x)

		self.stdscr, self.styles = stdscr, styles

	def init_ui(self):
		graph_banner = ' Graph' + ' ' * (GRAPH_BLOCK_WIDTH - 6)
		self.stdscr.addstr(TEXT_BLOCK_HEIGHT + 1, HISTORY_BLOCK_WIDTH, graph_banner, curses.A_BOLD | self.styles.title)

		# Score axis
		for k, v in self.y_to_score.items():
			self.window.addstr(k, 1, v, curses.A_BOLD)

		for i in range(1, 10):
			if i % 2 == 0:
				self.window.addstr(i, 5, ' |', curses.A_BOLD)
			else:
				self.window.addstr(i, 5, '_|', curses.A_BOLD)

		# History axis
		for k, v in self.x_to_index.items():
			self.window.addstr(10, k, v, curses.A_BOLD)

		for i in range(7, 38):
			self.window.addstr(9, i, '_', curses.A_BOLD)	

		self.draw_history()

	def draw_history(self):
		histories = load_history(GRAPH_ENTRIES)
		scores = [' '.join(h.split()).split()[2] for h in histories]
		for i, s in enumerate(scores):
			self.window.addstr(convert_score_to_y(s), 6 + (i + 1) * self.x_step, '*', curses.A_BOLD)

	def update(self):
		self.window.clear()
		self.init_ui()
		self.draw_history()


class SettingsBlock(Block):

	settings_and_options = {
		'Difficuly': ['Beginner', 'Intermediate', 'Advanced'],
		'Content': ['Novels'],
		'Auto Continue': ['ON', 'OFF'],
		'Overwrite Histories': ['ON', 'OFF'],
		'Graph Entries': ['5', '10'],
	}

	def __init__(self, stdscr, styles):
		self.height = TEXT_BLOCK_HEIGHT
		self.width = curses.COLS
		self.pos_y = 1
		self.pos_x = 0

		super(SettingsBlock, self).__init__(self.height, self.width, self.pos_y, self.pos_x)
		
		self.stdscr, self.styles = stdscr, styles
		self.window.nodelay(True)
		self.cursor_y, self.cursor_x = 0, 0	

		self.current_settings = load_config(len(self.settings_and_options))
		self.selected_setting_index = 0
		self.selected_option_index = self.current_settings[self.selected_setting_index]
		self.selected_setting = list(self.settings_and_options.keys())[self.selected_setting_index]
		self.selected_option = self.settings_and_options[self.selected_setting][self.selected_option_index]

	def init_ui(self):
		settings_banner = ' Settings' + ' ' * (curses.COLS - 59) + 'Press TAB to save changes and return to task mode '
		self.stdscr.addstr(0, 0, settings_banner, curses.A_BOLD | self.styles.title)
		self.current_settings = load_config(len(self.settings_and_options))
		self.selected_setting_index = 0
		self.selected_option_index = self.current_settings[self.selected_setting_index]
		self.selected_setting = list(self.settings_and_options.keys())[self.selected_setting_index]
		self.selected_option = self.settings_and_options[self.selected_setting][self.selected_option_index]
		self.update()

	def update(self):
		self.window.clear()
		for i, k in enumerate(self.settings_and_options):
			setting_style = curses.A_STANDOUT if i == self.selected_setting_index else curses.A_NORMAL
			self.window.addstr(2*i, 2, k, setting_style)
			
			for j, opt in enumerate(self.settings_and_options[k]):
				selected_option_style = curses.A_STANDOUT if i == self.selected_setting_index and j == self.selected_option_index else curses.A_NORMAL
				current_option_style = self.styles.selected_option if j == self.current_settings[i] else curses.A_NORMAL
				self.window.addstr(2*i, 25 + j * 15, opt, selected_option_style | current_option_style)		

	def next_setting(self, d = 1):
		self.selected_setting_index += d
		if self.selected_setting_index > len(self.settings_and_options) - 1:
			self.selected_setting_index = 0
		elif self.selected_setting_index < 0:
			self.selected_setting_index = len(self.settings_and_options) - 1
		self.selected_setting = list(self.settings_and_options.keys())[self.selected_setting_index]
		self.selected_option_index = self.current_settings[self.selected_setting_index]

	def next_option(self, d = 1):
		self.selected_option_index += d
		if self.selected_option_index > len(self.settings_and_options[self.selected_setting]) - 1:
			self.selected_option_index = 0
		elif self.selected_option_index < 0:
			self.selected_option_index = len(self.settings_and_options[self.selected_setting]) - 1
		self.selected_option = self.settings_and_options[self.selected_setting][self.selected_option_index]
		self.current_settings[self.selected_setting_index] = self.selected_option_index

	def save_changes(self):
		save_config(''.join(str(opt) for opt in self.current_settings))


#######################
#					  #
#   Helper Functions  #
#					  #
#######################

def init_ui(stdscr, styles):
	task_block = TaskBlock(stdscr, styles)
	score_block = ScoreBlock(stdscr, styles)
	result_block = ResultBlock(stdscr, styles)
	history_block = HistoryBlock(stdscr, styles)
	graph_block = GraphBlock(stdscr, styles)
	settings_block = SettingsBlock(stdscr, styles)

	task_block.init_ui()
	score_block.init_ui()
	result_block.init_ui()
	history_block.init_ui()
	graph_block.init_ui()

	return task_block, score_block, result_block, history_block, graph_block, settings_block


#######################
#					  #
#     Drawing UI      #
#					  #
#######################

def draw(stdscr):
	stdscr.clear()
	
	# Set cursor to invisible
	curses.curs_set(0)
	stdscr.nodelay(True)

	# Initialize all blocks
	task_block, score_block, result_block, history_block, graph_block, settings_block = init_ui(stdscr, Styles())

	# Refresh all windows after initialization
	stdscr.refresh()
	task_block.window.refresh()
	score_block.window.refresh()
	result_block.window.refresh()
	history_block.window.refresh()
	graph_block.window.refresh()

	# Main loop
	game_over = False
	settings_mode = False

	while True:
		# Get user input
		try:
			key = stdscr.getch()
		except:
			key = -1

		# Update score block
		if not settings_mode:
			score_block.update()

		# Handle game over
		if game_over:
			# Save history before updating result
			save_history(result_block.stage, score_block.score, result_block.tries)
			result_block.update(score_block.score)
			save_result(result_block.stage, result_block.stage_to_score[result_block.stage], result_block.record, result_block.tries)
			history_block.update()
			graph_block.update()
			task_block.update()
			task_block.reset_cursor()
			score_block.reset()
			game_over = False

			# Refresh windows
			result_block.window.refresh()
			history_block.window.refresh()
			graph_block.window.refresh()

			if AUTO_CONTINUE:
				continue
			else:
				break

		# Refresh windows
		if not settings_mode:
			score_block.window.refresh()
			task_block.window.refresh()
		else:
			settings_block.update()
			settings_block.window.refresh()

		# Handle user key inputs
		if key == curses.KEY_RESIZE:
			""" TODO: Resize all UIs """
			pass

		# Exit whenever ESC is pressed
		elif key == 27:
			break

		# Enter setting mode when TAB is pressed
		elif key == 9:
			settings_mode = not settings_mode
			if settings_mode:
				score_block.pause()
				settings_block.init_ui()
				settings_block.window.refresh()
			else:
				settings_block.save_changes()
				task_block.restore_state()
				score_block.restore_state()

		# In settings mode
		elif settings_mode:
			if key == curses.KEY_UP:
				settings_block.next_setting(-1)

			elif key == curses.KEY_DOWN:
				settings_block.next_setting(1)

			elif key == curses.KEY_LEFT:
				settings_block.next_option(-1)

			elif key == curses.KEY_RIGHT:
				settings_block.next_option(1)

		# In task mode
		elif not settings_mode:
			if key == curses.KEY_UP:
				continue

			elif key == curses.KEY_DOWN:
				continue

			elif key == ord(task_block.target_text[0]):
				score_block.correct_count += 1
				game_over = task_block.handle_correct_input()
				if game_over:
					continue

			elif key != -1 and key != ord(task_block.target_text[0]):
				score_block.error_count += 1
				task_block.handle_incorrect_input(key)

		stdscr.refresh()
		curses.napms(10)


def main():
	set_esc_delay()
	curses.wrapper(draw)


if __name__ == '__main__':
	main()