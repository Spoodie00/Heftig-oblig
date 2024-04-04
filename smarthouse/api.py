import uvicorn
from fastapi import FastAPI
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


@app.get("/smarthouse/floor", response_class=HTMLResponse)
def get_floor_info():
    connector = repo.conn.cursor()
    reading = connector.execute("""
        SELECT floor
        FROM rooms
        """, ).fetchall()
    connector.close()

    output = []

    for line in reading:
        if line[0] not in output:
            output.append(line[0])

    return output


@app.get("/smarthouse/floor/{fid}", response_class=HTMLResponse)
def get_floor_info(fid):
    connector = repo.conn.cursor()
    reading = connector.execute("""
        SELECT area, name
        FROM rooms
        WHERE floor = ?
        """, (fid,)).fetchall()
    connector.close()
    sqm = 0
    rooms = []
    for line in reading:
        sqm += line[0]
        rooms.append(line[1])

    output = "Square meters: {} <br> Rooms: {}".format(sqm, rooms)

    return output


@app.get("/smarthouse/floor/{fid}/room", response_class=HTMLResponse)
def get_floor_info():
    connector = repo.conn.cursor()
    reading = connector.execute("""
        SELECT name, id
        FROM rooms
        """, ).fetchall()
    connector.close()
    output = []
    for line in reading:
        output.append(list((line[1], line[0])))

    return output


@app.get("/smarthouse/floor/{fid}/room/{rid}", response_class=HTMLResponse)
def get_floor_info(rid):
    connector = repo.conn.cursor()
    reading = connector.execute("""
        SELECT name, area
        FROM rooms
        WHERE id = ?
        """, (rid,)).fetchall()

    devices = connector.execute("""
        SELECT id, supplier, product
        FROM devices
        WHERE room = ?
        """, (rid,)).fetchall()

    connector.close()

    output = "Name: {} <br> Square meters: {}  <br> ".format(reading[0][0], reading[0][1])

    for line in devices:
        output += "<br> Device ID: {} <br> Supplier: {} <br> Name: {} <br>".format(line[0], line[1], line[2])

    return output


@app.get("/smarthouse/room", response_class=HTMLResponse)
def get_floor_info():
    connector = repo.conn.cursor()

    devices = connector.execute("""
        SELECT id, supplier, product
        FROM devices
        """).fetchall()

    connector.close()

    output = ""

    for line in devices:
        output += "Device ID: {} <br> Supplier: {} <br> Name: {} <br><br>".format(line[0], line[1], line[2])

    return output



if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)


