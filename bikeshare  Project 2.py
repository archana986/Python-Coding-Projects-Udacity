import csv
import calendar
import datetime
from collections import Counter
from operator import itemgetter
import pprint
import time

def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.
    
    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n')
    city=str(city)
    if city.lower() == 'chicago':
        city = 'chicago'
    elif city.lower() == 'new york':
        city = 'new_york_city'
    elif city.lower() == 'washington':
        city = 'washington'
    else:
        print('We do not have this information\n')
        city = 'none'   
    return city

def load_cityfile(city):
    '''Loads the city file and the transformed columns to a list of dictionaries to be used in other functions.
    
    Args:
        city name.
    Returns:
        
        list of dictionaries containing bikeshare data
    '''
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    csvfile = city+'.csv'
    
    with open(csvfile) as f:
        open_city_file = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]
    city_file = []
    cnt = 0
    for row in open_city_file:
            CityDict = {}
            CityDict['Start_Time'] = datetime.datetime.strptime(row['Start Time'], DATETIME_FORMAT)
            CityDict['Start_Time_Month'] = datetime.datetime.strptime(row['Start Time'], DATETIME_FORMAT).strftime('%m')
            CityDict['Start_Time_Month_Nm'] = datetime.datetime.strptime(row['Start Time'], DATETIME_FORMAT).strftime('%B')
            CityDict['Start_Time_Day'] = datetime.datetime.strptime(row['Start Time'], DATETIME_FORMAT).strftime('%A')
            CityDict['Start_Time_Hr'] = datetime.datetime.strptime(row['Start Time'], DATETIME_FORMAT).strftime('%H')
            CityDict['End_time'] = datetime.datetime.strptime(row['End Time'], DATETIME_FORMAT)
            CityDict['duration'] = int(float(row['Trip Duration']))
            CityDict['Start_St'] = row['Start Station']
            CityDict['End_St'] = row['End Station']
            CityDict['Trip'] = '|'+row['Start Station']+' to '+row['End Station']+'|'
            if row['User Type'] == 'Customer':
                CityDict['User_Type'] = 'Customer'
            elif row['User Type'] == 'Subscriber':
                CityDict['User_Type'] = 'Subscriber'
            else:
                CityDict['User_Type'] = 'Unknown'
            if 'Gender' not in row:
                CityDict['Gender'] = 'U'
            else:
                if row['Gender'] == 'Male':
                    CityDict['Gender'] = 'Male'
                elif row['Gender'] == 'Female':
                    CityDict['Gender'] = 'Female'
                else:
                    CityDict['Gender'] = 'Unknown'
            if 'Birth Year' in row:
                try:
                    CityDict['Y_O_B'] = int(float(row['Birth Year']))
                except ValueError:
                    CityDict['Y_O_B'] = 0
            else:
                CityDict['Y_O_B'] = 0
            city_file.append(CityDict)
            cnt += 1
    return city_file

def get_month():
    '''Asks the user for a month and returns the specified month.

    Args:
        none.
    Returns:
        (str) Name of the "Month" for a city's bikeshare data.
    '''
    month = input('\nWhich month? January, February, March, April, May, or June?\n')
    month=str(month).lower().title()
    return month

def get_day():
    '''Asks the user for a day and returns the specified day.
    
    Args:
        none.
    Returns:
        (int) "Day number" for which you need city's bikeshare data and return the day of the week
    '''
    day = input('\nWhich day? Please type your response as an integer, 1 = Monday, 2 = Tuesday, 3= Wednesday, 4= Thursday, 5=Friday, 6=Saturday and 7=Sunday.\n')
    day=int(day)-1
    day=calendar.day_name[day]
    return day

def get_time_period():
    '''Asks the user for a time period and returns the specified filter.
    
    Args:
        none.
    Returns:
        (str) Choice of "Month" & Name of the month (OR) Day and Day Name (OR) None,  for a city's bikeshare data.
    '''
    timefilter = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
    timefilter=str(timefilter).lower()
    if timefilter=="month":
        month = get_month()
        time_period=(timefilter,month)
        return (time_period)
    elif timefilter=="day":
        day = get_day()
        time_period=(timefilter,day)
        return (time_period)
    else:
        timefilter=="none"
        time_period = (timefilter,'none')
        return (time_period)

