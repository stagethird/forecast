import pandas as pd
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys


def testArgs():  # Retrives args and formats / validates them
    def numbersCheck(latTest, lonTest):
        try:
            latTestFloat = float(latTest)
            lonTestFloat = float(lonTest)

        except ValueError:
            return False

        latTestPassed = True if latTestFloat > 17 and latTestFloat < 72 else False
        lonTestPassed = True if lonTestFloat > -179 and lonTestFloat < -50 else False

        if latTestPassed == True and lonTestPassed == True:
            return True
        return False

    stop = False  # Used to flag bad input args
    if len(sys.argv) == 1:
        # Return downtown Minneapolis lat / long if no coords provided
        coordsList = "44.9771", "-93.2724"

    elif len(sys.argv) == 2:  # Split coords if entered seperated by only a comma
        if "," in sys.argv[1]:
            coordsList = sys.argv[1].split(",")
        else:
            print("2 Coordinates needed, Latitude and Longitude\n")
            stop = True

    elif len(sys.argv) == 3:  # Coords seperated by space
        coordsList = [sys.argv[1], sys.argv[2]]
        # Get rid of comma in coordsList[0] if present between entered coords
        # (i.e. comma AND space)
        if coordsList[0][-1] == ",":
            tempString = coordsList[0]
            tempString2 = tempString[0 : len(tempString) - 1]
            coordsList[0] = tempString2

    else:
        print("There are too many arguments,", len(sys.argv) - 1, "\n")
        stop = True

    if stop == True:
        sys.exit(2)

    if stop == False:  # No 'errors' in previous operations
        # Add '-' to coordsList[1] if not present
        if "-" not in coordsList[1]:
            coordsList[1] = "-{}".format(coordsList[1])

        x = coordsList[0]
        y = coordsList[1]

        numbersValid = numbersCheck(x, y)  # Internal function to sanity check numbers
        if numbersValid == True:
            return (x, y)
        else:
            print(
                "Please confirm that the coords entered are both valid numbers, then try again\n"
            )
            sys.exit(2)


def location(strJSON):
    #  Reduce some of this
    dict1 = strJSON.json()
    dict2 = dict1["properties"]
    targetURL = dict2["forecastHourly"]
    dict3 = dict2["relativeLocation"]
    dict4 = dict3["properties"]
    targetCity = dict4["city"]
    targetState = dict4["state"]
    return (targetURL, targetCity, targetState)


try:
    lat, long = testArgs()  # Internal function
    locationPage = requests.get(
        "https://api.weather.gov/points/{},{}".format(lat, long)
    )
    url, city, state = location(locationPage)  # Internal function
    page = requests.get(url)
    dict1 = page.json()
    periodsList = dict1["properties"]["periods"]
    # raise ValueError("Just kidding!")
    # breakpoint()

except requests.exceptions.ConnectionError:
    print("ConnectionError: Site not reachable")
    sys.exit(1)

except Exception as e:
    print("Exception:", e)
    print("Error retriving data. Urls queried:", locationPage.url, page.url)
    print(f"Title: {dict1['title']}, Status: {dict1['status']}")
    print(dict1["detail"])
    sys.exit(1)

df = pd.DataFrame(periodsList)
df = df.drop(["name", "icon", "detailedForecast"], axis=1)
df["startTime"] = pd.to_datetime(df["startTime"])
df["endTime"] = pd.to_datetime(df["endTime"])

figure = plt.figure(figsize=(10, 6))
ax = figure.add_subplot(111)
myFmt = mdates.DateFormatter("%m/%d")
ax.xaxis.set_major_formatter(myFmt)
ax.xaxis.grid(True, which="major")
ax.yaxis.grid(True, which="major")
ax.xaxis.set_minor_locator(mdates.HourLocator())
ax.set(
    xlabel="Hourly Measurement",
    ylabel="Degrees F",
    title=f"Hourly Forecast: {city}, {state}",
)
ax.plot(df.startTime, df.temperature, ".-")

plt.show()
