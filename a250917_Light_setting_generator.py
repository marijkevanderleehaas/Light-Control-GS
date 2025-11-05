import csv
import json
from collections import defaultdict
import pandas as pd

#??not yet the right transformations
transformations = {
    "ao_DALI1LED1DimVal": (0.8353, 3.0087),
    "ao_DALI1LED21DimVal": (0.9773, 3.8556),
    "ao_DALI1LED41DimVal": (1.0871, 6.3631), #1.1345, 2.3096
    "ao_DALI2LED1DimVal": (1.0032, 3.5805),
    "ao_DALI2LED21DimVal": (0.9511, 4.2792),
    "ao_DALI2LED41DimVal": (0.9862, 5.0972),
    "ao_DALI3LED1DimVal": (0.9054, 1.7143),
    "ao_DALI3LED21DimVal": (1.0007, 3.2423),
    "ao_DALI3LED41DimVal": (1.0142, 4.4012)
}

def linear_transformation(area_id, int):
    a, b = transformations.get(area_id, (1,0))
    y = a * int + b
    yred = y * 0.88
    ygreen = 0
    yblue = y * 0.12
    yfarred = y * 0.20
    return yred, ygreen, yblue, yfarred

def int_to_setting_translation(lines):
    settings_list = []
    for _, line in lines.iterrows():
        id = line["id"]
        int_value = int(line["intensity"])
        start = line["start"]
        end = line["end"]
        index = int(line["index"])
        if "LED6" in id:
            red, green, blue, farRed = 0, 0, 0, 0
        else:
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
        ["ao_DALI1LED1DimVal", 180, "00:00", "23:59", 0],
        ["ao_DALI1LED21DimVal", 180, "00:00", "23:59", 0],
        ["ao_DALI1LED41DimVal", 180, "00:00", "23:59", 0],
        ["ao_DALI1LED64DimVal", 0, "00:00", "23:59", 0],
        ["ao_DALI2LED1DimVal", 180, "00:00", "23:59", 0],
        ["ao_DALI2LED21DimVal", 180, "00:00", "23:59", 0],
        ["ao_DALI2LED63DimVal", 0, "00:00", "23:59", 0],
        ["ao_DALI2LED41DimVal", 180, "00:00", "23:59", 0],
        ["ao_DALI2LED64DimVal", 0, "00:00", "23:59", 0],
        ["ao_DALI3LED1DimVal", 180, "00:00", "23:59", 0],
        ["ao_DALI3LED21DimVal", 180, "00:00", "23:59", 0],
        ["ao_DALI3LED63DimVal", 0, "00:00", "23:59", 0],
        ["ao_DALI3LED41DimVal", 180, "00:00", "23:59", 0],
        ["ao_DALI3LED64DimVal", 0, "00:00", "23:59", 0]
    ]

    # Path to store CSV
    intensities_csv = "generated_light_values.csv"

    with open(intensities_csv, mode="w", newline="") as f:
        writer = csv.writer(f)
        # Optional: write header
        writer.writerow(["id", "intensity", "start", "end", "index"])
        # Write all lines
        writer.writerows(lines)

    light_settings_csv = "generated_light_settings.csv"


    # Write to CSV

    #csv_file = pd.read_csv("250917 Test light intensities.csv")

    #csv_file = pd.read_csv("251002_int_pttrns_jun_rnd1/light_intensities_251002.csv")
    #settings_list = int_to_setting_translation(csv_file)
    #csv_file = pd.read_csv("generated_light_settings.csv")
    #msg = build_message_from_csv(csv_file)
    #with open('light_251002_180_24.json', 'w') as file:
    #    json.dump(msg, file)
    #print(msg)

import os
import glob
import pandas as pd
import json

# Input and output folders
input_folder = "251105_int_pttrns_rnd2"
output_folder = "251105_lght_sttngs_rnd2"

# Make sure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop over all CSV files in input folder
for file_path in glob.glob(os.path.join(input_folder, "*.csv")):
    print(f"Processing {file_path}...")

    # Load CSV
    df = pd.read_csv(file_path)

    # Run your translation function
    settings_list = int_to_setting_translation(df)

    # Read generated settings CSV (your pipeline requirement)
    generated_csv = pd.read_csv("generated_light_settings.csv")

    # Build message
    msg = build_message_from_csv(generated_csv)

    # Extract yymmdd from filename
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    yymmdd = base_name.split("_")[-1]   # takes the last part after underscore
    output_file = os.path.join(output_folder, f"light_{yymmdd}.json")

    # Save JSON
    with open(output_file, "w") as f:
        json.dump(msg, f, indent=2)

    print(f"Saved {output_file}")