def popular_month(city,city_file):
    ''' Question:  What is the most popular month for start time?
        
    Args:
        city,cityfile            
        Returns: none.
    '''
    popularmonth = Counter(k['Start_Time_Month_Nm'] for k in city_file if k.get('Start_Time_Month_Nm')) 
    for Start_Time_Month_Nm, count in popularmonth.most_common(1):
         print ("The most popular month for the city: {}'s bikeshare data is {} with {} occurrences.".format(city,Start_Time_Month_Nm,str(count)))

def popular_day(city,city_file, time_period):
    '''Question: What is the most popular day of week (Monday, Tuesday, etc.) for start time? If the filter chosen has a timeperiod, filter based on that
    
    Args:
        city,city_file, time_period
    Returns: Most popular Day with a print statement of the month and occurrences.
    '''
    timefilter=time_period[0]
    timefilter_nm=time_period[1]
    if timefilter == 'month':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Month_Nm'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                popularday = Counter(k['Start_Time_Day'] for k in cityfilemonth if k.get('Start_Time_Day')) 
                for Start_Time_Day, count in popularday.most_common(1):
                    print ("The most popular day for the city :{}'s bikeshare data with filters: ({},{}) is {} with {} occurrences.".format(city,timefilter,timefilter_nm,Start_Time_Day,str(count))) 
    else:
            popularday = Counter(k['Start_Time_Day'] for k in city_file if k.get('Start_Time_Day')) 
            for Start_Time_Day, count in popularday.most_common(1):
                print ("The most popular day for the city :{}'s bikeshare data is {} with {} occurrences.".format(city,Start_Time_Day,str(count)))
               
def popular_hour(city,city_file, time_period):
    '''Question: What is the most popular Hour for start time? If the filter chosen has a timeperiod, filter based on that
    
    Args:
        city,city_file, time_period
    Returns: none.
    '''
    timefilter=time_period[0]
    timefilter_nm=time_period[1]
    if timefilter == 'month':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Month_Nm'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                popularhour = Counter(k['Start_Time_Hr'] for k in cityfilemonth if k.get('Start_Time_Hr')) 
                for Start_Time_Hr, count in popularhour.most_common(1):
                    print ("The most popular hour for the city :{}'s bikeshare data with filters: ({},{}) is {} with {} occurrences.".format(city,timefilter,timefilter_nm,Start_Time_Hr,str(count))) 
    elif timefilter == 'day':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Day'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                popularhour = Counter(k['Start_Time_Hr'] for k in cityfilemonth if k.get('Start_Time_Hr')) 
                for Start_Time_Hr, count in popularhour.most_common(1):
                    print ("The most popular hour for the city :{}'s bikeshare data with filters: ({},{}) is {} with {} occurrences.".format(city,timefilter,timefilter_nm,Start_Time_Hr,str(count)))     
    else:
            popularhour = Counter(k['Start_Time_Hr'] for k in city_file if k.get('Start_Time_Hr')) 
            for Start_Time_Hr, count in popularhour.most_common(1):
                print ("The most popular hour for the city :{}'s bikeshare data is {} with {} occurrences.".format(city,Start_Time_Hr,str(count)))

def trip_duration(city,city_file, time_period):
    '''
    Question: What is the total trip duration and average trip duration? If the filter chosen has a timeperiod, filter based on that
    
    Args:
        city,city_file, time_period
    Returns: none.
    '''
    timefilter=time_period[0]
    timefilter_nm=time_period[1]
    if timefilter == 'month':
           cityfilemonth = list(filter(lambda x : x ['Start_Time_Month_Nm'] in timefilter_nm, city_file))
           if cityfilemonth==[]:
                print('There is no data with this filter criteria')
           else:
               total_duration = sum(item['duration'] for item in cityfilemonth)
               try:
                    avg_duration =sum(item['duration'] for item in cityfilemonth)/len(cityfilemonth)
                    print ("The \"trip\" related statistic for the the city :{}\'s bikeshare data with filters: ({},{}) is a total duration of {} with an average trip duration of {}.".format(city,timefilter,timefilter_nm,str(total_duration),str(avg_duration)))
               except ZeroDivisionError:
                    print('The \"trip\" related statistic for the the city :{}\'s bikeshare data with filters: ({},{}) resulted in an Error: Division by Zero.'.format(city,timefilter,timefilter_nm))
    elif timefilter == 'day':
           cityfilemonth = list(filter(lambda x : x ['Start_Time_Day'] in timefilter_nm, city_file))
           if cityfilemonth==[]:
               print('There is no data with this filter criteria')
           else:
               total_duration = sum(item['duration'] for item in cityfilemonth)
               try:
                   avg_duration=total_duration/len(cityfilemonth)
                   print ("The \"trip\" related statistic for the the city :{}\'s bikeshare data with filters: ({},{}) is a total duration of {} with an average trip duration of {}.".format(city,timefilter,timefilter_nm,str(total_duration),str(avg_duration)))     
               except ZeroDivisionError:
                   print('The \"trip\" related statistic for the the city :{}\'s bikeshare data with filters: ({},{}) resulted in Error: Division by Zero.'.format(city,timefilter,timefilter_nm))             
    else:
           total_duration = sum(item['duration'] for item in city_file)
           try:
               avg_duration=total_duration/len(city_file)
               print ("The \"trip\" related statistic for the the city :{}\'s bikeshare data  is a total duration of :{} with an average trip duration of :{}.".format(city,str(total_duration),str(avg_duration)))     
           except ZeroDivisionError:
               print('The \"trip\" related statistic for the the city :{}\'s bikeshare data resulted in Error: Division by Zero.'.format(city))

