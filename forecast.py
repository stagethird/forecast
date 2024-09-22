import nws_api as nws
import sys
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
    daily = nws.NWS(*get_coords())
    city = daily.targetCity
    state = daily.targetState
    daily.get_daily_forecast()
    periodsList = daily.dailyPeriodsList

    # h is a time period incrementer
    h = 0
    while True:
        timeSlice = periodsList[h]
        clear()
        print(f"Forecast for {city}, {state}\n")
        itemsToPrint = [1, 2, 3, 5, 8, 9, 10, 12, 13]

        for i, detail in enumerate(timeSlice):
            if i in itemsToPrint:
                if i == 2 or i == 3:
                    print(detail, ":", formatDateTime(timeSlice[detail]))
                elif i == 5:
                    print(f"{detail} : {timeSlice[detail]}F")
                elif i == 8:
                    testvar = timeSlice[detail]['value']
                    if testvar == None:
                        testvar = 0
                    print(f"{detail} : {testvar}%")
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

