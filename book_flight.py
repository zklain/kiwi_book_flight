# -*- coding: utf-8 -*-
import argparse
import json
# import requests
import sys


def book_flight(args):

    result = 'Berlin'
    print(result)


def main():
    arg_parser = argparse.ArgumentParser()
    # positional arguments
    arg_parser.add_argument("--date", type=str, required=True, help='')
    arg_parser.add_argument("--from", type=str, required=True, help='')
    arg_parser.add_argument("--to", type=str, required=True, help='')
    # optional arguments
    arg_parser.add_argument("--one-way", action="store_true", default='True', required=False, help='')
    arg_parser.add_argument("--return", type=int, required=False, help='')
    arg_parser.add_argument("--fastest", '--cheapest', action="store_true", required=False, help='')
    # arg_parser.add_argument("--cheapest", action="store_true", required=False)
    arg_parser.add_argument("--bags", type=int, required=False, help='')


    args = arg_parser.parse_args()

    print(args.fastest)
    # if args.

    book_flight(args)


if __name__ == "__main__":
    main()
