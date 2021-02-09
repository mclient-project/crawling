
import os
import logging
import pandas as pd
import pickle
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt
import seaborn as sns

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

if __name__ == "__main__":
    with open('./ds_content.pkl', 'rb') as f:
        ds_content = pickle.load(f)
    #ds_content = ds_content.where(ds_content < 0, 0)
    #ds_content[ds_content < 0] = 0
    ds_content['ds_content'] = ds_content['ds_content'].apply(lambda x : x if x > 0 else 0)
    print(ds_content.head(5))
    normalized_df=(ds_content-ds_content.min())/(ds_content.max()-ds_content.min())
    print(normalized_df.head(5))
    logging.info('Average IC is '+str(normalized_df['ds_content'].mean()))
    logging.info('Std IC is '+str(normalized_df['ds_content'].std()))
    logging.info('Max IC is '+str(normalized_df['ds_content'].max()))
    logging.info('Min IC is '+str(normalized_df['ds_content'].min()))


#normalized_df.boxplot(column=['ds_content'],
#                       grid=False)

normalized_df.boxplot(column='ds_content', return_type='axes')
plt.show()
#bplot = sns.boxplot(y='score', x='content',
#                 data=normalized_df,
#                 width=0.5)
