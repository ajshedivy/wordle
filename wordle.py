
import pandas as pd
import random

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

GAME_BOARD =  [
    [f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}"],
    [f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}"],
    [f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}"],
    [f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}"],
    [f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}"],
    [f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}",f"{bcolors.OKBLUE}-{bcolors.ENDC}"]
]

WORDS_FILE = 'words.txt'

class Wordle(object):

    def __init__(self) -> None:
        self.game_board         = GAME_BOARD
        self.move               = 0
        self.words              = self._import_words()
        self.wordle_query       = self._define_random_wordle()
        self.wordle             = self.wordle_query[0]
        self.wordle_id          = self.wordle_query[1]
        self.used_letters       = set()

        self.wordle_hash        = {
            i: self.wordle[i] for i in range(0, len(self.wordle))
        }

    def _import_words(self) -> dict:
        words = []
        with open(WORDS_FILE, 'r') as f:
            words = f.readlines()

        return {words[i].rstrip(): i for i in range(0, len(words))}

    def _define_random_wordle(self) -> str:
        return random.choice(list(self.words.items()))
        

    def print_game_board(self):
        df = pd.DataFrame(self.game_board)
        df.columns = [f"{bcolors.OKBLUE}1{bcolors.ENDC}",f"{bcolors.OKBLUE}2{bcolors.ENDC}",f"{bcolors.OKBLUE}3{bcolors.ENDC}",f"{bcolors.OKBLUE}4{bcolors.ENDC}",f"{bcolors.OKBLUE}5{bcolors.ENDC}"]
        print(df)
    
    def _check_wordle(self, guess):
        list_guess = {i: guess[i] for i in range(0, len(guess))}

        check = []
        self.stats              =  {
            'contains': set(),
            'not_in'  : set(), 
            'idx'     : {}
        }
        for i in range(0, 5):
            cur_guess = list_guess[i]
            if cur_guess == self.wordle_hash[i]:
                check.append(bcolors.OKGREEN + self.wordle_hash[i] + bcolors.ENDC)
                self.stats['idx'][i] = cur_guess
                self.stats['contains'].add(cur_guess)
            elif cur_guess in self.wordle_hash.values():
                check.append(bcolors.WARNING + cur_guess + bcolors.ENDC)
                self.stats['contains'].add(cur_guess)
            else:
                self.used_letters.add(cur_guess)
                check.append(bcolors.FAIL + cur_guess + bcolors.ENDC)
        return check

    def wordle_overlap(self):
        """
        determine how many possible words are left

        *work in progress*

        """
        possible_words = set()
        for word in self.words:
            if not any(char in self.used_letters for char in word) \
                and any(char in self.stats['contains'] for char in word) \
                and all(self.stats['idx'][i] == word[i] for i in self.stats['idx'].keys()):
                possible_words.add(word)

        print(f'number of possible words: {len(possible_words)}')

    def draw_game(self):
        while self.move < 6:
            self.print_game_board()
            guess = input("enter 5 letter word: ")
            if list(guess) == list(self.wordle):
                check_guess = self._check_wordle(guess)
                self.game_board[self.move] = check_guess
                self.print_game_board()
                print('you win')
                return
            check_guess = self._check_wordle(guess)
            self.wordle_overlap()
            self.game_board[self.move] = check_guess
            self.move+=1

        self.print_game_board()
        print(f'the wordle was: {self.wordle}')
        print(f"wordle id: {self.wordle_id}")






