#!/usr/bin/env python3

original_file = "/root/SecLists/Passwords/bt4-password.txt"
new_file = "/root/SecLists/Passwords/consolidated.txt"

def prnt_lengths():
    with open(original_file, "rb") as file:
    x = coun((line) for line in file.readlines())


def read_file_comprehen():
    with open(original_file, "rb") as file:
        file_list = ([line] for line in file.readlines())
        file.close()
    return file_list

def write_new_file(word: str):
    newfile = new_file
    with open(newfile, "a") as file:
        file.write(word)
        file.close()

def go():
    words = read_file_comprehen()
    errors = []
    for i in words:
        try:
            for x in words:
                for y in x:
                    z = str(y.decode("utf-8"))
                    write_new_file(z)
            print("Total Errors: " + str(errors.__len__()))
            for er in errors:
                print(er)

        except UnicodeDecodeError as a:
            print(str(a))
            errors.append(str(a))
            continue


if __name__ == '__main__':
    go()

