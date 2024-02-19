class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

class Device: #Muligens fakket det litt til her lols:D
    Type=str
    ModelName=str
    DeviceID=str
    DeviceProducer=str
    def __init__(self,Room, Type, DeviceID,ModelName, DeviceProducer):
        self.Location=Room
        self.Device=Type
        self.DeviceName=ModelName
        self.DeviceID=DeviceID
        self.DeviceProducer=DeviceProducer

class Measurements: #Gjorde dette for en stund tilbake, husker ikke helt hva jeg tnekte
    def handleTime(self, Time: DateTime):
        pass

    def handleValue(self, Value: float):
        pass

    def handleMeasurem(self, Measure: str):
        pass
class Sensor:
    def __init__(self):
        pass
    def accept(self, visitor: Measurements):
        pass

# TODO: Add your own classes here!




class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """

    def __init__(self):
        #Legg til countere her hvis nødvendig
        self.num_floors = []
        self.num_rooms = []
        self.floorspace = 0


    def register_floor(self, level):
        # Ferdig
        self.level = level
        self.num_floors.append(level)

    def register_room(self, floor, room_size, room_name = None):
        # Ferdig
        self.floor = floor
        self.room_size = room_size
        self.room_name = room_name
        self.num_rooms.append(room_name)
        self.floorspace += room_size


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
        #Ferdig
        return self.num_rooms


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        return self.floorspace


    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        pass

    
    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        pass

