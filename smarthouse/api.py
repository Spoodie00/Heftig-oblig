import uvicorn
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
import os
import datetime

def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    return SmartHouseRepository(str(db_file.absolute()))

app = FastAPI()

repo = setup_database()

smarthouse = repo.load_smarthouse_deep()

if not (Path.cwd() / "www").exists():
    os.chdir(Path.cwd().parent)
if (Path.cwd() / "www").exists():
    # http://localhost:8000/welcome/index.html
    app.mount("/static", StaticFiles(directory="www"), name="static")


def lookup(table, list_of_columns, fetch="all", condition_variable="", condition_value=""):

    if fetch not in ["all", "one"]:
        raise ValueError("fetch parameter must be 'all' or 'one'")

    connector = repo.conn.cursor()
    columns = ", ".join(list_of_columns)
    query = f"""
        SELECT {columns}
        FROM {table}
    """

    if condition_variable and condition_value:
        query += f"WHERE {condition_variable} = '{condition_value}'"

    if fetch == "all":
        output = connector.execute(query).fetchall()
    else:
        output = connector.execute(query).fetchone()

    connector.close()
    return output


# http://localhost:8000/ -> welcome page
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")


# Health Check / Hello World
@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}


# Starting point ...

@app.get("/smarthouse")
def get_smarthouse_info() -> dict[str, int | float]:
    """
    This endpoint returns an object that provides information
    about the general structure of the smarthouse.
    """
    return {
        "no_rooms": len(smarthouse.get_rooms()),
        "no_floors": len(smarthouse.get_floors()),
        "registered_devices": len(smarthouse.get_devices()),
        "area": smarthouse.get_area()
    }


@app.get("/smarthouse/floor")
def get_floor_info():
    reading = lookup("rooms", ["floor"])

    output = {"floors": []}

    for floor in reading:
        if floor[0] not in output["floors"]:
            output["floors"].append(floor[0])

    return output


@app.get("/smarthouse/floor/{fid}")
def get_floor_info(fid):

    reading = lookup("rooms", ["area", "name"], condition_variable="floor", condition_value=fid)

    sqm = 0
    rooms = []
    for line in reading:
        sqm += line[0]
        rooms.append(line[1])

    return {
        "sqm": sqm,
        "rooms": rooms,
    }


@app.get("/smarthouse/floor/{fid}/room")
def get_floor_rooms(fid):
    reading = lookup("rooms", ["name", "id"], condition_variable="floor", condition_value=fid)
    output = {}
    for line in reading:
        output[line[0]] = line[1]

    return output


@app.get("/smarthouse/floor/{fid}/room/{rid}")
def get_specific_room(rid):
    reading = lookup("rooms", ["name", "area"], fetch="one", condition_variable="id", condition_value=rid)
    devices = lookup("devices", ["id", "supplier", "product"], condition_variable="room", condition_value=rid)

    output = {
        "name": reading[0],
        "sqm": reading[0],
    }

    linecount = 0
    for line in devices:
        output["device " + str(linecount)] = {
            "device id": line[0],
            "supplier": line[1],
            "name": line[2]
        }
        linecount += 1

    return output


@app.get("/smarthouse/device")
def get_all_devices():
    devices = lookup("devices", ["id", "supplier", "product"])

    output = {}

    linecount = 0
    for line in devices:
        output["device " + str(linecount)] = {
            "device id": line[0],
            "supplier": line[1],
            "name": line[2]
        }
        linecount += 1

    return output


@app.get("/smarthouse/device/{uuid}")
def get_specific_device(uuid):
    reading = lookup("devices", ["*"], fetch="one", condition_variable="id", condition_value=str(uuid))
    room = lookup("rooms", ["name"], fetch="one", condition_variable="id", condition_value=reading[1])

    return {
        "supplier": reading[4],
        "product": reading[5],
        "kind": reading[2],
        "category": reading[3],
        "room": room[0]
    }


""" spesielle endepunkter for tilgang til sensor funksjoen"""

@app.get("/smarthouse/sensor/{uuid}/current")
def get_sensor(uuid):
    """get current sensor measurement for sensor uuid"""

    device_object = smarthouse.get_device_by_id(uuid)
    reading = repo.get_latest_reading(device_object)

    return reading

@app.post("/smarthouse/sensor/{uuid}/current")
def create_measurement(uuid):
    """Add measurement for sensor uuid"""
    device_object = smarthouse.get_device_by_id(uuid)
    sensor_object = device_object.last_measurement()

    timestamp = datetime.datetime.now()
    connector = repo.conn.cursor()

    query = f"""
           INSERT INTO measurements(device, ts, value, unit)
           VALUES('{uuid}', '{timestamp}', '{sensor_object.temp}', '{sensor_object.unit}')
       """
    connector.execute(query)
    connector.close()

    return sensor_object.temp


@app.get("/smarthouse/sensor/{uuid}/values")
def get_sensor_values(uuid, limit):
    """Get n latest available measurements for sensor uuid"""
    device_object = smarthouse.get_device_by_id(uuid)
    measurements = repo.get_latest_reading(device_object, limit)
    print(measurements)
    return measurements


@app.delete("/smarthouse/sensor/{uuid}/oldest")
def delete_oldest_measurement(uuid):
    """Delete oldest measurements for sensor uuid"""

    connector = repo.conn.cursor()

    query = f"""
        DELETE FROM measurements
        WHERE device = {uuid}
        ORDER BY ts ASC
        LIMIT 1
    """

    connector.execute(query)
    connector.close()

    return "Success"


@app.get("/smarthouse/actuator/{uuid}/current")
def get_current_actuator(uuid):
    """get current state for actuator uuid"""
    device = smarthouse.get_device_by_id(uuid)
    reading = 0
    if device.actuator:
        reading = lookup(f"update_actuator_state", ["is_active"], "one", "deviceid", uuid)
        if reading is None:
            repo.update_actuator_state(device)
            reading = lookup(f"update_actuator_state", ["is_active"], "one", "deviceid", uuid)
            return reading
    return reading[0]


@app.put("/smarthouse/device/{uuid}")
def update_device(uuid: str, state: dict = None):
    """update current state for actuator uuid"""
    device = smarthouse.get_device_by_id(uuid)
    if (state["is_active"] == "Off" and device.is_active()) or (state["is_active"] == "On" and not device.is_active()):
        repo.update_actuator_state(device)
    return {"is_active": device.is_active()}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
