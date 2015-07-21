import pygal
from csv import DictReader


def load_imf_unemployment():
    rdr = DictReader(open('../data/imf_indicators.tsv', 'rb'), delimiter='\t')
    return [r for r in rdr if r.get('Subject Descriptor') and
            'Unemployment' in r.get('Subject Descriptor')]


def load_iso_codes():
    iso_dict = {}
    for row in DictReader(open('../data/iso-2.csv', 'rb')):
        iso_dict[row.get('Name')] = row.get('Code')
    return iso_dict


def load_and_merge_data():
    iso_dict = load_iso_codes()
    imf_data = load_imf_unemployment()
    for d in imf_data:
        d['iso'] = iso_dict[d.get('Country')]
    return imf_data


def draw_unemployment():
    imf_data = load_and_merge_data()
    worldmap_data = {}
    for row in imf_data:
        worldmap_data[row.get('iso').lower()] = float(row.get('2015'))
    worldmap_chart = pygal.Worldmap()
    worldmap_chart.title = '2015 Unemployment'
    worldmap_chart.add('Total Unemployment (%)', worldmap_data)
    worldmap_chart.render()
