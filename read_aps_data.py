#%%

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 18:30:34 2022

@author: sujaiban
"""

#%%
def change_file_extension(folder):
    
    import os

    # Dictionary for extension mappings 
    rename_dict = {'sum': 'txt'}
    for filename in os.listdir(folder):

        # Get the extension and remove . from it
        base_file, ext = os.path.splitext(filename)
        ext = ext.replace('.','')

        # If you find the extension to rename
        if ext in rename_dict:
            # Create the new file name
            new_ext = rename_dict[ext]
            new_file = base_file + '.' + new_ext
            
            # Create the full old and new path
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_file)
            
            # Rename the file
            os.rename(old_path, new_path)
            
        return
    
#%%
    
change_file_extension(r'C:\LocalData\sujaiban\sujai.banerji\Aerosol Optical Properties\2021')

#%%

def read_aps_data(level_zero_path, start_date, end_date_plus_one):       
    
    from datetime import date, timedelta
    import os
    import pandas as pd
    # import math as mt
    
    y1 = int(str(start_date)[0:4])
    m1 = int(str(start_date)[4:6])
    d1 = int(str(start_date)[6:8])
    
    y2 = int(str(end_date_plus_one)[0:4])
    m2 = int(str(end_date_plus_one)[4:6])
    d2 = int(str(end_date_plus_one)[6:8])

    start_datetime = date(y1, m1, d1)
    end_datetime_plus_one = date(y2, m2, d2)  
    
    def daterange(start_datetime, end_datetime_plus_one):
        for n in range(int((end_datetime_plus_one - start_datetime).days)):
            yield start_datetime + timedelta(n)
            
    # density = 1.5
    
    start_datetime_plus_one = start_datetime + timedelta(1)
    start_datetime_file_name = 'aps' + str(start_datetime.strftime('%Y%m%d')) + '.txt'
    level_one_name = str(start_datetime_plus_one.year)
    level_one_path = os.path.join(level_zero_path, level_one_name)
    start_datetime_file_path = os.path.join(level_one_path, start_datetime_file_name)
    df_start_datetime = pd.read_csv(start_datetime_file_path, sep = '\s+')
    aps_diameters = list(df_start_datetime.columns.values)    
    df_aps_diameters = pd.DataFrame({'col': aps_diameters})
    df_aps_diameters = df_aps_diameters.iloc[2:, 0]
    df_aps_diameters = df_aps_diameters.to_numpy()
    df_aps_diameters = df_aps_diameters.reshape((1, 53))
    df_aps_diameters = pd.DataFrame(df_aps_diameters)
    # df_aps_diameters = df_aps_diameters/mt.sqrt(density)
    aps_timestamps = df_start_datetime.iloc[:, 0]
    df_aps_timestamps = aps_timestamps.to_frame()
    
    n = 1
    
    for single_date in daterange(start_datetime_plus_one, end_datetime_plus_one):
        level_one_name = str(start_datetime_plus_one.year)
        level_one_path = os.path.join(level_zero_path, level_one_name)
        level_two_name = 'aps' + str(single_date.strftime('%Y%m%d')) + '.txt'
        level_two_path = os.path.join(level_one_path, level_two_name)
        df_rest = pd.read_csv(level_two_path, sep = '\s+')
        df_rest = df_start_datetime + df_rest
        n = n + 1
        
    df_rest_values = df_rest.iloc[:, 2: ]
    df_rest_values_average = df_rest_values/n
    df_rest_with_timestamps = pd.concat([df_aps_timestamps, df_rest_values_average], axis = 1) 
    df_rest_with_timestamps = df_rest_with_timestamps.set_index(df_rest_with_timestamps.iloc[:, 0])
    df_rest_with_timestamps = df_rest_with_timestamps.iloc[:, 1:]
    df_rest_with_timestamps.shape[1]
    range(df_rest_with_timestamps.shape[1])
    df_rest_with_timestamps.columns = range(df_rest_with_timestamps.shape[1])
    df_rest_with_timestamps = pd.concat([df_aps_diameters, df_rest_with_timestamps], axis = 0)
    df_rest_with_timestamps = df_rest_with_timestamps.rename(columns = df_rest_with_timestamps.iloc[0]).drop(df_rest_with_timestamps.index[0])

    return df_rest_with_timestamps

#%%
        
df = read_aps_data(r'C:\LocalData\sujaiban\sujai.banerji\Aerosol Optical Properties', 20210101, 20210111)
        
#%%