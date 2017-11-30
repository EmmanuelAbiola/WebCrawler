from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

parentlink = {}

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    if newUrl != self.baseUrl:
                        self.links = self.links + [newUrl]

    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if 'text/html' in response.getheader('Content-Type'):
            htmlBytes = response.read()
            htmlString = htmlBytes.decode("utf-8")
            self.feed(htmlString)
            return htmlString, self.links
        else:
            print(response.getheader('Content-Type'))
            return "",[]

def spider(url, word, maxPages):
    pagesToVisit = [url]
    alllinks = []
    parentlink[url] = -1
    numberVisited = 0
    foundWord = False
    while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
        numberVisited = numberVisited +1
        url = pagesToVisit[0]
        pagesToVisit = pagesToVisit[1:]
        try:
            # print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data, links = parser.getLinks(url)
            alllinks = alllinks+[url]
            links = list(set(links) - set(alllinks))
            pagesToVisit = pagesToVisit + links
            for x in links:
                parentlink[x] = url
            if data.find(word)>-1:
                foundWord = True
                print(" **Success!**")
        except Exception as e :
            print(" **Failed!**",e)
    if foundWord:
        print("The word", word, "was found at", url)
        print("The Path taken is", url)
        while parentlink[url]!=-1:
            print(parentlink[url],"<-")
            url = parentlink[url]
        # print(data)
    else:
        # print(parentlink)
        print("Word never found")

s = input("Search for?\n")
# s = " " + s + " "
spider("http://tomblomfield.com/",s,10)
