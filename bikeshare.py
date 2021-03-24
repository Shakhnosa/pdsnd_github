import datetime
import time
import calendar

import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    month = 'all'
    day = 'all'

    #Here im getting filters by city,month,day and all
    while True:
        city = input('Enter a city name: ').lower()
        if city not in CITY_DATA:
            print('Incorrect city name! \n Please choose either Chicago, New York, or Washington')
        else:
            print('You selected the city: {}'.format(city))
            break

    while True:
        time = input("Filter by month, day, all:  ").lower()
        if time == 'month':
            while True:
                month = input("Choose one of these months: \nJanuary \nFebruary \nMarch \nApril \nMay  \nJune: ").lower()
                if month.title() in calendar.month_name:
                    break
                else:
                    print("Unknown month: {}".format(month))
            break
        elif time == 'day':
            while True:
                day = input("Choose one of these days: \nMonday \nTuesday \nWednesday \nThursday \nFriday \nSaturday \nSunday: ").lower()
                if day.title() in calendar.day_name:
                    break
                else:
                    print("Unknown day: {}".format(day))
            break
        elif time == 'all':
            break
        else:
            print("You entered a wrong city name, please write again: ")

    print(city)
    print(month)
    print(day)
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Load data file into a dataframe
    #Convert the Start Time column to datetime
    #Extract month and day of week from Start Time to create new columns
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    if not df['month'].empty:
        common_month = df['month'].mode()[0]
        print("Most common month: {}".format(calendar.month_name[int(common_month)]))

    # Display the most common day of week
    if not df['day_of_week'].empty:
        common_day_of_week = df['day_of_week'].mode()[0]
        print("Most common day of week: {}".format(common_day_of_week))

    # Display the most common start hour
    if not df['day_of_week'].empty:
        common_hour = df['hour'].mode()[0]
        print("Most common start hour: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("Most common start station: {}".format(common_start))

    #Display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("Most common end station: {}".format(common_end))

    #Display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + ' to ' + df['End Station']
    common_combination = df['combination'].mode()[0]
    print("Most frequent combination: {}".format(common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time: {}".format(str(datetime.timedelta(seconds=int(total_time)))))

    #Display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean travel time: {}".format(str(datetime.timedelta(seconds=int(mean_time)))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].value_counts()
    print(users)

    # Display counts of gender,Washington has no gender
    if 'Gender' in df:
        genders = df['Gender'].value_counts()
        print(genders)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        print("Earliest birth year: {}".format(int(earliest)))

        recent = df['Birth Year'].max()
        print("Most recent birth year: {}".format(int(recent)))

        common_birth = df['Birth Year'].mode()[0]
        print("Median common birth year: {}".format(int(common_birth)))
    else:
        print("No information.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    pd.set_option('display.max_columns',180)

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        start=0
        end=5
        while True:
            more = input('\nWould you like some data? Enter yes or no.\n').lower()
            if more == 'yes':
                print(df.iloc[start:end])
                start+=5
                end+=5
            elif more == 'no':
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
