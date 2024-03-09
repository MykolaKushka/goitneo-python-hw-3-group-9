from datetime import datetime, timedelta
from collections import defaultdict

class Field:
    # Базовий клас для полів запису
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # Клас для зберігання імені контакту. Обов'язкове поле.
    pass

class Phone(Field):
    # Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits long.")
        super().__init__(value)

class Birthday(Field):
    # Клас для зберігання дня народження. Має валідацію формату (DD.MM.YYYY).
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY.")
        super().__init__(value)

class Record:
    # Клас для зберігання інформації про контакт, включаючи ім'я, телефон та день народження.
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        # Додавання телефону до запису
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        # Видалення телефону з запису
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        # Редагування телефону у записі
        for p in self.phones:
            if str(p) == old_phone:
                p.value = new_phone

    def add_birthday(self, birthday):
        # Додавання дня народження до запису
        self.birthday = Birthday(birthday)

    def __str__(self):
        # Представлення запису у вигляді рядка
        phones_str = "; ".join(str(p) for p in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "Not specified"
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {birthday_str}"

class AddressBook:
    # Клас для зберігання та управління записами
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        # Додавання нового запису до книги контактів
        self.data[record.name.value] = record

    def delete_record(self, name):
        # Видалення запису за іменем з книги контактів
        if name in self.data:
            del self.data[name]

    def find(self, name):
        # Пошук запису за іменем
        return self.data.get(name)

    def get_birthdays_per_week(self):
        # Створюємо словник для зберігання імен користувачів по днях тижня
        birthdays_per_week = defaultdict(list)

        # Отримуємо поточну дату
        today = datetime.today().date()

        # Визначаємо початок тижня (понеділок)
        monday = today - timedelta(days=today.weekday())

        # Перевіряємо, чи поточний рік є високосним
        leap_year = today.year % 4 == 0 and (today.year % 100 != 0 or today.year % 400 == 0)

        # Перебираємо записи в адресній книзі
        for record in self.data.values():
            # Отримуємо дані про користувача
            name = record.name.value
            birthday = record.birthday.value if record.birthday else None

            # Якщо є день народження, визначаємо, чи він в наступному тижні
            if birthday:
                try:
                    birthday_date = datetime.strptime(birthday, "%d.%m.%Y").date()
                    delta_days = (birthday_date - today).days
                    if 0 <= delta_days < 7:
                        # Визначаємо день тижня дня народження
                        birthday_weekday = (monday + timedelta(days=delta_days)).strftime("%A")

                        # Якщо день народження випадає на вихідний, зберігаємо його на понеділок
                        if birthday_date.weekday() >= 5:
                            birthday_weekday = "Monday"

                        # Додаємо ім'я користувача до відповідного дня тижня
                        birthdays_per_week[birthday_weekday].append(name)
                except ValueError:
                    pass  # Неправильний формат дня народження

        return birthdays_per_week

    def __str__(self):
        # Представлення книги контактів у вигляді рядка
        return "\n".join(str(record) for record in self.data.values())

class Bot:
    def __init__(self):
        self.address_book = AddressBook()

    def add_contact(self, name, phone):
        record = Record(name)
        record.add_phone(phone)
        self.address_book.add_record(record)
        print("Contact added successfully.")

    def change_phone(self, name, new_phone):
        record = self.address_book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, new_phone)
            print("Phone number changed successfully.")
        else:
            print("Contact not found.")

    def show_phone(self, name):
        record = self.address_book.find(name)
        if record:
            print(f"Phone number for {name}: {record.phones[0]}")
        else:
            print("Contact not found.")

    def add_birthday(self, name, birthday):
        record = self.address_book.find(name)
        if record:
            record.add_birthday(birthday)
            print("Birthday added successfully.")
        else:
            print("Contact not found.")

    def show_birthday(self, name):
        record = self.address_book.find(name)
        if record and record.birthday:
            print(f"Birthday for {name}: {record.birthday}")
        elif record and not record.birthday:
            print(f"No birthday specified for {name}.")
        else:
            print("Contact not found.")

    def birthdays_this_week(self):
        birthdays_per_week = self.address_book.get_birthdays_per_week()
        if birthdays_per_week:
            print("Birthdays for the next week:")
            for day, users in birthdays_per_week.items():
                print(f"{day}: {', '.join(users)}")
        else:
            print("No birthdays for the next week.")

    def list_all_contacts(self):
        print("All contacts in the address book:")
        print(self.address_book)

    def hello(self):
        print("Hello! I'm your address book bot.")

    def run(self):
        while True:
            command = input("Enter command: ").strip().lower()
            if command == "add":
                name = input("Enter contact name: ").strip()
                phone = input("Enter contact phone: ").strip()
                self.add_contact(name, phone)
            elif command == "change":
                name = input("Enter contact name: ").strip()
                new_phone = input("Enter new phone number: ").strip()
                self.change_phone(name, new_phone)
            elif command == "phone":
                name = input("Enter contact name: ").strip()
                self.show_phone(name)
            elif command == "add-birthday":
                name = input("Enter contact name: ").strip()
                birthday = input("Enter birthday (DD.MM.YYYY): ").strip()
                self.add_birthday(name, birthday)
            elif command == "show-birthday":
                name = input("Enter contact name: ").strip()
                self.show_birthday(name)
            elif command == "birthdays":
                self.birthdays_this_week()
            elif command == "all":
                self.list_all_contacts()
            elif command == "hello":
                self.hello()
            elif command == "close" or command == "exit":
                print("Exiting program...")
                break
            else:
                print("Invalid command. Please try again.")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
