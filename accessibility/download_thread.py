import requests
import concurrent.futures
import logging
import pandas as pd
import numpy as np
import os
import pickle

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def get_header(dist_url, timeout=1):
    try:
        r = requests.get(dist_url,timeout=timeout,stream=True)
        code = r.status_code
    except:
        code = 'NaN'
    return code

if __name__ == "__main__":
    dir = 'data'
    df_list=list()
    for file in os.listdir(dir):
        data_part = pd.read_csv(os.path.join(dir, file))
        logging.info('Processing file '+file)
        df_list.append(data_part)
    df_url=pd.concat(df_list,ignore_index=True)
    group = df_url.groupby('dist')
    group_df = group.apply(lambda x: x['url'].unique())
    code_list = []
    url_list = []
    size=len(group_df.keys())
    for key in group_df.keys():
            url_arr=group_df[key]
            for url in url_arr:
                url_list.append(url)
    splitted = [url_list[x:x+10] for x in range(0, len(url_list), 20)]
    counter=0
    for urls in splitted:
        counter=counter+1
        print(str(counter)+' '+str(len(splitted)))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for url in urls:
                futures.append(executor.submit(get_header, dist_url=url))
            for future in concurrent.futures.as_completed(futures):
                code_list.append(future.result())
            #if (counter % 500)==0:
            #    with open("./results/code_list"+str(counter)+".pkl", 'wb') as file:
            #        pickle.dump(code_list, file)
    with open("./results/code_list.pkl", 'wb') as file:
        pickle.dump(code_list, file)
