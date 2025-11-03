import csv
import json
from collections import defaultdict
import pandas as pd

#??not yet the right transformations
transformations = {
    "ao_DALI1LED1DimVal": (1.1971, 3.5945),
    "ao_DALI1LED21DimVal": (1.02032, 3.924),
    "ao_DALI1LED41DimVal": (0.881, 1.9586),
    "ao_DALI2LED1DimVal": (0.9959, 3.3907),
    "ao_DALI2LED21DimVal": (1.0513, 4.4751),
    "ao_DALI2LED41DimVal": (1.0139, 5.1517),
    "ao_DALI3LED1DimVal": (1.1037, 1.7276),
    "ao_DALI3LED21DimVal": (0.9992, 3.2273),
    "ao_DALI3LED41DimVal": (0.9859, 4.3165)
}

def linear_transformation(area_id, int):
    a, b = transformations.get(area_id, (1,0))
    y = a * int - b
    yred = y * 0.88
    ygreen = 0
    yblue = y * 0.12
    yfarred = y * 0.20
    return yred, ygreen, yblue, yfarred

def int_to_setting_translation(lines):
    settings_list = []
    for _, line in lines.iterrows():
        id = line["id"]
        int_value = line["value"]
        start = line["start"]
        end = line["end"]
        index = line["index"]
        red, green, blue, farRed = linear_transformation(id, int_value)
        settings_list.append([id, red, green, blue, farRed, start, end, index])
    csv_path = "generated_light_settings.csv"
    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "red", "green", "blue", "farRed", "start", "end", "index"])
        writer.writerows(settings_list)
    return(settings_list)

def build_message_from_csv(csv_file):
    # Ordered list of IDs from your sample message
    ordered_ids = [
        "ao_DALI1LED1DimVal",
        "ao_DALI1LED62DimVal",
        "ao_DALI1LED21DimVal",
        "ao_DALI1LED63DimVal",
        "ao_DALI1LED41DimVal",
        "ao_DALI1LED64DimVal",
        "ao_DALI2LED1DimVal",
        "ao_DALI2LED62DimVal",
        "ao_DALI2LED21DimVal",
        "ao_DALI2LED63DimVal",
        "ao_DALI2LED41DimVal",
        "ao_DALI2LED64DimVal",
        "ao_DALI3LED1DimVal",
        "ao_DALI3LED62DimVal",
        "ao_DALI3LED21DimVal",
        "ao_DALI3LED63DimVal",
        "ao_DALI3LED41DimVal",
        "ao_DALI3LED64DimVal"
    ]

    # Store periods for each ID
    periods_map = defaultdict(list)

    # CSV format: id,red,green,blue,farRed,start,end,index
    for _, row in csv_file.iterrows():
        period = {
            "red":int(row["red"]),
            "green":int(row["green"]),
            "blue":int(row["blue"]),
            "farRed":int(row["farRed"]),
            "tl":0,
            "period":[row["start"], row["end"]],
            "index":int(row["index"])
        }
        periods_map[row["id"]].append(period)

    # Build the areas list in the exact order
    areas = []
    for area_id in ordered_ids:
        areas.append({
            "id": area_id,
            "periods": periods_map.get(area_id, [])
        })

    # Wrap into final message
    message = {
        "namespace":"light",
        "request":"updateSettings",
        "value":{
            "areas":areas,
            "percentages":{
                "blueInWhite":27.2,
                "farRedInRed":0.48,
                "farRedInWhite":2.25,
                "greenInWhite":48.55,
                "redInFarRed":11.1,
                "redInWhite":22
            }
        }
    }
    message

    return message

#Making the message
if __name__ == "__main__":
    lines = [
        ["ao_DALI1LED1DimVal", 100, "08:00", "20:00", 0],
        ["ao_DALI1LED21DimVal", 150, "08:00", "20:00", 0],
        ["ao_DALI2LED1DimVal", 200, "08:00", "20:00", 0]
    ]

    # Path to store CSV
    intensities_csv = "generated_light_values.csv"

    with open(intensities_csv, mode="w", newline="") as f:
        writer = csv.writer(f)
        # Optional: write header
        writer.writerow(["id", "value", "start", "end", "index"])
        # Write all lines
        writer.writerows(lines)

    light_settings_csv = "generated_light_settings.csv"


    # Write to CSV

    #csv_file = pd.read_csv("250917 Test light intensities.csv")
    csv_file = pd.read_csv("generated_light_values.csv")
    settings_list = int_to_setting_translation(csv_file)
    csv_file = pd.read_csv("generated_light_settings.csv")
    msg = build_message_from_csv(csv_file)
    with open('250923 current.json', 'w') as file:
        json.dump(msg, file)
    print(msg)

