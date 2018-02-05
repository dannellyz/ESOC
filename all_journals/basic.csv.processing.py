import pandas as pd
import glob
import numpy as np
import os


output = ["Journal Code", "Unified Command", "Region", "Province", "Type of Engagement", "Reference", "Report RN", "Date",
     "Summary Report", "Enemy Side", "Government Side", "Civilian Side", "Firearms Gained", "Firearms Losses",
     "Items Recovered / Loss", "Other Details", "Action Taken", "Extra"]


all_data = pd.DataFrame()
print os.listdir(os.getcwd())
for filename in os.listdir(os.getcwd()):
    #print filename
    if filename.endswith('.csv'):
        df = pd.read_csv(filename, header=0)
        all_data = all_data.append(df,ignore_index=False)
#Number of non-NaNs in each column
#all_data.to_csv("ESOC_All_Data_2010_2012.csv",header=False, index=False, encoding='utf-8')
for key in all_data.keys():
    print key
    print all_data[key].count()
