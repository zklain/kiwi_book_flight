import argparse
import json
import requests
import sys


def book_flight(args):

    try:
        print(result)
    
    pass

def main():
    arg_parser = argparse.ArgumentParser()
    # positional arguments
    arg_parser.add_argument("--one-way", type=bool, required=False)
    arg_parser.add_argument("--to", type=string, required=True)
    arg_parser.add_argument("--from", type=string, required=True)
    arg_parser.add_argument("--date", type=string, required=True)
    # optional arguments
    arg_parser.add_argument("--fastest", required=False)
    arg_parser.add_argument("--cheapest", required=False)
    arg_parser.add_argument("--bags", type=int, required=False)

    args = arg_parser.parse_args()

    book_flight(args)


if __name__ == "__main__":
    main()