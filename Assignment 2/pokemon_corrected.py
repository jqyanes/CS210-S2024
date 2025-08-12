import csv
from collections import defaultdict
from collections import Counter

#Fixed functions: fill_blanks, type_to_pers

# Find out what percentage of "fire" type pokemons are at or above the "level" 40.
#(specifics in original file)
# Print the value to a file named "pokemon1.txt"
def fire_percent(f):
    fireCount = 0
    over40 = 0
    with open(f) as csvfile:
            reader = csv.DictReader(csvfile, delimiter = ',')
            for row in reader:
                values = list(row.values())
                if row['type'] == 'fire':
                    fireCount += 1
                    if float(row['level']) >= 40:
                        over40 += 1  
    roundedP = round((over40/fireCount) * 100)
    with open('pokemon1.txt', 'w', newline = '') as newcsvfile:
        newcsvfile.write(f'Percentage of fire type Pokemons at or above level 40 = {roundedP}')

# [10 pts] Fill in the missing "type" column values (given by NaN) by mapping them 
    # from the corresponding "weakness" values. You will see that typically a given pokemon weakness 
    # has a fixed "type", but there are some exceptions. So, fill in the "type" column with 
    # the most common "type" corresponding to the pokemon’s "weakness" value.
# In case of a tie, use the type that appears first in alphabetical order.

# [13 pts] Fill in the missing (NaN) values in the Attack ("atk"), Defense ("def") 
    # and Hit Points ("hp") columns as follows:
# Set the pokemon level threshold to 40.
# For a Pokemon having level above the threshold (i.e. > 40), fill in the missing value for atk/def/hp 
    # with the average values of atk/def/hp of Pokemons with level > 40. Round the average to one decimal place.
# For a Pokemon having level equal to or below the threshold (i.e. <= 40), fill in the missing value for atk/def/hp 
    # with the average values of atk/def/hp of Pokemons with level <= 40. Round the average to one decimal place. 
# After performing #2 and #3, write the modified data to another csv file named "pokemonResult.csv".

#Original error: included the Pokemon with NaN values in the counts for Pokemon >/<= 40,
    #lowering the respective hp/atk/def averages.
    #Each stat for Pokemon >/<= 40 now has its own count.
def fill_blanks(f):
    weaknessDict = defaultdict(list)
    hpOver40 = 0
    hpUnder40 = 0
    atkOver40 = 0
    atkUnder40 = 0
    defOver40 = 0
    defUnder40 = 0
    hpOver40Count = 0
    hpUnder40Count = 0
    atkOver40Count = 0
    atkUnder40Count = 0
    defOver40Count = 0
    defUnder40Count = 0
    with open(f) as csvfile:
            reader = csv.DictReader(csvfile, delimiter = ',')
            for row in reader:
                values = list(row.values())
                if row['type'] != 'NaN':
                    weaknessDict[row['weakness']].append(row['type'])
                if float(row['level']) > 40:
                    if row['hp'] != 'NaN':
                        hpOver40 += float(row['hp'])
                        hpOver40Count += 1
                    if row['atk'] != 'NaN':
                        atkOver40 += float(row['atk'])
                        atkOver40Count += 1
                    if row['def'] != 'NaN':
                        defOver40 += float(row['def'])
                        defOver40Count += 1
                else:
                    if row['hp'] != 'NaN':
                        hpUnder40 += float(row['hp'])
                        hpUnder40Count += 1
                    if row['atk'] != 'NaN':
                        atkUnder40 += float(row['atk'])
                        atkUnder40Count += 1
                    if row['def'] != 'NaN':
                        defUnder40 += float(row['def'])
                        defUnder40Count += 1
    with open(f) as csvfile:
        with open('pokemonResult.csv', 'w', newline = '') as newcsvfile:
            reader = csv.DictReader(csvfile, delimiter = ',')
            writer = csv.writer(newcsvfile)
            count = 0
            for row in reader:
                if count == 0:
                    writer.writerow(list(row.keys()))
                values = list(row.values())
                if row['type'] == 'NaN':
                    weakCheck = Counter(weaknessDict[row['weakness']])
                    typeTest, commonCount = (weakCheck.most_common(1))[0]
                    for key in weakCheck:
                        if weakCheck[key] == commonCount:
                            if key <= typeTest:
                                typeTest = key
                    values[4] = typeTest
                if row['hp'] == 'NaN':
                    if float(row['level']) > 40:
                        values[8] = str(round(hpOver40/hpOver40Count, 1))
                    else:
                        values[8] = str(round(hpUnder40/hpUnder40Count, 1))
                if row['atk'] == 'NaN':
                    if float(row['level']) > 40:
                        values[6] = str(round(atkOver40/atkOver40Count, 1))
                    else:
                        values[6] = str(round(atkUnder40/atkUnder40Count, 1))
                if row['def'] == 'NaN':
                    if float(row['level']) > 40:
                        values[7] = str(round(defOver40/defOver40Count, 1))
                    else:
                        values[7] = str(round(defUnder40/defUnder40Count, 1))
                writer.writerow(values)
                count += 1
                
# The following tasks (#4 and #5) should be performed on the pokemonResult.csv file that resulted above.

# [10 pts] Create a dictionary that maps pokemon types to their personalities. This dictionary would map 
    # a string to a list of strings. For example:
        # {"fire": ["docile", "modest", ...], "normal": ["mild", "relaxed", ...],  ...}
# Your dictionary should have the keys ordered alphabetically, and also items ordered alphabetically 
    # in the values list, as shown in the example above.
# Print the dictionary in the following format:
    # Pokemon type to personality mapping:
    # normal: mild, relaxed, ...
    # fire: docile, modest, ...
    # ...
# Print the dictionary to a file named "pokemon4.txt"

#Original errors: 
# keys and values were not ordered alphabetically
# values (personalities) included duplicates
def type_to_pers():
    tpDict = defaultdict(list)
    with open('pokemonResult.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter = ',')
            for row in reader:
                values = list(row.values())
                if row['personality'] not in tpDict[row['type']]:
                    tpDict[row['type']].append(row['personality'])
    with open('pokemon4.txt', 'w', newline = '') as newcsvfile:
            newcsvfile.write('Pokemon type to personality mapping:')
            count = 0
            for key in sorted(tpDict.keys()):
                newcsvfile.write('\n')
                newcsvfile.write(f'{key}: ')
                test = tpDict[key]
                test.sort()
                newcsvfile.write(', '.join(str(i) for i in test))
                count += 1
                
            
# [5 pts] Find out the average Hit Points ("hp") for pokemons of stage 3.0.
# Your program should print the value as follows (replace ... with value):
# Average hit point for Pokemons of stage 3.0 = ...
# You should round off the value, like in #1 above.
# Print the value to a file named "pokemon5.txt"
# If you do not print to a file, or your output file name is not exactly as required, you will get 0 points. 
def hpStage3():
    stage3Count = 0
    hpSum = 0
    with open('pokemonResult.csv') as csvfile:
            reader = csv.DictReader(csvfile, delimiter = ',')
            for row in reader:
                values = list(row.values())
                if row['stage'] == '3.0':
                    hpSum += float(row['hp'])
                    stage3Count += 1
    roundedHP = round(hpSum/stage3Count)
    with open('pokemon5.txt', 'w', newline = '') as newcsvfile:
        newcsvfile.write(f'Average hit point for Pokemons of stage 3.0 = {roundedHP}')
    
def main():
    fire_percent('pokemonTrain.csv')
    fill_blanks('pokemonTrain.csv')
    type_to_pers()
    hpStage3()
    
main()