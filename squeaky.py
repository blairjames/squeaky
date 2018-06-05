#!/usr/bin/env python3

#Squeaky takes any wordlist and cleans out dodgey characters, short words and duplicates.
import argparse
import os
import time
import multiprocessing
from typing import Generator, List


class Squeaky:

    def __init__(self):
        '''
        Instance Variables
        '''
        try:
            self.clean: set = set()
            self.input_files: str = ""
            self.output_file: str = ""
            self.min_word_length: int = 0
            self.procs: int = os.cpu_count() * 4
            self.dir_flag: bool = False
            self.dedup_flag: bool = False
        except Exception as e:
            print("Error! in init: " + str(e))

    def line_count(self, file: str) -> int:
        try:
            with open(file, "rb") as openfile:
                length = (1 for ln in openfile.readlines())
            return sum(length)
        except Exception as e:
            print("Error! in get_file_length: " + str(e))

    def clear_output_file(self) -> bool:
        try:
            with open(self.output_file, "w") as file:
                file.write("")
                file.close()
            return True
        except Exception as e:
            print("Error! in clear_output_file: " + str(e))

    def file_generator(self, path_to_file: str) -> Generator:
        try:
            t1 = time.perf_counter()
            with open(path_to_file, "rb") as file:
                word_list = (line for line in file.readlines())
            t2 = time.perf_counter()
            print("Read word list: " + str(round(t2 - t1, 4)) + " sec")
            return word_list
        except Exception as e:
            print("Error! in read_file: " + str(e))

    def filter_by_length(self, wrds: Generator) -> Generator:
        try:
            print("\n*** Filter by word length ***")
            t1 = time.perf_counter()
            word_lst = list(w for w in wrds)
            word_gen_1 = (w for w in word_lst)
            word_gen_2 = (w for w in word_lst)
            before_words: int = sum(1 for x in word_gen_1)
            print("Words before length filter: " + str(before_words))
            min_len = self.min_word_length

            filtered = (d for d in word_gen_2 if int(len(d)) > int(min_len))
            cp_filtered = list(f for f in filtered)
            filter1 = (c for c in cp_filtered)
            filter2 = (c for c in cp_filtered)
            filt_words: int = sum(1 for n in filter1)
            dif_words = int(before_words) - int(filt_words)
            print("Words after length filter: " + str(filt_words))
            print("Words Removed by Length Filter: " + str(dif_words))
            t2 = time.perf_counter()
            print("Time to filter by Length: " + str(round(t2 - t1, 4)) + " sec")
            return (f for f in filter2)
        except Exception as e:
            print("Error! in filter_by_length: " + str(e))

    def process_words(self) -> Generator:
        try:
            print("*** Remove Unicode errors ***")
            words = self.file_generator(self.input_files)
            words_1 = self.file_generator(self.input_files)
            starting_len = (str(sum(1 for x in words_1)))
            decoded_list = []
            apd = decoded_list.append
            t1 = time.perf_counter()
            for word in words:
                try:
                    decoded = word.decode("utf-8")
                    word_str = str(decoded)
                    apd(word_str)
                except UnicodeDecodeError:
                    pass
            t2 = time.perf_counter()
            print("Time to process words for Unicode errors: " + str(round(t2 - t1, 4)) + " sec")
            finished_len = sum(1 for d in decoded_list)
            dif = int(starting_len) - int(finished_len)
            print("Words before Unicode errors removed: " + str(starting_len))
            print("Words after Unicode errors removed: " + str(finished_len))
            print("Words with errors removed: " + str(dif))
            final = (d for d in decoded_list)
            if self.min_word_length > 0:
                word_len = self.filter_by_length(final)
                final = word_len
            if self.dedup_flag:
                deduped = self.de_duplicate(final)
                final = deduped
            return final
        except Exception as e:
            print("Error! in process_words: " + str(e))

    def de_duplicate(self, word_list: Generator) -> Generator:
        try:
            print("\n*** Remove Duplicates ***")
            cp = list(w for w in word_list)
            words = (c for c in cp)
            words2 = (c for c in cp)
            start_words: int = sum(1 for i in words)
            print("Words before removal of duplicates: " + str(start_words))
            t1 = time.perf_counter()
            unique = set(words2)
            deduped1 = (u for u in unique)
            deduped2 = (u for u in unique)
            after_words: int = sum(1 for i in deduped1)
            t2 = time.perf_counter()
            diff = int(start_words) - int(after_words)
            print("Words after removal of duplicates: " + str(after_words))
            print("Time to remove duplicates: " + str(round(t2 - t1, 4)) + " sec")
            print("Duplicate words removed: " + str(diff))
            return (d for d in deduped2)
        except Exception as e:
            print("Error! in de_duplicate: " + str(e))

    def parse_arguments(self) -> argparse.ArgumentParser.parse_args:
        try:
            new_args = argparse.ArgumentParser()
            new_args.add_argument("input_file")
            new_args.add_argument("output_file")
            new_args.add_argument("-d", "--dir",
                                  help="Input a directory of wordlists instead of single file.",
                                  action="store_true", default=False)

            new_args.add_argument("-l", "--len", type=int,
                                  help="Minimum word length, words shorter than "
                                  "specified length will be cleansed.", default=0)

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
            self.input_files: str = args.input_file
            self.output_file: str = args.output_file
            return True
        except Exception as e:
            print("Error! in set_instance_vars: " + str(e))

    def bulk_write(self, clean: Generator) -> bool:
        try:
            print("\n*** Writing to Disk ***")
            t1 = time.perf_counter()
            self.clear_output_file()
            with open(self.output_file, "a") as bulk_file:
                bulk_file.writelines(clean)
            t2 = time.perf_counter()
            print("Time to write to file: " + str(round(t2 - t1, 4)))
            return True
        except TypeError as t:
            print("Type Error! in bulk_write. Check input iterator is not passed in as NULL. exception: " + str(t))
        except Exception as e:
            print("Error! in bulk_write: " + str(e))

    def go(self):
        try:
            print("Ready..")
            time.sleep(.2)
            print("Set..")
            time.sleep(.2)
            print("\nGO!!\n")
            time.sleep(.2)
        except Exception as e:
            print("Error!! in go: " + str(e))

    def builder(self):
        try:
            new_squeaky = Squeaky()
            new_squeaky.clear_screen()
            new_squeaky.bruce()
            arguments = new_squeaky.parse_arguments()
            new_squeaky.set_instance_vars(arguments)
            new_squeaky.go()
            return new_squeaky
        except Exception as e:
            print("Error!! in builder: " + str(e))


def main():
    try:
        new_squeaky = Squeaky().builder()
        t1 = time.perf_counter()
        processed: Generator = new_squeaky.process_words()
        new_squeaky.bulk_write(processed)
        t2 = time.perf_counter()
        print("\n*** Completed Successfully ***")
        print("Output file: " + str(new_squeaky.output_file))
        print("Total processing time: " + str(round(t2 - t1, 4)) + " sec\n")

    except Exception as e:
        print("Error! in squeaky.main: " + str(e))

if __name__ == '__main__':
    main()

