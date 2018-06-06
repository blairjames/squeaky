#!/usr/bin/env python3

#Squeaky takes any wordlist and cleans out problematic characters, words below set length and removes duplicates.
import argparse
import time
import squeaky_utils
import os
from typing import Generator, List

#TODO: Read in existing output list as part of dedup
class Squeaky:

    def __init__(self):
        '''
        Instance variables assigned upon object construction.
        '''
        try:
            self.input_files: str = ""
            self.output_file: str = ""
            self.min_word_length: int = 0
            self.starting_wordcount: int = 0
            self.finished_wordcount: int = 0
            self.dir_flag: bool = False
            self.dedup_flag: bool = False
            self.utils = squeaky_utils.SqueakyUtils()
        except Exception as e:
            print("Error! in init: " + str(e))

    def get_words_from_file(self, path_to_file: str, open_as_bytes: bool) -> List:
        ''''
        Open input wordlist, read into a generator to be used in the application.
        '''
        try:
            if open_as_bytes:
                settings = "rb"
            else:
                settings = "r"
            t1 = time.perf_counter()
            with open(path_to_file, settings) as file:
                word_list = [line for line in file.readlines()]
            t2 = time.perf_counter()
            print("Read word list from disk: " + str(round(t2 - t1, 5)) + " sec")
            return word_list
        except Exception as e:
            print("Error! in read_file: " + str(e))

    def filter_by_length(self, wrds):
        '''
        Parse out words below the length set with the "-l" switch.
        returns a generator.
        '''
        try:
            tp = time.perf_counter
            t1 = tp()
            word_lst = [w for w in wrds]
            before_words: int = sum([1 for x in word_lst])
            min_len: int = self.min_word_length
            filtered: List = [w for w in word_lst if len(w) > min_len]
            after_words: int = sum([1 for x in filtered])
            t2 = tp()
            print("\n*** Filter by word length ***")
            print("Words before length filter: " + str(before_words))
            print("Words after length filter: " + str(after_words))
            print("Words removed by length filter: " + str(before_words - after_words))
            print("Filter by len method: " + str(round(t2 - t1, 6)))
            self.finished_wordcount = after_words
            return filtered
        except Exception as e:
            print("Error! in filter_by_length: " + str(e))

    def process_words(self, words):
        '''
        Iterates input words as bytes to avoid Unicode exceptions.
        performs controlled decode of all words to utf-8, catches any exceptions and parses them out.
        returns generator
        '''
        try:
            t1 = time.perf_counter()
            starting_len: int = sum([1 for x in words])
            self.starting_wordcount = starting_len
            decoded_list = []
            apd = decoded_list.append
            for word in words:
                try:
                    decoded = word.decode("utf-8")
                    word_str = str(decoded)
                    apd(word_str)
                except UnicodeDecodeError:
                    pass
            finished_len: int = sum([1 for d in decoded_list])
            dif = starting_len - finished_len
            t2 = time.perf_counter()
            print("Words before Unicode errors removed: " + str(starting_len))
            print("Words after Unicode errors removed: " + str(finished_len))
            print("Words with errors removed: " + str(dif))
            print("Time to remove Unicode errors: " + str(round(t2 - t1, 4)) + " sec")
            self.finished_wordcount = finished_len
            #Test - return gen and listify vs return list
            return decoded_list

        except Exception as e:
            print("Error! in process_words: " + str(e))

    def de_duplicate(self, word_list):
        '''
        Removes any duplicate entries using the "set()" function.
        Returns generator
        '''
        try:
            t1 = time.perf_counter()
            print("\n*** Removing Duplicates ***")
            start_words = sum([1 for i in word_list])
            print("Words before removal of duplicates: " + str(start_words))

            unique = set(word_list)

            after_words = sum([1 for i in unique])

            diff = int(start_words) - int(after_words)

            t2 = time.perf_counter()

            print("Words after removal of duplicates: " + str(after_words))
            print("Time to remove duplicates: " + str(round(t2 - t1, 4)) + " sec")
            print("Duplicate words removed: " + str(diff))
            return unique

        except Exception as e:
            print("Error! in de_duplicate: " + str(e))

    def set_instance_vars(self, args: argparse) -> bool:
        '''
        Set Instance vars using user inputs.
        '''
        try:
            self.dir_flag: bool = args.dir
            self.min_word_length: int = args.len
            self.input_files: str = args.input_file
            self.output_file: str = args.output_file
            return True
        except Exception as e:
            print("Error! in set_instance_vars: " + str(e))

    def bulk_write(self, clean) -> bool:
        '''
        Takes generator as input and uses one big ".writelines()" to fully utilise IO buffers.
        Generator means no loading into memory and no blocking on the process. It's fast for disk IO.
        '''
        try:
            print("\n*** Writing to Disk ***")
            t1 = time.perf_counter()
            with open(self.output_file, "a") as bulk_file:
                bulk_file.writelines(clean)
            t2 = time.perf_counter()
            print("Time to write to file: " + str(round(t2 - t1, 6)) + " sec")
            return True
        except TypeError as t:
            print("Type Error! in bulk_write. Check input iterator is not passed in as NULL. exception: " + str(t))
        except Exception as e:
            print("Error! in bulk_write: " + str(e))

    def builder(self):
        '''
        Builder Method to build new squeaky objects
        '''
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
        '''
        Co-ordinates the flow of execution.
        '''
        try:
            t1 = time.perf_counter()
            new_squeaky = Squeaky().builder()

            print("*** Removing Unicode errors ***")
            word_list_from_file = new_squeaky.get_words_from_file(new_squeaky.input_files, True)
            processed = new_squeaky.process_words(word_list_from_file)

            if new_squeaky.min_word_length > 0:
                filtered_len = new_squeaky.filter_by_length(processed)
                processed = filtered_len

            print("\n*** Reading current output file from disk ***")
            existing_output_file = new_squeaky.get_words_from_file(new_squeaky.output_file, False)
            deduped = new_squeaky.de_duplicate(processed + existing_output_file)
            processed = deduped

            new_squeaky.utils.clear_output_file(new_squeaky.output_file)
            new_squeaky.bulk_write(processed)

            t2 = time.perf_counter()

            print("\n*** Completed Successfully ***")
            print("Output file: " + str(new_squeaky.output_file))
            print("Total processing time: " + str(round(t2 - t1, 6)) + " sec\n")
        except Exception as e:
            print("Error! in director: " + str(e))

def main():
    '''
    The main(), triggers execution.
    '''
    try:
        Squeaky().builder().director()

    except Exception as e:
        print("Error! in squeaky.main: " + str(e))

if __name__ == '__main__':
    main()
