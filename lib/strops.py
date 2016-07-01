from __future__ import print_function
import re
import constants
from datetime import datetime, timedelta
import inspect
from constants import logger
import csv
import HTMLParser
import cgi


def bl(line, field_delimiter, num_occurrences_to_replace=0):
    """
    This script replaces the 'field_delimiter' with new line character
    :param line:
    :param field_delimiter:
    :param num_occurrences_to_replace:
    :return:
    """

    if field_delimiter == '|':
        field_delimiter = "["+field_delimiter+"]"

    return re.sub(
        field_delimiter,
        constants.char_newline,
        line.rstrip(constants.char_newline),
        num_occurrences_to_replace)


def test_bl():
    logger.info("Testing " + inspect.stack()[0][3])

    line = "Be happy always"
    expected = "Be\nhappy\nalways"
    actual = bl(line, " ")
    assert expected == actual

    line = "Be happy always"
    expected = "Be\nhappy always"
    actual = bl(line, " ", 1)
    assert expected == actual


def csv2tsv(filepointer_or_stdin):
    """
    This method reads a file pointer or sys.stdin containing comma delimited
    data and output tab delimited data
    :param filepointer_or_stdin:
    :return:
    """
    for line in csv.reader(filepointer_or_stdin):
        return "\t".join(line)


def test_csv2tsv():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = "R1C1\tthis, my friend is R2C2\tAnd this is R3C3"
    fp = open(constants.FILENAME_TEST_CSV2TSV, "r")
    actual = csv2tsv(fp)
    assert expected == actual

    expected = "a\tb\tc\nnewline"
    fp = open(constants.FILENAME_TEST_CSV2TSV_MULTILINE, "r")
    actual = csv2tsv(fp)
    assert expected == actual


def decode_punc(line):
    line = re.sub('\{FLOWERSTART}'  , '{', line)
    line = re.sub('\{FLOWEREND}'    , '}',  line)
    line = re.sub('\{PIPE}'         , '|', line)
    line = re.sub('\{TILDE}'        , '~', line)
    line = re.sub('\{SINGLEQUOTE}'  , "'", line)
    line = re.sub('\{ROUNDSTART}'   , "(", line)
    line = re.sub('\{ROUNDEND}'     , ')', line)
    line = re.sub('\{STAR}'         , '*', line)
    line = re.sub('\{PLUS}'         , '+', line)
    line = re.sub('\{COMMA}'        , ',',  line)
    line = re.sub('\{HYPHEN}'       , '-', line)
    line = re.sub('\{DOT}'          , '.', line)
    line = re.sub('\{FRONTSLASH}'   , '/', line)
    line = re.sub('\{SQUARESTART}'  , '[', line)
    line = re.sub('\{SQUAREEND}'    , ']', line)
    line = re.sub('\{BACKSLASH}'    , '\\\\', line)
    line = re.sub('\{CARET}'        , '^', line)
    line = re.sub('\{UNDERSCORE}'   , '_', line)
    line = re.sub('\{BACKTICK}'     , '`', line)
    line = re.sub('\{EXCLAMATION}'  , '!', line)
    line = re.sub('\{DOUBLEQUOTES}' , '"', line)
    line = re.sub('\{HASH}'         , '#', line)
    line = re.sub('\{DOLLAR}'       , '$', line)
    line = re.sub('\{PERCENTAGE}'   , '%', line)
    line = re.sub('\{AMPERSAND}'    , '&', line)
    line = re.sub('\{RATE}'         , '@', line)
    line = re.sub('\{EQUAL}'        , '=', line)
    line = re.sub('\{COLON}'        , ':', line)
    line = re.sub('\{SEMICOLON}'    , ';', line)
    line = re.sub('\{QUESTION}'     , '?', line)
    line = re.sub('\{ANGLESTART}'   , '<', line)
    line = re.sub('\{ANGLEEND}'     , '>', line)
    return line


