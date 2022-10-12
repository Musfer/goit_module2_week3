from functions import add_contact, show_all, add_number, help_me, delete_number, delete_contact, set_birthday
from functions import show_contact, empty, reset, delete_birthday, find, save_to_file, read_from_file, clear
from functions import add_email, delete_email, find_birthdays, rename, create_note, delete_note, edit_note
from functions import show_all_notes, show_note_list, show_note


commands = {
    "hello": lambda *_: "How can I help you?",
    "bye": lambda *_: "Good bye!",
    "add_contact": add_contact,
    "add_number": add_number,
    "find": find,
    "delete_contact": delete_contact,
    "delete_number": delete_number,
    "show": show_contact,
    "show_all": show_all,
    "help_me": help_me,
    "set_birthday": set_birthday,
    "empty": empty,
    "reset": reset,
    "save": save_to_file,
    "load": read_from_file,
    "clear": clear,
    "delete_birthday": delete_birthday,
    "add_email": add_email,
    "delete_email": delete_email,
    "show_birthday": find_birthdays,
    "rename": rename,
    "create_note": create_note,
    "delete_note": delete_note,
    "edit_note": edit_note,
    "show_all_notes": show_all_notes,
    "show_note_list": show_note_list,
    "show_note": show_note,
    0: lambda *_: "Sorry I can't understand you. Try 'help' command to see what I can.",
}


def def_mod(string: str):
    try:
        mods = {
            # ".": "exit",
            "hello": "hello",
            "good bye": "bye",
            "close": "bye",
            "exit": "bye",
            "save": "save",
            "load": "load",
            "clear": "clear",
            "add contact": "add_contact",
            "add phone number": "add_number",
            "add phone": "add_number",
            "add number": "add_number",
            "add email": "add_email",
            "find": "find",
            "delete contact": "delete_contact",
            "delete phone number": "delete_number",
            "delete phone": "delete_number",
            "delete number": "delete_number",
            "delete birthday": "delete_birthday",
            "show contact": "show",
            "show all": "show_all",
            "reset": "reset",
            "set birthday": "set_birthday",
            "help": "help_me",
            "delete email": "delete_email",
            "show birthday": "show_birthday",
            "rename": "rename",
            "create note": "create_note",
            "delete note": "delete_note",
            "edit note": "edit_note",
            "show notes": "show_all_notes",
            "show note list": "show_note_list",
            "show note": "show_note"
        }
        if not string:
            return "empty", ""
        for key_word in mods.keys():
            if key_word in string.lower():
                return mods[key_word], string.replace(key_word, "", 1)
        return 0, ""
    except Exception as err:
        return err
