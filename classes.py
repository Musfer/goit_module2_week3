# from collections import UserDict
from copy import copy, deepcopy
from datetime import datetime
import json
from pathlib import Path

from notes import Notes


class Field:
    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    def __copy__(self):
        copy_obj = Field()
        copy_obj.value = copy(self.value)
        return copy_obj

    @value.setter
    def value(self, new_value=None):
        self.__value = new_value


class Name(Field):
    def __init__(self, name: str):
        super().__init__()
        self.value = name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, name: str = ""):
        if name:
            self.__value = name


class Phone(Field):
    def __init__(self, phone_number=None):
        super().__init__()
        self.__value = None
        self.value = phone_number

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, phone_number: str = ""):
        if phone_number:
            phone_number = phone_number.strip().replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
            if phone_number.startswith("+"):
                if len(phone_number[1:]) == 12 and phone_number[1:].isdigit():
                    self.__value = phone_number
            else:
                if phone_number.isdigit and (len(phone_number) == 12 or
                                             len(phone_number) == 10 or len(phone_number) == 7):
                    self.__value = phone_number


class Birthday(Field):
    def __init__(self, birthday=""):
        super().__init__()
        self.__value = None
        self.value = convert_to_date(birthday)
        self.days_to_next_birthday = None
        if self.value is not None:
            self.days_to_next_birthday = self.days_to_birthday()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, birthday: datetime):
        if birthday and birthday.year > 1:
            self.__value = birthday

    def days_to_birthday(self):
        next_birthday = self.value.replace(year=datetime.now().year)
        next_birthday = next_birthday.replace(hour=0, minute=0, second=0, microsecond=0)
        current_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if next_birthday < current_day:
            next_birthday = next_birthday.replace(year=datetime.now().year + 1)
        return (next_birthday - current_day).days


class Email(Field):

    def __init__(self, email=""):
        super().__init__()
        self.__value = None
        self.value = email

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, email: str):
        if email:
            self.__value = email


class Record:
    def __init__(self, name: Name, phones: list[Phone] = []):
        self.name = name
        self.phones = phones
        self.birthday = None
        self.emails = []

    def __lt__(self, other):
        return self.name < other.name

    def __copy__(self):
        copy_obj = Record(Name(""))
        copy_obj.name = copy(self.name)
        copy_obj.phones = copy(self.phones)
        copy_obj.birthday = copy(self.birthday)
        copy_obj.emails = copy(self.emails)
        return copy_obj

    def __deepcopy__(self, memo):
        copy_obj = Record(Name(""))
        copy_obj.name = deepcopy(self.name)
        copy_obj.phones = deepcopy(self.phones)
        copy_obj.birthday = deepcopy(self.birthday)
        copy_obj.emails = deepcopy(self.emails)
        return copy_obj

    def __repr__(self):
        string = ""
        string += f"{self.name.value}:"
        if self.phones:
            string += f"\n\tPhone numbers: {', '.join([x.value for x in self.phones])}"
        if self.emails:
            string += f"\n\tE-mails: {', '.join([x.value for x in self.emails])}"
        if self.birthday:
            birthday = self.birthday.value
            if birthday.year > 2:
                string += f"\n\tBirthday: {birthday.strftime('%d %B %Y')}"
            else:
                string += f"\n\tBirthday: {birthday.strftime('%d %B')}"
            when_to_congratulate = self.birthday.days_to_next_birthday
            if when_to_congratulate is not None:
                if when_to_congratulate == 0:
                    string += f"\n\tToday is {self.name.value}'s birthday."
                elif when_to_congratulate == 1:
                    string += f"\n\t{self.name.value} has birthday tomorrow."
                else:
                    string += f"\n\t{self.name.value}'s birthday is in {when_to_congratulate} days."
        string += "\n"
        return string

    def add_number(self, number: Phone):
        self.phones.append(number)

    def del_number(self, number: Phone):
        for x in self.phones:
            if x.value == number.value:
                self.phones.remove(x)

    def set_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def add_email(self, email: Email):
        self.emails.append(email)

    def del_email(self, email: Email):
        for x in self.emails:
            if x.value == email.value:
                self.emails.remove(x)

    def days_to_birthday(self):
        next_birthday = self.birthday.value.replace(year=datetime.now().year)
        next_birthday = next_birthday.replace(hour=0, minute=0, second=0, microsecond=0)
        current_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if next_birthday < current_day:
            next_birthday = next_birthday.replace(year=datetime.now().year + 1)
        return (next_birthday - current_day).days


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AddressBook):
            return o.data
        elif isinstance(o, Record):
            return {o.name.value: (o.phones, o.birthday, o.emails)}
        elif isinstance(o, Birthday):
            return o.value.strftime("%m.%d.%Y")
        elif isinstance(o, Email):
            return o.value
        elif isinstance(o, Field):
            return o.value
        return super().default(0)


