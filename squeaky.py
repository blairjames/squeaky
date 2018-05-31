#!/usr/bin/env python3

#Squeaky takes any wordlist and cleans out dodgey characters, short words and duplicates.
import argparse
import os
import time
import multiprocessing
from typing import Generator


class Squeaky:

    def __init__(self):
        '''
        Instance Variables
        '''
        try:
            self.clean: set = set()
            self.input_files: str = ""
            self.output_file: str = ""
            self.min_word_length: int = 1
            self.procs: int = 1
            self.dir_flag: bool = False
            self.dedup_flag: bool = False
        except Exception as e:
            print("Error! in init: " + str(e))

    def get_file_length(self, file: str) -> int:
        try:
            wrds = self.read_file(file)
            length = sum(1 for w in wrds)
            return length
        except Exception as e:
            print("Error! in get_file_length: " + str(e))

    def read_file(self, path_to_file: str) -> Generator:
        try:
            with open(path_to_file, "rb") as file:
                file_list = ([line] for line in file.readlines())
            return file_list
        except Exception as e:
            print("Error! in read_file: " + str(e))

    def clear_output_file(self, word: str) -> bool:
        try:
            with open(self.output_file, "w") as file:
                file.write("")
                file.close()
            return True
        except Exception as e:
            print("Error! in write_to_output: " + str(e))

    def process_word(self, words) -> Generator:
        try:
            min_len = self.min_word_length + 1
            for line in words:
                try:
                    #w is an array, get elements out
                    decoded_words = (w.decode("utf-8") for w in words)
                    filtered = (dw for dw in decoded_words if len(dw) > min_len)
                    dedup = set(filtered)
                    unique = (d for d in dedup)
                    return unique
                except UnicodeDecodeError:
                    continue
        except Exception as e:
            print("Error! in process_word: " + str(e))

    def parse_arguments(self):
        try:
            new_args = argparse.ArgumentParser()
            new_args.add_argument("input_file")
            new_args.add_argument("output_file")
            new_args.add_argument("-d", "--dir",
                                  help="Input a directory of wordlists instead of single file.",
                                   action="store_true", default=False)

            new_args.add_argument("-l", "--len", type=int,
                                  help="Minimum word length, words shorter than "
                                  "specified length will be cleansed.", default=1)

            new_args.add_argument("-z", "--procs",
                                  help="Number of processes to supercharge processing.",
                                  type=int,
                                  default=multiprocessing.cpu_count() * 4)

            new_args.add_argument("-dd", "--dedup",
                                  help="delete duplicate words in word list",
                                  action="store_true", default=False)
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
        try:
            print("                                      ___          ")
            print("  _____________ ____  ____________ ___  /______  __")
            print("  __  ___/  __ `/  / / /  _ \  __ `/_  //_/_  / / /")
            print("  _(__  )/ /_/ // /_/ //  __/ /_/ /_  ,<  _  /_/ / ")
            print("  /____/ \__, / \__,_/ \___/\__,_/ /_/|_| _\__, /  ")
            print("           /_/                            /____/   \n\n")
            print("     Lean, Mean, List Cleaning Machine\n\n")
        except Exception as e:
            print("Error! in bruce: " + str(e))

    def set_instance_vars(self, args: argparse) -> bool:
        try:
            self.dedup_flag: bool = args.dedup
            self.dir_flag: bool = args.dir
            self.min_word_length: int = args.len
            self.procs: int = args.procs
            self.input_files: str = args.input_file
            self.output_file: str = args.output_file
            return True
        except Exception as e:
            print("Error! in set_instance_vars: " + str(e))

    def map_dedup(self):
        try:
            with open(self.output_file, "r") as filea:
                leng = sum(1 for x in filea.readlines())
                filea.close()
            raw_count = int(leng)
            with open(self.output_file, "r") as file:
                raw = (word for word in file.readlines())
            self.clear_output_file("")# clear file
            t1 = time.perf_counter()
            second = set(raw)
            t2 = time.perf_counter()
            second_count = int(len(list(r for r in second)))
            dupes_removed = raw_count - second_count

            print("Duplicates removed: " + str(dupes_removed))
            print("Time to remove duplicates: " + str(t2 - t1))

            wds = (w for w in second)
            self.bulk_write(wds)
        except Exception as e:
            print("Error! in map_dedup: " + str(e))

    def bulk_write(self, clean: Generator):
        try:
            with open(self.output_file, "a") as bulk_file:
                bulk_file.writelines(clean)
        except Exception as e:
            print("Error! in bulk_write: " + str(e))

    def go(self):
        try:
            print("Ready..")
            time.sleep(.5)
            print("Set..")
            time.sleep(.5)
            print("\nGO!!\n")
            time.sleep(.2)
        except Exception as e:
            print("Error!! in go: " + str(e))

    def builder(self):
        try:
            new_squeaky = Squeaky()
            new_squeaky.clear_screen()
            new_squeaky.bruce()
            new_squeaky.go()
            arguments = new_squeaky.parse_arguments()
            new_squeaky.set_instance_vars(arguments)
            return new_squeaky
        except Exception as e:
            print("Error!! in builder: " + str(e))


def main():
    try:
        t1 = time.perf_counter()
        new_squeaky = Squeaky().builder()
        wrdlen = new_squeaky.read_file(new_squeaky.input_files)
        wl = sum(1 for w in wrdlen)
        print("Length of initial wordlist: " + str(wl))
        words = new_squeaky.read_file(new_squeaky.input_files)
        clean_len = new_squeaky.process_word(words)
        print("Length after cleaning: " + str(sum(1 for c in clean_len)))
        clean = new_squeaky.process_word(words)

        new_squeaky.bulk_write(clean)

        if new_squeaky.dedup_flag:
            print("Removing Duplicate Entries from list.")
            new_squeaky.map_dedup()

        t2 = time.perf_counter()
        print("\nComplete! check output file: " + str(new_squeaky.output_file))
        print("Total processing time: " + str(t2 - t1) + " sec\n")

    # TODO: Point at dir, clean duplicates, cli output while processing.

    except Exception as e:
        print("Error! in squeaky.main: " + str(e))

if __name__ == '__main__':
    main()
