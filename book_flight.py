# -*- coding: utf-8 -*-
import argparse
import json
import requests
import sys
# from urllib3 import Request, urlopen


def convert_date_format(date):
    new_format = ''
    date_split = date.split('-')
    new_format += date_split[0] + '/'
    new_format += date_split[1] + '/'
    new_format += date_split[2]
    return new_format

def create_dateTo(date):
    date_split = date.split('/')
    date_split[1] = str(int(date_split[1]) + 1)
    new_date = date_split[0] + '/'
    new_date += date_split[1] + '/'
    new_date += date_split[2]
    return new_date
    

def book_flight(args):
    date_from = convert_date_format(args.date)
    date_to = create_dateTo(date_from)
    # TOOD: ONE WAY / RETURN
    get_r_string = 'https://api.skypicker.com/flights?flyFrom={}&to={}&dateFrom={}&dateTo={}&passengers=1&partner=picky&typeFlight=oneWay&sort=price'.format(args._from, args.to, date_from, date_to)
    print(get_r_string)
    
    # TODO: try as payload for request

    try:
        # TODO: use special api to book
        r = requests.get(get_r_string)
        r.raise_for_status()
        print(r.status_code)
        cheapest = r.json()['data'][0]
        booking_token = cheapest['booking_token']   
        deep_link = cheapest['deep_link']
        
        # print(booking_token)
        # print('Cheapest from BTS to A')
        # print(json.dumps(cheapest, indent=4))
        # else:
        #     print('ERROR CONNECTING')
        #     return 0

        book_data = {'bags' : str(args.bags), 'booking_token' : booking_token}
            # 'booking_token' : '' + booking_token,
            # 'bags' : str(args.bags)
        # }
        
        book_request = requests.post(
            # 'http://128.199.48.38:8080/booking?booking_token={}'.format(booking_token))
            'http://128.199.48.38:8080/booking?bags=2')
        book_request.raise_for_status()
        # book_request = requests.post(
        #     'http://128.199.48.38:8080/booking', data=book_data)
        print(book_request.status_code)
        print(book_request.json())
        # print(book_request.content)


        # print(book_request.status_code)


    except requests.exceptions.RequestException as err:
        print(err)
        sys.exit(0)

    # print(json.dumps(r.json(), indent=4))


def main():
    """
    Main method.
    Uses argparse library to add arguments.
    --from and --return arguments use 
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--date", '-d', type=str, required=True,\
            help='date in YYYY-MM-DD format')
    arg_parser.add_argument('--from', dest='_from', type=str, required=True,\
            help='airfield IATA code')
    arg_parser.add_argument("--to", '-t', type=str, required=True,\
            help='destination airfield IATA code')
    # optional arguments
    arg_parser.add_argument("--one-way", action="store_true", default='True', required=False, \
            help='no return ticket (default option)')
    arg_parser.add_argument("--return", dest='_return', type=int, required=False, help='specifies tiem of stay')
    arg_parser.add_argument("--fastest", action="store_true", default='True', required=False, \
            help='books the fastest flight')
    arg_parser.add_argument("--cheapest", action="store_true", required=False)    # TODO: not sure if right way
    arg_parser.add_argument("--bags", type=int, required=False, default=0, help='number of bags')


    args = arg_parser.parse_args()
    # args_list = args.split()
    print(args._from)
    print(args.to)

    print(args._return)
    print(args.bags)

    book_flight(args)


if __name__ == "__main__":
    main()


# TODO: one-way
# TODO: return
# TODO: fastest, cheapest correct
# TODO: bags
