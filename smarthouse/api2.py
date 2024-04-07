import uvicorn
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
import os
import sqlite3

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
        query += f"WHERE {condition_variable} = {condition_value}"

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
    """ information about a floor given by fid"""
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
    """information about all rooms on a given floor fid"""
    reading = lookup("rooms", ["name", "id"], condition_variable="floor", condition_value=fid)
    output = {}
    for line in reading:
        output[line[0]] = line[1]

    return output


@app.get("/smarthouse/floor/{fid}/room/{rid}")
def get_specific_room(rid):
    """information about a specific room rid on a given floor fid"""
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
    """ information for a given device identfied by uuid"""
    devices = lookup("devices", ["id", "supplier", "product"], condition_variable="device", condition_value=uuid)

    output = {
        "name": devices[0],
        "sqm": devices[0],
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


""" spesielle endepunkter for tilgang til sensor funksjone"""



"""GET smarthouse/sensor/{uuid}/current - get current sensor measurement for sensor uuid"""
@app.get("smarthouse/sensor/{uuid}/current")
def get_sensor(uuid: str, response: Response):
    """get current sensor measurement for sensor uuid"""
    devices = lookup("devices", ["id", "supplier", "product"],  condition_variable="devices", condition_value=uuid)

    currentdevice = {}
    linecount = 0

    for line in devices:
        currentdevice["device " + str(linecount)] = {
            "device id": line[0],
            "supplier": line[1],
            "name": line[2]
        }
        linecount += 1

    return currentdevice

@app.post("/smarthouse/sensor/{uuid}/current")
def create_measurement(uuid:str, currentdevice: sensor, response: Response) -> sensor | None:
    """Add measurement for sensor uuid"""
    add_measurement = SmartHouseRepository.get_latest_reading(uuid, currentdevice)
    return add_measurement


@app.get("/smarthouse/sensor/{uuid}/values")
def get_sensor_values(uuid: str, limit: Optional[int] = None, response: Response):
    """Get n latest available measurements for sensor uuid"""
    measurements = SmartHouseRepository.get_latest_reading(uuid)

    if limit is not None:
        measurements = measurements[:limit]

    return measurements


@app.delete("/smarthouse/sensor/{uuid}/oldest")
def delete_oldest_measurement(uuid: str, response: Response):
    """Delete oldest measurements for sensor uuid"""
    success = SmartHouseRepository.delete_oldest_measurement(uuid)

    if success:
        return {"message": "Oldest measurements deleted successfully"}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "No measurements found"}

    return None



@app.get("/smarthouse/actuator/{uuid}/current")
def get_current_actuator(uuid:str, response: Response):
    """get current state for actuator uuid"""
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

@app.put("/smarthouse/device/{uuid}")
def update_device(uuid:str, actuator: bool, response: Response):
    """update current state for actuator uuid"""
    device_result=SmartHouseRepository.update_actuator_state(uuid, actuator)
    if device_result:
        return device_result
    else:
        response.status_code = status.HTTP_404_NOT_FOUND

        return None