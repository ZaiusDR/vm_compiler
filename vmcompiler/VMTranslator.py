#!/usr/bin/env python3
import argparse
import os
import sys

from vmcompiler import compiler


def _parse_args(args):
    parser = argparse.ArgumentParser(
        description='Jack VM Compiler for Hack Computer Platform'
    )
    parser.add_argument('src_file', help='Source file to compile.')
    args = parser.parse_args()

    if not os.path.isfile(args.src_file):
        print('{0} file not found'.format(args.src_file))
        sys.exit(1)

    return args


def _parse_static_name(src_file):
    return os.path.basename(src_file).split('.')[0]


def main():
    args = _parse_args(sys.argv[1:])
    static_name = _parse_static_name(args.src_file)

    with open(args.src_file) as vm, \
            open(args.src_file.replace('.vm', '.asm'), 'w') as asm:
        compiler_instance = compiler.Compiler(vm, asm, static_name)
        compiler_instance.compile()


if __name__ == '__main__':
    main()