def popular_stations(city,city_file, time_period):
    '''Question: What is the most popular Hour for start time? If the filter chosen has a timeperiod, filter based on that
    
    Args:
        city,city_file, time_period
    Returns: none.
    '''
    timefilter=time_period[0]
    timefilter_nm=time_period[1]
    if timefilter == 'month':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Month_Nm'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                popularStart_St = Counter(k['Start_St'] for k in cityfilemonth if k.get('Start_St')) 
                for Start_St, count in popularStart_St.most_common(1):
                    print ("The most popular Start Station for the city :{}'s bikeshare data with filters: ({},{}) is {} with {} occurrences.".format(city,timefilter,timefilter_nm,Start_St,str(count))) 
                popularEnd_St = Counter(k['End_St'] for k in cityfilemonth if k.get('End_St')) 
                for End_St, count in popularEnd_St.most_common(1):
                    print ("The most popular End Station for the city :{}'s bikeshare data with filters: ({},{}) is {} with {} occurrences.".format(city,timefilter,timefilter_nm,End_St,str(count))) 
    elif timefilter == 'day':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Day'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                popularStart_St = Counter(k['Start_St'] for k in cityfilemonth if k.get('Start_St')) 
                for Start_St, count in popularStart_St.most_common(1):
                    print ("The most popular Start Station for the city :{}'s bikeshare data with filters: ({},{}) is {} with {} occurrences.".format(city,timefilter,timefilter_nm,Start_St,str(count)))     
                popularEnd_St = Counter(k['End_St'] for k in cityfilemonth if k.get('End_St')) 
                for End_St, count in popularEnd_St.most_common(1):
                    print ("The most popular End Station for the city :{}'s bikeshare data with filters: ({},{}) is {} with {} occurrences.".format(city,timefilter,timefilter_nm,End_St,str(count)))     
    else:
            popularStart_St = Counter(k['Start_St'] for k in city_file if k.get('Start_St')) 
            for Start_St, count in popularStart_St.most_common(1):
                print ("The most popular Start Station for the city :{} is {} with {} occurrences.".format(city,Start_St,str(count)))
            popularEnd_St = Counter(k['End_St'] for k in city_file if k.get('End_St')) 
            for End_St, count in popularEnd_St.most_common(1):
                print ("The most popular End Station for the city :{} is {} with {} occurrences.".format(city,End_St,str(count)))   

def popular_trip(city,city_file, time_period):
    '''Question: What is the most popular trip? If the filter chosen has a timeperiod, filter based on that
    
    Args:
        city,city_file, time_period
    Returns: none.
    '''
    timefilter=time_period[0]
    timefilter_nm=time_period[1]
    if timefilter == 'month':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Month_Nm'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                populartrip = Counter(k['Trip'] for k in cityfilemonth if k.get('Trip')) 
                for Trip, count in populartrip.most_common(1):
                    print ("The most popular Trip for the city :{} 's bikeshare data with filters: ({},{}) is {} with {} occurrences.".format(city,timefilter,timefilter_nm,Trip,str(count))) 
    elif timefilter == 'day':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Day'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                populartrip = Counter(k['Trip'] for k in cityfilemonth if k.get('Trip')) 
                for Trip, count in populartrip.most_common(1):
                    print ("The most popular Trip for the city :{}'s bikeshare data with filters: ({},{}) is {} with {} occurrences.".format(city,timefilter,timefilter_nm,Trip,str(count)))     
    else:
            populartrip = Counter(k['Trip'] for k in city_file if k.get('Trip')) 
            for Trip, count in populartrip.most_common(1):
                print ("The most popular Trip for the city :{} is {} with {} occurrences.".format(city,Trip,str(count)))

