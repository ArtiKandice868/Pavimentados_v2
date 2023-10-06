import numpy as np
import pandas as pd

def total_distance(lat1,lon1,lat2,lon2):
    """
    Calculate the distance between 2 gps points (lat1, lon1) y (lat2, lon2) using Haversine formula.
    """

    R = 6373.0 # approximate radius of earth in km.

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c*1000 #converts the distance to meters
    return distance


def area_calc(boxes,height, base): #pixels
    """
    Calculate the area of the bounding box
    """
    
    if len(boxes)>0:
        return ((boxes[2]-boxes[0])*height)*((boxes[3]-boxes[1])*base)
    else:
        return 0
        

def area_calc_meters(boxes, height, base, factor):
    """
    Calculate the area of the bounding box in square meters.
    """
    if len(boxes) > 0:
        width_pixels = boxes[2] - boxes[0]
        height_pixels = boxes[3] - boxes[1]
        width_meters = width_pixels * factor
        height_meters = height_pixels * factor
        area = width_meters * height * height_meters * base
        return area
    else:
        return 0


def box_center(boxes, height, base): #adjusted from original
    """
    Calculate the center of the bounding box.
    """
    if len(boxes) > 0:
        center_x = (boxes[0] + boxes[2]) / 2
        center_y = (boxes[1] + boxes[3]) / 2
        return center_x * base, center_y * height
    else:
        return None, None


def box_height(boxes,height): #pixels
    """
    Calculate the height of the box
    """
    if len(boxes)>0:
        return ((boxes[2]-boxes[0])*height)
    else:
        return None


def box_width(boxes,base):
    """
    Calculate the width of the box
    """
    if len(boxes)>0:
        return ((boxes[3]-boxes[1])*base)	
    else:
        return None


def fail_id_generator(df, min_photogram_distance):
    """
    Generate a FailID.
    """

    df_id_fails = []
    id_fail = 0
    
    for fail in list(df.classes.unique()):
        df_fail = df.loc[df.classes==fail].copy().reset_index(drop=True)
        frames = df_fail.frame
        id_section_fail = [id_fail]
        
        for i in range(len(frames)-1):
            if (frames[i+1]-frames[i])>min_photogram_distance:
                id_fail +=1
            id_section_fail.append(id_fail)
            
        id_section_fail = np.array(id_section_fail)
        
        if len(id_section_fail)>0:
            df_fail['fail_id_section'] = id_section_fail
            df_id_fails.append(df_fail)
            
    df = pd.concat(df_id_fails).sort_values(['frame','classes','fail_id_section']).reset_index(drop=True)
    
    return df


def stack_columns_dataset(df, variables, static_variables):
    df['ind'] = df.index 
    df_resulting = df[static_variables].copy()
    c = 0
    for v in variables:
        d = pd.DataFrame([[i,t] for  i,T in df[['ind',v]].values for t in T], columns=['ind',v])
        d['ind2'] = d.index
        if c==0:
            df_resulting = pd.merge(df_resulting,d, on='ind', how='left')
            c+=1
        else:
            df_resulting = pd.merge(df_resulting,d, on=['ind','ind2'], how='left')
    return df_resulting	


def assign_group_calculations(df):
    df['area'] = df.width.values*df.distances.values
    df['start_coordinate'] = list(map(lambda x,y: (x,y), df.latitude.values, df.longitude.values))
    df['end_coordenate'] = list(map(lambda x,y: (x,y), df.latitude.values, df.longitude.values))
    df['start_latitude'] = df.latitude
    df['end_latitude'] = df.latitude
    df['start_longitude'] = df.longitude
    df['end_longitude'] = df.longitude
    return df