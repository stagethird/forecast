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

        self._location()

    def _location(self):
        # add try block here
        self.locationPage = requests.get(f"https://api.weather.gov/points/{self.lat},{self.long}")
        _ = self.locationPage.json()
        self.dailyTargetURL = _['properties']['forecast']
        self.hourlyTargetURL = _['properties']['forecastHourly']
        self.targetCity =  _['properties']['relativeLocation']['properties']['city']
        self.targetState = _['properties']['relativeLocation']['properties']['state']

    def get_daily_forecast(self):
        try:
            self.dailyPage = requests.get(self.dailyTargetURL)
            dict1 = self.dailyPage.json()
            self.dailyPeriodsList = dict1['properties']['periods']
            return self.dailyPeriodsList

        except requests.exceptions.ConnectionError:
            print("ConnectionError: Site not reachable\n", dailyTargetURL)
            sys.exit(1)

        except Exception as e:
            print("Exception:", e)
            print("in NWS.set_daily_forecast().")
            sys.exit(1)

 #    def get_hourly_forecast(lat, long):
 #        try:
 #            lat, long = testArgs()  # Internal function
 #            locationPage = requests.get(
 #                "https://api.weather.gov/points/{},{}".format(lat, long)
 #            )
 #            url, city, state = location(locationPage)  # Internal function
 #            page = requests.get(url)
 #            dict1 = page.json()
 #            periodsList = dict1["properties"]["periods"]

 #        except requests.exceptions.ConnectionError:
 #            print("ConnectionError: Site not reachable")
 #            sys.exit(1)

 #        except Exception as e:
 #            print("Exception:", e)
 #            print("Error retriving data. Urls queried:", locationPage.url, page.url)
 #            print(f"Title: {dict1['title']}, Status: {dict1['status']}")
 #            print(dict1["detail"])
 #            sys.exit(1)

if __name__ == "__main__":
    me = NWS("45", "-93")
    print(type(me.get_daily_forecast()))

    # me._location()
    # print(me.dailyTargetURL)
    # print(me.targetCity)
    # print(me.targetState)


