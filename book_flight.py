# -*- coding: utf-8 -*-
import argparse
import json
import requests
import sys


def iata_code(code):
    if len(code) == 3:
        return code.upper()
    else:
        raise argparse.ArgumentTypeError('Not a correct IATA code!')

def date_type(date):
    pass

def convert_date_format(date):
    return date.replace('-', '/')


def create_dateTo(date):
    date_split = date.split('/')
    date_split[1] = str(int(date_split[1]) + 1)
    return '/'.join(date_split)

def create_request_url(fly_from, fly_to, date, fly_back, flights_sort):
    """
    Creates the url for GET request used in get_booking_token using arguments passed to the program.

    fly_from: flight start point.
    fly_to: flight destination.
    date: date of the flight.
    fly_back: type of the flight (one way / round)
    flight_sort: sorts the flight either by price (--cheapest) or duration (--fastest)
    return: string containing the url
    """
    type_flight = 'oneWay'
    days_in_destination_from = '1'

    # check if round flight
    if fly_back != None and fly_back > 0:
        days_in_destination_from = str(fly_back)
        type_flight = 'round'
    days_in_destination_to = days_in_destination_from

    if flights_sort == None:
        flights_sort = 'price'

    date_from = convert_date_format(date)

    # TODO: date range?
    date_to = create_dateTo(date_from)

    url = 'https://api.skypicker.com/flights?'
    url += 'flyFrom=' + fly_from
    url += '&to=' + fly_to
    url += '&dateFrom=' + date_from
    url += '&dateTo=' + date_from
    url += '&typeFlight=' + type_flight
    url += '&sort=' + flights_sort
    url += '&daysInDestinationFrom=' + days_in_destination_from
    url += '&daysInDestinationTo=' + days_in_destination_to
    url += '&curr=eur'
    url += '&limit=1'
    return url


def get_booking_token(fly_from, fly_to, date, fly_back, flights_sort):
    """
    Finds flight with given arguments.

    fly_from: start arfield IATA code.
    fly_to: destination airfiled IATA code.
    return: string with flights booking_token if a flight was found, an empty sting otherwise.
    """
    # create a url for get request
    url = create_request_url(fly_from, fly_to, date, fly_back, flights_sort)
    r = requests.get(url)
    # raise an exception for a http status code
    r.raise_for_status()
    response_data = r.json()['data']

    # string for a booking token
    booking_token = ''
    
    # TODO: not sure if correct
    # if flight waas found
    if len(response_data) > 0:
        booking_token = response_data[0]['booking_token']
        print('Found a flight! (Price: {} EUR)\n'.format(response_data[0]['price']))
        
    return booking_token


def book_flight(fly_from, fly_to, date, fly_back, flights_sort, bags):
    """
    Tries to book a flight using passed arguments.

    fly_from: flight start point.
    fly_to: flight destination.
    date: date of the flight.
    fly_back: type of the flight (one way / round).
    flight_sort: sorts the flight either by price (--cheapest) or duration (--fastest).
    bags: number of bags.
    return: reservation confirmation number if a flight was found, 0 otherwise
    """
    try:
        # get booking token using passed arguments
        booking_token = get_booking_token(fly_from, fly_to, date, fly_back, flights_sort)
        # if a flight was found
        if len(booking_token) > 0:
            # reservation number
            reservation_code = get_booking_reservation_code(booking_token, bags)
            # return reservation number
            return 'Succesfully booked a flight. Reservation code: ' + reservation_code
        else:
            print('Can\'t find a flight with given parameters.')
            return 0
    except requests.exceptions.RequestException as err:
        print(err)
        return 0


def get_booking_reservation_code(booking_token, bags):
    """
    Retrieves booking number.   

    booking_token: booking token retrieved by :get_booking_token
    bags: number of bags
    return: string containing the booking confirmation number
    """
    url = "http://128.199.48.38:8080/booking"

    # payload data
    booking_data = {
        "bags" : bags,
        "passengers" : {
            "documentID": "123456789",
            "birthday": "1964-01-02",
            "title" : "Mr",
            "firstName": "Bojack",
            "lastName": "Horseman",
            "email": "horseman@bojack.com"
        },
        "currency" : "EUR",
        "booking_token" : booking_token
    }
    
    headers = {"content-type" : "application/json"}

    book_request = requests.post(url, data=json.dumps(booking_data), headers=headers)
    # raise an exception for http error
    book_request.raise_for_status()
    # return confirmation number
    return book_request.json()["pnr"]
    

def main():
    """
    Main method.
    Uses argparse library to add arguments.
    --from and --return arguments use 
    """
    arg_parser = argparse.ArgumentParser()
    # required arguments
    arg_parser.add_argument("--date", '-d', type=str, required=True,\
            help='date in YYYY-MM-DD format')
    arg_parser.add_argument('--from', dest='fly_from', type=iata_code, required=True,\
            help='airfield IATA code')  
    arg_parser.add_argument("--to", '-t', dest='fly_to', type=iata_code, required=True,\
            help='destination airfield IATA code')
    
    # optional arguments
    arg_parser.add_argument("--one-way", dest='fly_back', action="store_const", const=None,
            help='one way flight')

    arg_parser.add_argument("--return", dest='fly_back', type=int, required=False, default=0, \
        help='specify time of stay and book return ticket')

    # luggage
    arg_parser.add_argument("--bags", type=int, required=False, default=0, help='number of bags')

    # sort argumnets
    arg_parser.add_argument("--cheapest", action="store_const", dest='flights_sort', const='price', required=False) 
    arg_parser.add_argument("--fastest", action="store_const", dest='flights_sort', const='duration', required=False, \
            help='books the fastest flight')
    # TODO: date as date_type, convert it right away

    args = arg_parser.parse_args()

    print(book_flight(args.fly_from, args.fly_to, args.date, args.fly_back, args.flights_sort, args.bags))


if __name__ == "__main__":
    main()


# TODO: chage date format