#!/usr/bin/env python3

import argparse
import os


class SqueakyUtils:
    def clear_output_file(self, outfile: str) -> bool:
        """
        Delete all content from output wordlist file.
        """
        try:
            with open(outfile, "w") as file:
                file.write("")
                file.close()
            return True
        except Exception as e:
            print("Error! in clear_output_file: " + str(e))

    def parse_arguments(self) -> argparse.ArgumentParser.parse_args:
        """
        Prints menu and handles user inputs.
        """
        try:
            new_args = argparse.ArgumentParser()
            new_args.add_argument("input_file")
            new_args.add_argument("output_file")
            new_args.add_argument(
                "-d",
                "--dir",
                help='Input a directory to process for word lists. (".txt" files) ',
                action="store_true",
                default=False,
            )

            new_args.add_argument(
                "-l",
                "--len",
                type=int,
                help="Minimum word length, words shorter than "
                "specified length will be removed.",
                default=0,
            )

            new_args.add_argument(
                "-u",
                "--unique",
                help="Delete duplicate words in word list",
                action="store_true",
                default=False,
            )

            parsed_args = new_args.parse_args()
            return parsed_args
        except Exception as e:
            print("Error!! in parse_arguments: " + str(e))

    def clear_screen(self) -> bool:
        """
        Clean the screen.
        """
        try:
            os.system("clear")
            return True
        except Exception as e:
            print("Error! in clearscreen: " + str(e))

    def check_file_exists(self, filename: str):
        """If filename parameter does not exist, create it."""
        try:
            import os
            import subprocess

            file = str(filename)
            if os.path.isfile(file):
                return True
            else:
                tch = "/bin/touch " + file
                touch_file = subprocess.run(
                    [tch],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=True,
                )
                if "Permission" in str(touch_file.stderr):
                    raise AssertionError
                if touch_file.returncode != 0:
                    raise Exception
                return True
        except AssertionError as a:
            print("ERROR! - in check_file_exists Insufficient Permissions: " + str(a))
        except Exception as e:
            print('ERROR! - In "check_file_exists": ' + str(e))

    def bruce(self):
        """
        Banner.
        """
        try:
            print("                                      ___          ")
            print("  _____________ ____  ____________ ___  /______  __")
            print("  __  ___/  __ `/  / / /  _ \  __ `/_  //_/_  / / /")
            print("  _(__  )/ /_/ // /_/ //  __/ /_/ /_  ,<  _  /_/ / ")
            print("  /____/ \__, / \__,_/ \___/\__,_/ /_/|_| _\__, /  ")
            print("           /_/                            /____/   \n\n")
            print(
                "\n     Lean, Mean, List Cleaning Machine\n         squeaky@blairjames.com\n"
            )
        except Exception as e:
            print("Error! in bruce: " + str(e))