def test_decode_punc():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = "{"
    actual = decode_punc("{FLOWERSTART}")
    assert expected == actual

    expected = "}"
    actual = decode_punc("{FLOWEREND}")
    assert expected == actual

    expected = "|"
    actual = decode_punc("{PIPE}")
    assert expected == actual

    expected = "~"
    actual = decode_punc("{TILDE}")
    assert expected == actual

    expected = "'"
    actual = decode_punc("{SINGLEQUOTE}")
    assert expected == actual

    expected = "("
    actual = decode_punc("{ROUNDSTART}")
    assert expected == actual

    expected = ")"
    actual = decode_punc("{ROUNDEND}")
    assert expected == actual

    expected = "*"
    actual = decode_punc("{STAR}")
    assert expected == actual

    expected = "+"
    actual = decode_punc("{PLUS}")
    assert expected == actual

    expected = ","
    actual = decode_punc("{COMMA}")
    assert expected == actual

    expected = "-"
    actual = decode_punc("{HYPHEN}")
    assert expected == actual

    expected = "."
    actual = decode_punc("{DOT}")
    assert expected == actual

    expected = "/"
    actual = decode_punc("{FRONTSLASH}")
    assert expected == actual

    expected = "["
    actual = decode_punc("{SQUARESTART}")
    assert expected == actual

    expected = "]"
    actual = decode_punc("{SQUAREEND}")
    assert expected == actual

    expected = '\\'
    actual = decode_punc("{BACKSLASH}")
    assert expected == actual

    expected = "^"
    actual = decode_punc("{CARET}")
    assert expected == actual

    expected = "_"
    actual = decode_punc("{UNDERSCORE}")
    assert expected == actual

    expected = "`"
    actual = decode_punc("{BACKTICK}")
    assert expected == actual

    expected = "!"
    actual = decode_punc("{EXCLAMATION}")
    assert expected == actual

    expected = '"'
    actual = decode_punc("{DOUBLEQUOTES}")
    assert expected == actual

    expected = "#"
    actual = decode_punc("{HASH}")
    assert expected == actual

    expected = "$"
    actual = decode_punc("{DOLLAR}")
    assert expected == actual

    expected = "%"
    actual = decode_punc("{PERCENTAGE}")
    assert expected == actual

    expected = "&"
    actual = decode_punc("{AMPERSAND}")
    assert expected == actual

    expected = "@"
    actual = decode_punc("{RATE}")
    assert expected == actual

    expected = "="
    actual = decode_punc("{EQUAL}")
    assert expected == actual

    expected = ":"
    actual = decode_punc("{COLON}")
    assert expected == actual

    expected = ";"
    actual = decode_punc("{SEMICOLON}")
    assert expected == actual

    expected = "?"
    actual = decode_punc("{QUESTION}")
    assert expected == actual

    expected = "<"
    actual = decode_punc("{ANGLESTART}")
    assert expected == actual

    expected = ">"
    actual = decode_punc("{ANGLEEND}")
    assert expected == actual


def encode_punc(line):
    line = re.sub('{'                  , 'FLOWERBRACKSTART', line)
    line = re.sub('}'                  , 'FLOWERBRACKEND'  , line)
    line = re.sub('FLOWERBRACKSTART'   , '{FLOWERSTART}'   , line)
    line = re.sub('FLOWERBRACKEND'     , '{FLOWEREND}'     , line)
    line = re.sub('[|]'                , '{PIPE}'          , line)
    line = re.sub('~'                  , '{TILDE}'         , line)
    line = re.sub("'"                  , '{SINGLEQUOTE}'   , line)
    line = re.sub("\("                 , '{ROUNDSTART}'    , line)
    line = re.sub('\)'                 , '{ROUNDEND}'      , line)
    line = re.sub('[*]'                , '{STAR}'          , line)
    line = re.sub('[+]'                , '{PLUS}'          , line)
    line = re.sub(','                  , '{COMMA}'         , line)
    line = re.sub('-'                  , '{HYPHEN}'        , line)
    line = re.sub('[.]'                , '{DOT}'           , line)
    line = re.sub('/'                  , '{FRONTSLASH}'    , line)
    line = re.sub('\['                 , '{SQUARESTART}'   , line)
    line = re.sub(']'                  , '{SQUAREEND}'     , line)
    line = re.sub('\\\\'               , '{BACKSLASH}'     , line)
    line = re.sub('\^'                 , '{CARET}'         , line)
    line = re.sub('_'                  , '{UNDERSCORE}'    , line)
    line = re.sub('`'                  , '{BACKTICK}'      , line)
    line = re.sub('!'                  , '{EXCLAMATION}'   , line)
    line = re.sub('"'                  , '{DOUBLEQUOTES}'  , line)
    line = re.sub('#'                  , '{HASH}'          , line)
    line = re.sub('\$'                 , '{DOLLAR}'        , line)
    line = re.sub('%'                  , '{PERCENTAGE}'    , line)
    line = re.sub('&'                  , '{AMPERSAND}'     , line)
    line = re.sub('@'                  , '{RATE}'          , line)
    line = re.sub('='                  , '{EQUAL}'         , line)
    line = re.sub(':'                  , '{COLON}'         , line)
    line = re.sub(';'                  , '{SEMICOLON}'     , line)
    line = re.sub('[?]'                , '{QUESTION}'      , line)
    line = re.sub('<'                  , '{ANGLESTART}'    , line)
    line = re.sub('>'                  , '{ANGLEEND}'      , line)
    return line


