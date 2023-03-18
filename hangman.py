# Write your code here
from random import choice

def play_game():
    alphabet = ['a', 'b', 'c', 'd', 'e',
                'f', 'g', 'h', 'i', 'j',
                'k', 'l', 'm', 'n', 'o',
                'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y',
                'z']
    word = choice(['python', 'java', 'swift', 'javascript'])
    guess = ('- ' * len(word)).split(' ')  # Turn into an array so we can modify
    guesses = 0
    guessed_letters = []

    while True:
        print("\n" + "".join(guess))

        _ = input('Input a letter: ')

        if len(_) != 1:
            print("Please, input a single letter...")
            continue
        elif _ not in alphabet:
            print("Please, enter a lowercase letter from the English alphabet.")
            continue
        elif _ in guessed_letters:
            print("You've already guessed this letter.")
            continue

        guessed_letters += _

        if "".join(guess).find(_) < 0:
            found = False

            for i in range(len(word)):
                if _ == word[i]:
                    found = True
                    guess[i] = _

            if not found:
                print("That letter doesn't appear in the word.")
                guesses += 1
        else:
            print("You've already guessed this letter.")
            guesses += 1

        if "".join(guess) == word:
            print(f"You guessed the word {word}!")
            return True
        if guesses >= 8:
            return False


if __name__ == '__main__':
    print("H A N G M A N")

    player_win, player_loss = 0, 0
    playing = True

    while playing:
        _ = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit: ').lower()

        if _ == 'play':
            if play_game():
                print("You survived!")
                player_win += 1
            else:
                print("You lost!")
                player_loss += 1
        elif _ == 'results':
            print(f"You won: {player_win} times.")
            print(f"You lost: {player_loss} times.")
        elif _ == 'exit':
            playing = False
