#!/usr/bin/python3

import os
from argparse import ArgumentParser

MESSAGE = {}
MESSAGE_ID = 0
PATH = ""


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument(
        'message_file', help='The *.g2msg message file to be processed')
    parser.add_argument(
        'message_id', help="ID to be given to this message (u16)"
    )
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
        MESSAGE["name"] = elements[1].lower()
        MESSAGE["fields"] = []
        MESSAGE["arrays"] = []
        MESSAGE["total_size"] = 2


def get_size_from_type(type):
    return int(type[1:])/8


def detect_normal_field(line):
    elements = line.split()
    if(len(elements) == 2) and MESSAGE["name"] and not elements[0] == "message":
        MESSAGE["fields"].append({"type": elements[0], "name": elements[1]})
        MESSAGE["total_size"] += get_size_from_type(elements[0])


def detect_array_field(line):
    elements = line.split()
    if(len(elements) == 3) and MESSAGE["name"] and elements[0].startswith('array'):
        size = elements[0].replace('array[', '')
        size = size.replace(']', '')
        MESSAGE["arrays"].append(
            {"type": elements[1], "name": elements[2], "size": int(size), "define_name":
             f'{MESSAGE["name"].upper()}_{elements[2].upper()}_SIZE'})
        MESSAGE["total_size"] += (get_size_from_type(elements[1]) * int(size))


def detect_message_end(line):
    if line == 'end':
        result_h = generate_h_file()
        full_path = os.path.join(PATH, f'{MESSAGE["name"]}')
        write_file(f'{full_path}.h', result_h)
        result_c = generate_c_file()
        write_file(f'{full_path}.c', result_c)
        MESSAGE["name"] = ""
        MESSAGE["fields"] = []
        MESSAGE["arrays"] = []


def get_c_type(type):
    sign = "" if type[0] == 'i' else "u"
    number = type[1:]
    return f"{sign}int{number}_t"


def get_define_type(type):
    sign = "I" if type[0] == 'i' else "U"
    number = type[1:]
    return f"{sign}{number}"


def generate_h_file():
    lines = []
    lines.append(f'''
#ifndef {MESSAGE["name"].upper()}_H
#define {MESSAGE["name"].upper()}_H
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#define {MESSAGE['name'].upper()}_ID (uint16_t){int(MESSAGE_ID)}
#define {MESSAGE['name'].upper()}_TOTAL_SIZE (size_t){int(MESSAGE['total_size'])}

''')
    for array in MESSAGE["arrays"]:
        lines.append(
            f"#define {array['define_name']} {array['size']}\n")
    lines.append(f'''

struct {MESSAGE["name"]} {{
''')

    for field in MESSAGE["fields"]:
        lines.append(f"    {get_c_type(field['type'])} {field['name']};\n")
    for array in MESSAGE["arrays"]:
        lines.append(
            f"    {get_c_type(array['type'])} {array['name']}[{array['define_name']}];\n")

    lines.append(f'''}};

bool {MESSAGE["name"]}_decode(const uint8_t *buffer, struct {MESSAGE["name"]} *msg);

bool {MESSAGE["name"]}_encode(const struct {MESSAGE["name"]} *msg, uint8_t *buffer);

#endif // {MESSAGE["name"].upper()}_H
''')
    return lines


