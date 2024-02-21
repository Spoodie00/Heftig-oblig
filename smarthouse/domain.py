class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit


# TODO: Add your own classes here!
class Device:
    def __init__(self, room1, device_type, deviceid, model_name, supplier, sensor_type=None):
        self.device_type = device_type
        self.room = room1
        SmartHouse.num_devices.append(device_type)
        self.id = deviceid
        SmartHouse.iddevice.append(deviceid)
        self.model_name = model_name
        self.supplier = supplier
        self.actuator = False
        self.sensor = False
        if sensor_type == "both":
            self.actuator = True
            self.sensor = False
        elif sensor_type == "sensor":
            self.sensor = True
        elif sensor_type == "actuator":
            self.actuator = True

    def is_actuator(self):
        return self.actuator

    def is_sensor(self):
        return self.sensor

    # Denne skal returnere room-objektet under, men ser ikke helt hvorfor den ikke gjør det
    # skal prøve senere med en sterkere espresso
    def room(self):
        return self.room


class Room:
    def __init__(self, floor, room_size, room_name=None):
        self.floor = floor
        self.room_size = room_size
        self.room_name = room_name

    def devices(self):
        output = []
        for device in SmartHouse.device_list:
            if device.room == self:
                output.append(device)
        return output



class Sensor:
    def __init__(self, device_id, supplier, model_name):
        self.type = Device.device_type


class Aktuator:
    def __init__(self, device_id, supplier, model_name):
        self.type = Device.device_type


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the
    house's physical layout) as well as register and modify smart devices and their state.
    """

    device_list = {}
    num_devices = []
    iddevice = []
    room_list = {}

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

    def register_floor(self, level):
        self.level = level
        self.num_floors.append(level)

    def register_room(self, floor, room_size, room_name=None):
        self.num_rooms.append(room_name)
        self.area.append(room_size)
        self.floorspace = sum(self.area)
        new_room = Room(floor, room_size, room_name=None)
        SmartHouse.room_list[room_name] = new_room

    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has
        registered a basement (level=0), a ground floor (level=1) and a first floor
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return self.num_floors

    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        return self.num_rooms

    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        return self.floorspace

    def register_device(self, room, device_type, deviceid, devicename, supplier, sensor_type=False):
        """
        This methods registers a given device in a given room.
        """
        new_device = Device(room, device_type, deviceid, devicename, supplier, sensor_type)
        SmartHouse.device_list[deviceid] = new_device


    def get_devices(self):
        output = []
        for key in SmartHouse.device_list:
            output.append(SmartHouse.device_list[key])
        return output

    def get_device_by_id(self, variable1):
        try:
            return SmartHouse.device_list[variable1]
        except KeyError:
            return None