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

def process_documents_stable(output_dir = "251105_int_pttrns_rnd2"):
    os.makedirs(output_dir, exist_ok = True)

    nrows = 4

    file_name_list = ["251106", "251107", "251108", "251109"]
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


process_documents_stable()


def process_documents(doc1, doc2, doc3, output_dir="251105_int_pttrns_rnd2"):
    os.makedirs(output_dir, exist_ok=True)

    df1 = pd.read_csv(doc3)
    nrows = len(df1)

    file_name_list = ["251110", "251111", "251112", "251113", "251114", "251115", "251116",
                      "251117", "251118", "251119", "251120", "251121", "251122", "251123",
                      "251124", "251125", "251126", "251127", "251128", "251129", "251130",
                      "251201", "251202", "251203", "251204", "251205", "251206", "251207",
                      "251208", "251209"]

    for i in range(nrows):
        #treatment 1 control
        #rnd 2 treatment 3 jun 0-430
        C1_1 = intensity_allocation("ao_DALI1LED1DimVal", doc2, i)
        C3_3 = intensity_allocation("ao_DALI3LED41DimVal", doc2, i)

        #treatment 2 jun 50-430
        #rnd2 treatment 4 sep 50-430
        C1_2 = intensity_allocation("ao_DALI1LED21DimVal", doc3, i)
        C3_2 = intensity_allocation("ao_DALI3LED21DimVal", doc3, i)

        # treatment 3 jun 0-430
        #rnd treatment 1 control
        C2_2 = pd.DataFrame([["ao_DALI2LED21DimVal", 180, "00:00", "23:59", 0]],
                            columns=["id", "intensity", "start", "end", "index"])
        C3_1 = pd.DataFrame([["ao_DALI3LED1DimVal", 180, "00:00", "23:59", 0]],
                            columns=["id", "intensity", "start", "end", "index"])

        #treatment 4 sep 50-430
        #rnd2 treatment 2 jun 50-430
        C2_1 = intensity_allocation("ao_DALI2LED1DimVal", doc1, i)
        C2_3 = intensity_allocation("ao_DALI2LED41DimVal", doc1, i)

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

Jun25_50_430 = "251105 Intensity patterns\\251002_June_25_light_50_430.csv"
Jun25_0_430 = "251105 Intensity patterns\\251002_June_25_light_0_430.csv"
Sep25_50_430 = "251105 Intensity patterns\\251002_Sep_25_light_50_430.csv"

process_documents(Jun25_50_430, Jun25_0_430, Sep25_50_430)




