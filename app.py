from tkinter.messagebox import showinfo
import pandas as pd
import wordle
from flask import Flask, request

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
wordle = wordle.Wordle()
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
    for i in range(len(wordle.wordle)):
        if is_max[i] == wordle.wordle[i]:
            color.append('color: green')
        elif is_max[i] in list(wordle.wordle):
            color.append('color: #999900')
        else:
            color.append("color: red")
        
    return color

@app.route('/')
def home():
    with open('index.html') as f:
        html = f.read()
    return html

@app.route('/wordle.html')
def show_wordle_home():
    home_df = df
    style = home_df.style.apply(color_board, word=wordle.wordle, axis=1)
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
    global df
    global moves
    global last_word
    if moves > 4:
        df = blank_board
        moves = 0
        last_word = ""
        return_home = """
            <a href="/">return home</a>
        """
        return "game over... wordle: " + wordle.wordle + return_home
    html = """
        <form method="POST">
          <label for="word_input">Enter a 5 letter word:</label>
          <input type="text", id="word_input", name="word_input">
          <input type="submit" value="Submit">
        </form>
    """
    word = request.form['word_input']
    if word == last_word:
        return show_wordle_home()
    last_word = word
    if word == wordle.wordle:
        df = blank_board
        moves = 0
        last_word = ""
        return "YOU WIN"
    word_list = pd.DataFrame([list(word)])
    df.iloc[moves] = word_list
    moves +=1
    style = df.style.apply(color_board, word=wordle.wordle, axis=1)

    return style.render() + html


if __name__ == '__main__':
    app.run(host="0.0.0.0")