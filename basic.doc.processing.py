import subprocess
import os
import docx2txt
import re
import operator
import pandas as pd

#Used to convert doc to docx for easier processing
def docToDocx ():
    for filename in os.listdir("all_journals/"):
        print filename
        if filename.endswith('.doc'):
            subprocess.call(['soffice', '--headless', '--convert-to', 'docx', filename])

def allDocxToxCsv():
    for filename in os.listdir("all_journals/"):
        print filename
        if filename.endswith('.docx'):
            journalEntries(filename)

def jornalToText(blocks):
    toCsv = [None] * 16
    if ")" in blocks: blocks.remove(")")
    #Get Unified Command and Region
    commReg = blocks[0].split("(",1)
    #Command
    toCsv[1] = commReg[0]
    #Region
    toCsv[2] = commReg[1].strip(")")
    # Get Province and Type of Engagement
    provEng = blocks[1].split("(", 1)
    # Province
    toCsv[3] = provEng[0]
    # Type of Engagement
    toCsv[4] = provEng[1].strip(")")
    #Get Reference Details
    refDetails = re.split('Ref: |Report RN: |dtd|', blocks[2])
    toCsv[5:7] = refDetails[1:]
    #Return if no main report
    if len(blocks) < 4:
        return toCsv
    #Return if only a main report
    toCsv[8] = blocks[3]
    if len(blocks) < 5:
        return toCsv
    #Check for main report line break
    detailBlock = {"Enemy Side:":0, "Government Side:":0, "Civilian Side:":0, "Firearms Gains:":0, "Firearms Losses:":0,
                   "Items Recovered / Loss: ":0, "Other Details:":0, "Action Taken:":0}

    #Main Report Continues
    if any(otherDetails not in blocks[4] for otherDetails in detailBlock):
        toCsv[8] = toCsv[8] + blocks[4]

    #Straigt to Extra Details
    for type in detailBlock:
        try:
            detailBlock[type] = blocks.index(type)
        except ValueError:
            detailBlock[type] = -1

    sort = sorted(detailBlock.items(), key=operator.itemgetter(1))

    #Additional Details
    for i in range(len(sort)):
        if sort[i][1] != -1:
            if len(sort) - sort.index(sort[i]) != 1:
                detailText = " ".join(blocks[sort[i][1]+1:sort[i+1][1]])
            else:
                detailText = " ".join(blocks[sort[i][1]+1:])
            detailIndex = {"Enemy Side:": 0, "Government Side:": 1, "Civilian Side:": 2, "Firearms Gains:": 3,
                           "Firearms Losses:": 4,
                           "Items Recovered / Loss: ": 5, "Other Details:": 6, "Action Taken:": 7}
            outIndex = detailIndex[blocks[sort[i][1]]]
            toCsv[outIndex + 9] = detailText
    return toCsv

#Converts the docx to an excel with information
def journalEntries(filename):
    #Import the docx
    journal_all = docx2txt.process(filename)
    hold = re.compile("\n\D{0,3}\d{5}\n")
    journal_nums = hold.findall(journal_all)
    #remove reference blocks
    journal_texts = hold.split(journal_all)[1:]
    #Create Empty Array and add headers
    output = [["Journal Code", "Unified Command", "Region", "Province", "Type of Engagement", "Reference", "Report RN", "Date", "Summary Report", "Enemy Side", "Government Side", "Civilian Side", "Firearms Gained", "Firearms Losses", "Items Recovered / Loss", "Other Details", "Action Taken"]]
    #output = pd.DataFrame(index=journal_nums,columns=columns)
    #Remove blanks and outliers
    for num, text in zip(journal_nums,journal_texts):
        out = jornalToText(filter(None, text.split(os.linesep)))
        out[0] = num.strip("\n")
        output.append(out)
    df = pd.DataFrame(output)
    print filename
    df.to_csv(filename.replace(".docx",".csv"),header=False, index=False, encoding='utf-8')
    print df










#docxtoCsv("Journal-Jan 12.docx")
allDocxToxCsv()