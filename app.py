from tkinter.messagebox import showinfo
import pandas as pd
import wordle
from flask import Flask, request
import copy

from wordle import Wordle

GAME_BOARD =  [
    ["-","-","-","-","-"],
    ["-","-","-","-","-"],
    ["-","-","-","-","-"],
    ["-","-","-","-","-"],
    ["-","-","-","-","-"],
    ["-","-","-","-","-"]
]
app = Flask(__name__)
df = pd.DataFrame(wordle.GAME_BOARD2)
blank_board = pd.DataFrame(GAME_BOARD)
pd.set_option('display.max_colwidth', 40)
moves = 0
wordle_obj = wordle.Wordle()
wordle = wordle_obj.wordle
last_word = ""

def color_positive_green(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: green'` for positive
    strings, black otherwise.
    """
    if val == '-':
        color = 'green'
    else:
        color = 'black'
    return 'color: %s' % color

def color_board(s, word):
    color = []
    is_max = pd.Series(s.to_dict())
    for i in range(len(wordle)):
        if is_max[i] == wordle[i]:
            color.append('color: green')
        elif is_max[i] in list(wordle):
            color.append('color: #999900')
        else:
            color.append("color: red")
        
    return color

def reset():
    global df, wordle, moves, last_word        
    wordle = wordle_obj.redraw_word()
    df = copy.deepcopy(blank_board)
    moves = 0
    last_word = ""

@app.route('/')
def home():
    with open('index.html') as f:
        html = f.read()
    return html

@app.route('/wordle.html')
def show_wordle_home():
    home_df = df
    style = home_df.style.apply(color_board, word=wordle, axis=1)
    html = """
        <form method="POST">
          <label for="word_input">Enter a 5 letter word:</label>
          <input type="text", id="word_input", name="word_input">
          <input type="submit" value="Submit">
        </form>
    """
    return style.render() + html

@app.route('/wordle.html', methods=["POST"])
def update_board():
    global wordle
    global wordle_obj
    global df
    global moves
    global last_word
    if moves > 4:
        cur_wordle = wordle
        reset()
        return_home = """
            <a href="/">return home</a>
        """
        return "game over... wordle: " + cur_wordle + return_home
    html = """
        <form method="POST">
          <label for="word_input">Enter a 5 letter word:</label>
          <input type="text", id="word_input", name="word_input">
          <input type="submit" value="Submit">
        </form>
    """
    word = request.form['word_input']
    if len(word) != 5:
        return show_wordle_home()
    if word == last_word:
        return show_wordle_home()
    last_word = word
    if word == wordle:
        cur_wordle = wordle
        reset()
        return_home = """
            <a href="/">return home</a>
        """
        return f"YOU WIN! wordle: {cur_wordle} " + return_home
    
    # redraw game board
    word_list = pd.DataFrame([list(word)])
    df.iloc[moves] = word_list
    moves +=1
    style = df.style.apply(color_board, word=wordle, axis=1)

    return style.render() + html


if __name__ == '__main__':
    app.run(host="0.0.0.0")