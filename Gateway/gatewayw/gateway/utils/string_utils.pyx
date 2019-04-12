# distutils: sources = lib/stringlib/stringlib.c
# distutils: include_dirs = lib/stringlib/
# cython: language_level=3

import re

#
# As mentioned in stringlib.h it is not necessary to use this version of the split_str() function,
# but why not use it, since I already implemented it to test Cython in this project.
#

# Define the c library
cdef extern from "../../lib/stringlib/stringlib.h":
    cdef struct args_t:
        char ** args
        char * arg_str
        size_t size

    args_t *split_command(char *command, short buffer_size)
    void dealloc_args(args_t * args)


cpdef split_str_c(s):
    """
    Splits the passed str after the colon by comma character.

    :param s: string that should be split
    :return: array of strings
    """

    print(s)
    cdef args_t * args_ptr = split_command(s.encode(), 10)

    print(args_ptr.size)
    splitted = []
    for i in range(args_ptr.size):
        print(args_ptr.args[i])
        splitted.append(args_ptr.args[i].decode("utf-8"))

    dealloc_args(args_ptr)

    return splitted


def clear_str(string):
    """
    Removes carriage return and new line character from the string.

    :param string: string that should be processed
    :type string: str
    :return: String without \n and \r characters
    :rtype: str
    """

    return re.sub('([\n\r])', '', string)


regex = re.compile(r"\\.|[\"',]", re.DOTALL)

def split_str(string):
    """
    Splits the passed str after semicolon and ignores it in double quotes.
    This function is depreciated! Please use the c implementation split_str().

    :param string: string that should be split
    :return: array of strings
    """

    delimiter = ''
    compos = [-1]
    for match in regex.finditer(string):
        g = match.group(0)
        if delimiter == '':
            if g == ',':
                compos.append(match.start())
            elif g in "\"'":
                delimiter = g
        elif g == delimiter:
            delimiter = ''
    # uncomment the next line to catch errors
    # if delimiter: raise ValueError("Unterminated string in data")
    compos.append(len(string))
    return [string[compos[i] + 1:compos[i + 1]] for i in range(len(compos) - 1)]

