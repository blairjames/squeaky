#!/usr/bin/env python3


import argparse
import time
import squeaky_utils
import os
from typing import List


class Squeaky:
    """
    Squeaky takes any wordlists and cleans out problematic characters.
    Can merge them, remove words below a certain length, and remove duplicates.
    """

    def __init__(self):
        """
        Instance variables created upon object construction.
        """
        try:
            self.input_file: str = ""
            self.output_file: str = ""
            self.min_word_length: int = 0
            self.starting_wordcount: int = 0
            self.finished_wordcount: int = 0
            self.dir_flag: bool = False
            self.unique_flag: bool = False
            self.utils = squeaky_utils.SqueakyUtils()
        except Exception as e:
            print("Error! in init: " + str(e))

    def get_words_from_file(self, path_to_file: str, open_as_bytes: bool) -> tuple:
        """'
        Open input wordlist, read into a list to be used in the application.
        """
        try:
            if open_as_bytes:
                settings: str = "rb"
            else:
                settings: str = "r"
            t1: float = time.perf_counter()
            self.utils.check_file_exists(path_to_file)
            with open(path_to_file, settings) as file:
                word_list: list = [line for line in file.readlines()]
            t2: float = time.perf_counter()
            perf_time_str: str = str(round(t2 - t1, 5)) + " sec"
            return word_list, perf_time_str
        except Exception as e:
            print("Error! in get_words_from_file: " + str(e))

    def filter_by_length(self, wrds: list) -> list:
        """
        Parse out words below the length set with the "-l" switch.
        """
        try:
            tp = time.perf_counter
            t1: float = tp()
            word_lst: list = [w for w in wrds]
            before_words: int = sum([1 for x in word_lst])
            min_len: int = self.min_word_length
            filtered: list = [w for w in word_lst if len(w) > min_len]
            after_words: int = sum([1 for x in filtered])
            t2: float = tp()
            print("\n*** Filter by word length ***")
            print("Words before length filter: " + str(before_words))
            print("Words after length filter: " + str(after_words))
            print("Words removed by length filter: " + str(before_words - after_words))
            print("Filter by length: " + str(round(t2 - t1, 5)) + " sec")
            self.finished_wordcount = after_words
            return filtered
        except Exception as e:
            print("Error! in filter_by_length: " + str(e))

    def process_words(self, words: list) -> list:
        """
        Iterates input words as bytes to avoid Unicode exceptions.
        performs controlled decode of all words to utf-8, catches any exceptions and parses them out.
        """
        try:
            t1: float = time.perf_counter()
            starting_len: int = sum([1 for x in words])
            self.starting_wordcount = starting_len
            decoded_list = []
            apd = decoded_list.append
            print("Words before Unicode errors removed: " + str(starting_len))
            for word in words:
                try:
                    decoded = word.decode("utf-8")
                    apd(str(decoded).lstrip("\n").lstrip(" "))
                except UnicodeDecodeError:
                    pass
            finished_len: int = sum([1 for d in decoded_list])
            dif = starting_len - finished_len
            t2: float = time.perf_counter()
            print("Words after Unicode errors removed: " + str(finished_len))
            print("Words with errors removed: " + str(dif))
            print("Time to remove Unicode errors: " + str(round(t2 - t1, 5)) + " sec")
            self.finished_wordcount = finished_len
            return decoded_list
        except Exception as e:
            print("Error! in process_words: " + str(e))

    def de_duplicate(self, word_list: list) -> set:
        """
        Removes any duplicate entries using the "set()" function.
        """
        try:
            t1: float = time.perf_counter()
            start_words = sum([1 for i in word_list])
            print("Words before removal of duplicates: " + str(start_words))
            unique = set(word_list)
            after_words = sum([1 for i in unique])
            diff = int(start_words) - int(after_words)
            t2: float = time.perf_counter()
            print("Words after removal of duplicates: " + str(after_words))
            print("Time to remove duplicates: " + str(round(t2 - t1, 5)) + " sec")
            print("Duplicate words removed: " + str(diff))
            return unique
        except Exception as e:
            print("Error! in de_duplicate: " + str(e))

    def set_instance_vars(self, args: argparse):
        """
        Set Instance vars using user inputs.
        """
        try:
            if args.unique and args.dir:
                raise SystemExit(
                    "\nSorry! the -u and -d switches cannot be used together."
                    + "\nPlease use the -d switch first to consolidate the directory, "
                    + "then use the -u switch to remove duplicates."
                )
            self.unique_flag: bool = args.unique
            self.dir_flag: bool = args.dir
            self.min_word_length: int = args.len
            self.input_file: str = args.input_file
            self.output_file: str = args.output_file
        except Exception as e:
            print("Error! in set_instance_vars: " + str(e))

    def bulk_write(self, clean: List) -> bool:
        """
        Takes list as input and uses one big ".writelines()" to fully utilise IO buffers.
        """
        try:
            print("\n*** Writing to Disk ***")
            t1: float = time.perf_counter()
            self.utils.check_file_exists(self.output_file)
            with open(self.output_file, "a") as bulk_file:
                bulk_file.writelines(clean)
            t2: float = time.perf_counter()
            print("Time to write to file: " + str(round(t2 - t1, 5)) + " sec")
            return True
        except TypeError as t:
            print(
                "Type Error! in bulk_write. Check input iterator is not passed in as NULL. exception: "
                + str(t)
            )
        except Exception as e:
            print("Error! in bulk_write: " + str(e))

    def builder(self):
        """
        Builder Method to build new squeaky objects
        """
        try:
            new_squeaky = Squeaky()
            self.utils.clear_screen()
            self.utils.bruce()
            arguments = self.utils.parse_arguments()
            new_squeaky.set_instance_vars(arguments)
            return new_squeaky
        except Exception as e:
            print("Error!! in builder: " + str(e))

    def director(self):
        """
        Co-ordinates the flow of execution.
        """
        try:
            t1: float = time.perf_counter()
            new_squeaky: Squeaky = Squeaky().builder()
            word_lists: list = []
            if new_squeaky.input_file.endswith("/"):
                new_squeaky.input_file = new_squeaky.input_file.rstrip("/")
            if new_squeaky.dir_flag:
                t22: float = time.perf_counter()
                add_to_word_lists = word_lists.append
                for base, subs, all_files in os.walk(new_squeaky.input_file):
                    files: list = [(file) for file in all_files]
                    [
                        add_to_word_lists(base + "/" + f)
                        for f in files
                        if os.path.join(f).endswith(".txt")
                    ]
                print("*** Discovering Wordlists ***")
                [print(ls) for ls in word_lists]
                t33 = time.perf_counter()
                print(
                    "\nTime to walk dirs for word lists: "
                    + str(round(t33 - t22, 5))
                    + " sec"
                )
                print("number of lists: " + str(len(word_lists)))
            else:
                word_lists.append(self.input_file)
            for word_list in word_lists:
                print("\n*** Processing List: " + word_list + " ***\n")
                self.runner(word_list)
            t2: float = time.perf_counter()
            print("\n*** Completed Successfully ***")
            print("Output file: " + str(new_squeaky.output_file))
            print("Total processing time: " + str(round(t2 - t1, 5)) + " sec\n")
        except Exception as e:
            print("Error! in director: " + str(e))

    def runner(self, word_list: list):
        try:
            print("*** Removing Unicode errors ***")
            word_list_from_file, perf_str = self.get_words_from_file(word_list, True)
            print("Time to read input file from disk: " + perf_str)
            processed: list = self.process_words(word_list_from_file)
            if self.min_word_length > 0:
                filtered_len = self.filter_by_length(processed)
                processed = filtered_len
            if self.unique_flag:
                existing_file, perf_time = self.get_words_from_file(
                    self.output_file, False
                )
                print("\n*** Removing Duplicates ***")
                print("Time to read existing word list from disk: " + perf_time)
                deduped = self.de_duplicate(existing_file + processed)
                processed = deduped
                self.utils.clear_output_file(self.output_file)
            self.bulk_write(processed)

        except Exception as e:
            print("Error! in runner: " + str(e))


def main():
    """
    The main(), triggers execution.
    """
    try:
        s = Squeaky().builder()
        s.director()

    except Exception as e:
        print("Error! in squeaky.main: " + str(e))


if __name__ == "__main__":
    main()
