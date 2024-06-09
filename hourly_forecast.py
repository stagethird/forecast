import nws_api as nws
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

if __name__ == '__main__':
    hourly = nws.NWS(*get_coords())
    city = hourly.targetCity
    state = hourly.targetState
    hourly.get_hourly_forecast()
    periodsList = hourly.hourlyPeriodsList

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
