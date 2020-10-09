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

qcewdata05.to_csv('QCEW2005.csv', index=False)
#qcewdata06.to_csv('QCEW2006.csv', index=False)
#qcewdata07.to_csv('QCEW2007.csv', index=False)
#qcewdata08.to_csv('QCEW2008.csv', index=False)
#qcewdata09.to_csv('QCEW2009.csv', index=False)
#qcewdata10.to_csv('QCEW2010.csv', index=False)
#qcewdata11.to_csv('QCEW2011.csv', index=False)
#qcewdata12.to_csv('QCEW2012.csv', index=False)
#qcewdata13.to_csv('QCEW2013.csv', index=False)
#qcewdata14.to_csv('QCEW2014.csv', index=False)
#qcewdata15.to_csv('QCEW2015.csv', index=False)