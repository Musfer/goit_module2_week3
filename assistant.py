import os
import sys
import shutil 

# from InquirerPy import inquirer, get_style

from classes import AddressBook
from commands import commands, def_mod
from functions import find_birthdays, print_c


def main():
    # os.system("color 07")
    # style = get_style({"questionmark": "#F2F2F2",
    #                    "answer": "#F2F2F2",
    #                    "question": "#F2F2F2",
    #                    "input": "#F2F2F2",
    #                    }, style_override=False)
    # style2 = get_style({"answer": "#33F108"}, style_override=False)
    print("\nWelcome to your personal Python assistant!")
    size = get_terminal_size()

    # if size < 15:
    #     print("\nYou can increase the size of the terminal to have a better experience working with the command line")
    print("What can I do for you today?")
    book = AddressBook()
    book.read_from_file()
    book.notes._restore()
    congratulate = []
    if find_birthdays(book, "0") != "Nobody has a birthday today":
        congratulate.append(find_birthdays(book, "0"))
    if find_birthdays(book, "1") != "Nobody has a birthday tomorrow":
        congratulate.append(find_birthdays(book, "1"))
    if congratulate:
        print("\nLet me remind that")
        print(print_c("\n".join(congratulate), book))
        print("Do not forget to congratulate them\n")
    # print("How can I help you today?")
    while True:
        size = get_terminal_size()
        # if size > 15:
        #     names = {}
        #     for name in book.names:
        #         names[name] = None
        #     request = inquirer.text(
        #         message="",
        #         completer=create_completer(book),
        #         multicolumn_complete=False,
        #     ).execute()
        #     command = request
        # else:
        #     command = input()
        command = input()
        mode, data = def_mod(command)
        output = commands.get(mode)(book, data)
        if output != '':
            print(print_c(output, book))
        if output == "Good bye!":
            book.write_to_file()
            book.notes._save()
            sys.exit()


def create_completer(book: AddressBook):
    names = {}
    for name in book.names:
        names[name] = None
    new_dict = {
        "hello": None,
        "exit": None,
        "good bye": None,
        "close": None,
        "save": None,
        "load": None,
        "phone": names,
        "create note": None,
        "add": {
            "contact": None,
            "number": names,
            "email": names,
        },
        "delete": {
            "contact": names,
            "number": names,
            "birthday": names,
            "note": None,
        },
        "find": None,
        "show": {
            "all": None,
            "note list": None,
            "note":None,
            "notes": None,
            "contact": names,
        },
        "set": {
            "birthday": names,
        },
        "help": None,
        "show birthday": None,
        "edit note": None,
        "rename": None,
    }
    return new_dict


def get_terminal_size():
    try:
        size = os.get_terminal_size().lines
    except OSError:
        try:
            rows = shutil.get_terminal_size().lines
            size = rows
        except OSError:
            size = 1
    return size


if __name__ == "__main__":
    main()
