import nws_api as nws
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Import data
hourly = nws.NWS(*nws.get_coords())
city = hourly.targetCity
state = hourly.targetState
hourly.get_hourly_forecast()
periodsList = hourly.hourlyPeriodsList

# Format dataframe
df = pd.DataFrame(periodsList)
df['startTime'] = pd.to_datetime(df['startTime'])
df.windSpeed = df.windSpeed.str.extract('(\d+)', expand=False).astype(int)
df=df[['number','windDirection','windSpeed','startTime']]

degrees = np.linspace(0,360,17)[0:-1]
direction = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
windDict = dict(zip(direction, degrees))
df = df.replace({"windDirection": windDict})
df=df.iloc[:24]
df=df.replace('',np.nan).dropna()

df2=df.groupby(['windDirection', 'windSpeed'])['number'].agg(['count'])
df2['ratio']=df2['count']/len(df)
df2=df2.reset_index()

# Create plots
fig=plt.figure(figsize=(7,7))
ax = plt.subplot(2,1,1,projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
cmap = mpl.colormaps['cool']

scaled_data = [datum for datum in df2['ratio']]
colors=[]
for decimal in scaled_data:
    colors.append(cmap(decimal))

cbar = plt.colorbar(mpl.cm.ScalarMappable(cmap=cmap), orientation='vertical',ax=ax)
cbar.set_ticks([0.0,0.2,0.4,0.6,0.8,1.0])
cbar.ax.set_yticklabels(['0%','20','40','60','80','100'])
_=ax.bar(x=df2['windDirection']*np.pi/180,width=(360*np.pi/180)/16,height=df2['windSpeed'],color=colors,alpha=0.5)
cbar.set_label(label='Duration, % of Day', size=10)
_=ax.text(.4, df2['windSpeed'].max()*1.2,"Windspeed\n(MPH)", ha="left", size=9)

starttime=df.iloc[0]['startTime'].strftime('%b %d, %H:%M')
endtime=df.iloc[-1]['startTime'].strftime('%b %d, %H:%M')
plt.figtext(0.05,0.88,'{}, {}\nWind Speed and Direction,\nFrom {}\nTo {}'.format(city,state,starttime,endtime),ha='left',size='large')

xval=np.arange(len(df))
ax2=plt.subplot(2,1,2)
for spine in plt.gca().spines.values():
    spine.set_visible(False)
_=ax2.stem(xval,df['windSpeed'])
_=ax2.set(xlabel='Time (hour)')
_=ax2.set(ylabel='Windspeed (MPH)')
_=ax2.set_xticks(xval,labels=df['startTime'].dt.strftime('%H'),rotation=90,size=8)
plt.show()