def generate_c_file():
    lines = []
    lines.append(f'''#include <string.h>
#include "{MESSAGE['name']}.h"

#define GET_U8(ptr) ((uint8_t) * (ptr))
#define GET_U16(ptr)             \\
  (((uint16_t)(GET_U8((ptr)))) + \\
   (((uint16_t)(GET_U8((ptr) + 1))) << 8))
#define GET_U32(ptr)              \\
  (((uint32_t)(GET_U16((ptr)))) + \\
   (((uint32_t)(GET_U16((ptr) + 2))) << 16))

#define GET_I8(ptr) (int8_t) * (ptr)
#define GET_I16(ptr)              \\
  (((int16_t)(GET_I8((ptr)))) + \\
   (((int16_t)(GET_I8((ptr) + 1))) << 8))
#define GET_I32(ptr)               \\
  (((int32_t)(GET_I16((ptr)))) + \\
   (((int32_t)(GET_I16((ptr) + 2))) << 16))

#define SET_U8(ptr, value) *((uint8_t*)(ptr)) = (value)
#define SET_U16(ptr, value)                   \\
  {{                                          \\
    SET_U8(ptr, (uint8_t)(value));            \\
    SET_U8(ptr + 1, (uint8_t)((value) >> 8)); \\
  }}
#define SET_U32(ptr, value)                      \\
  {{                                             \\
    SET_U16(ptr, (uint16_t)(value));             \\
    SET_U16(ptr + 2, (uint16_t)((value) >> 16)); \\
  }}

#define SET_I8(ptr, value) *((int8_t*)(ptr)) = (value)
#define SET_I16(ptr, value)                  \\
  {{                                         \\
    SET_I8(ptr, (int8_t)(value));            \\
    SET_I8(ptr + 1, (int8_t)((value) >> 8)); \\
  }}
#define SET_I32(ptr, value)                     \\
  {{                                            \\
    SET_I16(ptr, (int16_t)(value));             \\
    SET_I16(ptr + 2, (int16_t)((value) >> 16)); \\
  }}

bool {MESSAGE['name']}_decode(const uint8_t* buffer, struct {MESSAGE['name']}* msg) {{
  if (buffer && msg && (GET_U16(buffer) == {MESSAGE['name'].upper()}_ID)) {{
    buffer += 2;''')

    for field in MESSAGE["fields"]:
        lines.append(f'''
    msg->{field["name"]} = GET_{get_define_type(field["type"])}(buffer);
    buffer += {int(get_size_from_type(field["type"]))};''')

    for array in MESSAGE["arrays"]:
        lines.append(
            f"\n    for (size_t i = 0; i < {MESSAGE['name'].upper()}_{array['name'].upper()}_SIZE; i++) {{\n")
        lines.append(
            f"      msg->{array['name']}[i] = GET_{get_define_type(array['type'])}(buffer);\n")
        lines.append(
            f"      buffer += {int(get_size_from_type(array['type']))};\n")
        lines.append("    }")

    lines.append(f'''
    return true;
  }} else {{
    return false;
  }}
}}

bool {MESSAGE['name']}_encode(const struct {MESSAGE['name']}* msg, uint8_t* buffer) {{
  if (msg && buffer) {{
    SET_U16(buffer, {MESSAGE['name'].upper()}_ID);
    buffer += 2;''')

    for field in MESSAGE["fields"]:
        lines.append(f'''
    SET_{get_define_type(field["type"])}(buffer, msg->{field["name"]});
    buffer += {int(get_size_from_type(field["type"]))};''')

    for array in MESSAGE["arrays"]:
        lines.append(
            f"\n    for (size_t i = 0; i < {MESSAGE['name'].upper()}_{array['name'].upper()}_SIZE; i++) {{\n")
        lines.append(
            f"      SET_{get_define_type(array['type'])}(buffer, msg->{array['name']}[i]);\n")
        lines.append(
            f"      buffer += {int(get_size_from_type(array['type']))};\n")
        lines.append("    }")

    lines.append(f'''
    return true;
  }} else {{
    return false;
  }}
}}''')
    return lines


def write_file(file_name, lines):
    with open(file_name, 'w') as file_to_write:
        file_to_write.writelines(lines)


def main():
    global MESSAGE_ID
    global PATH

    args = parse_arguments()
    MESSAGE_ID = args.message_id
    PATH = os.path.dirname(args.message_file)

    content = read_file(args.message_file)
    content = remove_edge_whitespaces(content)
    content = remove_comments(content)

    for line in content:
        detect_message_start(line)
        detect_normal_field(line)
        detect_array_field(line)
        detect_message_end(line)


if __name__ == "__main__":
    main()
