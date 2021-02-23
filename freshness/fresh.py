import os
import pandas as pd
import arrow
import seaborn as sns
import matplotlib.pyplot as plt

dir='data/govdata'
df_list=list()
curl_date='2020-12-27'
for file in os.listdir(dir):
    data_part = pd.read_csv(os.path.join(dir, file))
    df_list.append(data_part)
final_df=pd.concat(df_list,ignore_index=True)
print(final_df.head(5))
curl_arrow = arrow.get(curl_date)
rows_list=list()
for index, row in final_df.iterrows():
    split_string = row['count'].split("+", 1)
    date_arrow = arrow.get(split_string[0])
    delta = (curl_arrow-date_arrow)
    print(delta.days)
    dict = {}
    dict['days_since_mod']=delta.days
    rows_list.append(dict)
fresh_df=pd.DataFrame(rows_list)

bplot = sns.boxplot(data=fresh_df,
                 width=0.2,
                 palette="colorblind")
plt.show()
