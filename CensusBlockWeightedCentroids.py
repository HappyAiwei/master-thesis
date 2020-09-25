import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geoplot as gplt
import shapefile
import osr
import dbf
import requests
import io
import tqdm
import glob
import tqdm

from urllib.request import urlopen
from zipfile import ZipFile
from shapely.geometry import shape, Point, Polygon


## Function definition: Read Blocks Shapefile within a State
def Blocks_Shapefile(doc_path):
    state_blocks = ZipFile(doc_path, 'r')

    filenames = [y for y in sorted(state_blocks.namelist())
                 for ending in ['dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)]
    dbf, prj, shp, shx = [io.BytesIO(state_blocks.read(filename)) for filename in filenames]
    r = shapefile.Reader(shp=shp, shx=shx, dbf=dbf)

    attributes, geometry = [], []
    field_names = [field[0] for field in r.fields[1:]]
    for row in r.shapeRecords():
        geometry.append(shape(row.shape.__geo_interface__))
        attributes.append(dict(zip(field_names, row.record)))

    prj = io.TextIOWrapper(prj, encoding='utf-8')
    proj4 = osr.SpatialReference(prj.read()).ExportToProj4()

    gdf = gpd.GeoDataFrame(data=attributes, geometry=geometry, crs=proj4)
    gdf[['INTPTLON10', 'INTPTLAT10']] = gdf[['INTPTLON10', 'INTPTLAT10']].apply(pd.to_numeric)
    gdf.sort_values(['COUNTYFP10', 'BLOCKCE10', 'TRACTCE10'], ascending=[True, True, True], inplace=True)
    gdf.reset_index(drop=True, inplace=True)

    return gdf


## Function definition: Read Population by Blocks within a State
def Blocks_Population(doc_path):
    pop = pd.read_csv(doc_path, header=1)
    pop['GEOID10'] = pop['id'].map(lambda x: x[9:])
    ### cols = pop.columns.tolist()   ## ['id', 'Geographic Area Name', 'Total', 'GEOID10']
    pop = pop[['id', 'Geographic Area Name', 'GEOID10', 'Total']]

    return pop


## Function definition: Read County Shapefile of USA
def USA_County_Shapefile(doc_path):
    allcounties = ZipFile(doc_path, 'r')

    filenames = [y for y in sorted(allcounties.namelist())
                 for ending in ['dbf', 'prj', 'shp', 'shx'] if y.endswith(ending)]
    dbf, prj, shp, shx = [io.BytesIO(allcounties.read(filename)) for filename in filenames]
    r = shapefile.Reader(shp=shp, shx=shx, dbf=dbf)

    attributes, geometry = [], []
    field_names = [field[0] for field in r.fields[1:]]
    for row in r.shapeRecords():
        geometry.append(shape(row.shape.__geo_interface__))
        attributes.append(dict(zip(field_names, row.record)))

    prj = io.TextIOWrapper(prj, encoding='utf-8')
    proj4 = osr.SpatialReference(prj.read()).ExportToProj4()

    gdf = gpd.GeoDataFrame(data=attributes, geometry=geometry, crs=proj4)
    gdf.sort_values(by=['STATEFP10', 'COUNTYFP10'], inplace=True)
    gdf.reset_index(drop=True, inplace=True)
    gdf[['INTPTLON10', 'INTPTLAT10']] = gdf[['INTPTLON10', 'INTPTLAT10']].apply(pd.to_numeric)

    gdf = gdf[(gdf.STATEFP10 != '02') & (gdf.STATEFP10 != '72') & (gdf.STATEFP10 != '15')]

    return gdf


## A list of file names and path in 'Census_Shapefiles' folder.
shapefile_list = glob.glob('/home/jinli/Desktop/DataForMasterThesis/Census_Shapefiles/*.zip')
pop_list = glob.glob('/home/jinli/Desktop/DataForMasterThesis/Census_Block_Population/*.csv')

namespace = globals()
for idx, val in enumerate(shapefile_list):
    namespace['gdf_%d' % idx] = Blocks_Shapefile(val)
    
for idx, val in enumerate(pop_list):
    namespace['df_%d' % idx] = Blocks_Population(val)
    
gdf = pd.concat([gdf_0, gdf_1, gdf_2, gdf_3, gdf_4, gdf_5, gdf_6, gdf_7, gdf_8, gdf_9, 
                 gdf_10, gdf_11, gdf_12, gdf_13, gdf_14, gdf_15, gdf_16, gdf_17, gdf_18, gdf_19,
                 gdf_20, gdf_21, gdf_22, gdf_23, gdf_24, gdf_25, gdf_26, gdf_27, gdf_28, gdf_29,
                 gdf_30, gdf_31, gdf_32, gdf_33, gdf_34, gdf_35, gdf_36, gdf_37, gdf_38, gdf_39,
                 gdf_40, gdf_41, gdf_42, gdf_43, gdf_44, gdf_45, gdf_46, gdf_47, gdf_48])

pop = pd.concat([df_0, df_1, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, 
                 df_10, df_11, df_12, df_13, df_14, df_15, df_16, df_17, df_18, gdf_19,
                 df_20, df_21, df_22, df_23, df_24, df_25, df_26, df_27, df_28, gdf_29,
                 df_30, df_31, df_32, df_33, df_34, df_35, df_36, df_37, df_38, gdf_39,
                 df_40, df_41, df_42, df_43, df_44, df_45, df_46, df_47, df_48])



geodata = pd.merge(gdf, pop, on='GEOID10')

'''
geodata.columns.str.replace(' ', '')
Index(['STATEFP10', 'COUNTYFP10', 'TRACTCE10', 'BLOCKCE10', 'GEOID10',
       'NAME10', 'MTFCC10', 'UR10', 'UACE10', 'UATYP10', 'FUNCSTAT10',
       'ALAND10', 'AWATER10', 'INTPTLAT10', 'INTPTLON10', 'geometry', 'id',
       'GeographicAreaName', 'Total']
'''

'''
geodata.set_axis(['STATEFP10', 'COUNTYFP10', 'TRACTCE10', 'BLOCKCE10', 'GEOID10',
                  'NAME10', 'MTFCC10', 'UR10', 'UACE10', 'UATYP10', 'FUNCSTAT10',
                  'ALAND10', 'AWATER10', 'INTPTLAT10', 'INTPTLON10', 'geometry', 'id',
                  'GeographicAreaName', 'Total'], axis=1, inplace=True)
'''

geodata = geodata[['STATEFP10', 'COUNTYFP10', 'GEOID10', 'Total', 'INTPTLON10', 'INTPTLAT10']]

geodata['LON*POP'] = geodata['Total']*geodata['INTPTLON10']
geodata['LAT*POP'] = geodata['Total']*geodata['INTPTLAT10']

## Calculation of population weighted centroids for each county
gdf_bycounty = geodata.groupby(['STATEFP10', 'COUNTYFP10'])[['Total', 'LON*POP', 'LAT*POP']].sum().reset_index()
gdf_bycounty['LON'] = gdf_bycounty['LON*POP']/gdf_bycounty['Total']
gdf_bycounty['LAT'] = gdf_bycounty['LAT*POP']/gdf_bycounty['Total']

gdf_bycounty.to_csv('CountyCentroids.csv', index=False)