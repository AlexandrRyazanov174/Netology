from pprint import pprint
import csv
import re
from Decorators2 import logger


@logger('phonebook.log')
def read_data():
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list[0], contacts_list[1:]

@logger('phonebook.log')
def process_names(data):
    for row in data:
        full_name = " ".join(row[:3]).strip().split(" ")
        row[0] = full_name[0] if len(full_name) > 0 else ""
        row[1] = full_name[1] if len(full_name) > 1 else ""
        row[2] = full_name[2] if len(full_name) > 2 else ""
    return data

@logger('phonebook.log')
def process_phones(data):
    phone_pattern = r'(\+7|8)\s?\(?(\d{3})\)?\s?\-?(\d{3})\s?\-?(\d{2})\s?\-?(\d{2})(\s\(?\доб.\s(\d+)\)?)?'
    replacement = r'+7(\2)\3-\4-\5'
    for row in data:
        if len(row) > 5 and row[5]:
            match = re.search(phone_pattern, row[5])
            if match:
                if match.group(6): 
                    replacement += r' доб.\7'
                row[5] = re.sub(phone_pattern, replacement, row[5])
    return data

@logger('phonebook.log')
def merge_duplicates(data):
    merged = {}
    for row in data:
        key = (row[0], row[1])
        if key not in merged:
            merged[key] = row.copy()
        else:
            existing = merged[key]
            for i in range(len(row)):
                if not existing[i] and row[i]:
                    existing[i] = row[i]
    return list(merged.values())

@logger('phonebook.log')
def save_data(headers, data):
    contacts_list = [headers] + data
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)
    return contacts_list

@logger('phonebook.log')
def main():
    headers, data = read_data()
    data = process_names(data)
    data = process_phones(data)
    data = merge_duplicates(data)
    contacts_list = save_data(headers, data)
    pprint(contacts_list)

    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

if __name__ == '__main__':
    main()