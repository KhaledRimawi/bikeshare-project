import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('\nWhich city would you like to analyze? (Chicago, New York, or Washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter Chicago, New York, or Washington.")
    
    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input('\nWhich month would you like to filter by? (all, January, February, March, April, May, June): ').lower()
        if month in months:
            break
        else:
            print("Invalid input. Please enter a valid month or 'all'.")
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('\nWhich day of the week would you like to filter by? (all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ').lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day or 'all'.")
    
    print('-'*40)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
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
        df = df[df['day_of_week'] == day]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    common_month = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f'Most Common Month: {months[common_month-1]}')
    
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0].title()
    print(f'Most Common Day of Week: {common_day}')
    
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {common_hour}')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print(f'Most Common Start Station: {common_start}')
    
    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print(f'Most Common End Station: {common_end}')
    
    # display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f'Most Common Trip: {common_trip}')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # display total travel time
    total_travel = df['Trip Duration'].sum()
    days = total_travel // 86400
    hours = (total_travel % 86400) // 3600
    minutes = (total_travel % 3600) // 60
    seconds = total_travel % 60
    print(f'Total Travel Time: {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds')
    
    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    minutes = mean_travel // 60
    seconds = mean_travel % 60
    print(f'Mean Travel Time: {int(minutes)} minutes, {int(seconds)} seconds')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of User Types:')
    for user_type, count in user_types.items():
        print(f'{user_type}: {count}')
    
    # Display counts of gender (if available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender:')
        for gender, count in gender_counts.items():
            print(f'{gender}: {count}')
    else:
        print('\nGender data not available for this city.')
    
    # Display earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print(f'\nEarliest Birth Year: {earliest}')
        print(f'Most Recent Birth Year: {most_recent}')
        print(f'Most Common Birth Year: {most_common}')
    else:
        print('\nBirth year data not available for this city.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays 5 rows of data at a time based on user input."""
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()
    start_loc = 0
    
    while view_data == 'yes':
        # Display 5 rows of data
        print(df.iloc[start_loc:start_loc+5].to_string())
        start_loc += 5
        
        # Check if user wants to continue viewing data
        view_data = input('\nWould you like to view the next 5 rows? Enter yes or no: ').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
