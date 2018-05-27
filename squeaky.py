#!/usr/bin/env python3

#Squeaky takes any wordlist and cleans out dodgey characters, short words and duplicates.
import argparse
import os
import time
import multiprocessing
from typing import Generator
#TODO: Point at dir and let her rip, clean duplicates, do gen vs list


class Squeaky:

    def __init__(self):
        '''
        Set your paths and min word length here:
        '''
        self.input_files = "/root/SecLists/Passwords/bt4-password.txt"
        self.output_file = "/root/SecLists/Passwords/consolidated.txt"
        self.min_word_length = 6
        self.procs: int = (multiprocessing.cpu_count() * 4)

    def get_file_length(self, file: str) -> int:
        t1 = time.perf_counter()
        wrds = self.read_file(file)
        length = sum(1 for w in wrds)
        t2 = time.perf_counter()
        print("get_file_length: " + str(t2 - t1))
        return length

    def read_file(self, path_to_file: str) -> Generator:
        t1 = time.perf_counter()
        with open(path_to_file, "rb") as file:
            file_list = ([line] for line in file.readlines())
        t2 = time.perf_counter()
        print("File read time: " + str(t2 - t1))
        return file_list

    def write_to_output(self, word: str) -> bool:
        with open(self.output_file, "a") as file:
            file.write(word)
            file.close()
        return True

    def process_word(self, word) -> bool:
        for x in word:
            try:
                z = str(x.decode("utf-8"))
                if not (len(z) < (self.min_word_length + 1)):
                    self.write_to_output(z)
                else:
                    continue
            except UnicodeDecodeError:
                continue
        return True

    def parse_arguments(self) -> argparse.ArgumentParser:
        try:
            new_args = argparse.ArgumentParser()
            new_args.add_argument("Input file")
            new_args.add_argument("output file")
            new_args.add_argument("-d", "--dir", help="Input a directory of wordlists instead of single file.")
            new_args.add_argument("-l", "--len", help="Minimum word length, words shorter than "
                                                      "specified length will be cleansed.")
            new_args.add_argument("-z", "--procs", help="Number of processes to supercharge processing.")
            parsed_args = new_args.parse_args()
            return parsed_args
        except Exception as e:
            print("Error!! in parse_arguments: " + str(e))

    def clear_screen(self) -> bool:
        try:
            os.system("clear")
            return True
        except Exception as e:
            print("Error! in clearscreen: " + str(e))

    def bruce(self):
        print("                                      ___          ")
        print("  _____________ ____  ____________ ___  /______  __")
        print("  __  ___/  __ `/  / / /  _ \  __ `/_  //_/_  / / /")
        print("  _(__  )/ /_/ // /_/ //  __/ /_/ /_  ,<  _  /_/ / ")
        print("  /____/ \__, / \__,_/ \___/\__,_/ /_/|_| _\__, /  ")
        print("           /_/                            /____/   \n\n")
        print("     Lean, Mean, Word List Cleaning Machine\n\n")

def main():
    t1 = time.perf_counter()
    new_squeaky = Squeaky()
    new_squeaky.clear_screen()
    new_squeaky.bruce()
    new_squeaky.parse_arguments()
    words = new_squeaky.read_file(new_squeaky.input_files)
    with multiprocessing.Pool(processes = new_squeaky.procs) as pool:
        pool.map(new_squeaky.process_word, words)
    t2 = time.perf_counter()
    print("\nTotal processing time: " + str(t2 - t1) + " sec")

if __name__ == '__main__':
    main()
