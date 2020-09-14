from set_math import *
from Lang import *
import ast, csv, math, random, statistics, sys

random.seed("Phonology is absolutely fantastic!")

if len(sys.argv) < 2:
    db = 'LangDatabase.csv'
    # db = 'Random.csv'
    # db = "Extreme.csv"
else:
    db = sys.argv[1]
csvfile = open(db, 'r', encoding='latin-1')
langreader = csv.reader(csvfile, delimiter = ',')

lang_dict = LangDict()

for row in langreader:
    if row[0] == "Language" or row[0] == "": #Easy way to remove those two lines.
        continue
    newlang = Language(row[0],row[1],row[2],row[7],row[8],row[9])
    lang_dict[row[0]] = newlang
csvfile.close()

# Average number of languages you would expect to use each correlate in a family of a given size
# Calculated in Generate_stddev.py
# This is a result of not being confident in doing my math and only needing to run it once
stddev_d =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.49, 3.01, 2.11, 1.94, 1.96, 2.0, 2.04, 2.08]
stddev_p =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.76, 3.53, 2.26, 1.89, 1.86, 1.89, 1.93, 1.97]
stddev_i =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.62, 3.23, 2.16, 1.94, 1.93, 1.97, 2.01, 2.05]
avd =  [0.0, 0.59, 1.19, 1.78, 2.37, 2.96, 3.56, 4.15, 4.74, 5.34, 5.93, 6.52, 7.11, 7.71, 8.3, 8.89, 9.49, 10.08, 10.67, 11.26, 11.86, 12.45]
avp =  [0.0, 0.68, 1.37, 2.05, 2.74, 3.42, 4.1, 4.79, 5.47, 6.15, 6.84, 7.52, 8.21, 8.89, 9.57, 10.26, 10.94, 11.62, 12.31, 12.99, 13.68, 14.36]
avi =  [0.0, 0.62, 1.25, 1.87, 2.49, 3.12, 3.74, 4.36, 4.99, 5.61, 6.23, 6.86, 7.48, 8.1, 8.72, 9.35, 9.97, 10.59, 11.22, 11.84, 12.46, 13.09]

def z_score(size, num, type):
    # calculates how many standard deviations away from average you are in a distribution
    # types are duration, pitch, or intensity
    if type == 0:
        avg = avd[size]
        std = stddev_d[size]
    elif type == 1:
        avg = avp[size]
        std = stddev_p[size]
    elif type == 2:
        avg = avi[size]
        std = stddev_i[size]

    z = abs(((num - avg) / std))
    return z



print(len(lang_dict.keys()))
'''
sub = lang_dict.fam("Indo-European")
for i in sub:
    print(i)
'''
if len(sys.argv) < 3:
    cutoff = int(input("How small a language family should we count? Good numbers are 5 and 10 "))
else:
    cutoff = int(sys.argv[2])
all = lang_dict.all()
all_values = [0,0,0]
all_no_datas = [0,0,0]
for lang in all:
    for j in range(3):
        cue = (lang.d, lang.p, lang.i)[j]
        if cue != None:
            all_values[j] += cue

#
probs = []
for family in lang_dict.fam_list():
    sub = lang_dict.fam(family)
    sub_values = [0,0,0]
    no_datas = [0,0,0]        #The number of langs in the family without a particular piece of data.

    if len(sub) >= cutoff: #Arbitrary cutoff.
        print(family, len(sub))
        for lang in sub:
            #I'm sorry this got so much uglier.
            if lang.d != None:
                sub_values[0] += lang.d
            else:
                no_datas[0] += 1
            if lang.p != None:
                sub_values[1] += lang.p
            else:
                no_datas[1] += 1
            if lang.i != None:
                sub_values[2] += lang.i
            else:
                no_datas[2] += 1

        for i in range(0,3):
            #print((all_values[i] / len(all)))
            #print(sub_values[i], "out of", len(sub))
            if ((all_values[i] / (len(all) - all_no_datas[i])) < (sub_values[i] / (len(sub) - no_datas[i]) )):
                o_u = "o"
            else:
                o_u = "u"

            #probs.append(s_chance(len(all), all_values[i], len(sub),sub_values[i], o_u)) #old draft version
            probs.append(z_score((len(sub) - no_datas[i]), sub_values[i], i))

print("Number of families large enough is: ", len(probs))
to_compare = statistics.mean(probs)
print("Average z-score (absolute) is: ", to_compare)
stddev_empirical = statistics.stdev(probs)
print("Standard deviation is: ", stddev_empirical)


fql = lang_dict.fam_quant_list() #.sort is to make the random seed deterministic.
fql.sort()
#print(fql)

rand_langs_template = lang_dict.all()
rand_langs_template.sort()

