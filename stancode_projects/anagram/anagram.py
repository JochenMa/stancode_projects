"""
File: anagram.py
Name:
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time

# Constants
FILE = 'dictionary.txt'  # This is the filename of an English dictionary
EXIT = '-1'  # Controls when to stop the loop
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

# Global Variable
# dict_list = []
dictionary = [set()for i in range(26)]


def main():
    print('Welcome to stanCode "Anagram Generator" (or -1 to quit)')
    while True:
        start = time.time()
        read_dictionary()
        anagrams = input('Find anagrams for: ')
        if anagrams == EXIT:
            break
        else:
            s = []
            for item in s:
                s.append(item)
            find_anagrams(anagrams)
            end = time.time()
            print(end - start)


def read_dictionary():
    with open(FILE, 'r') as f:
        for line in f:
            # global dict_list
            dictionary[ALPHABET.find(line[0])].add(line.lower().strip())


def find_anagrams(s):
    """
    :param s: list, the word import by user
    :return: str: the number of total anagrams and the word list
    """
    word_lst = []
    helper(s, [], word_lst)
    print(str(len(word_lst)) + " anagrams: " + str(word_lst))


def helper(lst, word, word_lst):
    """
    :param lst: list, the word import by user
    :param word: list, put the index of anagram
    :param word_lst: list, put the anagrams that is found in dictionary
    """
    # Base case
    if len(lst) == len(word):
        word_str = ""
        for order in word:
            word_str += lst[int(order)]
        # if has_prefix(word_str):
            if len(word_str) == len(lst):
                if word_str in dictionary[ALPHABET.find(word_str[0])] and word_str not in word_lst:
                    word_lst.append(word_str)
                    print("Searching...")
                    print("Found: " + word_str)
    else:
        for i in range(len(lst)):
            if i not in word:
                # Choose
                word.append(i)
                # Explore
                # if has_prefix(word):
                helper(lst, word, word_lst)
                # Un-choose
                word.pop()


# def has_prefix(sub_s):
#     """
#     :param sub_s: list
#     :return: bool, if the word is prefix, return True
#     """
#     for item in dict_list:
#         if item.startswith("".join(sub_s)):
#             return True


if __name__ == '__main__':
    main()
