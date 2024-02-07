from smarthouse.domain import SmartHouse

DEMO_HOUSE = SmartHouse()

# Building house structure
ground_floor = DEMO_HOUSE.register_floor(1)

entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
bathroom_1 = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom 1")
guest_room_1 = DEMO_HOUSE.register_room(ground_floor, 8, "Guest room 1")
living_room_and_kitchen = DEMO_HOUSE.register_room(ground_floor, 39.75, "Living room and kitchen")
garage = DEMO_HOUSE.register_room(ground_floor, 19, "garage")

second_floor = DEMO_HOUSE.register_floor(2)
bathroom_2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom 2")
guest_room_2 = DEMO_HOUSE.register_room(second_floor, 8, "Guest room 2")
guest_room_3 = DEMO_HOUSE.register_room(second_floor, 10, "Guest room 3")
office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
dressing_room = DEMO_HOUSE.register_room(second_floor, 4, "Dressing room")
hallway = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
master_bedroom = DEMO_HOUSE.register_room(second_floor, 17, "Master Bedroom")

# TODO: continue registering the remaining floor, rooms and devices