sum = 0
c = 10000   #Can increase or decrease number to try to get a more precise z-score. But we're reliably over 1.7, so who cares.
vals = []

# Kept track of the results for one language family in particular.
total_Austronesian = [0,0,0]
count_Austronesian = 0

for x in range(0,c):
    rand_langs = rand_langs_template[:]
    random.shuffle(fql)
    random.shuffle(rand_langs)
    new_probs = []
    for family in fql:
        sub = rand_langs[0:family]
        del rand_langs[0:family]
        sub_values = [0,0,0]
        no_datas = [0,0,0]

        if len(sub) >= cutoff:
            #The idea is to only count families that are substantial.
            #print("Family", family)
            for lang in sub:
                if lang.d != None:
                    sub_values[0] += lang.d
                else:
                    no_datas[0] += 1
                if lang.p != None:
                    sub_values[1] += lang.p
                else:
                    no_datas[1] += 1
                if lang.i != None:
                    sub_values[2] += lang.i
                else:
                    no_datas[2] += 1

            for i in range(0,3):
                #print((all_values[i] / len(all)))
                #print(sub_values[i], "out of", len(sub))

                if(len(sub) == 21):
                    #print("Austronesian here:")
                    count_Austronesian+=1
                    total_Austronesian[i] += sub_values[i]


                if ((all_values[i] / (len(all) - all_no_datas[i])) < (sub_values[i] / (len(sub) - no_datas[i]) )):
                    o_u = "o"
                else:
                    o_u = "u"

                #new_probs.append(s_chance(len(all), all_values[i], len(sub),sub_values[i], o_u))
                new_probs.append(z_score((len(sub) - no_datas[i]), sub_values[i], i))

    #print(new_probs)
    #print("Number is: ", len(new_probs))
    #print ("Comparative Average is: ", average(new_probs))
    sum += statistics.mean(new_probs)
    vals.append(statistics.mean(new_probs))

# In case you want to see some internal checks on Austronesian.
# for i in range(0,3):
#    print('Average Aus = ', total_Austronesian[i] / (count_Austronesian/3), total_Austronesian, count_Austronesian)
full_avg = sum / c
print("The overall expected z-score is:", full_avg)
meta_zscore_stdev = statistics.stdev(vals)
print("The standard deviation is:", meta_zscore_stdev)

meta_z_score_value = (to_compare - full_avg) / meta_zscore_stdev
print("Our meta_z_score (hopefully >1.65) is: ", meta_z_score_value)

print("That means that there's a very small chance of us seeing the z-score we see in our actual data set.")
print("Let's count the number of tries it takes to get a result as z-score as ours, shall we?")


max_z_score = 0
n = 0
if len(sys.argv) < 4:
    m = int(input("How many times should we try to hit our number? More than 200 will feel like an eternity. "))
else:
    m = int(sys.argv[3])
expected_sum = 0
while n < m:
    n += 1
    stopper = False
    until_stop = 0
    while not stopper:
        until_stop += 1
        rand_langs = rand_langs_template[:]
        random.shuffle(fql)
        random.shuffle(rand_langs)
        new_probs = []
        for family in fql:
            sub = rand_langs[0:family]
            del rand_langs[0:family]
            sub_values = [0,0,0]
            no_datas = [0,0,0]

            if len(sub) >= cutoff:
                #The idea is to only count families that are substantial.
                #print("Family", family)
                for lang in sub:
                    if lang.d != None:
                        sub_values[0] += lang.d
                    else:
                        no_datas[0] += 1
                    if lang.p != None:
                        sub_values[1] += lang.p
                    else:
                        no_datas[1] += 1
                    if lang.i != None:
                        sub_values[2] += lang.i
                    else:
                        no_datas[2] += 1

                for i in range(0,3):
                    #print((all_values[i] / len(all)))
                    #print(sub_values[i], "out of", len(sub))
                    if ((all_values[i] / (len(all) - all_no_datas[i])) < (sub_values[i] / (len(sub) - no_datas[i]) )):
                        o_u = "o"
                    else:
                        o_u = "u"
                    #new_probs.append(s_chance(len(all), all_values[i], len(sub),sub_values[i], o_u))
                    new_probs.append(z_score((len(sub) - no_datas[i]), sub_values[i], i))

        #print(new_probs)
        #print("Number is: ", len(new_probs))
        #print ("Comparative Average is: ", average(new_probs))
        av = statistics.mean(new_probs)
        if av >= to_compare:
            if(av > max_z_score):
                max_z_score = av
            stopper = True
        sum += av

    expected_sum += until_stop
    print("Oh my golly gee, it took us", until_stop, "tries to get our z-score", n, "times!")

expected = expected_sum / m
print("That means the mean time to happen is about once every", expected, "attempts!")
print("That's not very often!")
print("And the largest z score we ever saw was: ", max_z_score)
