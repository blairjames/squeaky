#!/usr/bin/env python3

#Squeaky takes any wordlist and cleans out dodgey characters and short words#

import time
import multiprocessing
from typing import Generator


# Set your paths and min word length here:
original_file = "/root/SecLists/Passwords/"
new_file = "/root/SecLists/Passwords/consolidated.txt"
min_word_length = 6


def get_file_length(file: str) -> int:
    i :int = 0
    wrds = read_file_comprehen(file)
    for w in wrds:
        i += 1
    return i


def read_file_comprehen(path_to_file: str) -> Generator:
    with open(path_to_file, "rb") as file:
        file_list = ([line] for line in file.readlines())
    return file_list


def write_new_file(word: str):
    with open(new_file, "a") as file:
        file.write(word)


def go(word):

    for x in word:
        try:
            z = str(x.decode("utf-8"))
            if not (len(z) < (min_word_length + 1)):
                write_new_file(z)
            else:
                continue
        except UnicodeDecodeError as a:
            continue


def main():

    t1 = time.perf_counter()
    words = read_file_comprehen(original_file)
    with multiprocessing.Pool(processes=32) as pool:
        pool.map(go, words)

    ridgy = get_file_length(original_file)
    newy = get_file_length(new_file)
    diff = (ridgy - newy)

    print("Number of words in original file: " + str(ridgy))
    print("Number of words in new file: " + str(newy))
    print("Words Removed: " + str(diff))
    t2 = time.perf_counter()
    print("\nTotal processing time: " + str(t2 - t1) + " sec")


if __name__ == '__main__':
    main()
