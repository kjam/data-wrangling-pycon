import xlrd


notebook = xlrd.open_workbook('../data/wb/GDP_Current_Dollars.xlsx')

for sheet in notebook.sheets():
    print sheet.name

sheet = notebook.sheet_by_name('Data')

titles = sheet.row_values(0)
print titles


def build_array(sheet, titles, start_row=1):
    new_arr = []
    while start_row < sheet.nrows:
        new_arr.append(
            dict(zip(titles, sheet.row_values(start_row)))
        )
        start_row += 1
    return new_arr


arr = build_array(sheet, titles)

for line in arr:
    print line.get('Country Name'), line.get('2014 [YR2014]')
