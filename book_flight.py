# -*- coding: utf-8 -*-
import argparse
import json
import requests
import sys


def convert_date_format(date):
    new_format = ''
    date_split = date.split('-')
    new_format += date_split[2] + '/'
    new_format += date_split[1]
    new_format += date_split[0]

def book_flight(args):
    r = requests.get('https://api.skypicker.com/flights?flyFrom=BTS&to=SXF&dateFrom=30/1/2018&dateTo=1/2/2018&partner=picky')
    print(r.status_code)
    print(json.dumps(r.json(), indent=4))


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--date", type=str, required=True, help='date in YYYY-MM-DD format')
    arg_parser.add_argument("--from", type=str, required=True, help='airfield IATA code')
    arg_parser.add_argument("--to", type=str, required=True, help='destination airfield IATA code')
    # optional arguments
    arg_parser.add_argument("--one-way", action="store_true", default='True', required=False, \
                help='no return ticket (default option)')
    arg_parser.add_argument("--return", type=int, required=False, help='specifies tiem of stay')
    arg_parser.add_argument("--fastest", '--cheapest', action="store_true", required=False, help='books the cheapest flight')
    # arg_parser.add_argument("--cheapest", action="store_true", required=False)    # TODO: not sure if right way
    arg_parser.add_argument("--bags", type=int, required=False, help='number of bags')


    args = arg_parser.parse_args()

    book_flight(args)


if __name__ == "__main__":
    main()
