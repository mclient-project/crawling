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
        # remove header
        logging.info('Processing file '+file)
        df_list.append(data_part)
    final_df=pd.concat(df_list,ignore_index=True)
    counts=final_df.groupby(['keyword']).count()
    max_freq=counts.max()
    rows_list = []
    for index, row in counts.iterrows():
        frac=row[0]/max_freq
        ds=np.log2(frac)
        keyword_IC=ds[0]
        dict1 = {}
        dict1['content']=keyword_IC
        dict1['keyword']=index
        rows_list.append(dict1)
    content=pd.DataFrame(rows_list)
    print(content.head(150))
    content.to_pickle("./content.pkl")
    #ds_list=final_df.ds.unique()

    #content.to_pickle("./content.pkl")
