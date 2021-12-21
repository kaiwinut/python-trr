from .utils import load_config

#########################
#					    #
#     User Interface    #
# 						#
#########################

TEXT_BLOCK_HEIGHT = 10

SCORE_BLOCK_HEIGHT = 6
SCORE_BLOCK_WIDTH = 20
SCORE_UPDATE_TIME_STEP = 0.2

HISTORY_BLOCK_HEIGHT = 4
HISTORY_BLOCK_WIDTH = 40

GRAPH_BLOCK_HEIGHT = 12
GRAPH_BLOCK_WIDTH = 40

assert TEXT_BLOCK_HEIGHT + SCORE_BLOCK_HEIGHT + HISTORY_BLOCK_HEIGHT + 3 <= 24
assert 2 * SCORE_BLOCK_WIDTH + GRAPH_BLOCK_WIDTH <= 80
assert HISTORY_BLOCK_WIDTH + GRAPH_BLOCK_WIDTH <= 80
assert SCORE_UPDATE_TIME_STEP <= 1

#########################
#					    #
#        Records        #
# 						#
#########################

# If set to True, then the program will look for the stored history in your local files. 
# If there is not one, it will be created. If set to False, it erases all existing histories
# stored in the file and overwrites them.
READ_RESULT_FROM_HISTORY = False
READ_HISTORY = False

# Specifies how many entries will be shown in the History block. The maximum is 3.
HISTORY_ENTRIES = 3

# Specifies how many entries will be shown in the Graph block. The value must be 5 or 10.
GRAPH_ENTRIES = 10

assert HISTORY_ENTRIES <= 3
assert GRAPH_ENTRIES == 5 or GRAPH_ENTRIES == 10

#########################
#						#
#     Game Settings     #
# 						#
#########################

AUTO_CONTINUE = True


#########################
#						#
#   Difficuly Setting   #
# 						#
#########################

# Specifies how many words ( or in fact keystrokes ) will be shown in the Text block. The maximum is 350.
WORD_COUNT = 20

assert WORD_COUNT <= 350


def update_config():
	global WORD_COUNT, AUTO_CONTINUE, READ_RESULT_FROM_HISTORY, READ_HISTORY, GRAPH_ENTRIES
	new_config = load_config(5)
	# 
	if new_config[0] == 0:
		WORD_COUNT = 100
	elif new_config[0] == 1:
		WORD_COUNT = 200
	else:
		WORD_COUNT = 350

	# 
	AUTO_CONTINUE = False if new_config[2] == 1 else True

	# 
	READ_RESULT_FROM_HISTORY = True if new_config[3] == 1 else False
	READ_HISTORY = True if new_config[3] == 1 else False

	# 
	GRAPH_ENTRIES = 5 if new_config[4] == 0 else 10

update_config()	