#!/usr/bin/python3

import os
from jinja2 import Environment, PackageLoader, select_autoescape
from argparse import ArgumentParser

MESSAGE = {}
MESSAGE_ID = -1
PATH = ""


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument(
        'message_file', help='The *.g2msg message file to be processed')
    return parser.parse_args()


def read_file(file_name):
    with open(file_name, 'r') as file_to_read:
        return file_to_read.readlines()


def remove_edge_whitespaces(content):
    return [line.strip() for line in content]


def remove_comments(content):
    return list(filter(lambda line: not line.startswith('#'), content))


def detect_message_start(line):
    elements = line.split()
    if (len(elements) == 2) and (elements[0] == 'message'):
        MESSAGE["name"] = elements[1].lower().replace(
            '-', '_').replace(' ', '_')
        MESSAGE["fields"] = []
        MESSAGE["arrays"] = []
        MESSAGE["total_size"] = 2


def detect_id(line):
    global MESSAGE_ID
    elements = line.split()
    if(len(elements) == 2) and (elements[0] == 'id'):
        MESSAGE_ID = int(elements[1])


def get_c_type(type):
    sign = "" if type[0] == 'i' else "u"
    number = type[1:]
    return f"{sign}int{number}_t"


def get_define_type(type):
    sign = "I" if type[0] == 'i' else "U"
    number = type[1:]
    return f"{sign}{number}"


def get_size_from_type(type):
    return int(int(type[1:])/8)


def detect_normal_field(line):
    elements = line.split()
    if(len(elements) == 2) and MESSAGE["name"] and not elements[0] == "message" and not elements[0] == 'id':
        name = elements[1].lower().replace('-', '_')
        type = elements[0]
        c_type = get_c_type(type)
        define_type = get_define_type(type)
        byte_count = get_size_from_type(type)
        MESSAGE["fields"].append(
            {"type": type, "name": name, "c_type": c_type, "define_type": define_type, "byte_count": byte_count})
        MESSAGE["total_size"] += byte_count


def detect_array_field(line):
    elements = line.split()
    if(len(elements) == 3) and MESSAGE["name"] and elements[0].startswith('array'):
        name = elements[2].lower().replace('-', '_')
        type = elements[1]
        c_type = get_c_type(type)
        size = elements[0].replace('array[', '')
        size = int(size.replace(']', ''))
        define_type = get_define_type(type)
        byte_count_per_entry = get_size_from_type(type)
        MESSAGE["arrays"].append(
            {"type": type, "name": name, "size": int(size),
             'c_type': c_type,  "define_type": define_type, "byte_count_per_entry": byte_count_per_entry})
        MESSAGE["total_size"] += (byte_count_per_entry * int(size))


def detect_message_end(line, h_template, c_template):
    if line == 'end':
        if MESSAGE_ID < 0:
            print(f"Error! No Message ID specified for {MESSAGE['name']}!")
        else:
            full_path = os.path.join(PATH, f'{MESSAGE["name"]}')
            generate_file(f'{full_path}.h', h_template)
            generate_file(f'{full_path}.c', c_template)
        MESSAGE["name"] = ""
        MESSAGE["fields"] = []
        MESSAGE["arrays"] = []


def generate_file(file_name, template):
    content = template.render(
        name=MESSAGE["name"], id=MESSAGE_ID, total_size=int(
            MESSAGE["total_size"]),
        fields=MESSAGE["fields"],
        arrays=MESSAGE["arrays"])
    write_file(file_name, content)


def write_file(file_name, lines):
    with open(file_name, 'w') as file_to_write:
        file_to_write.writelines(lines)


def init_templates():
    env = Environment(loader=PackageLoader(
        'g2labs-message-generator'), autoescape=select_autoescape())
    return env.get_template('h_file.h'), env.get_template('c_file.c')


def main():
    global PATH

    h_template, c_template = init_templates()

    args = parse_arguments()
    PATH = os.path.dirname(args.message_file)

    content = read_file(args.message_file)
    content = remove_edge_whitespaces(content)
    content = remove_comments(content)

    for line in content:
        line = line.replace(';','')
        detect_message_start(line)
        detect_id(line)
        detect_normal_field(line)
        detect_array_field(line)
        detect_message_end(line, h_template, c_template)


if __name__ == "__main__":
    main()
