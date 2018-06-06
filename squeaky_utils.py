#!/usr/bin/env python3

import time
import argparse
import os

class SqueakyUtils:

    def clear_output_file(self, outfile: str) -> bool:
        '''
        Delete all content from output wordlist file.
        '''
        try:
            with open(outfile, "w") as file:
                file.write("")
                file.close()
            return True
        except Exception as e:
            print("Error! in clear_output_file: " + str(e))

    def parse_arguments(self) -> argparse.ArgumentParser.parse_args:
        '''
        Prints menu and handles user inputs.
        '''
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
        '''
        Clean the screen.
        '''
        try:
            os.system("clear")
            return True
        except Exception as e:
            print("Error! in clearscreen: " + str(e))

    def bruce(self):
        '''
        Banner.
        '''
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

    def go(self):
        '''
        Ready, set, go.
        '''
        try:
            print("Ready..")
            time.sleep(.2)
            print("Set..")
            time.sleep(.2)
            print("\nGO!!\n")
            time.sleep(.2)
        except Exception as e:
            print("Error!! in go: " + str(e))