import numpy as np
import requests

# Average Time Delta
# This function calculates the average time delta, by determining the average
# time between each date returned from the API GET request. It is called by the Flyby function.
# Inputs: Count (as the number of dates in the record) & Results (as the dates themselves)
# Outputs: The latest date from the record & the calculated average time delta.

def avg_time_delta(count, results):
    dates = [result['date'] for result in results]

    dates = list(map(np.datetime64, dates))
    dates.sort()
    max_date = max(dates)

    intervals = []
    for i in range(1, len(dates)):
        last_date = np.datetime64(dates[i-1])
        curr_date = np.datetime64(dates[i])
        intervals.append(curr_date - last_date)
    avg_time_s = np.mean(intervals)

    return max_date, avg_time_s

# Flyby
# This function determines a prediction for when the next picture of the location
# specified by its inputs will be taken. It only does so when there is sufficient
# data available. It also checks for validity of inputs. Additionally, it makes
# the GET request to the NASA API to the extract all data.
# Inputs: Latitude and Longitude positions determining the location
# Outputs: The prediction (as a date) for when the next picture of the location determined
# by the inputs will be taken.

def flyby(lat, long):
    if (lat < -90 or lat > 90 or long < -180 or long > 180):
        raise Exception ('Invalid latitude or longitude coordinates!')

    today_date = np.datetime64('now')

    API_url = 'https://api.nasa.gov/planetary/earth/assets?'
    API_key = '9Jz6tLIeJ0yY9vjbEUWaH9fsXA930J9hspPchute'

    final_url = API_url+'lon='+str(long)+'&lat='+str(lat)+'&end='+str(today_date)+'&api_key='+API_key
    data = requests.get(final_url)
    data = data.json()

    count = data['count']
    results = data['results']

    if (count < 2):
        raise Exception('Insufficient data to calculate prediction!')

    max_date, avg_time = avg_time_delta(count, results)
    retval = max_date + avg_time

    while (retval <= today_date):
        retval = retval + avg_time

    print "Next time: " + str(retval)


# Test Cases:

testcases = [
    ("Zero_Test", 0.000000, 0.000000),
    ("America", 36.098592, -112.097796),
    ("America", 43.078154, -79.075891),
    ("America", 36.998979, -109.045183),
    ("America", 37.7937007, -122.4039064),
    ("Asia", 40.431908, 116.570374),
    ("Asia", 27.173891, 78.042068),
    ("Asia", -7.607874, 110.203751),
    ("Asia", 35.658581, 139.745438),
    ("Europe", 48.858093, 2.294694),
    ("Europe", 52.492069, 13.284844),
    ("Europe", 43.385956, -8.406495),
    ("Europe", 51.510357, -0.116773),
    ("Min Longitude", 0.000000, -180.000001),
    ("Min Longitude", 0.000000, -180.000000),
    ("Min Longitude", 0.000000, -179.999999),
    ("Min Latitude", -90.000001, 0.000000),
    ("Min Latitude", -90.000000,0.000000),
    ("Min Latitude", -89.999999,0.000000),
    ("Max Longitude", 0.000000, 179.999999),
    ("Max Longitude", 0.000000, 180.000000),
    ("Max Longitude", 0.000000, 180.000000),
    ("Max Latitude", 89.999999,0.000000),
    ("Max Latitude", 90.000000,0.000000),
    ("Max Latitude", 90.000001,0.000000),
    ("Edge Case Combinations", -90.000000, -180.000000),
    ("Edge Case Combinations", -90.000000, 180.000000),
    ("Edge Case Combinations", 90.000000, -180.000000),
    ("Edge Case Combinations", 90.000000, 180.000000)]

for test in testcases:
    print("Running testcase for", test[0])
    try:
        flyby(test[1], test[2])
        print("Test successful!")
    except Exception as instance:
        print("Test failed for", test[0], "due to exception:", instance)

