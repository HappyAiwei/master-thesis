import pandas as pd
import numpy as np
import glob

ids = pd.read_csv('Paired_County_ID.csv')
ids['id'] = ids['id'].astype(str)
ids['id'] = ids['id'].str.zfill(5)

def QCEW_IN_LIST(doc_path):

    #files = glob.glob('/home/jinli/Desktop/Thesis/Data/QCEW/2005.q1-q4.by_area/*.csv')

    files = glob.glob(doc_path + '*.csv')
    dfs = [pd.read_csv(file) for file in files]
    qcewdata = pd.concat(dfs, ignore_index=True)

    #qcewdata05 = qcewdata[qcewdata['area_fips'].apply(lambda x: str(x).isdigit())]

    qcewdata['area_fips'] = qcewdata['area_fips'].astype(str)
    qcewdata['area_fips'] = qcewdata['area_fips'].str.zfill(5)

    qcewdata.drop(qcewdata.columns[21:], axis=1, inplace=True)
    qcewdata = qcewdata.loc[qcewdata['own_code'] == 0]

    qcewdata = pd.merge(qcewdata, ids, left_on='area_fips', right_on='id')
    return qcewdata

qcewdata05 = QCEW_IN_LIST('/home/jinli/Desktop/Thesis/Data/QCEW/2005.q1-q4.by_area/')
#qcewdata06 = QCEW_IN_LIST('...')
#qcewdata07 = QCEW_IN_LIST('...')
#qcewdata08 = QCEW_IN_LIST('...')
#qcewdata09 = QCEW_IN_LIST('...')
#qcewdata10 = QCEW_IN_LIST('...')
#qcewdata11 = QCEW_IN_LIST('...')
#qcewdata12 = QCEW_IN_LIST('...')
#qcewdata13 = QCEW_IN_LIST('...')
#qcewdata14 = QCEW_IN_LIST('...')
#qcewdata15 = QCEW_IN_LIST('...')

qcewdata = pd.concat([qcewdata05, qcewdata06, qcewdata07, qcewdata08, qcewdata09, qcewdata10,
                      qcewdata11, qcewdata12, qcewdata13, qcewdata14, qcewdata15], ignore_index=True)

qcewdata.to_csv('QCEW.csv', index=False)