def users(city,city_file, time_period):
    '''Question: What are the counts of each user type? If the filter chosen has a timeperiod, filter based on that
    
    Args:
        city,city_file, time_period
    Returns: none.
    '''
    timefilter=time_period[0]
    timefilter_nm=time_period[1]
    if timefilter == 'month':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Month_Nm'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                users = Counter(map(itemgetter('User_Type'), cityfilemonth))
                print ("The user type counts for the city :{}'s bikeshare data with filters: ({},{}) are {}.".format(city,timefilter,timefilter_nm,users.most_common())) 
    elif timefilter == 'day':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Day'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                users = Counter(map(itemgetter('User_Type'), cityfilemonth))
                print ("The user type counts for the city :{}'s bikeshare data with filters: ({},{}) are {}.".format(city,timefilter,timefilter_nm,users.most_common())) 
    else:
            users = Counter(map(itemgetter('User_Type'), city_file))
            print ("The user type counts for the city :{} are {}.".format(city,users.most_common()))

def gender(city,city_file, time_period):
    '''Question: What are the counts of each user type? If the filter chosen has a timeperiod, filter based on that
    
    Args:
        city,city_file, time_period
    Returns: none.
    '''
    timefilter=time_period[0]
    timefilter_nm=time_period[1]
    if timefilter == 'month':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Month_Nm'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                Gender = Counter(map(itemgetter('Gender'), cityfilemonth))
                print ("The Gender counts for the city :{}'s bikeshare data with filters: ({},{}) are {}.".format(city,timefilter,timefilter_nm,Gender.most_common())) 
    elif timefilter == 'day':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Day'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                Gender = Counter(map(itemgetter('Gender'), cityfilemonth))
                print ("The Gender counts for the city :{}'s bikeshare data with filters: ({},{}) are {}.".format(city,timefilter,timefilter_nm,Gender.most_common())) 
    else:
            Gender = Counter(map(itemgetter('Gender'), city_file))
            print ("The Gender counts for the city :{}'s bikeshare data are {}.".format(city,Gender.most_common()))

def birth_years(city,city_file, time_period):
    '''Question: Question: What are the earliest, most recent, and most popular birth years? If the filter chosen has a timeperiod, filter based on that
    
    Args:
        city,city_file, time_period
    Returns: none.
    '''
    timefilter=time_period[0]
    timefilter_nm=time_period[1]
    exclude_yr =[0]
    if timefilter == 'month':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Month_Nm'] in timefilter_nm and x ['Y_O_B'] not in exclude_yr , city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                YOBseq = [x['Y_O_B'] for x in cityfilemonth]
                popularYOB = Counter(k['Y_O_B'] for k in cityfilemonth if k.get('Y_O_B')) 
                for Y_O_B, count in popularYOB.most_common(1):
                    print ("The most popular birth years for the city {}'s bikeshare data with filters: ({},{}) is {} with {} occurrences. \nThe earliest Birth Year is {} and the most recent Birth Year is {}.".format(city,timefilter,timefilter_nm,Y_O_B,str(count),min(YOBseq),max(YOBseq))) 
    elif timefilter == 'day':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Day'] in timefilter_nm and x ['Y_O_B'] not in exclude_yr , city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                YOBseq = [x['Y_O_B'] for x in cityfilemonth]
                popularYOB = Counter(k['Y_O_B'] for k in cityfilemonth if k.get('Y_O_B')) 
                for Y_O_B, count in popularYOB.most_common(1):
                    print ("The most popular birth year for the city {}'s bikeshare data with filters: ({},{}) is {} with {} occurrences. \nThe earliest Birth Year is {} and the most recent Birth Year is {}.".format(city,timefilter,timefilter_nm,Y_O_B,str(count),min(YOBseq),max(YOBseq))) 
    else:
            YOBseq = [x['Y_O_B'] for x in city_file]
            popularYOB = Counter(k['Y_O_B'] for k in city_file if k.get('Y_O_B')) 
            for Y_O_B, count in popularYOB.most_common(1):
                print ("The most popular birth years for the city {}'s bikeshare data is {} with {} occurrences.\nThe earliest Birth Year is {} and the most recent Birth Year is {}.".format(city,Y_O_B,str(count),min(YOBseq),max(YOBseq)))

