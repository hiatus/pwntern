#!/usr/bin/env python3

import argparse
import itertools
import math
import sys


BANNER = f'''\
pwntern [options] [charset1]? [charset2]? ... 
    -h, --help          show this banner
    -x, --hex           treat query as a hexadecimal string
    -l, --length [int]  the length of the pattern
    -q, --query  [str]  print only the offset of [str] in the pattern

    # Default Charsets
    - ABCDEFGHIJKLMNOPQRSTUVWXYZ
    - abcdefghijklmnopqrstuvwxyz
    - 0123456789\
'''

DEFAULT_CHARSETS = [
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'abcdefghijklmnopqrstuvwxyz',
    '0123456789'
]


def parse_args():
    parser = argparse.ArgumentParser(usage=BANNER, add_help=False)

    parser.add_argument('-h', '--help', action='store_true')
    parser.add_argument('-x', '--hex', action='store_true')
    parser.add_argument('-l', '--length', type=int, default=-1)
    parser.add_argument('-q', '--query', type=str)
    parser.add_argument('charsets', nargs='*')

    return parser.parse_args()


def generate_pattern(charsets: list, length=-1) -> str:
    segment_length = len(charsets)
    max_length = math.prod([len(cs) for cs in charsets]) * segment_length

    if length > max_length:
        raise ValueError(
            f'[!] {length} > {max_length}: '
            f'length greater than the largest possible pattern'
        )

    if length < 0:
        length = max_length

    pattern = ''
    combinations = itertools.product(*[list(c) for c in charsets])

    for _ in range(0, length, segment_length):
        pattern += ''.join(c for c in next(combinations))

    return pattern[:length]


def main(args) -> int:
    if args.help:
        print(BANNER)
        return 0

    charsets = args.charsets if args.charsets else DEFAULT_CHARSETS

    try:
        pattern = generate_pattern(charsets, length=args.length)
    except Exception as e:
        print(f'{type(e).__str__}: {e}')
        return 1

    if args.query is not None:
        query = args.query

        if args.hex:
            try:
                query = bytearray.fromhex(query).decode()
            except ValueError as e:
                print(f'{type(e).__str__}: {e}')
                return 1

        if (offset := pattern.find(query)) < 0:
            print('[!] String not found in pattern')
            return 1

        print(offset)
        return 0

    print(pattern)
    return 0


if __name__ == '__main__':
    args = parse_args()
    sys.exit(main(args))
