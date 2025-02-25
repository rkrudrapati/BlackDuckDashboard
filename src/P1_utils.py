
def sanctify_url(url):
    if 'http' in url and not 'https' in url:
        url.replace('http', 'https')
    if not 'https://' in url:
        url = 'https://' + url
    if url[-1] == '/':
        url = url[:-1]
    return url