def display_data(city,city_file,time_period):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.

    Args:
        city,city_file, time_period.
    Returns: none.
    '''
    timefilter=time_period[0]
    timefilter_nm=time_period[1]
    if timefilter == 'month':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Month_Nm'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                display = input('Would you like to view individual trip data?'
                    'Type \'yes\' or \'no\'. \n')
                display = display.lower()
                i = 0
                while display.lower() == 'yes':
                    pp = pprint.PrettyPrinter(indent=4)
                    pp.pprint(cityfilemonth[i:i+5])
                    i += 5
                    display = input("\nWould you like to view five more lines?" 
                                         "Type 'yes' or 'no'.\n")
                else:
                    print('No data selected to be displayed.')
                    
    elif timefilter == 'day':
            cityfilemonth = list(filter(lambda x : x ['Start_Time_Day'] in timefilter_nm, city_file))
            if cityfilemonth==[]:
                print('There is no data with this filter criteria')
            else:
                display = input('Would you like to view individual trip data?'
                    'Type \'yes\' or \'no\'. \n')
                display = display.lower()
                i = 0
                while display.lower() == 'yes':
                    pp = pprint.PrettyPrinter(indent=4)
                    pp.pprint(cityfilemonth[i:i+5])
                    i += 5
                    display = input("\nWould you like to view five more lines?" 
                                         "Type 'yes' or 'no'.\n")
                else:
                    print('No data selected to be displayed.')
    else:
            display = input('Would you like to view individual trip data?'
                    'Type \'yes\' or \'no\'. \n')
            display = display.lower()
            i = 0
            while display.lower() == 'yes':
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(city_file[i:i+5])
                i += 5
                display = input("\nWould you like to view five more lines?" 
                          "Type 'yes' or 'no'.\n")
            else:
                print('No data selected to be displayed.')

def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.

    Args:
        city.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()
    if city!='none':

        city_file = load_cityfile(city)
        # Filter by time period (month, day, none)
        time_period = get_time_period()
    
        # What is the most popular month for start time?
        if time_period[0] == 'none':
            print('Calculating the first statistic...')
            start_time = time.time()
            popular_month(city,city_file)
            print("That took %s seconds." % (time.time() - start_time))
            
        # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
        if time_period[0] == 'none' or time_period[0] == 'month':
            print("Calculating the next statistic...")
            start_time = time.time()
            popular_day(city,city_file, time_period)
            print("That took %s seconds." % (time.time() - start_time))
    
        # What is the most popular hour of day for start time?
        print("Calculating the next statistic...")
        start_time = time.time()
        popular_hour(city,city_file, time_period)
        print("That took %s seconds." % (time.time() - start_time))
    
        # What is the total trip duration and average trip duration?
        print("Calculating the next statistic...")
        start_time = time.time()
        trip_duration(city,city_file, time_period)
        print("That took %s seconds." % (time.time() - start_time))
    
        # What is the most popular start station and most popular end station?
        print("Calculating the next statistic...")
        start_time = time.time()
        popular_stations(city,city_file, time_period)
        print("That took %s seconds." % (time.time() - start_time))
    
        # What is the most popular trip?
        print("Calculating the next statistic...")
        start_time = time.time()
        popular_trip(city,city_file, time_period)
        print("That took %s seconds." % (time.time() - start_time))
    
        # What are the counts of each user type?
        print("Calculating the next statistic...")
        start_time = time.time()
        users(city,city_file, time_period)
        print("That took %s seconds." % (time.time() - start_time))
    
        # What are the counts of gender?
        print("Calculating the next statistic...")
        start_time = time.time()
        gender(city,city_file, time_period)
        print("That took %s seconds." % (time.time() - start_time))
    
        # What are the earliest, most recent, and most popular birth years?
        print("Calculating the next statistic...")
        start_time = time.time()
        birth_years(city,city_file, time_period)
        print("That took %s seconds." % (time.time() - start_time))
    
        # Display five lines of data at a time if user specifies that they would like to
        display_data(city,city_file, time_period)
    
    else:
        exit()
#    Restart?
    restart = input('Would you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()


if __name__ == "__main__":
	statistics()
