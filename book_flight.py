# -*- coding: utf-8 -*-
import argparse
import json
import requests
import sys


def convert_date_format(date):
    new_format = ''
    date_split = date.split('-')
    new_format += date_split[0] + '/'
    new_format += date_split[1] + '/'
    new_format += date_split[2]
    return new_format

def book_flight(args):
    date = convert_date_format(args.date)
    get_r_string = 'https://api.skypicker.com/flights?flyFrom={}&to={}&dateFrom={}&dateTo=1/2/2018&sort=price'.format(args.from_f, args.to, date)
    print(get_r_string)
    r = requests.get(get_r_string)
    print(r.status_code)
    cheapest = r.json()['data'][0]

    print('Cheapest form BTS to A')
    print(json.dumps(cheapest, indent=4))
    # print(json.dumps(r.json(), indent=4))


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--date", '-d', type=str, required=True, help='date in YYYY-MM-DD format')
    arg_parser.add_argument('--from' '-f', type=str, required=True, help='airfield IATA code')
    arg_parser.add_argument("--to", '-t', type=str, required=True, help='destination airfield IATA code')
    # optional arguments
    arg_parser.add_argument("--one-way", action="store_true", default='True', required=False, \
                help='no return ticket (default option)')
    arg_parser.add_argument("--return", type=int, required=False, help='specifies tiem of stay')
    arg_parser.add_argument("--fastest", '--cheapest', action="store_true", required=False, help='books the cheapest flight')
    # arg_parser.add_argument("--cheapest", action="store_true", required=False)    # TODO: not sure if right way
    arg_parser.add_argument("--bags", type=int, required=False, help='number of bags')


    args = arg_parser.parse_args()
    print(args.from_f)
    print(args.to)

    book_flight(args)


if __name__ == "__main__":
    main()
