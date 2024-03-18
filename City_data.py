import pandas as pd

def processData(city_data):
    # Convert 'Start Time' to datetime format
    city_data['Start Time'] = pd.to_datetime(city_data['Start Time'])
    
    # Extract month, day of week, and hour of day
    city_data['Month'] = city_data['Start Time'].dt.month_name()
    city_data['Day of Week'] = city_data['Start Time'].dt.day_name()
    city_data['Hour of Day'] = city_data['Start Time'].dt.hour
    
    return city_data

def popular_times_of_travel(city_data):
    most_common_month = city_data['Month'].mode()[0]
    most_common_day_of_week = city_data['Day of Week'].mode()[0]
    most_common_hour_of_day = city_data['Hour of Day'].mode()[0]
    
    return most_common_month, most_common_day_of_week, most_common_hour_of_day

def popular_stations_and_trip(city_data):
    most_common_start_station = city_data['Start Station'].mode()[0]
    most_common_end_station = city_data['End Station'].mode()[0]
    most_common_trip = city_data.groupby(['Start Station', 'End Station']).size().idxmax()
    
    return most_common_start_station, most_common_end_station, most_common_trip

def tripDuration(city_data):
    total_travel_time = city_data['Trip Duration'].sum()
    average_travel_time = city_data['Trip Duration'].mean()
    
    return total_travel_time, average_travel_time

def userInfo(city_data):
    user_type_counts = city_data['User Type'].value_counts()
    gender_counts = city_data['Gender'].value_counts() if 'Gender' in city_data else None
    birth_year_info = (city_data['Birth Year'].min(), city_data['Birth Year'].max(), city_data['Birth Year'].mode()[0]) if 'Birth Year' in city_data else None
    
    return user_type_counts, gender_counts, birth_year_info

# Load data from CSV files
dataframes = {}
for city in ['chicago', 'new_york_city', 'washington']:
    dataframes[city] = pd.read_csv(f'{city}.csv')

def select_city():
    while True:
        city = input("Enter a city name (chicago, new_york_city, washington): ").lower()
        if city in dataframes:
            return city
        else:
            print("Invalid city name. Please try again.")

def select_month():
    while True:
        try:
            month = input("Enter a month (January, February, March, April, May, or June): ").title()
            if month.lower() in ['january', 'february', 'march', 'april', 'may', 'june']:
                return month
            else:
                raise ValueError
        except ValueError:
            print("Invalid month. Please try again.")

def select_day():
    while True:
        try:
            day = input("Enter a day of the week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ").title()
            if day.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                return day
            else:
                raise ValueError
        except ValueError:
            print("Invalid day. Please try again.")

def display_data(city_data):
    start_idx = 0
    while True:
        show_data = input("Do you want to see 5 rows of data? Enter yes or no: ")
        if show_data.lower() != 'yes':
            break
        print(city_data.iloc[start_idx:start_idx+5])
        start_idx += 5

while True:
    city = select_city()
    print(f"City: {city.title()}\n")
    data = processData(dataframes[city])
    
    most_common_month, most_common_day_of_week, most_common_hour_of_day = popular_times_of_travel(data)
    print("1. Popular times of travel:")
    print(f"- Most common month: {most_common_month}")
    print(f"- Most common day of week: {most_common_day_of_week}")
    print(f"- Most common hour of day: {most_common_hour_of_day}\n")

    most_common_start_station, most_common_end_station, most_common_trip = popular_stations_and_trip(data)
    print("2. Popular stations and trip:")
    print(f"- Most common start station: {most_common_start_station}")
    print(f"- Most common end station: {most_common_end_station}")
    print(f"- Most common trip from start to end: {most_common_trip}\n")

    total_travel_time, average_travel_time = tripDuration(data)
    print("3. Trip duration:")
    print(f"- Total travel time: {total_travel_time} seconds")
    print(f"- Average travel time: {average_travel_time} seconds\n")

    user_type_counts, gender_counts, birth_year_info = userInfo(data)
    print("4. User info:")
    print("- Counts of each user type:")
    print(user_type_counts.to_string())
    if gender_counts is not None:
        print("\n- Counts of each gender:")
        print(gender_counts.to_string())
    if birth_year_info is not None:
        print("\n- Earliest, most recent, most common year of birth:")
        print(f"  Earliest: {birth_year_info[0]}")
        print(f"  Most recent: {birth_year_info[1]}")
        print(f"  Most common: {birth_year_info[2]}")
    print("\n")

    month = select_month()
    day = select_day()

    filtered_data = data[(data['Month'] == month) & (data['Day of Week'] == day)]

    most_common_hour_of_day_filtered = filtered_data['Hour of Day'].mode()[0]
    print(f"Most common hour of the day for {month} on {day}: {most_common_hour_of_day_filtered}\n")

    display_data(filtered_data)

    restart = input("Would you like to restart? Enter yes or no: ")
    if restart.lower() != 'yes':
        break
