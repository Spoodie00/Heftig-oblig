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
        self.conn = sqlite3.connect(file)

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
        self.conn.commit()
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

        for device in measurements_result:
            value = device[2]
            test_house.register_device(value)

        return test_house


    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here
        connector = self.conn.cursor()
        reading = connector.execute("SELECT * FROM measurements WHERE device = ? ORDER BY ts DESC LIMIT 1", (sensor.id,)).fetchone()
        connector.close()
        output1 = sensor.last_measurement(reading)
        if isinstance(output1, str) or reading == None:
            return None
        else:
            return output1

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
            state=1 if actuator.is_active() or actuator.turnon() else 0
            # Update the existing actuator state
            cursor.execute("UPDATE update_actuator_state SET is_active = ?, tunron=? WHERE deviceid = ?",
                           (actuator.is_active(), actuator.turnon(), actuator.get_id()))
            existing_actuator = cursor.fetchall()
        else:
            state=1 if actuator.is_active() or actuator.turnon() else 0
            # Insert a new record for the actuator
            cursor.execute("INSERT INTO update_actuator_state (deviceid, is_active, turnon) VALUES (?,?,?)",
                           (actuator.get_id(), actuator.is_active(), actuator.turnon()))
            existing_actuator=cursor.fetchall()

        self.conn.commit()
        cursor.close()
        return existing_actuator

    # statistics

    
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
        # TODO: This and the following statistic method are a bit more challenging. Try to design the respective 
        #       SQL statements first in a SQL editor like Dbeaver and then copy it over here.  
        connector = self.conn.cursor()
        reading = connector.execute("SELECT * FROM measurements WHERE value>(SELECT AVG(value) FROM measurement WHERE deivce=(SELECT id FROM devices WHERE room=?) ) = ? ORDER BY ts DESC LIMIT 1",
                                    (room.id,)).fetchall()
        connector.close()
        output = room.last_measurement(reading)
        if isinstance(output1, str) or reading == None:
            return None
        else:
            return output

    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        connector = self.conn.cursor()
        humidityabove=[]

        reading = connector.execute(
            "SELECT * FROM measurements WHERE value>(SELECT AVG(value) FROM measurement WHERE deivce=(SELECT id FROM devices WHERE room=?) ) = ? ORDER BY ts DESC LIMIT 1",
            (room.id,)).fetchall()
        output=connector.execute(reading, (room.id, date)).fetchall()
        connector.close()

        for hour, avg_humidity in output:
            # Query to get the count of measurements above the average humidity for each hour
            above_avg_count_query = """
                SELECT COUNT(*) 
                FROM measurements 
                WHERE device IN (
                    SELECT id 
                    FROM devices 
                    WHERE room = ?
                ) 
                AND date(ts) = ? 
                AND strftime('%H', ts) = ? 
                AND value > ?
                """
            # Execute the query with room ID, date, hour, and average humidity
            above_avg_count = connector.execute(above_avg_count_query, (room.id, date, hour, avg_humidity)).fetchone()[
                0]

            # If the count is greater than 3, add the hour to the result list
            if above_avg_count > 3:
                humidityabove.append(hour)

        return humidityabove