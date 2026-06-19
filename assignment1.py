#!/usr/bin/env python3
'''
OPS445 Assignment 1
Program: assignment1.py
Author: "Jahid Ahmmed"
Semester: "Summer 2026"

The python code in this file (assignment1.py) is original work written by
"Jahid Ahmmed". No code in this file is copied from any other source
except those provided by the course instructor, including any person,
textbook, or on-line resource. I have not shared this python script
with anyone or anything except for submission for grading. I understand
that the Academic Honesty Policy will be enforced and
violators will be reported and appropriate action will be taken.

Description: This script calculates the number of weekend days
(Saturdays and Sundays) between two dates provided by the user.
'''

import sys


def usage():
    '''
    Prints a usage message to the user when invalid arguments are given,
    then exits the program.
    '''
    print("Usage: assignment1.py YYYY-MM-DD YYYY-MM-DD")
    print("Please provide two valid dates in YYYY-MM-DD format.")
    sys.exit(1)


def leap_year(year: int) -> bool:
    '''
    Returns True if the given year is a leap year, False otherwise.
    Accounts for the century and 400-year rules.
    '''
    if year % 400 == 0:
        return True      # divisible by 400 is always a leap year
    if year % 100 == 0:
        return False     # divisible by 100 but not 400 is not a leap year
    if year % 4 == 0:
        return True      # divisible by 4 is a leap year
    return False         # all other years are not leap years


def mon_max(month: int, year: int) -> int:
    '''
    Returns the maximum number of days in a given month and year.
    Uses leap_year() to determine February's days.
    '''
    feb_max = 29 if leap_year(year) else 28  # Feb has 29 days in leap years
    mon_dict = {1: 31, 2: feb_max, 3: 31, 4: 30, 5: 31, 6: 30,
                7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    return mon_dict[month]


def after(date: str) -> str:
    '''
    after() -> date for next day in YYYY-MM-DD string format

    Return the date for the next day of the given date in YYYY-MM-DD format.
    This function takes care of the number of days in February for leap year.
    This function has been tested to work for years after 1582.
    '''
    str_year, str_month, str_day = date.split('-')
    year = int(str_year)
    month = int(str_month)
    day = int(str_day)

    tmp_day = day + 1  # move to the next day

    if tmp_day > mon_max(month, year):
        to_day = 1          # reset day to 1 when past month's max
        tmp_month = month + 1
    else:
        to_day = tmp_day
        tmp_month = month

    if tmp_month > 12:
        to_month = 1        # reset month to January when past December
        year += 1           # increment the year
    else:
        to_month = tmp_month

    return f"{year}-{to_month:02}-{to_day:02}"


def before(date: str) -> str:
    '''
    Returns the previous day's date in YYYY-MM-DD format.
    '''
    str_year, str_month, str_day = date.split('-')
    year = int(str_year)
    month = int(str_month)
    day = int(str_day)

    tmp_day = day - 1  # move to the previous day

    if tmp_day < 1:
        tmp_month = month - 1   # go back a month if day goes below 1
        if tmp_month < 1:
            to_month = 12       # wrap back to December
            year -= 1           # decrement year
        else:
            to_month = tmp_month
        to_day = mon_max(to_month, year)  # last day of previous month
    else:
        to_day = tmp_day
        to_month = month

    return f"{year}-{to_month:02}-{to_day:02}"


def day_of_week(date: str) -> str:
    '''
    Returns the day of the week for a given date string in YYYY-MM-DD format.
    Returns a 3-letter lowercase abbreviation: mon, tue, wed, thu, fri, sat, sun.
    Uses Tomohiko Sakamoto algorithm.
    '''
    str_year, str_month, str_day = date.split('-')
    year = int(str_year)
    month = int(str_month)
    day = int(str_day)

    days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    if month < 3:
        year -= 1
    day_num = (year + year // 4 - year // 100 + year // 400 + t[month - 1] + day) % 7
    return days[day_num]

def valid_date(date: str) -> bool:
    '''
    Returns True if the given date string is a valid date in YYYY-MM-DD format.
    Checks that the year, month, and day are all within acceptable ranges.
    '''
    try:
        parts = date.split('-')
        if len(parts) != 3:
            return False   # must have exactly 3 parts
        str_year, str_month, str_day = parts
        if len(str_year) != 4:
            return False   # year must be exactly 4 digits
        year = int(str_year)
        month = int(str_month)
        day = int(str_day)
    except ValueError:
        return False   # not in correct format or non-integer parts

    if month < 1 or month > 12:
        return False   # month must be between 1 and 12

    if day < 1 or day > mon_max(month, year):
        return False   # day must be valid for that month and year

    return True


def day_count(start_date: str, end_date: str) -> int:
    '''
    Counts and returns the number of weekend days (Saturdays and Sundays)
    between start_date and end_date, inclusive of both dates.
    Both dates should be in YYYY-MM-DD format.
    '''
    weekend_count = 0
    current_date = start_date  # begin at the start date

    while current_date <= end_date:
        day = day_of_week(current_date)   # get name of the day
        if day in ('sat', 'sun'):
            weekend_count += 1            # count it if it's a weekend
        current_date = after(current_date)  # advance to the next day

    return weekend_count


if __name__ == "__main__":

    # check that exactly 2 date arguments were provided
    if len(sys.argv) != 3:
        usage()

    date1 = sys.argv[1]
    date2 = sys.argv[2]

    # validate both dates
    if not valid_date(date1) or not valid_date(date2):
        usage()

    # ensure start_date is always the earlier date, even if entered in wrong order
    if date1 <= date2:
        start_date = date1
        end_date = date2
    else:
        start_date = date2
        end_date = date1

    # calculate and display the result
    count = day_count(start_date, end_date)
    print(f"The period between {start_date} and {end_date} includes {count} weekend days.")
