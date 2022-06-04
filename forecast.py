#! /usr/bin/python3
import sys
import requests
import json
from subprocess import call
from getkey import getkey, keys # External add-on module

def testArgs(): # Retrives args and formats / validates them
    def numbersCheck(latTest, lonTest):
        try:
            latTestFloat = float(latTest)
            lonTestFloat = float(lonTest)

        except ValueError:
            return False

        if latTestFloat > 17 and latTestFloat < 72:
            latTestPassed = True
        else:
            latTestPassed = False

        if lonTestFloat > -179 and lonTestFloat < -50:
            lonTestPassed = True
        else:
            lonTestPassed = False

        if latTestPassed == True and lonTestPassed == True:
            return True
        else:
            return False

    stop = False # Used to flag bad input args
    if len(sys.argv) == 1: 
		# Return downtown Minneapolis lat / long if no coords provided
        coordsList = '44.9771', '-93.2724'

    elif len(sys.argv) == 2: # Split coords if entered seperated by only a comma
        if ',' in sys.argv[1]:
            coordsList = sys.argv[1].split(',')
        else:
    	    print("2 Coordinates needed, Latitude and Longitude\n")
    	    stop = True

    elif len(sys.argv) == 3: #Coords seperated by space
        coordsList = [sys.argv[1], sys.argv[2]]
        # Get rid of comma in coordsList[0] if present between entered coords
        # (i.e. comma AND space)
        if coordsList[0][-1] == ',':
            tempString = coordsList[0]
            tempString2 = tempString[0:len(tempString)-1]
            coordsList[0] = tempString2

    else:
        print("There are too many arguments,", len(sys.argv) - 1, "\n")
        stop = True

    if stop == True:
        sys.exit(2)

    if stop == False: # No 'errors' in previous operations
        # Add '-' to coordsList[1] if not present
        if '-' not in coordsList[1]:
            coordsList[1] = "-{}".format(coordsList[1])

        x = coordsList[0]
        y = coordsList[1]

        numbersValid = numbersCheck(x, y) # Internal function to sanity check numbers
        if numbersValid == True:
            return (x, y)
        else:
            print("Please confirm that the coords entered are both valid numbers, then try again\n")
            sys.exit(2)

def location(strJSON):
    dict1 = strJSON.json()
    dict2 = dict1['properties']
    targetURL = dict2['forecast']
    dict3 = dict2['relativeLocation']
    dict4 = dict3['properties']
    targetCity = dict4['city']
    targetState = dict4['state']
    return (targetURL, targetCity, targetState)

def clear():
    _ = call('clear') # Screen clearing function assumes posix OS without testing

def formatDateTime(teststr):
    testlst = teststr.split('T')
    teststr2 = testlst[1]
    testlst2 = teststr2.split('-')
    outstr = "Date: {}, Time: {}".format(testlst[0], testlst2[0])
    return outstr

try:
    lat, long = testArgs() # Internal function
    locationPage = requests.get("https://api.weather.gov/points/{},{}".format(lat, long))
    url, city, state = location(locationPage) # Internal function
    page = requests.get(url)
    dict1 = page.json()
    dict2 = dict1['properties']
    periodsList = dict2['periods']

except Exception: # Make this production-worthy
	print("\033[31mError retriving data. Urls queried: \033[0m", locationPage.url, page.url)
	print("\n\033[31mData recieved: \033[0m", page.text[:500])

h = 0
looping = True
while looping == True:
    timeSlice = periodsList[h]
    clear()
    print("Forecast for {}, {}\n".format(city, state))
    itemsToPrint = [1, 2, 3, 5, 7, 8, 9, 11, 12]
    i = 0
    for detail in timeSlice:
        if i in itemsToPrint:
            if i == 2 or i == 3:
                print(detail, " : ", formatDateTime(timeSlice[detail]))
            else:
                print(detail, " : ", timeSlice[detail])
        i += 1

    print('\n\033[31mPress right and left arrows to go fwd / back, [ESC] to exit.\033[0m')
    key = getkey()
    if key == keys.RIGHT and h < len(periodsList) - 1:
        h += 1
    elif key == keys.LEFT and h > 0:
        h -= 1
    elif key == keys.ESCAPE:
        looping = False