
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import os
from collections import Counter

bad_list = ['NULL', 'null', 'NaN', '-NaN', 'nan', '-nan', '']

deal_method = 4

file_list = ["movies_dataset.csv"
             , 'Alzheimer Disease and Healthy Aging Data In US.csv'
             , "repository_data.csv"
             , "github_dataset.csv"
             ]

if not os.path.exists("Result"):
    os.mkdir('Result')

# 打开文件
for file_path in file_list:
    try:
        f = open(file_path, 'r', encoding='utf-8', errors='ignore')
    except:
        print(f'read {file_path} error!')

    # 读取文件
    data = pd.read_csv(f, low_memory=False)
    column = data.columns
    datalist = data.values.tolist()
    print(column)
    f.close()

    for method_ in range(1, 5):
        deal_method = method_
        if not os.path.exists("Result\\%s_%d" % (file_path, deal_method)):
            os.mkdir("Result\\%s_%d" % (file_path, deal_method))

        # 建立字典
        dict = {}
        for index, col_name in enumerate(column):
            dict[index] = []
        nan_list = []
        type_list = {}

        # 缺失值处理
        for row_index, row in enumerate(datalist):
            flag = 0
            for column_index, item in enumerate(row):
                if type(item) == float and math.isnan(item):
                    if deal_method == 1:
                        continue
                    else:
                        nan_list.append((row_index, column_index))
                        continue
                else:
                    if column_index not in type_list.keys():
                        type_list[column_index] = type(item)
                    # print(column_index, item)
                    dict[column_index].append(item)

        print(len(nan_list))
        if deal_method == 2:
            dict_add = {}
            for item in nan_list:
                if len(dict[item[1]]) != 0:
                    if item[1] not in dict_add.keys():
                        item_counts = Counter(dict[item[1]])
                        dict_add[item[1]] = max(item_counts.items(), key=lambda x: x[1])[0]
                    dict[item[1]].append(dict_add[item[1]])

        if deal_method == 3:

            dict_add = {}
            for item in nan_list:
                if len(dict[item[1]]) != 0:
                    if item[1] not in dict_add.keys():
                        item_counts = Counter(dict[item[1]])
                        dict_add[item[1]] = max(item_counts.items(), key=lambda x: x[1])[0]

            nan_column_list = []
            coexist_pair_count = {}
            col_tc = {}
            for lost_item in nan_list:
                if lost_item[1] not in nan_column_list and len(dict[lost_item[1]]) != 0:
                    nan_column_list.append(lost_item[1])

            # 统计共现数据对
            for row_index, row in enumerate(datalist):
                for column_index, item in enumerate(row):
                    if column_index in nan_column_list:
                        if type(item) == float and math.isnan(item):
                            continue
                        for i in range(0, len(row)):
                            if (type(row[i]) == float and math.isnan(row[i])) or i == column_index:
                                continue
                            if (i, column_index) not in coexist_pair_count.keys():
                                coexist_pair_count[(i, column_index)] = {}
                            if row[i] not in coexist_pair_count[(i, column_index)].keys():
                                coexist_pair_count[(i, column_index)][row[i]] = {}
                            if item not in coexist_pair_count[(i, column_index)][row[i]].keys():
                                coexist_pair_count[(i, column_index)][row[i]][item] = 0
                            coexist_pair_count[(i, column_index)][row[i]][item] += 1

            for (col1, col2) in coexist_pair_count.keys():
                if col2 not in col_tc.keys():
                    col_tc[col2] = {}
                if col1 not in col_tc[col2].keys():
                    col_tc[col2][col1] = 0
                for item in coexist_pair_count[(col1, col2)].keys():
                    col_tc[col2][col1] += len(coexist_pair_count[(col1, col2)][item].keys())

            for col in col_tc.keys():
                col_tc[col] = sorted(col_tc[col].items(), key=lambda x: x[1])
                #print(col_tc[col])

            for k, lost_item in enumerate(nan_list):
                if k%100 == 0:
                    print(k)
                if len(dict[lost_item[1]]) == 0:
                    continue
                current_value = {}
                row = datalist[lost_item[0]]
                for i in col_tc[lost_item[1]]:
                    #print(i)
                    if type(row[i[0]]) == float and math.isnan(row[i[0]]):
                        continue
                    if lost_item[1] not in nan_column_list:
                        continue
                    if row[i[0]] not in coexist_pair_count[(i[0], lost_item[1])].keys():
                        continue
                    for key in coexist_pair_count[(i[0], lost_item[1])][row[i[0]]].keys():
                        if key not in current_value.keys():
                            current_value[key] = 0
                        current_value[key] += coexist_pair_count[(i[0], lost_item[1])][row[i[0]]][key]
                    if len(current_value.keys()) != 0:
                        break
                item_counts = Counter(current_value)
                #print(lost_item, item_counts)
                if item_counts != Counter():
                    #print(item_counts)
                    dict[lost_item[1]].append(max(item_counts.items(), key=lambda x: x[1])[0])
                else:
                    dict[lost_item[1]].append(dict_add[lost_item[1]])

        if deal_method == 4:
            nan_column_list = []
            coexist_pair_count = {}
            for lost_item in nan_list:
                if lost_item[1] not in nan_column_list and len(dict[lost_item[1]]) != 0:
                    nan_column_list.append(lost_item[1])

            dict_add = {}
            for item in nan_list:
                if len(dict[item[1]]) != 0:
                    if item[1] not in dict_add.keys():
                        item_counts = Counter(dict[item[1]])
                        dict_add[item[1]] = max(item_counts.items(), key=lambda x: x[1])[0]

            # 统计共现数据对
            for row_index, row in enumerate(datalist):
                for column_index, item in enumerate(row):
                    if column_index in nan_column_list:
                        if type(item) == float and math.isnan(item):
                            continue
                        for i in range(0, len(row)):
                            if (type(row[i]) == float and math.isnan(row[i])) or i == column_index:
                                continue
                            if (i, column_index) not in coexist_pair_count.keys():
                                coexist_pair_count[(i, column_index)] = {}
                            if row[i] not in coexist_pair_count[(i, column_index)].keys():
                                coexist_pair_count[(i, column_index)][row[i]] = {}
                            if item not in coexist_pair_count[(i, column_index)][row[i]].keys():
                                coexist_pair_count[(i, column_index)][row[i]][item] = 0
                            coexist_pair_count[(i, column_index)][row[i]][item] += 1

            for k, lost_item in enumerate(nan_list):
                if k%100 == 0:
                    print(k)
                if len(dict[lost_item[1]]) == 0:
                    continue
                current_value = {}
                row = datalist[lost_item[0]]
                for i in range(0, len(row)):
                    if type(row[i]) == float and math.isnan(row[i]):
                        continue
                    if lost_item[1] not in nan_column_list:
                        continue
                    if row[i] not in coexist_pair_count[(i, lost_item[1])].keys():
                        continue
                    for key in coexist_pair_count[(i, lost_item[1])][row[i]].keys():
                        if key not in current_value.keys():
                            current_value[key] = 0
                        current_value[key] += coexist_pair_count[(i, lost_item[1])][row[i]][key]
                item_counts = Counter(current_value)
                #print(lost_item, item_counts)
                if item_counts != Counter():
                    dict[lost_item[1]].append(max(item_counts.items(), key=lambda x: x[1])[0])
                else:
                    dict[lost_item[1]].append(dict_add[lost_item[1]])

        col_nan = {}
        for index, col_name in enumerate(column):
            col_nan[index] = 0
        for (r, c) in nan_list:
            if len(dict[c]) == 0:
                continue
            elif type_list[c] == float or type_list[c] == int:
                col_nan[c] += 1

        try:
            file = open('Result\\%s_%d\\analyse.txt' % (file_path, deal_method), mode='a', encoding='utf-8')
        except:
            print(f'open analyse file error!')
            continue

        for index, col_name in enumerate(column):
            plt.clf()
            if len(dict[index]) == 0:
                print("%s has none item." % col_name)
            elif type_list[index] == float or type_list[index] == int:
                plt.boxplot(dict[index])
                plt.xticks([1], [col_name])
                Minimum = min(dict[index])
                Maximum = max(dict[index])
                Q1 = np.percentile(dict[index], 25)
                Median = np.median(dict[index])
                Q3 = np.percentile(dict[index], 75)
                print("%s, Minimum = %lf, Q1 = %lf, Median = %lf, Q3 = %lf, Maximum = %lf, Nan = %d" % (col_name, Minimum, Q1, Median, Q3, Maximum, col_nan[index]))
                plt.savefig('Result\\%s_%d\\%s.jpg' % (file_path, deal_method, col_name), bbox_inches='tight')
                #plt.show()
                file.write("%s\nMinimum = %lf, Q1 = %lf, Median = %lf, Q3 = %lf, Maximum = %lf, Nan = %d\n\n" % (col_name, Minimum, Q1, Median, Q3, Maximum, col_nan[index]))
            else:
                letter_counts = Counter(dict[index])
                #print(type(letter_counts))
                #print(letter_counts.most_common(30))
                plt.figure()
                df = pd.DataFrame(letter_counts.most_common(30))
                df = pd.DataFrame(letter_counts.most_common(30), index=df[0])
                #print(df)
                df.plot(kind='bar')
                plt.legend().remove()
                plt.xlabel('%s' % col_name)
                plt.savefig('Result\\%s_%d\\%s.jpg' % (file_path, deal_method, col_name), bbox_inches='tight')
                #plt.show()
                file.write("%s\n" % col_name)
                df = pd.DataFrame(letter_counts.most_common())
                for row in df.index:
                    file.write('%s\t\t%d\n' % (df.loc[row][0], df.loc[row][1]))
                file.write('\n')

        file.close()
