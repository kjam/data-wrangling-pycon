weather['STATION_NAME'] = weather['STATION_NAME'].map(lambda x: x.replace('BERLIN ', ''))

weather[weather['STATION_NAME'] == 'TEMPELHOF GM']['PRCP'].plot()

weather[weather['STATION_NAME'] == 'TEMPELHOF GM'].reset_index().plot('DATE', 'PRCP', style='g--')
