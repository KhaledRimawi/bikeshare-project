import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_user_input(prompt_msg, valid_options):
    """Helper function to get validated user input"""
    while True:
        user_input = input(prompt_msg).lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please enter one of: {', '.join(valid_options)}.")

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    city = get_user_input('\nWhich city would you like to analyze? (Chicago, New York, or Washington): ', CITY_DATA.keys())

    month = get_user_input(
        '\nWhich month would you like to filter by? (all, January, February, ..., June): ',
        ['all'] + MONTHS
    )

    day = get_user_input(
        '\nWhich day of the week would you like to filter by? (all, Monday, Tuesday, ..., Sunday): ',
        ['all'] + DAYS
    )

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads and filters bikeshare data based on city, month, and day.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_num = MONTHS.index(month) + 1
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start = time.time()

    common_month = df['month'].mode()[0]
    print(f'Most Common Month: {MONTHS[common_month - 1].title()}')

    common_day = df['day_of_week'].mode()[0]
    print(f'Most Common Day of Week: {common_day.title()}')

    common_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {common_hour}')

    print(f"\nThis took {time.time() - start:.2f} seconds.")
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trips."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start = time.time()

    print(f'Most Common Start Station: {df["Start Station"].mode()[0]}')
    print(f'Most Common End Station: {df["End Station"].mode()[0]}')

    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    print(f'Most Common Trip: {df["Trip"].mode()[0]}')

    print(f"\nThis took {time.time() - start:.2f} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start = time.time()

    total = int(df['Trip Duration'].sum())
    mean = int(df['Trip Duration'].mean())

    print(f'Total Travel Time: {total // 86400}d {total % 86400 // 3600}h {total % 3600 // 60}m {total % 60}s')
    print(f'Mean Travel Time: {mean // 60}m {mean % 60}s')

    print(f"\nThis took {time.time() - start:.2f} seconds.")
    print('-' * 40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start = time.time()

    print('Counts of User Types:')
    print(df['User Type'].value_counts().to_string())

    if 'Gender' in df.columns:
        print('\nCounts of Gender:')
        print(df['Gender'].value_counts().to_string())
    else:
        print('\nGender data not available.')

    if 'Birth Year' in df.columns:
        print(f"\nEarliest Birth Year: {int(df['Birth Year'].min())}")
        print(f"Most Recent Birth Year: {int(df['Birth Year'].max())}")
        print(f"Most Common Birth Year: {int(df['Birth Year'].mode()[0])}")
    else:
        print('\nBirth year data not available.')

    print(f"\nThis took {time.time() - start:.2f} seconds.")
    print('-' * 40)

def display_data(df):
    """Displays 5 rows of data based on user input."""
    show_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()
    i = 0
    while show_data == 'yes':
        print(df.iloc[i:i+5].to_string(index=False))
        i += 5
        show_data = input('\nView next 5 rows? Enter yes or no: ').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        if input('\nWould you like to restart? Enter yes or no: ').lower() != 'yes':
            break

if __name__ == "__main__":
    main()
