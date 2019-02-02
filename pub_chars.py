#!/usr/bin/env python3
import gatt
import struct
import paho.mqtt.client as mqtt

# change to YOUR ble uuids
svc_uuid = 'ee81b7c3-727e-46de-8624-d6f88da7abf3'
lat_uuid = 'ee81b7c3-727e-46de-8624-d6f88da7abf4'
lon_uuid = 'ee81b7c3-727e-46de-8624-d6f88da7abf5'
temp_uuid = 'ee81b7c3-727e-46de-8624-d6f88da7abf6'
hum_uuid = 'ee81b7c3-727e-46de-8624-d6f88da7abf7'
pressure_uuid = 'ee81b7c3-727e-46de-8624-d6f88da7abf8'
light_uuid = 'ee81b7c3-727e-46de-8624-d6f88da7abf9'
airvtoc_uuid = 'ee81b7c3-727e-46de-8624-d6f88da7abfa'
airco2_uuid = 'ee81b7c3-727e-46de-8624-d6f88da7abfb'

client = mqtt.Client()
# change to YOUR mqtt user and password if any
client.username_pw_set('mqttuser',password='password')
# and YOUR mqtt cloud server ip address and port
client.connect('w.x.y.z',port=1883)

class AnyDevice(gatt.Device):
    def services_resolved(self):
        super().services_resolved()

        device_information_service = next(
            s for s in self.services
            if s.uuid == svc_uuid)
        latitude_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == lat_uuid)
        longitude_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == lon_uuid)
        temperature_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == temp_uuid)
        humidity_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == hum_uuid)
        pressure_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == pressure_uuid)
        light_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == light_uuid)
        airvtoc_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == airvtoc_uuid)
        airco2_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == airco2_uuid)

        self.have_lat = False
        self.have_lon = False
        self.have_temp = False
        self.have_hum = False
        self.have_light = False
        self.have_pressure = False
        self.have_airvtoc = False
        self.have_airco2 = False
        self.latitude = 0
        self.longitude = 0
        latitude_characteristic.enable_notifications()
        longitude_characteristic.enable_notifications()
        temperature_characteristic.enable_notifications()
        humidity_characteristic.enable_notifications()
        pressure_characteristic.enable_notifications()
        light_characteristic.enable_notifications()
        airvtoc_characteristic.enable_notifications()
        airco2_characteristic.enable_notifications()
        

    def characteristic_value_updated(self, characteristic, value):
        if (characteristic.uuid == lat_uuid ):
                self.latitude = struct.unpack('<f',value)[0]
                self.lat_mqtt = value
                self.have_lat = True
                if (self.have_lat & self.have_lon & self.have_temp & self.have_hum & self.have_pressure & self.have_light & self.have_airvtoc & self.have_airco2):
                        self.publish()
        if (characteristic.uuid == lon_uuid ):
                self.longitude = struct.unpack('<f',value)[0]
                self.lon_mqtt = value
                self.have_lon = True
                if (self.have_lat & self.have_lon & self.have_temp & self.have_hum & self.have_pressure & self.have_light & self.have_airvtoc & self.have_airco2):
                        self.publish()
        if (characteristic.uuid == temp_uuid ):
                print("latitude: {:3.6f}".format(self.latitude))
                print("longitude: {:3.6f}".format(self.longitude))
                print("temperature: {:3.2f}".format(struct.unpack('<f',value)[0]))
                self.temp_mqtt = value
                self.have_temp = True
                if (self.have_lat & self.have_lon & self.have_temp & self.have_hum & self.have_pressure & self.have_light & self.have_airvtoc & self.have_airco2):
                        self.publish()
        if (characteristic.uuid == hum_uuid ):
                print("humidity: {:3.2f}".format(struct.unpack('<f',value)[0]))
                self.hum_mqtt = value
                self.have_hum = True
                if (self.have_lat & self.have_lon & self.have_temp & self.have_hum & self.have_pressure & self.have_light & self.have_airvtoc & self.have_airco2):
                        self.publish()
        if (characteristic.uuid == pressure_uuid ):
                print("pressure: {:3d}".format(struct.unpack('<I',value)[0]))
                self.pressure_mqtt = value
                self.have_pressure = True
                if (self.have_lat & self.have_lon & self.have_temp & self.have_hum & self.have_pressure & self.have_light & self.have_airvtoc & self.have_airco2):
                        self.publish()
        if (characteristic.uuid == light_uuid ):
                print("light: {:3d}".format(struct.unpack('<I',value)[0]))
                self.light_mqtt = value
                self.have_light = True
                if (self.have_lat & self.have_lon & self.have_temp & self.have_hum & self.have_pressure & self.have_light & self.have_airvtoc & self.have_airco2):
                        self.publish()
        if (characteristic.uuid == airvtoc_uuid ):
                print("air vtoc: {:3d}".format(struct.unpack('<I',value)[0]))
                self.airvtoc_mqtt = value
                self.have_airvtoc = True
                if (self.have_lat & self.have_lon & self.have_temp & self.have_hum & self.have_pressure & self.have_light & self.have_airvtoc & self.have_airco2):
                        self.publish()
        if (characteristic.uuid == airco2_uuid ):
                print("air co2: {:3d}".format(struct.unpack('<I',value)[0]))
                self.airco2_mqtt = value
                self.have_airco2 = True
                if (self.have_lat & self.have_lon & self.have_temp & self.have_hum & self.have_pressure & self.have_light & self.have_airvtoc & self.have_airco2):
                        self.publish()

    def publish(self):
        #print(self.lat_mqtt+self.lon_mqtt+self.temp_mqtt+self.hum_mqtt+self.pressure_mqtt+self.light_mqtt+self.airvtoc_mqtt+self.airco2_mqtt)
        client.publish('/nxpriot',self.lat_mqtt+self.lon_mqtt+self.temp_mqtt+self.hum_mqtt+self.pressure_mqtt+self.light_mqtt+self.airvtoc_mqtt+self.airco2_mqtt)
        self.have_lat = False
        self.have_lon = False
        self.have_temp = False
        self.have_hum = False
        self.have_pressure = False
        self.have_light = False
        self.have_airvtoc = False
        self.have_airco2 = False


manager = gatt.DeviceManager(adapter_name='hci0')

# set YOUR NXP Rapid IoT device mac address here, in lower case
# find with:  hcitool lescan
device = AnyDevice(manager=manager, mac_address='00:60:37:aa:bb:cc')

device.connect()

manager.run()


