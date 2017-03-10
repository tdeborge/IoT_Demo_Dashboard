"""
Tutorial/Example how to use the class helper `SeriesHelper`
"""

from influxdb import InfluxDBClient
from influxdb import SeriesHelper

# InfluxDB connections settings
host = 'localhost'
port = 8086
user = 'psteiner'
password = 'change12_me'
dbname = 'IoT_Demo'

myclient = InfluxDBClient(host, port, user, password, dbname)

# Uncomment the following code if the database is not yet created
myclient.create_database(dbname)
myclient.create_retention_policy('awesome_policy', '3d', 3, default=True)


class MySeriesHelper(SeriesHelper):
    # Meta class stores time series helper configuration.
    class Meta:
        # The client should be an instance of InfluxDBClient.
        client = myclient
        # The series name must be a string. Add dependent fields/tags in curly brackets.
        series_name = 'events.stats.{deviceType}'
        # Defines all the fields in this time series.
        fields = ['deviceID', 'payload']
        # Defines all the tags for the series.
        tags = ['deviceType']
        # Defines the number of data points to store prior to writing on the wire.
        bulk_size = 5
        # autocommit must be set to True when using bulk_size
        autocommit = True


# The following will create *five* (immutable) data points.
# Since bulk_size is set to 5, upon the fifth construction call, *all* data
# points will be written on the wire via MySeriesHelper.Meta.client.
MySeriesHelper(deviceType="Temperature", deviceID="1", payload=10)
MySeriesHelper(deviceType="Temperature", deviceID="2", payload=15)
MySeriesHelper(deviceType="Temperature", deviceID="1", payload=10)
MySeriesHelper(deviceType="Temperature", deviceID="2", payload=15)
MySeriesHelper(deviceType="Temperature", deviceID="1", payload=11)
MySeriesHelper(deviceType="Temperature", deviceID="2", payload=15)
MySeriesHelper(deviceType="Temperature", deviceID="1", payload=12)
MySeriesHelper(deviceType="Temperature", deviceID="2", payload=17)
MySeriesHelper(deviceType="Temperature", deviceID="1", payload=13)
MySeriesHelper(deviceType="Temperature", deviceID="2", payload=18)

# To manually submit data points which are not yet written, call commit:
MySeriesHelper.commit()

# To inspect the JSON which will be written, call _json_body_():
MySeriesHelper._json_body_()
