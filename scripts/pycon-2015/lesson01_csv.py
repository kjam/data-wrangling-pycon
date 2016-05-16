from csv import DictReader


rdr = DictReader(open('../data/imf_indicators.tsv', 'rb'), delimiter='\t')

all_lines = [r for r in rdr]

print all_lines[0].keys()

for line in all_lines:
    try:
        if 'Gross domestic product' in line.get('Subject Descriptor') and \
           'international dollar' in line.get('Units'):
            print '{}: {} ({} {})'.format(
                line.get('Country'), line.get('2015'), '2015', line.get('Scale'))
    except:
        print "ERROR: ", line
