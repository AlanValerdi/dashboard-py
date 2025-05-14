# This file is supposed to only load data
import streamlit as st 
import plotly.express as px
import pandas as pd
import numpy as np

@st.cache_resource
def loadData():
    df = pd.read_csv("actions/madrid_spain_Cleansed.csv")
    dfMx = pd.read_csv("actions/México_DesviaciónEstandar_Limpio.csv")
    dfGr = pd.read_csv("actions/Grecia.csv")
    
    # ----------Spain----------
    # select both numeric cols and lists
    numericDf = df.select_dtypes('float', 'int')
    numericCols = numericDf.columns

    # select both string cols and list 
    textDf = df.select_dtypes('object')  
    textCols = textDf.columns

    categoricalHostIsSuperhost = df['host_is_superhost']
    categoricalHostIdentityVerified = df['host_identity_verified']

    # unique values of categories columns, this will be pair to pair with categorical columns
    uniqueValuesHostIsSuperhost = categoricalHostIsSuperhost.unique()
    uniqueValuesHostIdentityVerified = categoricalHostIdentityVerified.unique()

    # ----------Mex----------
    numericDfMx = dfMx.select_dtypes('float', 'int')
    numericColsMx = numericDfMx.columns

    textDfMx = dfMx.select_dtypes('object')  
    textColsMx = textDfMx.columns

    categoricalHostIsSuperhostMx = dfMx['host_is_superhost']
    categoricalHostIdentityVerifiedMx = dfMx['host_identity_verified']

    uniqueValuesHostIsSuperhostMx = categoricalHostIsSuperhostMx.unique()
    uniqueValuesHostIdentityVerifiedMx = categoricalHostIdentityVerifiedMx.unique()

    # ----------Greece----------
    numericDfGr = dfGr.select_dtypes('float', 'int')
    numericColsGr = numericDfGr.columns

    textDfGr = dfGr.select_dtypes('object')  
    textColsGr = textDfGr.columns

    categoricalHostIsSuperhostGr = dfGr['host_is_superhost']
    categoricalHostIdentityVerifiedGr = dfGr['host_identity_verified']

    uniqueValuesHostIsSuperhostGr = categoricalHostIsSuperhostGr.unique()
    uniqueValuesHostIdentityVerifiedGr = categoricalHostIdentityVerifiedGr.unique()

    # ----------------------------------------------------------------------------------------
    # Data operations 

    # ----------Spain----------
    spainTotalValues = df.count().sum()

    # ---------- Correlation Insights (Spain) ----------
    corr_matrix_spain = numericDf.corr()
    corr_unstacked = corr_matrix_spain.where(~np.eye(corr_matrix_spain.shape[0], dtype=bool)).unstack().dropna()

    max_corr = corr_unstacked.idxmax()
    max_corr_val = corr_unstacked.max()

    min_corr = corr_unstacked.idxmin()
    min_corr_val = corr_unstacked.min()

    top_correlations_spain = {
        "max_pair": max_corr,
        "max_value": max_corr_val,
        "min_pair": min_corr,
        "min_value": min_corr_val
    }

    # ----------Mex----------
    mexTotalValues = dfMx.count().sum()

    # ---------- Correlation Insights (Mexico) ----------
    corr_matrix_mex = numericDfMx.corr()
    corr_unstacked_mx = corr_matrix_mex.where(~np.eye(corr_matrix_mex.shape[0], dtype=bool)).unstack().dropna()

    max_corr_mx = corr_unstacked_mx.idxmax()
    max_corr_val_mx = corr_unstacked_mx.max()

    min_corr_mx = corr_unstacked_mx.idxmin()
    min_corr_val_mx = corr_unstacked_mx.min()

    top_correlations_mex = {
        "max_pair": max_corr_mx,
        "max_value": max_corr_val_mx,
        "min_pair": min_corr_mx,
        "min_value": min_corr_val_mx
    }

    # ----------Greece----------
    greeceTotalValues = dfGr.count().sum()

    # ---------- Correlation Insights (Greece) ----------
    corr_matrix_greece = numericDfGr.corr()
    corr_unstacked_gr = corr_matrix_greece.where(~np.eye(corr_matrix_greece.shape[0], dtype=bool)).unstack().dropna()

    max_corr_gr = corr_unstacked_gr.idxmax()
    max_corr_val_gr = corr_unstacked_gr.max()

    min_corr_gr = corr_unstacked_gr.idxmin()
    min_corr_val_gr = corr_unstacked_gr.min()

    top_correlations_greece = {
        "max_pair": max_corr_gr,
        "max_value": max_corr_val_gr,
        "min_pair": min_corr_gr,
        "min_value": min_corr_val_gr
    }

    # ---------- For Card Display ----------
    spDiffVsMex = round(((spainTotalValues - mexTotalValues) / mexTotalValues) * 100, 2)
    mxDiffVsSpain = round(((mexTotalValues - spainTotalValues) / spainTotalValues) * 100, 2)

    # ---------- For Charts display ---------- 
    superHostPieSp = df["host_is_superhost"].value_counts().reset_index()
    superHostPieMx = dfMx["host_is_superhost"].value_counts().reset_index()
    superHostPieGr = dfGr["host_is_superhost"].value_counts().reset_index()

    identityVerifiedPieSp = df["host_identity_verified"].value_counts().reset_index()
    identityVerifiedPieMx = dfMx["host_identity_verified"].value_counts().reset_index()
    identityVerifiedPieGr = dfGr["host_identity_verified"].value_counts().reset_index()

    return {

        # Spain
        "df": df,
        "numericDf": numericDf,
        "numericCols": numericCols,
        "textDf": textDf,
        "textCols": textCols,
        "categoricalHostIdentityVerified": categoricalHostIdentityVerified,
        "categoricalHostIsSuperhost": categoricalHostIsSuperhost,
        "uniqueValuesHostIdentityVerified": uniqueValuesHostIdentityVerified,
        "uniqueValuesHostIsSuperhost": uniqueValuesHostIsSuperhost,
        "spainTotalValues": spainTotalValues,
        "spDiffVsMex": spDiffVsMex,
        "superHostPieSp" : superHostPieSp,
        "identityVerifiedPieSp": identityVerifiedPieSp,
        "top_correlations_spain": top_correlations_spain,

        # Mex
        "dfMx": dfMx,
        "numericDfMx": numericDfMx,
        "numericColsMx": numericColsMx,
        "textDfMx": textDfMx,
        "textColsMx": textColsMx,
        "categoricalHostIdentityVerifiedMx": categoricalHostIdentityVerifiedMx,
        "categoricalHostIsSuperhostMx": categoricalHostIsSuperhostMx,
        "uniqueValuesHostIdentityVerifiedMx": uniqueValuesHostIdentityVerifiedMx,
        "uniqueValuesHostIsSuperhostMx": uniqueValuesHostIsSuperhostMx,
        "mexTotalValues": mexTotalValues,
        "mxDiffVsSpain": mxDiffVsSpain,
        "superHostPieMx": superHostPieMx,
        "identityVerifiedPieMx": identityVerifiedPieMx,
        "top_correlations_mex": top_correlations_mex,

        # Greece
        "dfGr": dfGr,
        "numericDfGr": numericDfGr,
        "numericColsGr": numericColsGr,
        "textDfGr": textDfGr,
        "textColsGr": textColsGr,
        "categoricalHostIdentityVerifiedGr": categoricalHostIdentityVerifiedGr,
        "categoricalHostIsSuperhostGr": categoricalHostIsSuperhostGr,
        "uniqueValuesHostIdentityVerifiedGr": uniqueValuesHostIdentityVerifiedGr,
        "uniqueValuesHostIsSuperhostGr": uniqueValuesHostIsSuperhostGr,
        "greeceTotalValues": greeceTotalValues,
        "superHostPieGr": superHostPieGr,
        "identityVerifiedPieGr": identityVerifiedPieGr,
        "top_correlations_greece": top_correlations_greece,

    }