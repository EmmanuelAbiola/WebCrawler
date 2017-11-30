import urllib2
import urlparse
import httplib
from BeautifulSoup import BeautifulSoup

baseUrl = "http://tomblomfield.com/"

urlStack = {baseUrl}  # stack to scrape
indexed = {baseUrl}  # previously indexed

f = open('sitemap.xml', 'w')
f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
while len(urlStack) > 0:
    
    currentURL = urlStack.pop()
    
    request = urllib2.Request(currentURL)
    
    try:
        rawHtml = urllib2.urlopen(request).read()
    except urllib2.HTTPError, e:
        print('HTTPError = ' + str(e.code))
    except urllib2.URLError, e:
        print('URLError = ' + str(e.reason))
    except httplib.HTTPException, e:
        print('HTTPException')
    except Exception:
        import traceback
        
        print('generic exception: ' + traceback.format_exc())

soup = BeautifulSoup(rawHtml)
    
    print len(urlStack)
    
    for link in soup.findAll('a', href=True):
        link['href'] = urlparse.urljoin(baseUrl, link['href'])
        if baseUrl in link['href'] and link['href'] not in indexed:
            urlStack.add(link['href'])
            indexed.add(link['href'])
            f.write('<url>\n')
            f.write('<loc>')
            f.write(link['href'])
            f.write('</loc>\n')
            print link['href']
            f.write('</url>\n')


print indexed
f.write('</urlset>\n')
f.close()
