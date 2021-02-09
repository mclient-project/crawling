import os
import logging
import pandas as pd
import pickle
import numpy as np
from statistics import mean

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    dir = 'data'
    df_list=list()
    for file in os.listdir(dir):
        data_part = pd.read_csv(os.path.join(dir, file))
        logging.info('Processing file '+file)
        df_list.append(data_part)
    final_df=pd.concat(df_list,ignore_index=True)
    with open('./content.pkl', 'rb') as f:
        content = pickle.load(f)
    group = final_df.groupby('ds')
    grouped_ds = group.apply(lambda x: x['keyword'].unique())
    rows_list = []
    print(grouped_ds.head(5))
    #print(content.head(5))
    counter=0
    for key_arr in grouped_ds:
        counter=counter+1
        print(counter)
        #print(str(len(grouped_ds))+' '+str(counter))
        log_sum=0.0
        size=len(key_arr)
        for key in key_arr:
            try:
                count = content.loc[content['keyword'] == key, 'content'].values[0]
            except IndexError:
                count = 0
                size = size-1
            #print(str(count))
            log_sum=log_sum+count
            #print(str(log_sum))
        log=-(log_sum/size)
        #print(log)
        dict1 = {}
        dict1['ds_content']=log
        rows_list.append(dict1)
    ds_content=pd.DataFrame(rows_list)
    ds_content.to_pickle("./ds_content.pkl")
    #logging.info('Average IC is '+str(ds_content['ds_content'].mean()))
    #logging.info('Std IC is '+str(ds_content['ds_content'].std()))
    #logging.info('Max IC is '+str(ds_content['ds_content'].max()))
    #logging.info('Min IC is '+str(ds_content['ds_content'].min()))
    # find all keywords for a dataset
