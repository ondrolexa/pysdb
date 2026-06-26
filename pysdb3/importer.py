import csv
import json
from pathlib import Path

from lxml import etree


def parse_gpx(fname):
    """Parse GPX waypoints. Returns list of (name, lon, lat) tuples."""
    NSMAP = {"gpx": "http://www.topografix.com/GPX/1/1"}
    tree = etree.parse(str(fname))
    return [
        (
            elem.find("gpx:name", namespaces=NSMAP).text,
            float(elem.attrib["lon"]),
            float(elem.attrib["lat"]),
        )
        for elem in tree.findall("gpx:wpt", namespaces=NSMAP)
    ]


def parse_csv(fname):
    """Parse CSV file. Returns (columns, rows) tuple."""
    with Path(fname).open() as src:
        sample = src.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        has_header = csv.Sniffer().has_header(sample)
        src.seek(0)
        rows = list(csv.reader(src, dialect=dialect))
    if has_header:
        columns = rows[0]
        rows = rows[1:]
    else:
        columns = [f"Col {n + 1}" for n in range(len(rows[0]))]
    return columns, rows


def parse_geojson(fname):
    """Parse GeoJSON FeatureCollection of Points.

    Returns (properties, features) where features is a list of
    (props_dict, (lon, lat)) tuples.
    Raises ValueError for unsupported formats or empty collections.
    """
    with Path(fname).open() as src:
        data = json.load(src)
    if data["type"] != "FeatureCollection":
        raise ValueError("GeoJSON must contain FeatureCollection")
    if not data["features"]:
        raise ValueError("There are no features in file")
    if data["features"][0]["geometry"]["type"] != "Point":
        raise ValueError("Features must be points")
    props = list(data["features"][0]["properties"].keys())
    features = [
        (
            feature["properties"],
            (
                float(feature["geometry"]["coordinates"][0]),
                float(feature["geometry"]["coordinates"][1]),
            ),
        )
        for feature in data["features"]
    ]
    return props, features
