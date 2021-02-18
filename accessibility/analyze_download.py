import requests
import logging
import pandas as pd
import numpy as np
import os
import pickle
from itertools import groupby
import seaborn as sns
import matplotlib.pyplot as plt

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
if __name__ == "__main__":
    with open('./results/code_list.pkl', 'rb') as file2:
        code_list = pickle.load(file2)
    logging.info('Total no. of queried URLs '+str(len(code_list)))
    clean_code_list = [x for x in code_list if str(x) != 'NaN']
    logging.info('Total no. of status code responses '+str(len(clean_code_list)))
    code_results = {value: len(list(freq)) for value, freq in groupby(sorted(clean_code_list))}
    logging.info('Status code counts '+str(code_results))
    access_df=pd.DataFrame.from_dict(list(code_results.items()))
    access_df.columns=['status_code', 'counts']
    print(access_df.head(5))
    bplot = sns.boxplot(data=access_df,
                     y='counts', x='status_code',
                     width=0.5,
                     palette="colorblind")
    bplot.set(xlabel='Status code', ylabel='Number')
    plt.show()
