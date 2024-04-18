import sqlite3
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file: str) -> None:
        self.file = file
        self.conn = sqlite3.connect(file, check_same_thread=False)

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        # TODO: START here! remove the following stub implementation and implement this function 
        #       by retrieving the data from the database via SQL `SELECT` statements.

        test_house = SmartHouse()

        connector = self.conn.cursor()
        connector.execute("SELECT * FROM rooms;")
        result = connector.fetchall()
        connector.close()

        for room in result:
            floor = room[1]
            floor_size = room[2]
            name = room[3]
            if floor not in SmartHouse.floor_list:
                test_house.register_floor(floor)
            test_house.register_room(floor, floor_size, name)

        connector = self.conn.cursor()
        connector.execute("SELECT * FROM devices;")
        result = connector.fetchall()
        connector.close()

        for device in result:
            room_list = test_house.get_rooms()
            room = room_list[device[1]-1]
            device_type = device[2]
            deviceid = device[0]
            device_name = device[5]
            supplier = device[4]
            sensor_type = device[3]
            test_house.register_device(room, device_type, deviceid, device_name, supplier, sensor_type)

        connector = self.conn.cursor()
        connector.execute("SELECT * FROM measurements;")
        measurements_result = connector.fetchall()
        connector.close()

        connector = self.conn.cursor()
        connector.execute("SELECT deviceid, is_active FROM update_actuator_state ;")
        result = connector.fetchall()
        connector.close()
        for row in result:
            device = test_house.get_device_by_id(row[0])
            device.is_active1 = bool(row[1] == 1)

        return test_house

    def get_latest_reading(self, sensor, n=1):
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here
        connector = self.conn.cursor()
        if int(n) == 1:
            print(n)
            reading = connector.execute(f"SELECT * FROM measurements WHERE device = '{sensor.id}' ORDER BY ts DESC").fetchone()
        else:
            print("tedt")
            reading = connector.execute(
                f"SELECT * FROM measurements WHERE device = '{sensor.id}' ORDER BY ts DESC LIMIT '{n}'").fetchall()
        connector.close()
        output1 = sensor.last_measurement(reading)
        if isinstance(output1, str) or reading is None:
            return None
        else:
            return reading

    def update_actuator_state(self, actuator):
        cursor = self.cursor()

        # Check if the actuator state table exists, if not create it
        cursor.execute('''CREATE TABLE IF NOT EXISTS update_actuator_state (
                              deviceid TEXT,
                              is_active INTEGER,
                              turnon INTEGER
                          )''')

        # Check if the actuator already exists in the table
        cursor.execute("SELECT * FROM update_actuator_state WHERE deviceid = ?", (actuator.get_id(),))
        existing_actuator = cursor.fetchall()

        if existing_actuator:
            state = 0 if actuator.is_active() or actuator.turn_on() else 1
            # Update the existing actuator state
            print(state)
            cursor.execute("UPDATE update_actuator_state SET is_active = ?, turnon=? WHERE deviceid = ?",
                           (state, actuator.turn_on(), actuator.get_id()))
            if state == 0:
                actuator.is_active1 = False
        else:
            state=1 if actuator.is_active() or actuator.turn_on() else 0
            print("tetete")
            # Insert a new record for the actuator
            cursor.execute("INSERT INTO update_actuator_state (deviceid, is_active, turnon) VALUES (?,?,?)",
                           (actuator.get_id(), actuator.is_active(), actuator.turn_on()))

        self.conn.commit()
        cursor.close()

        pass

    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        device_list = []
        params = []
        result = []
        query = """
                SELECT ts, value, unit
                FROM measurements
                WHERE device = ?
                AND unit = '°C'
                """

        if from_date is not None:
            query += " AND ts >= ?"
            params.append(from_date)
        if until_date is not None:
            until_date = until_date[:-2] + str(int(until_date[-2:]) + 1)
            query += " AND ts <= ?"
            params.append(until_date)

        for device in room.devices():
            device_list.append(device.get_id())

        connector = self.conn.cursor()
        for device in device_list:
            reading = connector.execute(query, (device, *params)).fetchall()
            result.append(reading)
        connector.close()

        reading_dict = {}
        for device_reading in result:
            for row in device_reading:
                timestamp = row[0][0:10]
                reading = row[1]
                try:
                    reading_dict[timestamp].append(reading)
                except KeyError:
                    reading_dict[timestamp] = [reading]

        avg_temp_dict = {}
        for key, value in reading_dict.items():
            avg_temp = sum(value) / len(value)
            avg_temp_dict[key] = avg_temp

        return avg_temp_dict

    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        timestamps = {}
        sensor_id = ""
        output = []
        device_list = room.devices()

        for device in device_list:
            if device.is_sensor():
                sensor_id = device.get_id()
                break

        connector = self.conn.cursor()
        reading = connector.execute("""
            SELECT ts, value
            FROM measurements
            WHERE device = ?
            AND strftime('%Y-%m-%d', ts) = ?
            ORDER BY ts ASC
            """, (sensor_id, date)).fetchall()
        connector.close()

        humidity_readings = list(map(lambda x: x[1], reading))
        avg = sum(humidity_readings) / len(humidity_readings)

        for row in reading:
            timestamp_hour = str(row[0])[11:13]
            if row[1] > avg:
                try:
                    timestamps[timestamp_hour] += 1
                except KeyError:
                    timestamps[timestamp_hour] = 1

        for key in timestamps:
            if timestamps[key] > 3:
                output.append(int(key))

        return output

    def get_floor_info(self, floor_id):
        connector = self.conn.cursor()
        reading = connector.execute("""
            SELECT *
            FROM rooms
            WHERE floor = ?
            """, floor_id).fetchall()
        connector.close()