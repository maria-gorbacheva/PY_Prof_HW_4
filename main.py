
import re
import csv


def phonebook_open(name="phonebook_raw.csv"):
    with open(name, encoding='utf8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def name_alignment(contacts: list):
    # должны быть указаны хотя бы фамилия и имя, что логично.
    # экзотические варианты вроде Иванов Алексеевич не рассматриваются
    pattern_1 = re.compile("[\s]+$")
    for item in contacts:
        full_name = item[0] + ' ' + item[1] + ' ' + item[2]
        name_clear = pattern_1.sub('', full_name)
        if len(re.split('[\s]', name_clear)) < 3:
            item[0:2] = re.split('[\s]', name_clear)
        else:
            item[0:3] = re.split('[\s]', name_clear)
    return contacts


def column_alignment(contacts):
    # Удаляет лишнюю запятую вконце.
    # Если лишняя запятая где-то в середине, невозможно разобраться, какую именно убирать.
    for raw in contacts:
        if len(raw) >= 8:
            del raw[-1]


def duplicates_elimination(contacts):
    last_names = {}
    for item in contacts:
        second_met = contacts.index(item)
        first_met = last_names.setdefault(item[0], second_met)
        combined_info = zip(contacts[second_met], contacts_list[first_met])
        if contacts[first_met][1] != contacts[second_met][1]:
            continue
        if first_met != second_met:
            contacts_list[first_met] = [y if y != '' else x for x, y in combined_info]
            del contacts_list[second_met]
    return contacts


def number_alignment(contacts: list):
    pattern_phone = re.compile(r"(\+7|8){1}[\s\(]*(\d{3})[\)\s-]*(\d{3})[-\s]?(\d{2})[-\s]?(\d+)")
    pattern_add = re.compile(r"[\s]*\(?доб.\s*(\d+)\)?")
    for contact in contacts:
        contact[5] = pattern_phone.sub(r"+7(\2)\3-\4-\5", contact[5])
        contact[5] = pattern_add.sub(r" доб.\1", contact[5])
    return contacts


def phonebook_write(data: list, name="phonebook_edited.csv"):
    with open(name, "w", encoding='utf8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(data)


if __name__ == '__main__':
    contacts_list = phonebook_open()
    column_alignment(contacts_list)
    name_alignment(contacts_list)
    zero_duplication = duplicates_elimination(contacts_list)
    contacts_list_app = number_alignment(zero_duplication)
    phonebook_write(contacts_list_app)



