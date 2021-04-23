"""
File: boggle.py
Name: Jo
----------------------------------------
This program create a Boggle Game recursively finds all the words
from the 4*4 boggle board that user input letters for each row
"""

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'
dictionary = [set()for i in range(26)]
word_list = []
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def main():
    """
    Make a boggle board game in 4*4 letters, and automatically find the words in the board.
    """
    read_dictionary()
    # Create a boggle board
    boggle = []
    for i in range(4):
        letters = input(str(i + 1) + " row of letters: ")
        boggle_position = []
        for j in range(4):
            boggle_position += letters[(2 * j)]
        boggle.append(boggle_position)
        if len(letters) != 7:
            print("Illegal input")
            break
    # Give each letter a position. For example: f = (0,0)
    for i in range(4):
        for j in range(4):
            word = boggle[i][j]
            boggle_position = [(i, j)]
            find_word(boggle, i, j, word, boggle_position)
            boggle_position.clear()
    print("There are " + str(len(word_list)) + " word(s) in total.")


def find_word(boggle, a, b, word, boggle_position):
    """
    :param boggle: lst, list of a given word list input by user
    :param a: int, each position of the row
    :param b: int each position of the column
    :param word: lst, the list with letters
    :param boggle_position: tuple, position of row and column
    """
    global word_list
    # # Base case, if the word is a four-letter word
    if len(word) >= 4:
        if has_prefix(word):
            # if four-letter word is in the dictionary
            if word in dictionary[ALPHABET.find(word[0])] and word not in word_list:
                print('Found: ', word)
                # add to word list
                word_list.append(word)
                # find longer word
                find_longer(boggle, a, b, word, boggle_position)
            else:
                # if the word is not in the dictionary, find longer word
                find_longer(boggle, a, b, word, boggle_position)
    else:
        for i in range(a-1, a+2):
            for j in range(b-1, b+2):
                if 4 > i >= 0 and 4 > j >= 0 and (i, j) not in boggle_position:
                    # Choose
                    word += boggle[i][j]
                    boggle_position.append((i, j))
                    # Explore
                    find_word(boggle, i, j, word, boggle_position)
                    # Un-choose
                    boggle_position.pop()
                    word = word[:-1]


def find_longer(boggle, a, b, word, boggle_position):
    """
    :param boggle: lst, list of a given word list input by user
    :param a: int, each position of the row
    :param b: int each position of the column
    :param word: lst, the list with letters
    :param boggle_position: tuple, position of row and column
    """
    # Base case
    if word not in word_list and word in dictionary[ALPHABET.find(word[0])]:
        print('Found: ', word)
        word_list.append(word)
    else:
        for i in range(a - 1, a + 2):
            for j in range(b - 1, b + 2):
                if 4 > i >= 0 and 4 > j >= 0 and (i, j) not in boggle_position:
                    # Choose
                    word += boggle[i][j]
                    boggle_position.append((i, j))
                    # Explore
                    find_word(boggle, i, j, word, boggle_position)
                    # Un-choose
                    boggle_position.pop()
                    word = word[:-1]


def read_dictionary():
    with open(FILE, 'r') as f:
        for line in f:
            # global dict_list
            if len(line.strip()) >= 4:
                dictionary[ALPHABET.find(line[0])].add(line.lower().strip())


def has_prefix(sub_s):
    """
    :param sub_s: list
    :return: bool, if the word is prefix, return True
    """
    for item in dictionary[ALPHABET.find(sub_s[0])]:
        if item.startswith("".join(sub_s)):
            return True


if __name__ == '__main__':
    main()
