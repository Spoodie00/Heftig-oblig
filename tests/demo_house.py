from smarthouse.domain import SmartHouse
# TODO: continue registering the remaining floor, rooms and devices

# Tenkte sånn, men ork å modifiere nå, hvis jeg tenker feil å decives.

DEMO_HOUSE = SmartHouse()

# Building house structure
# Floors
ground_floor = DEMO_HOUSE.register_floor(1)
first_floor = DEMO_HOUSE.register_floor(2)
# Rooms
# Ground floor
Entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
Bathroom1 = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom 1")
GuestRoom1 = DEMO_HOUSE.register_room(ground_floor, 8, "Guest Room 1")
LivingRoomKitchen = DEMO_HOUSE.register_room(ground_floor, 39.75, "Living Room/Kitchen")
Garage = DEMO_HOUSE.register_room(ground_floor, 19, "Garage")
# First floor
Hallway = DEMO_HOUSE.register_room(first_floor, 10, "Hallway")
Bathroom2 = DEMO_HOUSE.register_room(first_floor, 9.25, "Bathroom 2")
GuestRoom2 = DEMO_HOUSE.register_room(first_floor, 8, "Guest Room 2")
GuestRoom3 = DEMO_HOUSE.register_room(first_floor, 10, "Guest Room 3")
Dresser = DEMO_HOUSE.register_room(first_floor, 4, "Dressing Room")
MasterBedroom = DEMO_HOUSE.register_room(first_floor, 17, "Master Bedroom")
Office = DEMO_HOUSE.register_room(first_floor, 11.75, "Office")

# Devices
# Devices Ground floor
AutomaticGarageDoor = DEMO_HOUSE.register_device(Garage, "Automatic Garage Door", "9a54c1ec-0cb5-45a7-b20d-2a7349f1b132", "Guardian Lock 9000", "MythicalTech")
SmartLock = DEMO_HOUSE.register_device(Entrance, "Smart Lock", "4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", "Guardian Lock 7000", "MythicalTech")
ElectricityMeter = DEMO_HOUSE.register_device(Entrance, "Electricity Meter", "a2f8690f-2b3a-43cd-90b8-9deea98b42a7", "Volt Watch Elite", "MysticEnergy Innovations")
MotionSensor = DEMO_HOUSE.register_device(LivingRoomKitchen, "Motion Sensor", "cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5", "MoveZ Detect 69","NebulaGuard Innovations", "sensor")
CO2Sensor = DEMO_HOUSE.register_device(LivingRoomKitchen, "CO2 sensor", "8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e", "Smoke Warden 1000", "	ElysianTech")
HeatPump = DEMO_HOUSE.register_device(LivingRoomKitchen, "Heat Pump", "5e13cabc-5c58-4bb3-82a2-3039e4480a6d", "Thermo Smart 6000","	ElysianTech", "actuator")
HumiditySensor = DEMO_HOUSE.register_device(Bathroom1, "Humidity Sensor", "3d87e5c0-8716-4b0b-9c67-087eaaed7b45", "Aqua Alert 800", "AetherCorp")
SmartOven = DEMO_HOUSE.register_device(GuestRoom1, "Smart Oven", "8d4e4c98-21a9-4d1e-bf18-523285ad90f6", "Pheonix HEAT 333","AetherCorp")


# Devices First floor
SmartOven1 = DEMO_HOUSE.register_device(MasterBedroom, "Smart Oven", "c1e8fa9c-4b8d-487a-a1a5-2b148ee9d2d1", "Ember Heat 3000", "IgnisTech Solutions")
TemperatureSensor = DEMO_HOUSE.register_device(MasterBedroom, "Temperature Sensor", "4d8b1d62-7921-4917-9b70-bbd31f6e2e8e", "SmartTemp 42", "AetherCorp", "sensor")
AirQualitySensor = DEMO_HOUSE.register_device(GuestRoom3, "Air Quality Sensor", "7c6e35e1-2d8b-4d81-a586-5d01a03bb02c", "AeroGuard Pro", "CelestialSense Technologies")
LightBulb = DEMO_HOUSE.register_device(GuestRoom2, "Light Bulp", "6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28", "Lumina Glow 4000", "Elysian Tech", "actuator")
Dehumidifier = DEMO_HOUSE.register_device(Bathroom2, "Dehumidifier", "9e5b8274-4e77-4e4e-80d2-b40d648ea02a", "Hydra Dry 8000", "ArcaneTech Solutions	")
SmartPlg = DEMO_HOUSE.register_device(Office, "Smart Plug", "1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79", "FlowState X", "MysticEnergy Innovations")
