#! /usr/bin/env python3
import sys
import requests
import json
from subprocess import call
from getkey import getkey, keys # External add-on module

def extract_args():
    if len(sys.argv) == 1:
        return 

    elif len(sys.argv) == 2: 
        if ',' in sys.argv[1]:
            coordsList = sys.argv[1].split(',')
        else:
            print("2 Coordinates needed, Latitude and Longitude\n")
            sys.exit(2)

    elif len(sys.argv) == 3:
        coordsList = [sys.argv[1].replace(',',''), sys.argv[2]]

    else:
        print(f"{len(sys.argv) - 1} coordinates were supplied, there should be only 2\n")
        sys.exit(2)

    if '-' not in coordsList[1]:
        coordsList[1] = f"-{coordsList[1]}"

    return tuple(coordsList)

def validate_args(coords_tuple):
    try:
        latTestFloat = float(coords_tuple[0])
        lonTestFloat = float(coords_tuple[1])

    except ValueError:
        return False

    if latTestFloat <= 17 or latTestFloat >= 72:
        return False

    if lonTestFloat <= -179 or lonTestFloat >= -50:
        return False

    return True
    
def get_coords():
    MINNEAPOLIS = ('44.9771', '-93.2724')
    
    if extract_args():
        if validate_args(extract_args()):
            lat, long = extract_args()
        else:
            print("Please confirm that the coords entered are both valid numbers, then try again\n")
            sys.exit(2)

    else:
        lat, long = MINNEAPOLIS

    return (lat, long)

def location(locationPage):
    _ = locationPage.json()
    targetURL = _['properties']['forecast']
    targetCity =  _['properties']['relativeLocation']['properties']['city']
    targetState = _['properties']['relativeLocation']['properties']['state']
    return (targetURL, targetCity, targetState)
    
def get_daily_forecast(lat, long):
    try:
        locationPage = requests.get(f"https://api.weather.gov/points/{lat},{long}")
        # breakpoint()
        url, city, state = location(locationPage)
        page = requests.get(url)
        dict1 = page.json()
        periodsList = dict1['properties']['periods']
        return (city, state, periodsList)

    except requests.exceptions.ConnectionError:
        print("ConnectionError: Site not reachable")
        sys.exit(1)

    except Exception as e:
        print("Exception:", e)
        print("Error retriving data. Urls queried:", locationPage.url, page.url)
        print(f"Title: {dict1['title']}, Status: {dict1['status']}")
        print(dict1['detail'])
        sys.exit(1)

def clear():
    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        _ = call('clear')
    elif sys.platform.startswith('win32'):
        _ = call('cls')
    else:
        print(f"Operating System {sys.platform} detected but is not supported")
        sys.exit(1)

def formatDateTime(teststr):
    testlst = teststr.split('T')
    teststr2 = testlst[1]
    testlst2 = teststr2.split('-')
    outstr = "Date: {}, Time: {}".format(testlst[0], testlst2[0])
    return outstr

if __name__ == '__main__':
    city, state, periodsList = get_daily_forecast(*get_coords())
    # h is a time period incrementer
    h = 0
    while True:
        timeSlice = periodsList[h]
        clear()
        print(f"Forecast for {city}, {state}\n")
        itemsToPrint = [1, 2, 3, 5, 8, 9, 10, 11, 12, 15]

        for i, detail in enumerate(timeSlice):
            if i in itemsToPrint:
                if i == 2 or i == 3:
                    print(detail, ":", formatDateTime(timeSlice[detail]))
                elif i == 5:
                    print(f"{detail} : {timeSlice[detail]}F")
                elif i == 8 or i == 10:
                    testvar = timeSlice[detail]['value']
                    if testvar == None:
                        testvar = 0
                    print(f"{detail} : {testvar}%")
                elif i == 9:
                    testvar = timeSlice[detail]['value']
                     # Convert C to F
                    testvar = int(testvar * 1.8 + 32)
                    print(f"{detail} : {testvar}F")
                else:
                    print(detail, ":", timeSlice[detail])

        print('\n\033[31mPress right and left arrows to go fwd / back, [ESC] to exit.\033[0m')
        key = getkey()
        if key == keys.RIGHT and h < len(periodsList) - 1:
            h += 1
        elif key == keys.LEFT and h > 0:
            h -= 1
        elif key == keys.ESCAPE:
            sys.exit(0) 

