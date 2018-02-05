import pandas as pd
import glob
import numpy as np
import os
from collections import defaultdict
from collections import Counter
import matplotlib.pyplot as plt

def engagementsCount(df):
    # Data to plot
    toChart = all_data["Type of Engagement"].value_counts()
    labels = toChart.keys()
    sizes = toChart.values

    # Plot
    plt.pie(sizes, labels=labels,
            autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.show()


def commRegionProvince(df):
    commands = df["Unified Command"].unique()
    #print commands
    comms_regions =  dict.fromkeys(commands,[])
    for (idx, row) in df.iterrows():
        comm = row.loc['Unified Command']
        region = row.loc['Region']
        if region not in comms_regions[comm]:
            comms_regions[comm].append(region)
    regions_comms = defaultdict(list)
    for k, v in comms_regions.iteritems():
        for region in v:
            regions_comms[region].append(k)
    print regions_comms

def type_counts(group,toCount):
    return group[toCount].value_counts()


def commands_in_regions(df):
    #print commands
    grouping = df.groupby("Unified Command")
    results = grouping.apply(type_counts, "Region").unstack(0)
    print results


def regionProvince(df):
    region = df["Region"].unique()
    #print commands
    regions_province =  dict.fromkeys(region,[])
    for (idx, row) in df.iterrows():
        reg = row.loc['Region']
        prov = row.loc['Province']
        if prov not in regions_province[reg]:
            regions_province[reg].append(prov)
    print regions_province[""]


output = ["Journal Code", "Unified Command", "Region", "Province", "Type of Engagement", "Reference", "Report RN", "Date",
     "Summary Report", "Enemy Side", "Government Side", "Civilian Side", "Firearms Gained", "Firearms Losses",
     "Items Recovered / Loss", "Other Details", "Action Taken", "Extra"]


all_data = pd.DataFrame()
os.chdir("/home/zayne/PycharmProjects/ESOC_Research/all_journals")

for filename in os.listdir(os.getcwd()):
    #print filename
    if filename.endswith('.csv'):
        df = pd.read_csv(filename, header=0)
        all_data = all_data.append(df,ignore_index=False)
#Number of non-NaNs in each column
all_data.to_csv("ESOC_All_Data_2010_2012.csv",header=True, index=False, encoding='utf-8')
'''for key in all_data.keys():
    print key
    print all_data[key].count()
    '''
print len(all_data["Journal Code"].value_counts())
#engagementsCount(all_data)
#commands_in_regions(all_data)
commands_in_regions(all_data)

def getRegions():
    # Get list of all regions each command is in and counts of involvement
    regProvinces = dict.fromkeys(region_results, [])

    for reg in regions:
        hold = region_results[reg].dropna(axis=0)
        regProvinces[reg] = hold.keys()
    print regProvinces["ARMM"]