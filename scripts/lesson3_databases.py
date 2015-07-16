import dataset

db = dataset.connect('sqlite:///../data/data_analysis.db')

my_sources = db['sources']

my_sources.insert({'organization': 'IMF',
                   'file_name': 'imf_indicators.tsv',
                   'url': 'http://www.imf.org/external/pubs/ft/weo/2015/01/weodata/index.aspx',
                   'description': 'IMF World Economic Outlook Dataset',
                   })

my_sources.insert({'organization': 'World Bank',
                   'file_name': 'wb/GDP_Current_Dollars.xlsx',
                   'url': 'http://databank.worldbank.org/data/reports.aspx?source=2&series=NY.GDP.MKTP.CD#',
                   'description': 'World Bank GDP Dataset',
                   })

print db.tables

for row in db['sources']:
    print row['description']
