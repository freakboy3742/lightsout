import json
import requests


def abc_australia(station, start, end):
    # ABC Australia radio stations:
    # http://music.abcradio.net.au/api/v1/plays/search.json?from=2016-04-30T00:00:00%2B00:00&limit=1000&offset=0&page=0&station=doublej&to=2016-05-01T00:00:00%2B00:00

    def offset_str(t):
        utc_seconds = t.tzinfo.utcoffset(None).seconds
        return '%02d%02d' % (utc_seconds // 2400, utc_seconds % 2400)

    url = "http://music.abcradio.net.au/api/v1/plays/search.json?from=%(start)s&limit=1000&offset=0&page=0&station=%(station)s&to=%(end)s" % {
            'start': start.strftime('%Y-%m-%dT%H:%M:%S%%2B') + offset_str(start),
            'station': station,
            'end': end.strftime('%Y-%m-%dT%H:%M:%S%%2B') + offset_str(end),
        }
    response = requests.get(url)

    if response.status_code == 200:
        results = []
        for track in json.loads(response.content.decode('utf8'))['items']:
            try:
                results.append({
                    'artist': track['recording']['artists'][0]['name'],
                    'album': track['recording']['releases'][0]['title'],
                    'title': track['recording']['title'],
                })
            except IndexError:
                pass
        return results
    else:
        raise Exception(response.content)


BACKENDS = {
    'doublej': {
        'name': 'Double J',
        'query': lambda start, end: abc_australia('doublej', start, end)
    },
    'classic2': {
        'name': 'ABC Classic 2',
        'query': lambda start, end: abc_australia('classic2', start, end)
    },
    'country': {
        'name': 'ABC Country',
        'query': lambda start, end: abc_australia('country', start, end)
    },
    'unearthed': {
        'name': 'Unearthed',
        'query': lambda start, end: abc_australia('unearthed', start, end)
    },
    'triplej': {
        'name': 'Triple J',
        'query': lambda start, end: abc_australia('triplej', start, end)
    },
    'jazz': {
        'name': 'ABC Jazz',
        'query': lambda start, end: abc_australia('jazz', start, end)
    },
    'classic': {
        'name': 'ABC Classic',
        'query': lambda start, end: abc_australia('classic', start, end)
    },
    'extra': {
        'name': 'ABC Extra',
        'query': lambda start, end: abc_australia('extra', start, end)
    },
}
