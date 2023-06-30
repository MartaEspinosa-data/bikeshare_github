import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input("Which city would you like to explore? Chicago, New york city or Washington?: ").lower()
        if city not in ["chicago", "new york city", "washington"]:
            print("Sorry I didn't understand the city. Can you repeat it?")
            continue
        else:
            break


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to explore? January, February, March, April,May, June or type 'all' if you don't have a preference: \n").lower()
        if month not in ["january", "february","march","april","may","june", "all"]:
            print("Sorry I didn't understand. please try again")
            continue
        else:
            break       


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Please select a day of the week: Monday,Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday: \n").lower()
        if day not in ["monday", "tuesday", "wednesday", "thursday", "friday","saturday", "sunday"]:
            continue
        else:
            break


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
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        day_dict = {
            "monday" : 2,
            "tuesday" : 3,
            "wednesday" : 4,
            "thursday" : 5,
            "friday" : 6,
            "saturday" : 7,
            "sunday" : 1,
        }
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day_dict[day.lower()]]

    return df




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].value_counts().idxmax()
    print("the most common month is:", most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].value_counts().idxmax()
    print("The most common weekday is:", most_common_day)
    
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common hour is: ", df['hour'].value_counts().idxmax())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].value_counts().idxmax()
    print("The most common start station is " + start_station)
    
    # display most commonly used end station
    end_station = df['End Station'].value_counts().idxmax()
    print("The most common start station is " + end_station)

    # display most frequent combination of start station and end station trip
    most_common_combination_station = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print("Most common combination of start station and end station is " ,most_common_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_duration = df['Trip Duration'].sum() / 3600.0
    print("total travel time in hours is: ", total_travel_duration)   

    # display mean travel time
    mean_travel = df['Trip Duration'].sum() / 3600.0
    print("the mean travel time in hours is: ", mean_travel)



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print(user_types)

    # Display counts of gender
    try:
        gender = df["Gender"].value_counts()
        print(gender)
    except KeyError:
        print("No data available for this month")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df["Birth Year"].min())
        print(earliest_year)
    except KeyError:
        print("No data available for this month")
    
    try:
        most_recent_year = int(df["Birth Year"].max())
        print(most_recent_year)
    except KeyError:
        print("No data available for this month")

    try:   
        most_common_year = int(df["Birth Year"].value_counts().idxmax())
        print(most_common_year)
    except KeyError:
        print("No data available for this month")

    print(f"\nThis took {str(time.time() - start_time)} seconds.")
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data.lower() != 'no':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue? Enter yes or no: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
