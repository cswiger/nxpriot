# nxpriot
NXP Rapid IoT contest project custom code

python script to run on the RPi Zero W connects to the NXP Rapid IoT device via bluetooth low energy 
(BLE) and receive sensor charactoristic data value updates. When all sensors monitored have updated,
including GPS location latitude and longitude, temperature, humidity, barometric pressure, light level,
air quality TVOC and CO2 - then a mqtt message containing the readings is published.

On the cloud server side, a nodejs script monitors the mqtt topic and any incoming messaages are stored with
timestamp in a mongodb collection.

When a report is desired, a python script can extract data between specified timestamps to create a csv 
file of the data, and csv2geojson run to create a geojson feature collection of the sensor data.

Lastly, the geojson feature collection is used to create a clickable map of the sensor readings. 

