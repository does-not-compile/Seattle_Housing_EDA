import pandas as pd
import numpy as np
import plotly.express as px

def read_csv(fp: str) -> pd.DataFrame:
    return _clean_df(pd.read_csv(fp))

def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """cleans the King County Housing data.
    CAUTION: THIS IS NOT A GENERALIZED FUNCTION!
    It works only with the dataframe provided during the neuefische DS Bootcamp!
    """
    # type date column as datetime object
    df['date'] = pd.to_datetime(df['date'], format="%m/%d/%Y").dt.date
    # type sqft_basement as numeric (will be float, because has NaNs)
    df['sqft_basement'] = pd.to_numeric(df['sqft_basement'], errors='coerce')
    df['sqft_basement'] = df['sqft_basement'].replace(np.nan, 0)
    # replace 0 with np.nan in yr_renovated (there are only few places renovated)
    df['yr_renovated'] = df['yr_renovated'].replace(0, np.nan)

    return df

def recommendations(df: pd.DataFrame, filter: dict, specialBool: dict) -> pd.DataFrame:
    """Returns a filtered pandas DataFrame based on a filter dictionary.

    Args:
        df (pd.DataFrame)
        filter (dict): Keys have to match column names of df. Values can have the following datatypes:
            1. Tuple: Interpreted as range (lower, upper). Boundaries are included.
            2. List:  Items are used to check for item is in df[key] == true
            3. Single value: Returns rows with column = key matching value.
            4. Booleans: checks for booleans in column = key
        specialBool (dict): Dictionary indicating custom values for pairs of {key: (True, False)}

    Returns:
        pd.DataFrame: Filtered DataFrame
    """
    print('---')
    for key, val in filter.items():

        # single values of type string, integer, or float indicate simple matching
        if type(val) == str or type(val) == int or type(val) == float: 
            df = df[df[key] == val]

        # tuples indicate a range (can only have length of 2!)
        elif type(val) == tuple and len(val) == 2:
            print(f'backend.recommendations(): Filtering {key} for values between {val[0]} and {val[1]}')
            df = df[df[key].between(val[0], val[1])]

        # lists indicate multiple matches allowed
        elif type(val) == list and len(val) > 0:
            print(f'backend.recommendations(): Filtering {key} for {val}')
            df = df[df[key].isin(val)]

        # booleans to check for True/False or Has/Has not (or other custom binary values)
        elif type(val) == bool:
            print(f'backend.recommendations(): Filtering {key} for {val} values.')
            if type(df[key]) == bool: 
                df = df[df[key] == val]
            
            # can also be used to check if value is not null or use customized booleans
            else: 
                print(f" --> received boolean for key '{key}', but '{key}' is not a boolean. Will instead check for specialBool for '{key}'.")
                if key in specialBool.keys():

                    # if two values given, assign true and false
                    if len(specialBool[key]) == 2:
                        print(f" --> specialBool: True = {specialBool[key][0]}, False = {specialBool[key][1]}")
                        print(f" --> Value given: {val}")
                        if val: df = df[df[key] == specialBool[key][0]]
                        else: df = df[df[key] == specialBool[key][1]]
                    # if only one value given, assume it is the False value
                    else:
                        print(f" --> specialBool: True  = 'not {specialBool[key][0]}', False = '{specialBool[key][0]}'")
                        print(f" --> Value given: {val}")
                        if val: 
                            print(f" --> Looking for: not {specialBool[key][0]}")
                            df = df[df[key] != specialBool[key][0]]
                        else: 
                            print(f" --> Looking for: {specialBool[key][0]}")
                            df = df[df[key] == specialBool[key][0]]
                else:
                    print(f" --> No specialBool found for '{key}'. Skipping filterting.")

    print('---')
    return df.reset_index()

def plot(df: pd.DataFrame, size: tuple = (800, 600)) -> px.scatter_mapbox:
    """Returns a plotly object with geographical data.

    Args:
        df (pd.DataFrame): Has to contain columns "lat" and "long" with latitudes and longitudes
        size (tuple):      Tuple giving width and height of returned plot in pixels. Default is (600, 600).

    Returns:
        plotly scatter_mapbox: Map with plotted data
    """
    fig = px.scatter_mapbox(df, lat="lat", lon="long", hover_name="id", hover_data=["price", "zipcode"],
                        color_discrete_sequence=["blue"], zoom=8.8, width=size[0], height=size[1])
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig