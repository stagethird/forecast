import nws_api as nws
import sys
from subprocess import call
from getkey import getkey, keys # External add-on module

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
    daily = nws.NWS(*nws.get_coords())
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

