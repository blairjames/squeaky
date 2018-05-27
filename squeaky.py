#!/usr/bin/env python3

#Squeaky takes any wordlist and cleans out dodgey characters and short words.

import time
import multiprocessing
from typing import Generator, List

#TODO: Point at dir and let her rip, clean duplicates
# Set your paths and min word length here:
original_file = "/root/SecLists/Passwords/darkweb2017-top10000.txt"
new_file = "/root/SecLists/Passwords/consolidated.txt"
min_word_length = 6

class Squeaky:

    def __init__(self):
        self.dir_to_enum = "/root/SecLists/Passwords/"
        self.new_file = "/root/SecLists/Passwords/consolidated.txt"
        self.min_word_length = 6

    def get_file_length(self, file: str) -> int:
        wrds = self.read_file(file)
        length = sum(1 for w in wrds)
        print(str(length))
        return length

    def read_file(self, path_to_file: str) -> List:
        t1 = time.perf_counter()
        with open(path_to_file, "rb") as file:
            file_list = list([line] for line in file.readlines())
        t2 = time.perf_counter()
        print(str(t2 - t1))
        return file_list

    def write_new_file(self, word: str):
        t1 = time.perf_counter()
        with open(new_file, "a") as file:
            file.write(word)
        t2 = time.perf_counter()
        print(str(t2 - t1))

    def go(self, word):
        for x in word:
            try:
                z = str(x.decode("utf-8"))
                if not (len(z) < (min_word_length + 1)):
                    self.write_new_file(z)
                else:
                    continue
            except UnicodeDecodeError as a:
                continue

def main():

    t1 = time.perf_counter()
    new_squeaky = Squeaky()

    words = new_squeaky.read_file(original_file)
    with multiprocessing.Pool(processes=32) as pool:
        pool.map(new_squeaky.go, words)

    ridgy = new_squeaky.get_file_length(original_file)

    print("Number of words in input file: " + str(ridgy))

    t2 = time.perf_counter()
    print("\nTotal processing time: " + str(t2 - t1) + " sec")


if __name__ == '__main__':
    main()
