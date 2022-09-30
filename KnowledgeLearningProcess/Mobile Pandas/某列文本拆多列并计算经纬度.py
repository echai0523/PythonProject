# -*- coding: UTF-8 -*-

"""
Author: Ethan Chai
Date: 2022/9/3 12:01

input:

output:

Short Description:
    - 知识点：
        - pandas
            - pd.isnull(df[0][0])  # 判断是否为空值
        - pgeocode
            - nomi = pgeocode.Nominatim('au')
                - code = nomi.query_postal_code()
                    - code.latitude  # 纬度
                    - code.longitude # 经度
            - dist = pgeocode.GeoDistance('au')
                - dist.query_postal_code()
Change History:

"""
import pandas as pd
import pgeocode

nomi = pgeocode.Nominatim('au')
dist = pgeocode.GeoDistance('au')


def main(csv_path):
    df = pd.read_csv(csv_path)
    df["startCity"] = [None] * len(df)
    df["startState"] = [None] * len(df)
    df["startZipcode"] = [None] * len(df)
    df["endCity"] = [None] * len(df)
    df["endState"] = [None] * len(df)
    df["endZipcode"] = [None] * len(df)
    df['tripDistance'] = [None] * len(df)
    for index, row in df[:100].iterrows():
        # print(index, row["startAddress"])
        if row["startAddress"] != row["startAddress"] or len(row["startAddress"].split(",")) < 3:
            continue

        *start, start_info, _ = row["startAddress"].split(",")
        if isinstance(start_info, float):
            df["startZipcode"][index] = str(int(start_info))
        elif start_info.isupper():
            df["startState"][index] = start_info
        else:
            start_split = start_info.strip().split()
            for for_start in start_split:
                if str(for_start).isdigit():
                    df["startZipcode"][index] = str(int(for_start))
                elif for_start.isupper():
                    df["startState"][index] = for_start
                else:
                    continue
            if df["startState"][index] and df["startZipcode"][index]:
                df["startCity"][index] = ' '.join(start_split[:-2])
            elif df["startState"][index] or df["startZipcode"][index]:
                df["startCity"][index] = ' '.join(start_split[:-1])
            else:
                df["startCity"][index] = ' '.join(start_split)

        if row["endAddress"] != row["endAddress"] or len(row["endAddress"].split(",")) < 3:
            continue

        *end, end_info, _ = row["endAddress"].split(",")
        if isinstance(end_info, float):
            df["endZipcode"][index] = str(int(end_info))
        elif end_info.isupper():
            df["endState"][index] = end_info
        else:
            end_split = end_info.strip().split()
            for for_end in end_split:
                if str(for_end).isdigit():
                    df["endZipcode"][index] = str(int(for_end))
                if for_end.isupper():
                    df["endState"][index] = for_end
                else:
                    continue
            if df["endState"][index] and df["endZipcode"][index]:
                df["endCity"][index] = ' '.join(end_split[:-2])
            elif df["endState"][index] or df["endZipcode"][index]:
                df["endCity"][index] = ' '.join(end_split[:-1])
            else:
                df["endCity"][index] = ' '.join(end_split)

        if pd.isnull(df['DispatchStatus'][index]):
            if not pd.isnull(df['startZipcode'][index]):
                code = nomi.query_postal_code(df['startZipcode'][index])
                # 纬度
                df['PickupLatitude'][index] = code.latitude
                # 经度
                df['PickupLongitude'][index] = code.longitude
            if not pd.isnull(df['endZipcode'][index]):
                code = nomi.query_postal_code(df['endZipcode'][index])
                df['DestinationLatitude'][index] = code.latitude
                df['DestinationLongitude'][index] = code.longitude
            if not pd.isnull(df['startZipcode'][index]) and not pd.isnull(df['endZipcode'][index]):
                df['tripDistance'][index] = dist.query_postal_code(str(int(df['startZipcode'][index])), str(int(df['endZipcode'][index])))

    df.to_csv(f"Result_out.csv", encoding='utf-8', index=False)


if __name__ == '__main__':
    main("../../EthanFileData/csv/City_State_Zipcode_100.csv")
    # main("../../EthanFileData/csv/City_State_Zipcode.csv")







