import requests
import json

class NWS:
    def __init__(self, lat: str, long: str):
        self.lat = lat
        self.long = long
        self.locationPage = None
        self.targetURL = ""
        self.targetCity = ""
        self.targetState = ""

    def _location(self):
        self.locationPage = requests.get(f"https://api.weather.gov/points/{self.lat},{self.long}")
        _ = self.locationPage.json()
        self.targetURL = _['properties']['forecast']
        self.targetCity =  _['properties']['relativeLocation']['properties']['city']
        self.targetState = _['properties']['relativeLocation']['properties']['state']

if __name__ == "__main__":
    me = NWS("45", "-93")
    me._location()
    print(me.targetURL)
    print(me.targetCity)
    print(me.targetState)



 #    def get_daily_forecast(lat, long):
 #        try:
 #            # locationPage = requests.get(f"https://api.weather.gov/points/{lat},{long}")
 #            url, city, state = location(locationPage)
 #            page = requests.get(url)
 #            dict1 = page.json()
 #            periodsList = dict1['properties']['periods']
 #            raise ValueError("Just kidding!")
 #            breakpoint()
 #            return (city, state, periodsList)

 #        except requests.exceptions.ConnectionError:
 #            print("ConnectionError: Site not reachable")
 #            sys.exit(1)

 #        except Exception as e:
 #            print("Exception:", e)
 #            print("Error retriving data. Urls queried:", locationPage.url, page.url)
 #            print(f"Title: {dict1['title']}, Status: {dict1['status']}")
 #            print(dict1['detail'])
 #            sys.exit(1)

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
