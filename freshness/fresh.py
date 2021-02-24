import os
import pandas as pd
#import arrow
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

dir='data'
end_date = datetime.datetime(2021,2,23)
files = ['mcloud','govdata', 'all']
df_list=list()
for file_dir in files:
#curl_date='2021-02-23'
    part_list=list()
    for file in os.listdir(os.path.join(dir, file_dir)):
        data_part = pd.read_csv(os.path.join(dir, file_dir, file))
        part_list.append(data_part)
    final_df=pd.concat(part_list,ignore_index=True)
    print(final_df.head(5))
    rows_list=list()
    for index, row in final_df.iterrows():
        try:
            split_string = row['date'].split("+", 1)[0].split(" ", 1)[0].split("T", 1)
            date=split_string[0].split("-")
            start_date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]))
            num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            print(num_months)
            dict = {}
            dict[file_dir]=num_months
            rows_list.append(dict)
        except:
            print('Skipping this one!')
    fresh_df=pd.DataFrame(rows_list)
    df_list.append(fresh_df)
analyze_df=pd.concat(df_list, join = 'outer', axis = 1)
bplot = sns.boxplot(data=analyze_df,
                 width=0.2,
                 palette="colorblind",
                 showfliers=False)
bplot.set(xlabel='Catalog', ylabel='Months since issued')
plt.show()
