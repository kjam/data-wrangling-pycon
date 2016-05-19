from bokeh.plotting import figure, show, output_file
from csv import DictReader


def load_imf_unemployment():
    rdr = DictReader(open('../data/imf_indicators.tsv', 'rb'), delimiter='\t')
    return [r for r in rdr if r.get('Subject Descriptor') and
            'Unemployment' in r.get('Subject Descriptor')]


def mscatter(chart, x, y, typestr):
    chart.scatter(x, y, marker=typestr, line_color="#6666ee",
                  fill_color="#ee6666", fill_alpha=0.5, size=12)


def draw_scatter():
    chart = figure(title="IMF Unemployment")
    output_file("../../static/unemployment.html")
    imf_data = load_imf_unemployment()
    for line in imf_data:
        for year in ['2013', '2014', '2015']:
            mscatter(chart, int(year), float(line.get(year)), 'circle')
    show(chart)
