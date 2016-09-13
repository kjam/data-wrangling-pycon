
MATCHING += (('Julia', '(J|j)ulia'), )

def count_languages():
    stories = get_top_stories()
    final_tallies = {}
    for s in stories:
        long_string = u'{} {}'.format(s.get('title'), s.get('url'))
        for language, regex in dict(MATCHING).items():
            if re.search(regex, long_string):
                if language not in final_tallies.keys():
                    final_tallies[language] = {
                        'score': s.get('score'),
                        'descendants': s.get('descendants'),
                        'urls': [s.get('url')]}
                else:
                    final_tallies[language]['score'] += s.get('score')
                    final_tallies[language][
                        'descendants'] += s.get('descendants')
                    final_tallies[language]['urls'].append(s.get('url'))
    return final_tallies

count_languages()
