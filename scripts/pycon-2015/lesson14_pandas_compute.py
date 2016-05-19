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


def get_gdp():
    return pd.read_excel('../data/wb/GDP_Current_Dollars.xlsx',
                         index_col=3, header=0)


def clean_market_columns():
    market_data = get_wb_market_data()
    market_data.columns = market_data.columns.map(lambda x: x[:3])
    market_data.index = market_data.index.map(lambda x: '{} SM'.format(x))
    return market_data.transpose()


def update_gdp_cols(colname):
    if colname[:4].isdigit():
        return '{} GDP'.format(colname[:4])
    return colname


def join_market_and_gdp():
    market_data = clean_market_columns()
    gdp_data = get_gdp()
    gdp_data.columns = gdp_data.columns.map(update_gdp_cols)
    return market_data.join(gdp_data)


def just_spain():
    joined = join_market_and_gdp()
    spain = joined.loc['ESP'].copy()
    spain_gdp = spain[spain.index.map(lambda x: 'GDP' in x)]
    spain_stock = spain[spain.index.map(lambda x: 'SM' in x)]
    spain_gdp.index = spain_gdp.index.map(lambda x: x.rstrip(' GDP'))
    spain_stock.index = spain_stock.index.map(lambda x: x.rstrip(' SM'))
    spain_stock.name = 'Stocks'
    spain_gdp.name = 'GDP'
    return spain_stock, spain_gdp


def merge_back():
    spain_stock, spain_gdp = just_spain()
    return pd.concat([spain_stock, spain_gdp], axis=1)
