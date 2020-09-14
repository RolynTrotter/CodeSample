class Language():
    # Represents a language from the database
    def __init__(self, name, family, secondary, duration, pitch, intensity):
        self.name = name
        self.fam = family
        self.secondary = secondary

        #In case there are blanks.
        try:
            self.d = int(duration)
        except ValueError:
            self.d = None
        try:
            self.p = int(pitch)
        except ValueError:
            self.p = None
        try:
            self.i = int(intensity)
        except ValueError:
            self.i = None

    def __str__(self):
        return("%s (%s): %s %s %s".format(self.name, self.fam, self.d, self.p, self.i))

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        return str(self) < str(other)

    def __gt__(self, other):
        return str(self) > str(other)

class LangDict(dict):
    def __init__(self):
        self = {}

    def fam(self, fam_name):
        l = []
        k = self.keys()
        for i in k:
            if self[i].fam == fam_name:
                l.append(self[i])
        return l

    def all(self):
        l = []
        k = self.keys()
        for i in k:
            l.append(self[i])
        return l

    def fam_list(self):
        #Returns a list of all language families in the dictionary
        s = set()
        for lang in self:
            s.add(self[lang].fam)
        return list(s)

    def fam_quant_list(self):
        #returns a list of the FREQUENCIES of language families. This'll get shuffled later.
        f_list = self.fam_list()
        to_return = [0] * len(f_list)
        count = 0
        for family in f_list:
            for l in self:
                #I'm a person who nests loops in functions that are only called once. Sue me.
                if self[l].fam == family:
                    to_return[count] += 1
            count += 1
        return to_return

    def get_feature_frequencies(self, feature):
        #return the number of durations, pitches, etc. Not really used.
        sum = 0
        pos = 0
        for l in self.all():
            #skip counting if the item is none (aka 2 in the csv)
            if feature == 'd':
                if l.d == 1:
                    sum += 1
                    pos += 1
                elif l.d == 0:
                    sum += 1
            elif feature == 'p':
                if l.p:
                    sum += 1
                    pos += 1
                elif l.p == 0:
                    sum += 1
            elif feature == 'i':
                if l.i:
                    sum += 1
                    pos += 1
                elif l.i == 0:
                    sum += 1
        return(sum,pos)

# def num_sets(size, sub):
#     #Calculates the number of subsets of a particular size you can make
#     size_fac = (math.factorial(size) / math.factorial(size - sub)) / math.factorial(sub)
#     return size_fac
#
# def num_sets_of_features_for_specific_num(size, feature_size, sub, num):
#     #size is the total sample size (141)
#     #feature_size is how many languages have the feature (83)
#     #sub is the size of the subset we are generating (20)
#     #num is the target number we're checking
#     sum = 0.0
#     if((size - feature_size) < sub - num):  #Can't possibly make that size of thing, yo.
#         pass
#     else:
#         sum += num_sets(feature_size, num) * num_sets(size - feature_size, sub - num)
#                                                             #44-35,
#     #print(sum)
#     return sum
#
# def s_chance(total, pos, per, target, over_under):
#     sum_chance = 0
#     #0 to target+1 if you're looking for odds of below, target to max+1 (21) if you're looking for odds of above.
#     if (over_under == "o"):
#         for i in range(target, per + 1):
#             sum_chance += num_sets_of_features_for_specific_num(total,pos,per,i) / num_sets(total,per)
#         #print("Chance of having exactly this many or more: ", sum_chance)
#     elif (over_under == "u"):
#         for i in range(0, target + 1):
#             sum_chance += num_sets_of_features_for_specific_num(total,pos,per,i) / num_sets(total,per)
#         #print("Chance of having exactly this many or less: ", sum_chance)
#     return sum_chance