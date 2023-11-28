import requests
import xml.etree.ElementTree as ET
import json

def generate_hanoi_bounding_boxes(min_lat, min_lon, max_lat, max_lon, rows, cols):
    # Calculate the size of each grid cell
    lat_step = (max_lat - min_lat) / rows
    lon_step = (max_lon - min_lon) / cols

    # Generate bounding boxes
    bounding_boxes = []
    for i in range(rows):
        for j in range(cols):
            # Calculate the coordinates for each bounding box
            box_min_lat = min_lat + i * lat_step
            box_min_lon = min_lon + j * lon_step
            box_max_lat = box_min_lat + lat_step
            box_max_lon = box_min_lon + lon_step

            # Format the bounding box coordinates
            bbox_coordinates = f"{box_min_lat},{box_min_lon},{box_max_lat},{box_max_lon}"
            bounding_boxes.append(bbox_coordinates)

    return bounding_boxes

def get_shops_in_bbox(bbox):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f'[bbox:{bbox}]; node["shop"]({bbox}); out;'

    response = requests.post(overpass_url, data=overpass_query)

    try:
        response.raise_for_status()  # Check for errors in the response
        data = response.content
       

        # Process and extract shop data in JSON format from the XML response
        shops = parse_xml_data(data)
        return shops
    except requests.RequestException as e:
        print(f"Error in Overpass API request: {e}")
        return []

def parse_xml_data(xml_data):
    root = ET.fromstring(xml_data)
    shops = []

    for node in root.findall('.//node'):
        shop_info = {
            "type": "node",
            "id": node.attrib["id"],
            "lat": node.attrib["lat"],
            "lon": node.attrib["lon"],
            "tags": {tag.attrib["k"]: tag.attrib["v"] for tag in node.findall('./tag')}
        }
        shops.append(shop_info)

    return shops

# Example: Hanoi coordinates
min_latitude = 20.9980
min_longitude = 105.3271
max_latitude = 21.0508
max_longitude = 105.8544

# Example: Generate a 3x3 grid of bounding boxes
rows = 3
cols = 3
hanoi_bounding_boxes = generate_hanoi_bounding_boxes(min_latitude, min_longitude, max_latitude, max_longitude, rows, cols)

# Iterate over bounding boxes and retrieve data
all_shops_data = []
for bbox_coordinates in hanoi_bounding_boxes:
    shops_data = get_shops_in_bbox(bbox_coordinates)
    all_shops_data.extend(shops_data)

# Store the result in a JSON file with explicit encoding specification
output_file = "hanoi_shops_data.json"
with open(output_file, "w", encoding='utf-8') as json_file:
    json.dump(all_shops_data, json_file, ensure_ascii=False, indent=4)

print(f"Data stored in {output_file}")
