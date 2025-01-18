import nws_api as nws
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

hourly = nws.NWS(*nws.get_coords())
city = hourly.targetCity
state = hourly.targetState
hourly.get_hourly_forecast()
periodsList = hourly.hourlyPeriodsList

df = pd.DataFrame(periodsList)
df = df.drop(["name", "icon", "detailedForecast"], axis=1)
df["startTime"] = pd.to_datetime(df["startTime"])
df["endTime"] = pd.to_datetime(df["endTime"])

df2 = pd.json_normalize(df.probabilityOfPrecipitation)
df.probabilityOfPrecipitation = df2.value

figure = plt.figure(figsize=(10, 6))
ax1 = plt.subplot(2, 1, 1)
myFmt = mdates.DateFormatter("%m/%d")
ax1.xaxis.set_major_formatter(myFmt)
ax1.xaxis.grid(True, which="major")
ax1.yaxis.grid(True, which="major")
ax1.xaxis.set_minor_locator(mdates.HourLocator())
ax1.set_ylabel("Degrees F", color='maroon')
ax1.plot(df.startTime, df.temperature, ".-", color='maroon')
ax2 = plt.subplot(2, 1, 2, sharex=ax1)
ax2.xaxis.grid(True, which="major")
ax2.yaxis.grid(True, which="major")
ax2.set_ylabel("Prob. of Precip.", color='purple')
ax2.set(xlabel="Hourly Measurement")
ax2.plot(df.startTime, df.probabilityOfPrecipitation, ".-", color='purple')
for ax in ax1, ax2:
    ax.grid(True)
    ax.label_outer()

ax1.fill_between(df.startTime, df.temperature.min()-1, df.temperature, color='maroon', alpha=.1)
ax2.fill_between(df.startTime, df.probabilityOfPrecipitation.min(), df.probabilityOfPrecipitation,
             color='purple', alpha=.1)
figure.suptitle(f"Hourly Forecast: {city}, {state}")
plt.show()
