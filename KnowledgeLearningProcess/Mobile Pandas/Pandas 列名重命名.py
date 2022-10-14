# -*- coding: utf-8 -*-
"""
Author  : Ethan Chai
Date    : 2022/10/13 01:09
input   : 
output  :   
Short Description: 
Change History:
"""
import pandas as pd
import json
from datetime import datetime


def main(json_path):
    with open(json_path, 'r', encoding='utf-8') as readfile:
        inp_json_data = json.load(readfile)
    df = pd.DataFrame(inp_json_data)
    df = df[["instr_id", "instruction"]]
    df = df.rename(columns={"instr_id": "id", "instruction": "content"})
    df.to_csv(f"Result_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv",
              encoding='utf-8-sig',
              index=False)


if __name__ == '__main__':
    main("inp.json")
