from __future__ import print_function
import json
import sys
import re
from constants import logger
import inspect


def json2object(json_str):
    json_map = json.loads(json_str)
    return json_map


def test_json2object():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = 'Sawyer'
    output_dict = json2object('{"Tom": "Sawyer", "Henry": "Ford"}')
    actual = output_dict.get("Tom")
    assert expected == actual
    assert isinstance(output_dict, dict)

    expected = [1, 2, 3, 4, 5]
    actual = json2object('[1,2,3,4,5]')
    assert expected == actual
    assert isinstance(actual, list)


def map2json(input_dict):
    output = []
    for k, v in input_dict.items():
        output.append('"{0}":"{1}"'.format(k, v))

    return "{" + ", ".join(output) + "}"


def test_map2json():
    logger.info("Testing " + inspect.stack()[0][3])

    expected1 = '{"Tom":"Sawyer", "Henry":"Ford"}'
    expected2 = '{"Henry":"Ford", "Tom":"Sawyer"}'
    input_dict = dict(Tom="Sawyer", Henry="Ford")

    actual = map2json(input_dict)
    assert expected1 == actual or expected2 == actual


def json2kv(json_str,
            only_keys=False,
            only_values=False,
            json_at_col_num=None):
        json_str = json_str.strip("\n")
        json_str = handle_colons_in_string(json_str)
        json_str = re.sub(r'([0-9A-Za-z_]+):', r'"\1":', json_str)

        json_str_list = []
        if json_at_col_num is None:
            json_str_to_process = escape_special_chars(json_str)

        else:
            json_str_list = json_str.split("\t")
            json_str_to_process = escape_special_chars(
                json_str_list[json_at_col_num - 1])

        try:
            values = json.loads(json_str_to_process)
        except ValueError:
            print("[ERROR]: '{0}' is not json".format(json_str_to_process),
                  file=sys.stderr)

        stack = []
        output_json_str = []
        process_dict(values, stack, output_json_str, only_keys, only_values)

        output = display_output(json_str_list, output_json_str, json_at_col_num)
        return output


def test_json2kv():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = 'a=1\tb.0=1\tb.1=2\tb.2=3\tb.3=4\tb.4.c=10'
    actual = json2kv('{"a":1, "b":[1,2,3,4,{"c":10}]}')
    assert expected == actual

    expected = 'a\tb.0\tb.1\tb.2\tb.3\tb.4.c'
    actual = json2kv('{"a":1, "b":[1,2,3,4,{"c":10}]}', True)
    assert expected == actual

    expected = '1\t1\t10\t2\t3\t4'
    actual = json2kv('{"a":1, "b":[1,2,3,4,{"c":10}]}', False, True)
    assert expected == actual

    expected = '__col0={"a":1, "b":[1,2,3,4,{"c":10}]}\ta=1\tb.0=1\tb.1=2\t' \
               'b.2=3\tb.3=4\tb.4.c=10'
    actual = json2kv('{"a":1, "b":[1,2,3,4,{"c":10}]}', False, False, 1)
    assert expected == actual


def display_output(json_str_list, output_json_str, json_at_col_num):
    my_json_str = None
    if json_at_col_num is None:
        my_json_str = "\t".join(sorted(output_json_str))

    else:
        full_output_json_str = []
        for i in range(len(json_str_list)):
            col_value = escape_special_chars(json_str_list[i])
            full_output_json_str.append("__col{0}={1}".format(i, col_value))

        my_json_str = "\t".join(full_output_json_str) + "\t" + "\t".join(sorted(
            output_json_str))

    my_json_str = my_json_str.replace("{COLON}", ":")
    my_json_str = my_json_str.replace("{DOUBLE_QUOTE}", '"')
    return my_json_str


def handle_colons_in_string(json_str):
    is_double_quotes_open = 0
    newline = []

    for i in range(len(json_str)):
        char = json_str[i]

        if char == '"':
            if is_double_quotes_open == 0:
                is_double_quotes_open = 1
            else:
                is_double_quotes_open = 0

        if is_double_quotes_open:
            if char == ':':
                char = "{COLON}"

        newline.append(char)

    return "".join(newline)


def escape_special_chars(json_str):
    json_str = json_str.strip('"')
    json_str = json_str.replace('\\\\"', "{DOUBLE_QUOTE}")
    json_str = json_str.replace(':""', ':"{EMPTY}"')
    json_str = json_str.replace("=", "{EQUAL}")
    json_str = json_str.replace("\t", "{TAB}")
    return json_str


def process_dict(values, stack, output_line, only_keys, only_values):
    for key, value in values.items():
        stack.append(key)

        if value.__class__ is dict:
            process_dict(value, stack, output_line, only_keys, only_values)

        elif value.__class__ is list:
            process_list(value, stack, output_line, only_keys, only_values)

        else:
            process_leaf_value(value, stack, output_line, only_keys,
                               only_values)

        stack.pop()


def process_list(values, stack, output_line, only_keys, only_values):
    cnt = 0
    for value in values:
        stack.append("{0}".format(cnt))
        cnt += 1

        if value.__class__ is dict:
            process_dict(value, stack, output_line, only_keys, only_values)

        elif value.__class__ is list:
            process_list(value, stack, output_line, only_keys, only_values)

        else:
            process_leaf_value(value, stack, output_line, only_keys, only_values)

        stack.pop()


def process_leaf_value(value, stack, output_line, only_keys, only_values):
    if only_keys is True:
        output_line.append(".".join(stack))

    elif only_values is True:
        output_line.append(str(value))

    else:
        output_line.append(".".join(stack) + "=" + str(value))


if __name__ == "__main__":
    # Execute all test methods. All test methods should start with string
    # "test_"
    for name in dir():
        if name.startswith("test_"):
            eval(name)()

    logger.info("All tests run fine")
