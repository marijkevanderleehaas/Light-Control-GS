import pandas as pd
import os
Start_times = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00",
               "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
               "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
End_times = ["00:59", "01:59", "02:59", "03:59", "04:59", "05:59", "06:59", "07:59",
             "08:59", "09:59", "10:59", "11:59", "12:59", "13:59", "14:59", "15:59",
             "16:59", "17:59", "18:59", "19:59", "20:59", "21:59", "22:59", "23:59"]
def intensity_allocation(ID, doc, index):
    df = pd.read_csv(doc)
    row = df.iloc[index]

    intensities = row.iloc[3:-2]

    lines = []
    for i, intensity in enumerate(intensities):
        start_time = Start_times[i]
        end_time = End_times[i]
        line = [ID, intensity, start_time, end_time, i]
        lines.append(line)

    return pd.DataFrame(lines, columns=["id", "intensity", "start", "end", "index"])

def intensity_allocation_treat4(ID):
    intensities = [] #the list of intensities

    lines = []
    for i, intensity in enumerate(intensities):
        start_time = Start_times[i]
        end_time = End_times[i]
        line = [ID, intensity, start_time, end_time, i]
        lines.append(line)

    return pd.DataFrame(lines, columns=["id", "intensity", "start", "end", "index"])

def process_documents_stable(doc1, doc2, output_dir = "251024_int_pttrns_jun_rnd1"):
    os.makedirs(output_dir, exist_ok = True)

    df1 = pd.read_csv(doc1)
    nrows = 4

    file_name_list = ["251002", "251003", "251004", "251005"]
    print(file_name_list)

    for i in range(nrows):
        C1_1 = pd.DataFrame([["ao_DALI1LED1DimVal", 180, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        C1_2 = pd.DataFrame([["ao_DALI1LED21DimVal", 180, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        C1_3 = pd.DataFrame([["ao_DALI1LED41DimVal", 180, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        C2_1 = pd.DataFrame([["ao_DALI2LED1DimVal", 180, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        C2_2 = pd.DataFrame([["ao_DALI2LED21DimVal", 180, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        C2_3 = pd.DataFrame([["ao_DALI2LED41DimVal", 180, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        C3_1 = pd.DataFrame([["ao_DALI3LED1DimVal", 180, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        C3_2 = pd.DataFrame([["ao_DALI3LED21DimVal", 180, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        C3_3 = pd.DataFrame([["ao_DALI3LED41DimVal", 180, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        WCD1_1 = pd.DataFrame([["ao_DALI1LED62DimVal", 0, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        WCD1_2 = pd.DataFrame([["ao_DALI1LED63DimVal", 0, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        WCD1_3 = pd.DataFrame([["ao_DALI1LED64DimVal", 0, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        WCD2_1 = pd.DataFrame([["ao_DALI2LED62DimVal", 0, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        WCD2_2 = pd.DataFrame([["ao_DALI2LED63DimVal", 0, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        WCD2_3 = pd.DataFrame([["ao_DALI2LED64DimVal", 0, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        WCD3_1 = pd.DataFrame([["ao_DALI3LED62DimVal", 0, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        WCD3_2 = pd.DataFrame([["ao_DALI3LED63DimVal", 0, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])
        WCD3_3 = pd.DataFrame([["ao_DALI3LED64DimVal", 0, "00:00", "23:59", 0]],
                         columns=["id", "intensity", "start", "end", "index"])


        combined = pd.concat([C1_1, WCD1_1, C1_2, WCD1_2, C1_3, WCD1_3,
                              C2_1, WCD2_1, C2_2, WCD2_2, C2_3, WCD2_3,
                              C3_1, WCD3_1, C3_2, WCD3_2, C3_3, WCD3_3], ignore_index=True)

        file_name = file_name_list[i]
        filename = f"light_intensities_{file_name}.csv"

        combined.to_csv(os.path.join(output_dir, filename), index = False)


process_documents_stable("250931_June_25_light_50_430.csv", "250931_June_25_light_0_430.csv")


def process_documents(doc1, doc2, doc3, output_dir="251024_int_pttrns_jun_rnd1"):
    os.makedirs(output_dir, exist_ok=True)

    df1 = pd.read_csv(doc3)
    nrows = len(df1)

    file_name_list = ["251006", "251007", "251008", "251009", "251010", "251011", "251012",
                      "251013", "251014", "251015", "251016", "251017", "251018", "251019",
                      "251020", "251021", "251022", "251023", "251024", "251025", "251026",
                      "251027", "251028", "251029", "251030", "251031", "251101", "251102",
                      "251103", "251104"]

    for i in range(nrows):
        #treatment 1 control
        C1_1 = pd.DataFrame([["ao_DALI1LED1DimVal", 180, "00:00", "23:59", 0]],
                            columns=["id", "intensity", "start", "end", "index"])
        C3_3 = pd.DataFrame([["ao_DALI3LED41DimVal", 180, "00:00", "23:59", 0]],
                            columns=["id", "intensity", "start", "end", "index"])

        #treatment 2 jun 50-430
        C1_2 = intensity_allocation("ao_DALI1LED21DimVal", doc1, i)
        C3_2 = intensity_allocation("ao_DALI3LED21DimVal", doc1, i)

        # treatment 3 jun 0-430
        C2_2 = intensity_allocation("ao_DALI2LED21DimVal", doc2, i)
        C3_1 = intensity_allocation("ao_DALI3LED1DimVal", doc2, i)

        #treatment 4 sep 50-430
        C2_1 = intensity_allocation("ao_DALI2LED1DimVal", doc3, i)
        C2_3 = intensity_allocation("ao_DALI2LED41DimVal", doc3, i)

        # used for WP2
        C1_3 = pd.DataFrame([["ao_DALI1LED41DimVal", 180, "00:00", "23:59", 0]],
                            columns=["id", "intensity", "start", "end", "index"])

        #power outlets
        WCD1_1 = pd.DataFrame([["ao_DALI1LED62DimVal", 0, "00:00", "23:59", 0]],
                              columns=["id", "intensity", "start", "end", "index"])
        WCD1_2 = pd.DataFrame([["ao_DALI1LED63DimVal", 0, "00:00", "23:59", 0]],
                              columns=["id", "intensity", "start", "end", "index"])
        WCD1_3 = pd.DataFrame([["ao_DALI1LED64DimVal", 0, "00:00", "23:59", 0]],
                              columns=["id", "intensity", "start", "end", "index"])
        WCD2_1 = pd.DataFrame([["ao_DALI2LED62DimVal", 0, "00:00", "23:59", 0]],
                              columns=["id", "intensity", "start", "end", "index"])
        WCD2_2 = pd.DataFrame([["ao_DALI2LED63DimVal", 0, "00:00", "23:59", 0]],
                              columns=["id", "intensity", "start", "end", "index"])
        WCD2_3 = pd.DataFrame([["ao_DALI2LED64DimVal", 0, "00:00", "23:59", 0]],
                              columns=["id", "intensity", "start", "end", "index"])
        WCD3_1 = pd.DataFrame([["ao_DALI3LED62DimVal", 0, "00:00", "23:59", 0]],
                              columns=["id", "intensity", "start", "end", "index"])
        WCD3_2 = pd.DataFrame([["ao_DALI3LED63DimVal", 0, "00:00", "23:59", 0]],
                              columns=["id", "intensity", "start", "end", "index"])
        WCD3_3 = pd.DataFrame([["ao_DALI3LED64DimVal", 0, "00:00", "23:59", 0]],
                              columns=["id", "intensity", "start", "end", "index"])

        combined = pd.concat([C1_1, WCD1_1, C1_2, WCD1_2, C1_3, WCD1_3,
                              C2_1, WCD2_1, C2_2, WCD2_2, C2_3, WCD2_3,
                              C3_1, WCD3_1, C3_2, WCD3_2, C3_3, WCD3_3], ignore_index=True)

        file_name = file_name_list[i]
        filename = f"light_intensities_{file_name}.csv"

        combined.to_csv(os.path.join(output_dir, filename), index=False)


process_documents("251002_June_25_light_50_430.csv", "251002_June_25_light_0_430.csv", "251002_Sep_25_light_50_430.csv")




