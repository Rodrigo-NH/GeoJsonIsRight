from osgeo import ogr
from osgeo import osr
import sqlite3

#
#The formal EPSG definition provides the axis-order used to interpret coordinate values.

def main():
    EPSGcodes = []
    database = r"C:\Program Files\GDAL\projlib\proj.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT code FROM crs_view WHERE auth_name = 'EPSG';")
    rows = cur.fetchall()
    for row in rows:
        EPSGcodes.append(row[0])

    LatLong_count = 0
    LongLat_count = 0
    for epsg in EPSGcodes:
        records = []
        osrs = osr.SpatialReference()
        osrs.ImportFromEPSG(epsg)
        if "AXIS" in str(osrs):
            ga = str(osrs).split('\n')
            for line in ga:
                if "AXIS" in line:
                    records.append(line.strip().upper())
            if "LATITUDE" in records[0] or "NORTH" in records[0] or "NORTHING" in records[0]:
                LatLong_count += 1
            if "EASTING" in records[0] or "EAST" in records[0] or "LONGITUDE" in records[0]:
                LongLat_count += 1


    result = "From {total} EPSG codes evaluated, {longp}% defines Long/Lat order and {latp}% defines Lat/Long order."
    totalEPSG = LatLong_count + LongLat_count
    latp = round(LatLong_count/totalEPSG * 100, 1)
    longp = round(LongLat_count / totalEPSG * 100, 1)
    print(result.format(total=totalEPSG,latp=latp,longp=longp))


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

if __name__ == "__main__":
        main()