# Forecast (forecast.py)

This program interacts with a United States National Weather Service
REST API to retrive a 10-day weather forecast and display it in an
interactive command shell. It can be passed latitude and longitude 
coordinates or, if none are passed, it will return the forcast for 
downtown **Minneapolis, Minnesota**.

---
Latitude and Longitude coordinates, if passed, can be seperated by a 
comma or a space, and can include or exclude a '-' in front of the 
longitude coordinate. Note that only coordinates within a box roughly 
enclosing the United States are accepted as valid input, as the forecast
is provided by a U.S. government agency.

[![forthebadge](https://forthebadge.com/images/badges/works-on-my-machine.svg)][def]

[def]: https://forthebadge.com

