import journalism
import logging
from csv import reader

text_type = journalism.TextType()
number_type = journalism.NumberType()
date_type = journalism.DateType()


def get_table(datarows, types, titles):
    try:
        table = journalism.Table(datarows, types, titles)
        return table
    except:
        logging.exception('problem loading table')
    return None


def clean_text(row):
    new_row = []
    for item in row:
        if isinstance(item, (str, unicode)):
            item = item.decode('utf-8', 'replace')
        if item in [u'--', u'n/a']:
            item = None
        new_row.append(item)

    return new_row


def clean_rows(all_rows):
    new_data = []
    for row in all_rows:
        new_data.append(clean_text(row))
    return new_data


def load_imf_data():
    rdr = reader(open('../data/imf_indicators.tsv', 'rb'), delimiter='\t')
    all_rows = [r for r in rdr if len(r) > 1]
    titles = all_rows.pop(0)
    cleaned_rows = clean_rows(all_rows)
    types = [text_type, text_type, text_type, text_type, text_type,
             number_type, number_type, number_type, number_type,
             number_type, number_type, number_type, number_type,
             date_type]
    return get_table(cleaned_rows, types, titles)


def add_last_percent_change():
    table = load_imf_data()
    table = table.where(lambda r: r.get('2015') is not
                        None and r.get('2014') is not None)
    table = table.where(lambda r: 'Unemployment' in
                        r.get('Subject Descriptor'))
    table = table.percent_change('2014', '2015', 'last_change')
    return table
