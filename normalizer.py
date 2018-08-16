#!/usr/bin/env python

import fileinput
import csv
from datetime import datetime, timedelta
import sys


def convert_datetime(input):
    """Converts datetime string to datetime object in ISO-8601 format, adjusted for EST"""
    return (datetime.strptime(input, '%m/%d/%y %I:%M:%S %p') + timedelta(hours=3)).isoformat()


def format_zip(input):
    """Formats zipcode input as 5 digits. Assume 0 as prefix if input is less than 5 digits"""
    return str(int(input)).zfill(5)


def convert_to_seconds(input):
    """Convert duration input to floating point seconds format"""
    duration = input.split(':')
    _hours = duration[0]
    _mins = duration[1]
    _rest = duration[2].split('.')
    _seconds = _rest[0]
    _ms = _rest[1]
    total = (int(_hours) * 3600) + (int(_mins) * 60) + \
        int(_seconds) + ((int(_ms)/1000) % 60)
    return total


def validate_address(input):
    """Validate address to account for quoted strings"""
    str_output = input
    if ',' in input:
        str_output = '"{}"'.format(str_output)
    return str_output


# Read input as csv
# csv module will account for commas in address column
inputstring = csv.reader(fileinput.input())
# do not process headers
headers = next(inputstring)
print(','.join(headers))


for line in inputstring:
    processed_line = []
    timestamp = convert_datetime(line[0])
    processed_line.append(timestamp)

    address = validate_address(line[1])
    processed_line.append(address)

    _zip = format_zip(line[2])
    processed_line.append(_zip)

    # Convert names to uppercase
    _name = line[3].upper()
    processed_line.append(_name)

    _fooduration = convert_to_seconds(line[4])
    _barduration = convert_to_seconds(line[5])

    processed_line.append(str(_fooduration))
    processed_line.append(str(_barduration))

    _totalduration = float(_fooduration) + float(_barduration)
    processed_line.append(str(_totalduration))

    processed_line.append(str(line[7]))

    # On decode error, replace with default replacement character
    _processed = [x.decode(encoding='utf-8', errors='replace')
                  for x in processed_line]

    # Set stdout's encoding to avoid UnicodeEncodeError
    encoding = sys.stdout.encoding or 'utf-8'
    print(",".join(_processed).encode(encoding))
