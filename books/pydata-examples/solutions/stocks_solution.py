from datetime import datetime

ibm = data.DataReader('IBM', 'yahoo', datetime(2007,1, 1), datetime(2016, 1, 1))
ibm['Stock'] = 'IBM'

merged = merged.append(ibm)


lowest_ibm = merged[merged['Stock'] == 'IBM'].sort_values('Close').head(1)
lowest_fb = merged[merged['Stock'] == 'FB'].sort_values('Close').iloc[0]
lowest_goog = merged[merged['Stock'] == 'GOOGL'].sort_values('Close').ix[0]

(lowest_ibm.index, lowest_fb.name, lowest_goog.name)
