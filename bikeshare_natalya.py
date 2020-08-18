import time
import pandas as pd
import numpy as np

#Explore bikeshare data based on city, month, and day of the week data specified by user
#validate input paramenters and handle errors

CITY_DATA = { 'chicago': 'chicago.csv',
              'chi': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv',
              'wa': 'washington.csv' }

MONTHS_DATA = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'all'}

DAYS_DATA = {1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday', 7: 'sunday', 8: 'all'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''

    while city.lower() not in CITY_DATA.keys():
        city = input("Please enter City name selection as Chicago (CHI), New York City (NYC) or Washington (WA): ")
        city = city.lower()

        if city not in CITY_DATA.keys():
            print("Incorrect value. Please try again!")

    city_name, extention = CITY_DATA[city].split('.')
    print("You were intested to learn about: {}".format(city_name.title().replace('_',' ')))

    # get user input for month (all, january, february, ... , june)
    month = ''

    while month not in MONTHS_DATA.keys():
        try:
            month = int(input("Please enter month selection as 1 for January, 2 for February, 3 for March, 4 for April, 5 for May, 6 for June or 7 for All: "))
        except ValueError as ve:
            print(f'You entered incorrect selection for month, please use a number 1 - 7.')

        if month not in MONTHS_DATA.keys():
            print("Incorrect value. Please try again!")

    print("You were intested to get stats for : {}".format(MONTHS_DATA[month].capitalize()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''

    while day not in DAYS_DATA.keys():
        try:
            day = int(input("Please enter day of week selection as 1 for Mon, 2 for Tue, 3 for Wed, 4 for Thu, 5 for Fri, 6 for Sat, 7 for Sun or 8 for All: "))
        except ValueError as ve:
            print(f'You entered incorrect selection for day, please use a number 1 - 8.')

        if day not in DAYS_DATA.keys():
            print("Incorrect value. Please try again!")

    print("You were intested to get stats for : {}".format(DAYS_DATA[day].capitalize()))

    print('-'*40)
    return city, MONTHS_DATA[month], DAYS_DATA[day]


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and Start hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.capitalize()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month to travel:', MONTHS_DATA[common_month].capitalize())

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most common day of week to travel:', common_day_of_week)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour to travel:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(f"The most popular Start Station: {popular_start_station}")

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(f"The most popular End Station: {popular_end_station}")

    # display most frequent combination of start station and end station trip
    df['start_end_station_pair'] = df['Start Station'].str.cat(df['End Station'], sep = ' and ')
    popular_start_end_station_pair = df['start_end_station_pair'].mode()[0]
    print(f"The most popular Start to End Station trip: {popular_start_end_station_pair}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_duration = df['Trip Duration'].sum()
    # breakdown total duration time from seconds to hours, minutes, seconds
    minute, second = divmod(total_travel_duration, 60)
    hour, minute = divmod(minute, 60)
    second = round(second)

    print(f"Total Trip Duration: {hour} hours, {minute} minutes and {second} seconds")

    # display mean travel time rounding mean result to whole number
    mean_travel_duration = round(df['Trip Duration'].mean())
    # breakdown total duration time from seconds to hours, minutes, seconds
    minute, second = divmod(mean_travel_duration, 60)
    hour, minute = divmod(minute, 60)
    second = round(second)

    print(f"Average Trip Duration: {hour} hours, {minute} minutes and {second} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"The counts by user type:\n\n{user_type}")

    # display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe counts by gender:\n\n{gender}")
    except:
        print("\nNo gender data in the file!")

    # display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('\nUser Birth Year Stats...\n')
        print(f"The earliest Birth Year: {earliest_birth_year}, Most recent Birth Year: {recent_birth_year}, Most common Birth Year: {common_birth_year}")
    except:
        print("\nNo Birth Year data in the file!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw data on users request."""
    start_time = time.time()
    display = ''
    n = 5
    m = 0

    display = input('\nWould you like to see some raw data? Enter yes or no.\n')

    while display.lower() not in ['n', 'no']:

        if display.lower() in ['y','yes']:
            # show first 5 records from the file
            print('\nRetrieving raw data...\n')
            print(df.iloc[m:n])
            n += 5
            m += 5
        else:
            print("Incorrect value. Please try again!")

        display = input('\nWould you like to see more raw data? Enter yes or no.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
