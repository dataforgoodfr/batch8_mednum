from functools import wraps
import numpy as np
import pandas as pd
import unicodedata
from pathlib import Path

def strip_accents(s):
    if s is None:
        s = ''
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


def reduce_mem_usage(props, to_cat = 150):
    start_mem_usg = props.memory_usage().sum() / 1024**2 
    print("Memory usage of properties dataframe is :",start_mem_usg," MB")
    NAlist = [] # Keeps track of columns that have missing values filled in. 
    for col in props.columns:
        print(col)
        if props[col].dtype != object:  # Exclude strings
            
            # Print current column type
            print("******************************")
            print("Column: ",col)
            print("dtype before: ",props[col].dtype)
            
            # make variables for Int, max and min
            try:
                IsInt = False
                mx = props[col].max()
                mn = props[col].min()

                # Integer does not support NA, therefore, NA needs to be filled
                if not np.isfinite(props[col]).all(): 
                    NAlist.append(col)
                    props[col].fillna(mn-1,inplace=True)  

                # test if column can be converted to an integer
                asint = props[col].fillna(0).astype(np.int64)
                result = (props[col] - asint)
                result = result.sum()
                if result > -0.01 and result < 0.01:
                    IsInt = True


                # Make Integer/unsigned Integer datatypes
                if IsInt:
                    if mn >= 0:
                        if mx < 255:
                            props[col] = props[col].astype(np.uint8)
                        elif mx < 65535:
                            props[col] = props[col].astype(np.uint16)
                        elif mx < 4294967295:
                            props[col] = props[col].astype(np.uint32)
                        else:
                            props[col] = props[col].astype(np.uint64)
                    else:
                        if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                            props[col] = props[col].astype(np.int8)
                        elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                            props[col] = props[col].astype(np.int16)
                        elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                            props[col] = props[col].astype(np.int32)
                        elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                            props[col] = props[col].astype(np.int64)    

                # Make float datatypes 32 bit
                else:
                    props[col] = props[col].astype(np.float32)
            except Exception as e:
                print(e)
                continue
        else:
            n_val = props[col].nunique()
            if to_cat > n_val:
                props[col] = props[col].astype("category")
        # Print new column type
        print("dtype after: ",props[col].dtype)
        print("******************************")
    
    # Print final result
    print("___MEMORY USAGE AFTER COMPLETION:___")
    mem_usg = props.memory_usage().sum() / 1024**2 
    print("Memory usage is: ",mem_usg," MB")
    print("This is ",100*mem_usg/start_mem_usg,"% of the initial size")
    return props, NAlist

def cache_pandas_result(cache_dir, hard_reset: bool, geoformat=False):
    '''
    This decorator caches a pandas.DataFrame returning function.
    It saves the pandas.DataFrame in a parquet file in the cache_dir.
    It uses the following naming scheme for the caching files:
        cache_dir / function_name + '.trc.pqt'
    Parameters:
    cache_dir: a pathlib.Path object
    hard_reset: bool
    '''
    def build_caching_function(func):
        @wraps(func)
        def cache_function(*args, **kwargs):
            if not isinstance(cache_dir, Path):
                raise TypeError('cache_dir should be a pathlib.Path object')

            cache_file = cache_dir / (func.__name__ + '.trc.pqt')

            if hard_reset or (not cache_file.exists()):
                result = func(*args, **kwargs)
                if not isinstance(result, pd.DataFrame):
                    raise TypeError(f"The result of computing {func.__name__} is not a DataFrame")
                result.to_parquet(cache_file)
                return result
            print("{} exist".format(cache_file.name))
            if geoformat:
                import geopandas as gpd
                result = gpd.read_parquet(cache_file)
            else:
                result = pd.read_parquet(cache_file)
            return result
        return cache_function
    return build_caching_function


def css2dict(css_str):
    css_style = {}
    lines = css_str.split("\n")
    css_clean = [line for line in lines if line.strip() != ""]
    for style in css_clean.replace(';','').split('\n'):
        if style:
            try:
                k,v = style.split(':')
                css_style[k]=v
            except Exception as e:
                print(e)
                print(style)
                pass
    return css_style
