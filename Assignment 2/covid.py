# Given a Covid-19 data CSV file with 12 feature columns, perform the tasks given below. 
    # Use the sample file covidTrain.csv to test your code.
import re
import csv
from collections import defaultdict
from collections import Counter

# After performing all these tasks, write the whole data back to another CSV file named "covidResult.csv".
# This result file should have all of the rows from the input file - rows that were modified 
    # as well as rows that were not modified.
# If you do not write data back to another CSV file, or your output file name is not exactly as required, 
    # you will get 0 points. 
    
def main(f):     
    loDict = defaultdict(list)
    laDict = defaultdict(list)
    cityDict = defaultdict(list)
    symptomDict = defaultdict(list)
    with open(f) as csvfile:
            reader = csv.DictReader(csvfile, delimiter = ',')
            for row in reader:
                values = list(row.values())
                if row['longitude'] != 'NaN':
                    loDict[row['province']].append(float(row['longitude']))
                if row['latitude'] != 'NaN':
                    laDict[row['province']].append(float(row['latitude']))
                if row['city'] != 'NaN':
                    cityDict[row['province']].append(row['city'])
                if row['symptoms'] != 'NaN':
                    symList = row['symptoms'].split(';')
                    for item in symList:
                        symptomDict[row['province']].append(item.strip())
    with open(f) as csvfile:
        with open('covidResult.csv', 'w', newline = '') as newcsvfile:
            reader = csv.DictReader(csvfile, delimiter = ',')
            writer = csv.writer(newcsvfile)
            count = 0
            for row in reader:
                if count == 0:
                    writer.writerow(list(row.keys()))
                values = list(row.values())
                # Fill in the missing “city” values by the most occurring city value in that province. 
                # In case of a tie, use the city that appears first in alphabetical order.
                if row['city'] == 'NaN':
                    provCheck = Counter(cityDict[row['province']])
                    cityTest, commonCount = (provCheck.most_common(1))[0]
                    for key in provCheck:
                        if provCheck[key] == commonCount:
                            if key <= cityTest:
                                cityTest = key
                    values[3] = cityTest
                # Fill in the missing "symptom" values by the single most frequent symptom in the province where 
                # the case was recorded. In case of a tie, use the symptom that appears first in alphabetical order.
                if row['symptoms'] == 'NaN':
                    provCheck = Counter(symptomDict[row['province']])
                    symTest, commonCount = (provCheck.most_common(1))[0]
                    for key in provCheck:
                        if provCheck[key] == commonCount:
                            if key <= symTest:
                                symTest = key
                    values[11] = symTest
                # In the age column, wherever there is a range of values, replace it by the rounded off average value. 
                # E.g., for 10-14 substitute 12. (Rounding should be done like in 1.1). 
                # You might want to use regular expressions here, but it is not required.
                ageSum = 0
                res = re.findall(r"[0-9]{1,}", row['age'])
                for item in res:
                    ageSum += float(item)
                values[1] = round(ageSum/len(res))
                # Change the date format for the date columns - date_onset_symptoms, date_admission_hospital and 
                # date_confirmation from dd.mm.yyyy to mm.dd.yyyy. Again, you can use regexps here, but it is not required.
                for datecol in range(8,11):
                    dateSwap = values[datecol].split('.')
                    newDate = dateSwap[1] + '.' + dateSwap[0] + '.' + dateSwap[2]
                    values[datecol] = newDate
                # Fill in the missing (NaN) "latitude" and "longitude" values by the average of the latitude and 
                # longitude values for the province where the case was recorded. Round the average to 2 decimal places.
                if row['latitude'] == 'NaN':
                    laSum = 0
                    for item in laDict[row['province']]:
                        laSum += float(item)
                        values[6] = round(laSum/len(laDict[row['province']]), 2)
                if row['longitude'] == 'NaN':
                    loSum = 0
                    for item in loDict[row['province']]:
                        loSum += float(item)
                        values[7] = round(loSum/len(loDict[row['province']]), 2)
                
                writer.writerow(values)
                count += 1
    
main('covidTrain.csv')

# Note: While iterating through records, if you come across multiple symptoms for a single record, you need 
    # to consider them individually for frequency counts.
# Watch out!: Some symptoms could be separated by a '; ' , i.e., semicolon plus space and some by ';' , 
    # i.e., just a semicolon, even within the same record. For example:
        # "fever; sore throat;cough;weak; expectoration;muscular soreness"
# Also, the symptoms column has values such as "fever 37.7 C" and "fever (38-39 C)". For these values, 
    # you shouldn't do any special processing, so the symptoms should be extracted as "fever 37.7 C" 
    # and "fever (38-39 C)", as presented in the data.