def test_encode_punc():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = "{FLOWERSTART}"
    actual = encode_punc("{")
    assert expected == actual

    expected = "{FLOWEREND}"
    actual = encode_punc("}")
    assert expected == actual

    expected = "{PIPE}"
    actual = encode_punc("|")
    assert expected == actual

    expected = "{TILDE}"
    actual = encode_punc("~")
    assert expected == actual

    expected = "{SINGLEQUOTE}"
    actual = encode_punc("'")
    assert expected == actual

    expected = "{ROUNDSTART}"
    actual = encode_punc("(")
    assert expected == actual

    expected = "{ROUNDEND}"
    actual = encode_punc(")")
    assert expected == actual

    expected = "{STAR}"
    actual = encode_punc("*")
    assert expected == actual

    expected = "{PLUS}"
    actual = encode_punc("+")
    assert expected == actual

    expected = "{COMMA}"
    actual = encode_punc(",")
    assert expected == actual

    expected = "{HYPHEN}"
    actual = encode_punc("-")
    assert expected == actual

    expected = "{DOT}"
    actual = encode_punc(".")
    assert expected == actual

    expected = "{FRONTSLASH}"
    actual = encode_punc("/")
    assert expected == actual

    expected = "{SQUARESTART}"
    actual = encode_punc("[")
    assert expected == actual

    expected = "{SQUAREEND}"
    actual = encode_punc("]")
    assert expected == actual

    expected = '{BACKSLASH}'
    actual = encode_punc("\\")
    assert expected == actual

    expected = "{CARET}"
    actual = encode_punc("^")
    assert expected == actual

    expected = "{UNDERSCORE}"
    actual = encode_punc("_")
    assert expected == actual

    expected = "{BACKTICK}"
    actual = encode_punc("`")
    assert expected == actual

    expected = "{EXCLAMATION}"
    actual = encode_punc("!")
    assert expected == actual

    expected = '{DOUBLEQUOTES}'
    actual = encode_punc('"')
    assert expected == actual

    expected = "{HASH}"
    actual = encode_punc("#")
    assert expected == actual

    expected = "{DOLLAR}"
    actual = encode_punc("$")
    assert expected == actual

    expected = "{PERCENTAGE}"
    actual = encode_punc("%")
    assert expected == actual

    expected = "{AMPERSAND}"
    actual = encode_punc("&")
    assert expected == actual

    expected = "{RATE}"
    actual = encode_punc("@")
    assert expected == actual

    expected = "{EQUAL}"
    actual = encode_punc("=")
    assert expected == actual

    expected = "{COLON}"
    actual = encode_punc(":")
    assert expected == actual

    expected = "{SEMICOLON}"
    actual = encode_punc(";")
    assert expected == actual

    expected = "{QUESTION}"
    actual = encode_punc("?")
    assert expected == actual

    expected = "{ANGLESTART}"
    actual = encode_punc("<")
    assert expected == actual

    expected = "{ANGLEEND}"
    actual = encode_punc(">")
    assert expected == actual


def enclose(line, enclose_string):
    return enclose_string + line + enclose_string


def test_exclose():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = "#redmond#"
    actual = enclose("redmond", "#")
    assert expected == actual


def html_decode(line):
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(line)


def test_html_decode():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = "<a>link</a>"
    actual = html_decode("&lt;a&gt;link&lt;/a&gt;")
    assert expected == actual


def html_encode(line):
    return cgi.escape(line, quote=True).replace(u'\n', u'<br />').\
        replace(u'\t', u'&emsp;').\
        replace(u'  ', u' &nbsp;')


def test_html_encode():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = "&lt;a&gt;link&lt;/a&gt;"
    actual = html_encode("<a>link</a>")
    assert expected == actual


def ibl(filepointer_or_stdin, field_delimiter, fields_to_use):
    field_list = fields_to_use.split(",")

    tracking_cols = "{nothing yet. we will get then later}"

    first_line = True

    ouput = []
    for line in filepointer_or_stdin:

        line = line.strip("\n")
        if field_delimiter == "\\t":
            line_list = line.split("\t")
        else:
            line_list = line.split(field_delimiter)

        if first_line:
            tracking_cols = __get_list_items_as_string(line_list, field_list)

        new_tracking_cols = __get_list_items_as_string(line_list, field_list)

        if not first_line and new_tracking_cols != tracking_cols:
            ouput.append("\n")
            ouput.append(line)

            tracking_cols = new_tracking_cols
        else:
            ouput.append(line)

        first_line = False

    return ouput


def __get_list_items_as_string(inlist, items):
    return_string = ""

    for i in items:
        return_string = return_string + "{@#@}" + (inlist[int(i) - 1])

    return return_string


def test_ibl():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = str(['1', '\n', '2', '2', '\n', '3', '3'])
    fp = open(constants.FILENAME_TEST_IBL, "r")
    actual = str(ibl(fp, "\t", '1'))
    assert expected == actual


def is_blank_line(line):
    if len(line) < 1:
        return True
    else:
        return False


def test_ignore_blank_lines():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = False
    actual = is_blank_line("aman")
    assert expected == actual

    expected = True
    actual = is_blank_line("")
    assert expected == actual


def ignore_lines(filepointer_or_stdin, lines_to_ignore):
    ignore_line_list = lines_to_ignore.split(",")

    linenum = 0
    for line in filepointer_or_stdin:
        linenum += 1
        if str(linenum) in ignore_line_list:
            continue

        yield line


def test_ignore_lines():
    logger.info("Testing " + inspect.stack()[0][3])

    expected = ['1\n', '3\n', '4\n', '6']
    fp = open(constants.FILENAME_TEST_IGNORE_LINES, "r")
    actual = []
    for token in ignore_lines(fp, '2,5'):
        actual.append(token)

    assert str(expected) == str(actual)


if __name__ == "__main__":
    # Execute all test methods. All test methods should start with string
    # "test_"
    for name in dir():
        if name.startswith("test_"):
            eval(name)()

    logger.info("All tests run fine")
