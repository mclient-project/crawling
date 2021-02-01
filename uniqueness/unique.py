import os
import logging
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

# length of datasets without replicates
TF=41823
HIGHER_WEIGHT=0.5
LOWER_WEIGHT=0.25

def log(tf,vf):
    number=1+((tf-vf+0.5)/(vf+0.5))
    return np.log2(number)

def calc_uniqueness(df,file_name):
    vf_all=df.groupby([file_name]).count()
    score_norm=log(TF,1)
    rows_list = []
    # Iterate through the new df and calculate the score for each ?ds
    for index, row in df.iterrows():
        try:
            vf=vf_all.loc[row[file_name], 'ds']
            score=log(TF,vf)
            uniqueness=score/score_norm
        except KeyError:
            uniquenss=float('NaN')
        dict1 = {}
        dict1[file_name]=uniqueness
        rows_list.append(dict1)
    return pd.DataFrame(rows_list)

def calc_compound(final_df):
    compound_scores = []
    for i in range(TF-1):
        compound_score=0.0
        for (columnName, columnData) in final_df.iteritems():
            if columnName=='id':
                weight=HIGHER_WEIGHT
            else:
                weight=LOWER_WEIGHT
            compound_score=compound_score+(weight*columnData.values[i])
        compound_scores.append(compound_score)
    return np.asarray(compound_scores)

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    dir = 'data'
    files = ['title.csv', 'id.csv', 'desc.csv']
    replika = 'replikate.csv'
    df_list=list()
    for file in files:
        file_name=file.replace('.csv','')
        df = pd.read_csv(os.path.join(dir, file))
        logging.info('Processing file '+file)
        rep_frame =  pd.read_csv(os.path.join(dir, replika))
        # Iterate through replika.csv and for each replika, delete rows in file that have a match in column ?ds
        logging.info('Removing dataset duplicates from '+file)
        for i in range(len(rep_frame)):
            replika_url=rep_frame.loc[i, "ds"]
            df.drop(df.index[df['ds'] == replika_url], inplace = True)
        logging.info('Calculating uniqueness scores for file '+file)
        results=calc_uniqueness(df,file_name)
        df_list.append(results)
    final_df=pd.concat(df_list, join = 'outer', axis = 1)
    compound_array=calc_compound(final_df)
    logging.info('Compound Average uniqueness is '+str(np.nanmean(compound_array, axis=0)))
    logging.info('Compound Std uniqueness is '+str(np.nanstd(compound_array, axis=0)))
    logging.info('Compound Max uniqueness is '+str(np.nanmax(compound_array, axis=0)))
    logging.info('Compound Min uniqueness is '+str(np.nanmin(compound_array, axis=0)))

    # Calculate compound score
    #logging.info('The compound mean is '+str(compound_mean))
    for (columnName, columnData) in final_df.iteritems():
        logging.info('Average uniqueness for '+columnName+' is '+str(final_df[columnName].mean()))
        logging.info('Std uniqueness for '+columnName+' is '+str(final_df[columnName].std()))
        logging.info('Max uniqueness for '+columnName+' is '+str(final_df[columnName].max()))
        logging.info('Min uniqueness for '+columnName+' is '+str(final_df[columnName].min()))
