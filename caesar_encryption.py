# /usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================================================================
  Cryptography - Part 1: The Caesar Encryption
================================================================================
What it does:
This script demonstrates an encryption method used by the wellknown roman emperor
Gaius Julius Caesar. The encryption method is classified as monographic,
monopartite, monoalphabethic substitution.

What it is dedicated to:
Written by qpd00z@makerkidsfuerth.de for educational use with maker kids from
above 12 years.

"""

import sys
import os
from typing import List

# defaults
CHARS_PER_LINE: int = 120
ALPHABET: str = 'abcdefghijklmnopqrstuvwxyz'  # alphabet
SPECIAL_CHARS: List = [['ä', 'ae'], ['ö', 'oe'], ['ü', 'ue'], ['ß', 'sz']]  # special chars and replacement chars


# read file
def read_file(path: str):
    with open(path, 'r') as f:
        text: str = f.read()
    return text


# write file
def write_file(path: str, content: str):
    with open(path, 'w') as f:

        if f.write(content):
            return True
        else:
            return False


# encrypt plaintext
def encrypt(plaintext: str, rotation: int) -> str:
    cipher_text: str = ''

    plaintext = substitute_special_char(plaintext)

    for char in plaintext:
        cipher_text = cipher_text + substitute(char, rotation)

    return cipher_text


# decrypt plaintext
def decrypt(cipher_text: str, rotation: int) -> str:
    plain_text: str = ''
    rotation: int = len(ALPHABET) - rotation

    for char in cipher_text:
        plain_text = plain_text + substitute(char, rotation)

    return plain_text


# cryptanalysis
def analyze(cipher_text: str) -> int:

    if len(cipher_text) < CHARS_PER_LINE:
        chars_per_line = len(cipher_text)
    else:
        chars_per_line = CHARS_PER_LINE

    print('\n')
    print(chars_per_line * '=')
    print('CRYPTANALYSIS')
    print(chars_per_line * '=')

    analysis: str = ''

    for i in range(1, len(ALPHABET)):
        hint: int = 0

        if i < 10:
            rotation: str = ' ' + str(i)
        else:
            rotation: str = str(i)

        analysis = analysis + rotation + ': '

        for z in range(0, chars_per_line):
            analysis = analysis + substitute(cipher_text[z], i)

            if substitute(cipher_text[z], i) == 'e':
                hint = hint + 1

        analysis = analysis + ' | e: ' + str(hint) + '\n'

    print(str.upper(analysis))

    key: int = set_key()
    return key


# substitute single character by rotation
def substitute(character: str, rotation: int) -> str:
    cipher: str = ''
    for i in range(0, len(ALPHABET)):
        if str.lower(character) == ALPHABET[i]:
            cipher = ALPHABET[(i + rotation) % len(ALPHABET)]

    return cipher


# substitute umlaut
def substitute_special_char(plaintext: str) -> str:
    for i in range(0, len(SPECIAL_CHARS)):
        plaintext = plaintext.replace(SPECIAL_CHARS[i][0], SPECIAL_CHARS[i][1])
    return plaintext


# format cipher_text into groups for better readability
def format_cipher_text(cipher_text: str, group_length: int, blocks_per_line: int) -> str:
    block_counter: int = 0
    blocks: str = ''

    for i in range(0, len(cipher_text)):
        if i % group_length == 0 and i != 0:
            blocks = blocks + ' '       # add separator
            block_counter = block_counter + 1         # increase group counter

            if blocks_per_line != 0:

                if block_counter % blocks_per_line == 0 and block_counter != 0:
                    blocks = blocks + '\n'  # add new line

        blocks = blocks + cipher_text[i]

    return str.upper(blocks)


# format plain_text into lines
def format_plain_text(plain_text: str, chars_per_line: int) -> str:
    char_counter: int = 0
    output: str = ''

    for char in plain_text:
        if char_counter % chars_per_line == 0 and char_counter != 0:
            output = output + '\n'       # add new line

        output = output + char
        char_counter = char_counter + 1  # increase character counter

    return str.upper(output)


def set_mode() -> int:
    mode = ''
    while not mode.isdigit():
        mode = input('please select mode  [0]=encrypt [1]=decrypt [2]=analyze [enter}=abort: ')  # select mode

        # abort
        if mode == '':
            operation_aborted()

    # encryption
    if mode == '0':
        return 0
    # decryption
    if mode == '1':
        return 1
    # cryptanalysis
    if mode == '2':
        return 2


def set_key() -> int:
    key: str = ''
    while not key.isdigit():
        key = input('rotation key  [enter}=abort: ')

        # abort
        if key == '':
            operation_aborted()

    return int(key)


def set_text() -> str:
    text: str = input('text or path to text file: ')

    if text == '':
        operation_aborted()

    if os.path.isfile(text):
        text = read_file(text)

    return text


def set_chars_per_block() -> int:
    chars_per_block: str = ''
    while not chars_per_block.isdigit():
        chars_per_block = input('chars per block (max. 10) [0] = no formatting  [enter}=abort: ')

        # abort
        if chars_per_block == '':
            operation_aborted()

        # validate group size
        if int(chars_per_block) > 10:
            chars_per_block = ''

    return int(chars_per_block)


def set_blocks_per_line(chars_per_block: int) -> int:
    blocks_per_line: str = ''
    gpl_max = int(CHARS_PER_LINE / (chars_per_block + 1))
    while not blocks_per_line.isdigit():
        blocks_per_line = input('blocks per line (max. ' + str(gpl_max) + ') [0] = no lines  [enter}=abort: ')

        # abort
        if blocks_per_line == '':
            operation_aborted()

    return int(blocks_per_line)


def set_chars_per_line() -> int:
    chars_per_line: str = ''
    cpl: int = CHARS_PER_LINE + 1

    while not chars_per_line.isdigit() and cpl > CHARS_PER_LINE:
        chars_per_line = input('chars per line (max. ' + str(CHARS_PER_LINE) + ') [0] = no formatting  [enter}=abort: ')

        # abort
        if chars_per_line == '':
            operation_aborted()

        cpl = int(chars_per_line)

    return int(chars_per_line)


def operation_aborted():
    print('\noperation aborted!\n')
    sys.exit(0)


def save_results(path: str, content: str):
    choice = ''

    while not choice == 'y' and not choice == 'n':
        choice = input('would you like to save results to file?  [y] = yes  [n] =no: ')

    if choice == 'y':
        if write_file(path, content):
            print('result was successfully saved to ' + path + '!\n')
        else:
            print('something wrong happened! work could not be saved to file!\n')


def restart():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)  # restart script


def main():
    print('\n\n')
    print(CHARS_PER_LINE * '=')
    # noinspection SpellCheckingInspection
    print('CENCRYPT - A DEMONSTRATION OF THE CAESAR ENCRYPTION ALGORITHM (OPTIMIZED FOR GERMAN AND ENGLISH TEXTES)')
    print(CHARS_PER_LINE * '=')
    print('\n')

    key: int = 0

    # input parameters

    # mode
    mode: int = set_mode()    # set operation mode 0=encrypt 1=decrypt 2=analyze or abort

    # key
    if mode == 0 or mode == 1:
        key = set_key()

    # text or path to text file
    text: str = set_text()

    # encryption mode
    if mode == 0:

        # encrypt text
        cipher_text: str = encrypt(text, key)

        # set block length
        chars_per_block: int = set_chars_per_block()
        # set line length to default
        chars_per_line: int = CHARS_PER_LINE

        if chars_per_block > 0:

            # blocks per line
            blocks_per_line: int = set_blocks_per_line(chars_per_block)

            # format cipher text by given parameters
            cipher_text = format_cipher_text(cipher_text, chars_per_block, blocks_per_line)

            if blocks_per_line == 0:
                # set length of parting line to default value if no line separation is wanted
                chars_per_line: int = CHARS_PER_LINE
            else:
                # calculate length of parting line
                chars_per_line: int = chars_per_block * blocks_per_line + (blocks_per_line - 1)

        print('\n\n')
        print(chars_per_line * '=')
        print('CIPHER TEXT:')
        print(chars_per_line * '=')
        print(cipher_text)
        print(chars_per_line * '-')

        save_results('encrypted.txt', cipher_text)

    # decryption mode
    if mode == 1:
        chars_per_line: int = set_chars_per_line()
        # set line length on global default value
        if chars_per_line == 0:
            chars_per_line = CHARS_PER_LINE
        # decrypt text
        plain_text: str = format_plain_text(decrypt(text, key), chars_per_line)

        print('\n\n')
        print(chars_per_line * '=')
        print('PLAIN TEXT:')
        print(chars_per_line * '=')
        print(plain_text)
        print(chars_per_line * '-')

        save_results('decrypted.txt', plain_text)

    # analyze
    if mode == 2:
        key: int = analyze(text)

        plain_text: str = format_plain_text(decrypt(text, key), CHARS_PER_LINE)

        print('\n\n')
        print(CHARS_PER_LINE * '=')
        print('PLAIN TEXT:')
        print(CHARS_PER_LINE * '=')
        print(plain_text)
        print(CHARS_PER_LINE * '-')

        save_results('decrypted.txt', plain_text)


if __name__ == '__main__':
    main()
