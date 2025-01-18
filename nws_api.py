import requests
import json
import sys

class NWS:
    def __init__(self, lat: str, long: str):
        self.lat = lat
        self.long = long
        self.locationPage = None
        self.dailyTargetURL = ""
        self.hourlyTargetURL = ""
        self.targetCity = ""
        self.targetState = ""
        self.dailyPage = None
        self.dailyPeriodsList = []
        self.hourlyPage = None
        self.hourlyPeriodsList = []

        self._location()

    def _location(self):
        try:
            self.locationPage = requests.get(f"https://api.weather.gov/points/{self.lat},{self.long}")
            _ = self.locationPage.json()
            self.dailyTargetURL = _['properties']['forecast']
            self.hourlyTargetURL = _['properties']['forecastHourly']
            self.targetCity =  _['properties']['relativeLocation']['properties']['city']
            self.targetState = _['properties']['relativeLocation']['properties']['state']

        except requests.exceptions.ConnectionError:
           print("\nConnectionError: Site not reachable")
           print(f"https://api.weather.gov/points/{self.lat},{self.long}\n")
           sys.exit(1)

        except Exception as e:
            print("\nException:", e)
            print("in NWS._location().\n")

    def get_daily_forecast(self):
        try:
            self.dailyPage = requests.get(self.dailyTargetURL)
            dict1 = self.dailyPage.json()
            self.dailyPeriodsList = dict1['properties']['periods']
            return self.dailyPeriodsList

        except requests.exceptions.ConnectionError:
            print("\nConnectionError: Site not reachable\n", self.dailyTargetURL)
            print()
            sys.exit(1)

        except Exception as e:
            print("\nException:", e)
            print("in NWS.get_daily_forecast().\n")
            sys.exit(1)

    def get_hourly_forecast(self):
        try:
            self.hourlyPage = requests.get(self.hourlyTargetURL)
            dict1 = self.hourlyPage.json()
            self.hourlyPeriodsList = dict1["properties"]["periods"]
            return self.hourlyPeriodsList

        except requests.exceptions.ConnectionError:
            print("\nConnectionError: Site not reachable\n", self.hourlyTargetURL)
            print()
            sys.exit(1)

        except Exception as e:
            print("\nException:", e)
            print("in NWS.get_hourly_forecast().\n")
            sys.exit(1)

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