class AddressBook:
    def __init__(self):
        self.notes = Notes()
        self.data = {}
        self.showing_records = False  # when True 'enter' shows next N contacts
        self.page = 0  # number of next page showed with show all
        self.contacts_per_page = 10  # number of contacts showed by show all
        self.show = None  # iterator is not created
        self.filename = str(Path(__file__).parent.resolve()) + r"/AddressBook.json"
        self.names = []
        self.size = 0

    def clear(self):
        self.data = {}

    def write_to_file(self, filename=""):
        if not filename:
            filename = self.filename
        with open(filename, "w") as fh:
            json.dump(self, fh, cls=CustomEncoder, indent=4)
        return f"Your Address book has been saved to '{filename}'"

    def read_from_file(self, filename=""):
        if not filename:
            filename = self.filename
        if not Path(filename).exists() or not Path(filename).is_file():
            return f"No such file '{filename}'"
        else:
            with open(filename, "r") as fh:
                data = json.load(fh)
                if not isinstance(data, dict):
                    return f"Error: 'filename' is not an Address book"
                else:
                    self.data = {}
                    for name, record in data.items():
                        phones = record[name][0]
                        birthday = record[name][1]
                        emails = record[name][2]
                        record = Record(Name(name), [])
                        self.add_record(record)
                        if birthday:
                            self.data.get(name).set_birthday(Birthday(birthday))
                        if phones:
                            for phone in phones:
                                self.data.get(name).add_number(Phone(phone))
                        if emails:
                            for email in emails:
                                self.data.get(name).add_email(Email(email))

            return "Done"

    def add_record(self, record: Record):
        self.names.append(record.name.value)
        self.names.sort()
        self.data[record.name.value] = record
        self.reset_iterator(self.contacts_per_page)
        self.size += 1

    def reset_iterator(self, n: int):
        self.show = self.iterator(n)

    def delete_record(self, name: str):
        self.data.pop(name)
        self.names.remove(name)
        self.names.sort()
        self.size -= 1

    def iterator(self, n: int):
        # string = ""
        # for i, name in enumerate(self.names):
        #     contact = name
        #     if not i % n:
        #         string = ""
        #     string += str(self.data.get(contact))
        #     if not (i + 1) % n or i == len(self.data.keys()) - 1:
        #         yield string
        lst = []
        for i, name in enumerate(self.names):
            contact = name
            if not i % n:
                lst = []
            lst.append(contact)
            # string += str(self.data.get(contact))
            if not (i + 1) % n or i == len(self.data.keys()) - 1:
                yield lst

    def search_in_names(self, text: str = ""):
        lst = []
        text = text.strip().lower()
        for name in self.data.keys():
            if text in name.lower():
                lst.append(name)
        return lst

    def search_in_phones(self, text: str = ""):
        lst = []
        text = text.strip().lower()
        for name in self.data.keys():
            for phone in self.data.get(name).phones:
                if text in phone.value.lower():
                    lst.append((name, phone.value.lower()))
        return lst

    def search_in_emails(self, text: str = ""):
        lst = []
        text = text.strip().lower()
        for name in self.data.keys():
            for email in self.data.get(name).emails:
                if text in email.value.lower():
                    lst.append((name, email.value.lower()))
        return lst


def convert_to_date(birthday: str = None):
    birthday_date = None
    try:
        birthday_date = datetime.strptime(birthday, '%m.%d.%Y')
    except ValueError:
        pass
    try:
        birthday_date = datetime.strptime(birthday, '%m.%d')
        birthday_date = birthday_date.replace(year=2)
    except ValueError:
        pass
    try:
        birthday = birthday.replace("29", "28", 1)
        birthday_date = datetime.strptime(birthday, '%m.%d.%Y')
    except:
        pass
    return birthday_date