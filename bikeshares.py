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
    print("Hello! Let's explore some US bikeshare data!\n")
    # get user input for city (chicago, new york city, washington)
    citylist = ['chicago', 'new york city', 'washington']
    cityname = ''
    city = ''
    while city.lower() not in citylist:
        city = input("Would you like data on 'chicago', 'new york city', or 'washington': ")
        if city.lower() not in citylist:
            print("Input not recognized. Please choose from the following: ", citylist)
    cityname = city.title()
    print("\nGreat, let's looks at data for {}.\n".format(cityname))
    # get user input for month (all, january, february, ... , june)
    monthlist = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = ''
    monthname = ''
    while month.lower() not in monthlist:
        month = input("Would you like data on 'all' months or a specific month like 'january', 'february', 'march', etc? (NOTE: Data only availible Jan - June): ")
        if month.lower() not in monthlist:
            print("Input not recognized. Please choose from the following:", monthlist)
    if month == 'all':
        monthname = 'all months'
    else:
        monthname = month.title()
    print("\nGreat, let's looks at data for {}.\n".format(monthname))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    daylist = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = ''
    dayname = ''
    while day.lower() not in daylist:
        day = input("Would you like data on 'all' days of the week or a specific day like 'monday', 'tuesday', 'wednesday', etc?: ")
        if day.lower() not in daylist:
            print("Input not recognized. Please choose from the following:", daylist)
    if day == 'all':
        dayname = 'all days of the week'
    else:
        dayname = day.title() + "s"
    print("\nGreat, let's looks at data for {}.\n".format(dayname))

    print('-'*40)

    print("\nWe will look at data for {} durring {} on {}.\n".format(cityname,monthname,dayname))
    city = city.lower()
    month = month.lower()
    day = day.lower()
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
    df['day_of_week'] = df['Start Time'].dt.day_name()
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
        df = df[df['day_of_week'] == day.title()]

    """While loop allows user to view as much of the raw data as they want"""
    raw = ""
    counter = 0
    try:
        while raw.lower() != "n":
            raw = input("Would you like to view 5 lines of the raw data? ('y'/'n'): ")
            if raw.lower() == "y":
                print(df[counter:counter+5])
                counter += 5
            elif raw.lower() != "n":
                print("Input was not understood. Please use 'y' for yes or 'n' for no.")
    except:
        print("No further data to view")

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    cmonth = df['month'].mode()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months[int(cmonth[0])-1]
    print("The most common month for travel was", month.title())
    # display the most common day of week
    cday = df['day_of_week'].mode()
    print("The most common day of the week for travel was", cday[0])
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    chour = df['hour'].mode()
    print("the most common start time was: {}:00 hours.".format(str(chour[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    cstart = df['Start Station'].mode()
    print("The most common start station was:", cstart[0])

    # display most commonly used end station
    cend = df['End Station'].mode()
    print("The most common end station was:", cend[0])

    # display most frequent combination of start station and end station trip
    df['sande'] = df['Start Station'] + " and " + df['End Station']
    csande = df['sande'].mode()
    print("The most common combination start and end station was:", csande[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tottime = df['Trip Duration'].sum()
    print("The total travel time for this data was {} hours or {} days.".format(round(tottime/3600,2),round(tottime/86400,2)))
    # display mean travel time
    avgtime = df['Trip Duration'].mean()
    print("The mean travel time for this data was {} seconds or {} minutes.".format(round(avgtime,2),round(avgtime/60,2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    utype = df['User Type'].value_counts()

    print("The count of user types for this data are as follows:")
    if "Dependent" in df['User Type']:
        print("Subscribers: {}\nCustomer: {}\nDependent: {}\n".format(utype['Subscriber'], utype['Customer'], utype['Dependent']))
        usersum = utype['Subscriber']+utype['Customer']+utype['Dependent']
        print("The percentage of usertype catagories are as follows:")
        print("Subscribers: {}%\nCustomers: {}%\nDependents: {}%\n".format(round(utype['Subscriber']/usersum*100,4), round(utype['Customer']/usersum*100,4), round(utype['Dependent']/usersum*100,4)))
    else:
        print("Subscribers: {}\nCustomer: {}\n".format(utype['Subscriber'], utype['Customer']))
        usersum = utype['Subscriber']+utype['Customer']
        print("The percentage of usertype catagories are as follows:")
        print("Subscribers: {}%\nCustomers: {}%\n".format(round(utype['Subscriber']/usersum*100,4), round(utype['Customer']/usersum*100,4)))

    # display counts of gender
    if city == "washington":
        print("Gender and Year of Birth data not avalible for Washington")
    else:
        gen = df['Gender'].value_counts()
        print("Users for this data had a gender split as follows:")
        print("Men: {}\nWomen: {}".format(gen['Male'],gen['Female']))
        print("\nThis data shows a user split of:")
        print("{}% men".format(round(int(gen['Male'])/(int(gen['Female'])+int(gen['Male']))*100,2)))
        print("{}% women\n".format(round(int(gen['Female'])/(int(gen['Male'])+int(gen['Female']))*100,2)))
        # display earliest, most recent, and most common year of birth
        print("For this data:")
        eby = df['Birth Year'].max()
        print("The most recent year of birth of a user was:", str(eby)[0:4])
        nby = df['Birth Year'].min()
        print("The earliest year of birth of a user was:",str(nby)[0:4])
        cby = df['Birth Year'].mode()
        print("The most common year of birth of a user was:",str(cby[0])[0:4])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
