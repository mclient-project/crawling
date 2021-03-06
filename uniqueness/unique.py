import os
import logging
import pandas as pd
import pickle
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt
import seaborn as sns

# length of datasets without replicates
TF=0
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
    print(TF)
    for i in range(TF-1):
        compound_score=0.0
        for (columnName, columnData) in final_df.iteritems():
            if columnName=='id':
                weight=HIGHER_WEIGHT
            else:
                weight=LOWER_WEIGHT
                print(str(columnData.values[i]))
            compound_score=compound_score+(weight*columnData.values[i])
        compound_scores.append(compound_score)
    return np.asarray(compound_scores)

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    dir = 'data'
    files = ['title', 'id', 'desc']
    for file_dir in files:
        file_list=list()
        for dir_file in os.listdir(os.path.join(dir, file_dir)):
            print(dir_file)
            data_part = pd.read_csv(os.path.join(dir, file_dir, dir_file))
            # remove header
            logging.info('Processing file '+dir_file)
            file_list.append(data_part)
        concat_df=pd.concat(file_list,ignore_index=True)
        concat_df.reset_index(drop=True,inplace=True)
        concat_df.to_csv(os.path.join(dir, file_dir+'.csv'),index=False)
    replika = 'replikate.csv'
    df_list=list()
    for file_name in files:
        file=file_name+'.csv'
        df = pd.read_csv(os.path.join(dir, file))
        logging.info('Processing file '+file)
        rep_frame =  pd.read_csv(os.path.join(dir, replika))
        # Iterate through replika.csv and for each replika, delete rows in file that have a match in column ?ds
        logging.info('Removing dataset duplicates from '+file)
        for i in range(len(rep_frame)):
            replika_url=rep_frame.loc[i, "ds"]
            df.drop(df.index[df['ds'] == replika_url], inplace = True)
        TF=len(df)
        logging.info('Calculating uniqueness scores for file '+file)
        results=calc_uniqueness(df,file_name)
        df_list.append(results)
    final_df=pd.concat(df_list, join = 'outer', axis = 1)
    print(final_df.head(5))
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

#final_df.boxplot(return_type='axes')
final_df = final_df.rename(columns={'desc': 'description'})
bplot = sns.boxplot(data=final_df,
                 width=0.5,
                 palette="colorblind",
                 showfliers=False)
bplot.set(xlabel='DCAT field', ylabel='Uniqueness')
plt.show()
