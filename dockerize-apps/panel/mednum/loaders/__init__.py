
from pathlib import Path

import geopandas as gpd
import pandas as pd

from mednum.tools import cache_pandas_result, strip_accents

hard_reset = False
data_path = Path("../data")

if not data_path.exists():
    data_path = Path("./data")

interim_data = data_path / "interim/"
cache_dir = interim_data


@cache_pandas_result(cache_dir, hard_reset=hard_reset, geoformat=True)
def iris_df(cont_iris):
    cont_iris_df = gpd.read_file(cont_iris)
    cont_iris_df.nom_dep = cont_iris_df.nom_dep.str.title().apply(strip_accents)
    cont_iris_df.nom_reg = cont_iris_df.nom_reg.str.title().apply(strip_accents)
    return cont_iris_df


@cache_pandas_result(cache_dir, hard_reset=hard_reset, geoformat=True)
def get_regions_df(regions):
    reg_df = gpd.read_file(regions) #.with_suffix(".parquet"))
    reg_df.nom = reg_df.nom.str.title().apply(strip_accents)
    return reg_df


@cache_pandas_result(cache_dir, hard_reset=hard_reset, geoformat=True)
def get_dept_df(dept):
    dept_df = gpd.read_file(dept) #.with_suffix(".parquet"))
    dept_df.nom = dept_df.nom.str.title().apply(strip_accents)
    return dept_df


@cache_pandas_result(cache_dir, hard_reset=hard_reset, geoformat=False)
def get_indice_frag(indice_frag):
    ifrag_df = pd.read_csv(indice_frag, sep=";", decimal=",")
    return ifrag_df


@cache_pandas_result(cache_dir, hard_reset=hard_reset, geoformat=False)
def get_indice_frag_pivot(ifrag_df):
    ifrag_df_pivot = ifrag_df.pivot(
        index=[
            "Code Iris",
            "Nom Com",
            "Nom Iris",
            "Classement de SCORE GLOBAL region 1",
        ],
        columns="Noms de mesures",
        values=["Valeurs de mesures"],
    )
    ifrag_df_pivot.columns = ifrag_df_pivot.columns.droplevel(0)
    ifrag_df_pivot = ifrag_df_pivot.rename_axis(None, axis=1)
    ifrag_df_pivot.reset_index(inplace=True)
    ifrag_df_pivot.rename(
        {"Nom Com": "nom_com", "Code Iris": "code_iris", "Nom Iris": "nom_iris"},
        axis=1,
        inplace=True,
    )
    return ifrag_df_pivot


@cache_pandas_result(cache_dir, hard_reset=hard_reset, geoformat=True)
def get_merged_iris_data(cont_iris_df, ifrag_df_pivot):
    ifrag_cont_df_merged = pd.merge(
        cont_iris_df, ifrag_df_pivot, on=["code_iris", "nom_com", "nom_iris"]
    )
    return ifrag_cont_df_merged
    