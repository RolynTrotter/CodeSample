# Make stddev and averages for langs.
# If ya want to run it, just copy it over to Lang_Prob_Parser.py where the lists are.

def calc_std_dev(total_pos, per):
    total = total_pos[0]
    pos = total_pos[1]
    avg_sum = 0
    avg_count = 0
    stupidly_long_list = Enormous_Iterable([])
    for x in range(0,per + 1):
        sub_chance = num_sets_of_features_for_specific_num(total, pos, per, x)
        avg_sum += (sub_chance * x)
        avg_count += sub_chance
        stupidly_long_list.append(sub_chance / (2.0 ** 60))
    return (statistics.stdev(stupidly_long_list), avg_sum/avg_count)


# Pretty much brute force counting
stddev_d = [calc_std_dev(lang_dict.get_feature_frequencies('d'),n) for n in range(22)]
stddev_p = [calc_std_dev(lang_dict.get_feature_frequencies('p'),n) for n in range(22)]
stddev_i = [calc_std_dev(lang_dict.get_feature_frequencies('i'),n) for n in range(22)]

temp_thing = get_list_string(stddev_d)
stddev_d = temp_thing[0]
avd = temp_thing[1]
temp_thing = get_list_string(stddev_p)
stddev_p = temp_thing[0]
avp = temp_thing[1]
temp_thing = get_list_string(stddev_i)
stddev_i = temp_thing[0]
avi = temp_thing[1]

print('stddev_d = ', stddev_d)
print('stddev_p = ', stddev_p)
print('stddev_i = ', stddev_i)
print('avd = ', avd)
print('avp = ', avp)
print('avi = ', avi)

# stddev_d =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.49, 3.01, 2.11, 1.94, 1.96, 2.0, 2.04, 2.08]
# stddev_p =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.76, 3.42, 2.2, 1.89, 1.87, 1.9, 1.94, 1.98]
# stddev_i =  [0.71, 1.0, 1.29, 1.58, 1.87, 2.16, 2.45, 2.74, 3.03, 3.32, 3.61, 3.89, 4.18, 4.47, 4.62, 3.23, 2.16, 1.94, 1.93, 1.97, 2.01, 2.05]
# avd =  [0.0, 0.59, 1.19, 1.78, 2.37, 2.96, 3.56, 4.15, 4.74, 5.34, 5.93, 6.52, 7.11, 7.71, 8.3, 8.89, 9.49, 10.08, 10.67, 11.26, 11.86, 12.45]
# avi =  [0.0, 0.62, 1.25, 1.87, 2.49, 3.12, 3.74, 4.36, 4.99, 5.61, 6.23, 6.86, 7.48, 8.1, 8.72, 9.35, 9.97, 10.59, 11.22, 11.84, 12.46, 13.09]
# avp =  [0.0, 0.68, 1.36, 2.04, 2.72, 3.39, 4.07, 4.75, 5.43, 6.11, 6.79, 7.47, 8.15, 8.82, 9.5, 10.18, 10.86, 11.54, 12.22, 12.9, 13.58, 14.26]
