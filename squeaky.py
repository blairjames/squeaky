#!/usr/bin/env python3

#Squeaky takes any wordlist and cleans out problematic characters, words below set length and removes duplicates.
import argparse
import time
import squeaky_utils
import os
import asyncio
from typing import List


#TODO: Val for output file exists
class Squeaky:

    def __init__(self):
        '''
        Instance variables assigned upon object construction.
        '''
        try:
            self.input_file: str = ""
            self.output_file: str = ""
            self.min_word_length: int = 0
            self.starting_wordcount: int = 0
            self.finished_wordcount: int = 0
            self.dir_flag: bool = False
            self.dedup_flag: bool = False
            self.unicode: bool = True
            self.utils = squeaky_utils.SqueakyUtils()
        except Exception as e:
            print("Error! in init: " + str(e))

    async def get_words_from_file(self, path_to_file: str, open_as_bytes: bool) -> List:
        ''''
        Open input wordlist, read into a list to be used in the application.
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

    async def filter_by_length(self, wrds):
        '''
        Parse out words below the length set with the "-l" switch.
        '''
        try:
            tp = time.perf_counter
            t1 = tp()
            word_lst = [w for w in wrds]
            before_words: int = sum([1 for x in word_lst])
            min_len: int = self.min_word_length
            filtered = [w for w in word_lst if len(w) > min_len]
            after_words: int = sum([1 for x in filtered])
            t2 = tp()
            print("\n*** Filter by word length ***")
            print("Words before length filter: " + str(before_words))
            print("Words after length filter: " + str(after_words))
            print("Words removed by length filter: " + str(before_words - after_words))
            print("Filter by length: " + str(round(t2 - t1, 5)) + " sec")
            self.finished_wordcount = after_words
            return filtered
        except Exception as e:
            print("Error! in filter_by_length: " + str(e))

    async def process_words(self, words: List):
        '''
        Iterates input words as bytes to avoid Unicode exceptions.
        performs controlled decode of all words to utf-8, catches any exceptions and parses them out.
        '''
        try:
            t1 = time.perf_counter()
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
            t2 = time.perf_counter()
            print("Words after Unicode errors removed: " + str(finished_len))
            print("Words with errors removed: " + str(dif))
            print("Time to remove Unicode errors: " + str(round(t2 - t1, 5)) + " sec")
            self.finished_wordcount = finished_len

            #Test - return gen and listify vs return list
            return decoded_list
        except Exception as e:
            print("Error! in process_words: " + str(e))

    async def de_duplicate(self, word_list):
        '''
        Removes any duplicate entries using the "set()" function.
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
            print("Time to remove duplicates: " + str(round(t2 - t1, 5)) + " sec")
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
            self.input_file: str = args.input_file
            self.output_file = self.utils.check_file_exists(args.output_file)
            self.dedup_flag: bool = args.dedup
            return True
        except Exception as e:
            print("Error! in set_instance_vars: " + str(e))

    async def bulk_write(self, clean) -> bool:
        '''
        Takes list as input and uses one big ".writelines()" to fully utilise IO buffers.
        '''
        try:
            print("\n*** Writing to Disk ***")
            t1 = time.perf_counter()
            with open(self.output_file, "a") as bulk_file:
                bulk_file.writelines(clean)
            t2 = time.perf_counter()
            print("Time to write to file: " + str(round(t2 - t1, 5)) + " sec")
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

    async def director(self):
        '''
        Co-ordinates the flow of execution.
        '''
        try:
            t1 = time.perf_counter()
            new_squeaky = Squeaky().builder()
            word_lists = []
            if new_squeaky.input_file.endswith("/"):
                new_squeaky.input_file = new_squeaky.input_file.rstrip("/")

            if new_squeaky.dir_flag:
                t22 = time.perf_counter()
                add_to_word_lists = word_lists.append
                for base, subs, all_files in os.walk(new_squeaky.input_file):
                    files = [(file) for file in all_files]
                    [add_to_word_lists(base + "/" + f) for f in files if os.path.join(f).endswith(".txt")]
                print("*** Discovering Wordlists ***")
                [print(ls) for ls in word_lists]
                t33 = time.perf_counter()
                print("\nTime to walk dirs for word lists: " + str(t33 - t22))
                print("number of lists: " + str(len(word_lists)))
            else:
                word_lists.append(self.input_file)

            for word_list in word_lists:
                print("\nProcessing List: " + word_list)
                await self.runner(word_list)

            t2 = time.perf_counter()
            print("\n*** Completed Successfully ***")
            print("Output file: " + str(new_squeaky.output_file))
            print("Total processing time: " + str(round(t2 - t1, 5)) + " sec\n")

        except Exception as e:
            print("Error! in director: " + str(e))

    async def runner(self, word_list):
        try:
            processed = []

            if self.unicode:
                print("*** Removing Unicode errors ***")
                word_list_from_file = await self.get_words_from_file(word_list, True)
                processed = await self.process_words(word_list_from_file)

            if self.min_word_length > 0:
                filtered_len = await self.filter_by_length(processed)
                processed = filtered_len

            if self.dedup_flag:
                print("\n*** Reading current output file from disk ***")
                existing_output_file = await self.get_words_from_file(self.output_file, False)
                deduped = await self.de_duplicate(existing_output_file + processed)
                processed = deduped
                self.utils.clear_output_file(self.output_file)
            await self.bulk_write(processed)

        except Exception as e:
            print("Error! in runner: " + str(e))

def main():
    '''
    The main(), triggers execution.
    '''
    try:
        s = Squeaky().builder()
        loop = asyncio.get_event_loop()
        loop.run_until_complete( s.director())

    except Exception as e:
        print("Error! in squeaky.main: " + str(e))

if __name__ == '__main__':
    main()
