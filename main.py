from wordle import Wordle
import pandas as pd

def color_positive_green(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: green'` for positive
    strings, black otherwise.
    """
    if val > 0:
        color = 'green'
    else:
        color = 'black'
    return 'color: %s' % color

def main() -> None:
    # w = Wordle()
    # w.draw_game()

    df = pd.DataFrame([[1,-2,2],[3,-4,8]])
    df.style.applymap(color_positive_green)
    print(df)
    

if __name__ == '__main__':
    main()