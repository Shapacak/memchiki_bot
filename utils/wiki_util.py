from pprint import pprint
from bs4 import BeautifulSoup as BS
import requests

API_URL = 'http://ru.wikipedia.org/w/api.php'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' \
             ' AppleWebKit/537.36 (KHTML, like Gecko)' \
             ' Chrome/99.0.4844.51 Safari/537.36'

def search(query, results=10, suggestion=False):
    search_params = {'list': 'search',
                     'srprop': '',
                     'srlimit': results,
                     'limit': results,
                     'srsearch': query}
    if suggestion:
        search_params['srinfo'] = 'suggestion'

    raw_results = _wiki_request(search_params)

    search_results = (d['title'] for d in raw_results['query']['search'])
    if suggestion:
        if raw_results['query'].get('searchinfo'):
            return list(search_results), raw_results['query']['searchinfo']['suggestion']
        else:
            return list(search_results), None

    return list(search_results)


def suggest(query):
    search_params = {'list': 'search',
                     'srinfo': 'suggestion',
                     'srprop': '',
                     'srsearch': query}

    raw_result = _wiki_request(search_params)

    if raw_result['query'].get('searchinfo'):
        return raw_result['query']['searchinfo']['suggestion']
    return None


def summary(title, auto_suggest=True, redirect=True):
    page_info = page(title)
    title = page_info[1]
    pageid = page_info[0]

    query_params = {
        'prop': 'extracts',
        'explaintext': '',
        'titles': title}

    request = _wiki_request(query_params)
    recived_summary = request['query']['pages'][pageid]['extract']
    return recived_summary


def _wiki_request(params):
    params['format'] = 'json'

    if not 'action' in params:
        params['action'] = 'query'

    headers = {'User-Agent': USER_AGENT}

    r = requests.get(API_URL, params=params, headers=headers)
    return r.json()


def page(title, redirect=True, preload=False):
    query_params = {'prop': 'info|pageprops',
                    'inprop': 'url',
                    'ppprop': 'disambiguation',
                    'redirects': '',
                    'titles': title}

    request = _wiki_request(query_params)

    query = request['query']
    pageid = list(query['pages'].keys())[0]
    recived_page = query['pages'][pageid]

    if 'missing' in recived_page:
        print('ну ебать')
        return
    elif 'redirects' in query:
        if redirect:
            redirects = query['redirects'][0]

            if 'normalized' in query:
                normalized = query['normalized'][0]
                assert normalized['from'] == title
                from_title = normalized['to']
            else:
                from_title = title
            assert redirects['from'] == from_title
            page(redirects['to'], redirect=redirect, preload=preload)
        else:
            print('вообще пиздец')
            return

    elif 'pageprops' in recived_page:
        query_params = {'prop': 'revisions',
                        'rvprop': 'content',
                        'rvparse': '',
                        'rvlimit': 1}
        if hasattr(recived_page, 'pageid'):
            query_params['pageids'] = pageid
        else:
            query_params['titles'] = title
        request = _wiki_request(query_params)
        html = request['query']['pages'][pageid]['revisions'][0]['*']

        lis = BS(html, 'html.parser').find_all('li')
        filtered_lis = [li for li in lis if not 'tocsection' in ''.join(li.get('class', []))]
        may_refer_to = [li.a.get_text() for li in filtered_lis if li.a]

        print('пизда')
        return may_refer_to
    else:
        return [pageid, recived_page['title'], recived_page['fullurl']]

