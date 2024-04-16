import random
import datetime

class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit


class Device:
    def __init__(self, room, device_type, deviceid, model_name, supplier, sensor_type=None):
        self.device_type = device_type
        self.room = room
        SmartHouse.num_devices.append(device_type)
        self.id = deviceid
        SmartHouse.iddevice.append(deviceid)
        self.model_name = model_name
        self.supplier = supplier
        self.actuator = False
        self.sensor = False
        self.is_active1 = False
        self.target_value = 0  # Setter definisjonene til enheten

        if sensor_type == "both":  # Setter scenario for definisjon til enhetstypen.
            self.actuator = True
            self.sensor = True
        elif sensor_type == "sensor":
            self.sensor = True
        elif sensor_type == "actuator":
            self.actuator = True

    def get_id(self):
        return self.id


    def is_actuator(self):
        return self.actuator

    def is_sensor(self):
        return self.sensor

    def room(self):
        return self.room

    def last_measurement(self, measurement=None):  # Setter målenene til sensor variabel
        if self.sensor:
            output = Sensor(measurement)
            return output
        else:
            return "Not a sensor"

    def turn_on(self, value=0):  # Setter aktivering for aktuator
        if self.actuator:
            self.is_active1 = True
            self.target_value = value

    def turn_off(self):  # ""_"" deaktivering
        if self.actuator:
            self.is_active1 = False

    def is_active(self):
        return self.is_active1


class Sensor:
    def __init__(self, measurement_tuple=None):  # setter definisjonene til sensor klassen
        if not measurement_tuple:
            self.temp = random.uniform(10.5, 75.5)
            self.unit = "°C"
            timestamp = datetime.datetime.now()
            self.timestamp = timestamp
        else:
            self.timestamp = measurement_tuple[0][1]
            self.reading = measurement_tuple[0][2]
            self.unit = measurement_tuple[0][3]

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value

    @property
    def value(self):
        return self.temp

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value


class Room:
    def __init__(self, floor, room_size, room_name=None):
        self.floor = floor
        self.room_size = room_size
        self.room_name = room_name

    def devices(self):  # Setter enhet i rom.
        output = []
        for device in SmartHouse.device_list:
            if SmartHouse.device_list[device].room == self:
                output.append(SmartHouse.device_list[device])
        return output


class HouseFloor:
    def __init__(self, level):
        self.level = level


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the
    house's physical layout) as well as register and modify smart devices and their state.
    """
# Setter plass for variablene
    device_list = {}
    num_devices = []
    iddevice = []
    room_list = {}
    floor_list = []

    def __init__(self):
        # Legg til countere her hvis nødvendig
        self.num_floors = []
        self.num_rooms = []
        self.floorspace = 0
        self.area = []
        self.a = []
        self.b = []
        self.floor = None
        self.room_size = None
        self.room_name = None
        self.level = None
        self.device = None
        self.deviceId = None
        self.DeviceName = None
        self.Producer = None
        self.variable1 = None
        self.room = None
        self.id = None

    def register_floor(self, level):  # Definerer og lagrer etasje
        int_level = int(level)
        SmartHouse.floor_list.append(int_level)

    def register_room(self, floor, room_size, room_name=None):  # "_" rom
        self.num_rooms.append(room_name)
        self.area.append(room_size)
        self.floorspace = sum(self.area)
        new_room = Room(floor, room_size, room_name)
        SmartHouse.room_list[room_name] = new_room
        return new_room

    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has
        registered a basement (level=0), a ground floor (level=1) and a first floor
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return SmartHouse.floor_list

    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        output = []
        for key in SmartHouse.room_list:
            output.append(SmartHouse.room_list[key])
        return output

    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        return self.floorspace

    def register_device(self, room, device_type=None, deviceid=None, devicename=None, supplier=None, sensor_type=False):
        """
        This methods registers a given device in a given room.
        """
        if deviceid:
            new_device = Device(room, device_type, deviceid, devicename, supplier, sensor_type)
            SmartHouse.device_list[deviceid] = new_device
        else:
            device_type.room = room

    def get_devices(self):  # Gir liste med enheter registert
        output = []
        for key in SmartHouse.device_list:
            output.append(SmartHouse.device_list[key])
        return output

    def get_device_by_id(self, variable1):  # Gir enhet fra liste ved input av enhetsid.
        try:
            return SmartHouse.device_list[variable1]
        except KeyError:
            return None