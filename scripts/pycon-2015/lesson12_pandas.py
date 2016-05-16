import pandas as pd


def get_wb_unemployment_data():
    return pd.read_excel('../data/wb/unemployment.xlsx',
                         index_col=0, header=0, skiprows=[1])


def get_wb_market_data():
    return pd.read_excel('../data/wb/stock_market.xlsx',
                         index_col=0, header=0, skiprows=[1])


def get_metadata():
    return pd.read_excel('../data/wb/stock_metadata.xlsx',
                         sheetname=1, index_col=0, header=0)
