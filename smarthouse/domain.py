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
    def __init__(self, device_type,  device_id, supplier, model_name):
        self.id = device_id
        self.supplier = supplier
        self.model_name = model_name
        self.device_type = device_type
        self.type = None


class Sensor():
    def __init__(self, device_id, supplier, model_name):
        self.type = Device.device_type


class Aktuator():
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

    def __init__(self):
        # Legg til countere her hvis nødvendig
        self.num_floors = []
        self.num_rooms = []
        self.floorspace = 0
        self.num_devices = []
        self.iddevice = []
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
        self.devices3 = []
        self.room = None
        self.id = None

    def register_floor(self, level):
        self.level = level
        self.num_floors.append(level)

    def register_room(self, floor, room_size, room_name=None):
        self.floor = floor
        self.room_size = room_size
        self.room_name = room_name
        self.num_rooms.append(room_name)
        self.area.append(room_size)
        self.floorspace = sum(self.area)


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

    def register_device(self, room, Type, DeviceID, DeviceName, Producer):
        """
        This methods registers a given device in a given room.
        """
        self.device = Type
        self.room = room
        self.num_devices.append(Type)
        self.id = DeviceID
        self.iddevice.append(DeviceID)
        self.DeviceName = DeviceName
        self.Producer = Producer
        self.devices3.append(self)



    def get_devices(self):
        """
        This method retrieves a device object via its id.
        """
        return self.num_devices

    def get_device_by_id(self, variable1):
        for unit1 in self.devices3:
            if unit1.id == variable1:
                return unit1