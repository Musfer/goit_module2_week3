import pickle
import codecs
from collections import UserDict, UserList

import keyboard


class Tags(UserList):
    """
    Tags class. Contains tags strings in list
    """
    
    def __init__(self, tags):
        super().__init__()
        self.data = tags
    
    def __repr__(self):
        if len(self.data) >= 1 and self.data[0] != "":    
            return ",".join(self.data)
        else:
            return "NONE"

    def change_tag(self, new_tags):  # Rewrites tags in list
        self.data = new_tags


class Note:
    def __init__(self, name, note, tags):
        self.name = name
        self.note = note
        self.tags = tags

    def __repr__(self):  # Class call returns a string with name, content and tags of note
        note = "".join(self.note)
        return f'''Name: {self.name}
Tags: {self.tags}
Note:
{note}
        '''

    def change_name(self, new_name):  # Changes notes name
        self.name = new_name

    def change_note(self, new_note):  # Changes notes content
        self.note = new_note
    
    def change_tags(self, new_tags):  # Changes notes tags
        self.tags.change_tag(new_tags)

    def _tags(self):  # Hidden function. Returns list of tags of note
        return self.tags

    def _name(self):  # Hidden function. Returns name of note
        return self.name

    def _note(self):  # Hidden function. Returns content of note
        return self.note


class Notes(UserDict):
    """
    Notes dict {unique ID:object of class Note()}
    """
    
    __file_name = "notes.pickle"
    
    def __init__(self):
        super().__init__()
        self.data = {}
        self.note_id = 0

    def _restore(self):
        try:
            with open(self.__file_name, "rb+") as file:
                book = pickle.load(file)
                self.data.update(book)
                self.note_id = len(self.data)
        except Exception:
            print("Notes not restored!")

    def _save(self):
        try:
            with open(self.__file_name, "wb+") as file:
                pickle.dump(self.data, file, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:
            print("Some problems with saving!")

    def add_note(self, note: Note):  # Adds new note
        self.data.update({self.note_id: note})
        self.note_id += 1

    def edit_note(self):
        """
        Edits existing note.
        """
        try:
            note = self.find_note_by_id(self.enter_name_id())
            note.change_name(input_with_default("Name: ", note._name()))
            note.change_note(input_with_default("Note: ", "".join(note._note())))
            note.change_tags(input_with_default("Tags: ", note._tags()).split(","))
        except AttributeError:
            pass

    def delete_note(self):  # deletes the note
        note = self.enter_name_id()
        try:
            self.data.pop(note)
            self._id_order()
            print("Note deleted successfully")
        except KeyError:
            print("This note does not exists!")

    def find_note_by_id(self, note_id: int):  # Search by ID
        try:
            return self.data[note_id]
        except KeyError:
            print("This note does not exists!")

    def find_by_tags(self, *tags):  # Search by tags
        to_return = []
        for note_id, each in self.data.items():
            if all(elem in each._tags() for elem in tags):
                to_return.append(each)
            elif any(elem in each._tags() for elem in tags):
                to_return.append(each)
        return to_return

    def _find_id_by_name(self, name):  # Search by name
        for note_id, note in self.data.items():
            if name.lower() in note._name().lower():
                return note_id
    
    def find_by_name(self, name):
        to_return = []
        for note_id, note in self.data.items():
            if name.lower() in note._name().lower():
                to_return.append(note)
        return to_return

    def show_note_list(self):   # Prints the names of all existing notes
        for each in self.data.values():
            print(each._name())
    
    def show_all(self):  # Shows all notes
        for note_id, note in self.data.items():
            print(f'Note ID: {note_id}')
            print(note)

    def show_note(self):  # Shows a certain note
        try:
            note_id = self.enter_name_id()
            return self.data[note_id]
        except KeyError:
            print("This note does not exists!")
            return ""

    def search_in_notes(self, text: str):  # Search text in notes
        to_return = []
        for each in self.data.values():
            if text in each._note():
                to_return.append(each)
        return to_return

    def enter_name_id(self):
        """Checks if entered string is notes ID. If not - calls find_by_name() function"""
        while True:
            string = input("Enter name or ID: ")
            if string == "" or string == " ":
                print("Non-valid name or id")
                continue
            else:
                try:
                    return int(string)
                except:
                    return self._find_id_by_name(string)
    
    def _id_order(self):  # Hidden function, called by delete_note() function. Makes notes ID's ordered to prevent accidental rewrite.
        data = self.data.copy()
        self.data.clear()
        self.note_id = 0
        for note in data.values():
            self.add_note(note)


def input_with_default(prompt_, default_):
    if prompt_ == "Note: ":
        default_ = repr(default_).replace("'", "")
        keyboard.write(default_)
        print(prompt_, end="\n")
        s = input()
        try:
            s = codecs.decode(s, 'unicode_escape')
            return s
        except UnicodeDecodeError:
            print("You entered invalid string literal! Changes not saved.")
            return codecs.decode(default_, 'unicode_escape')     
    elif prompt_ == "Tags: ":
        if default_[0] == "NONE" or default_[0] == "":
            return input(prompt_)
        else:
            keyboard.write(",".join(default_))
            return input(prompt_)
    else:
        keyboard.write(default_)
        return input(prompt_)