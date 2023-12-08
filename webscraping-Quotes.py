from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from plotly.graph_objs import Bar
from plotly import offline

originurl = 'http://quotes.toscrape.com/page/'
def quotesbypage(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url, headers=headers)
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    
    quotes = soup.select('.quote')
    data = {
        "quotes": [],
        "authors": {},
        "tags": {}
    }
    
    for quote in quotes:
        author = quote.select_one('.author').get_text()
        data["authors"][author] = data["authors"].get(author, 0) + 1
        text = quote.select_one('.text').get_text()
        tags = [tag.get_text() for tag in quote.select('.tag')]
        data["quotes"].append({
            "author": author,
            "text": text,
            "length": len(text.split()),  # Length of quote in terms of words
            "tags": tags,
        })

        for tag in tags:
            data["tags"][tag] = data["tags"].get(tag, 0) + 1
    
    return data

quotecount = {}
totallength = 0
numquotes = 0
totaltags = {}

for page in range(1, 11):
    url = originurl + str(page)
    pagedata = quotesbypage(url)
    
    for author, count in pagedata['authors'].items():
        quotecount[author] = quotecount.get(author, 0) + count

    totallength += sum(quote["length"] for quote in pagedata["quotes"])
    numquotes += len(pagedata["quotes"])

    for tag, count in pagedata["tags"].items():
        totaltags[tag] = totaltags.get(tag, 0) + count

mostquotes = max(quotecount, key=quotecount.get)
leastquotes = min(quotecount, key=quotecount.get)

averagequotelength = totallength / numquotes

longest_quote = max(pagedata["quotes"], key=lambda x: x["length"])
shortest_quote = min(pagedata["quotes"], key=lambda x: x["length"])
common_tag = max(totaltags, key=totaltags.get)

print(f'Author with the most quotes: {mostquotes} ({quotecount[mostquotes]})')
print(f'Author with the least quotes: {leastquotes} ({quotecount[leastquotes]})')
print(f'Average length:: {averagequotelength:.2f} words')
print(f'The longest quote is {longest_quote["length"]} words')
print(f'The shortest quote is {shortest_quote["length"]} words')
print(f'The most common tag is "{common_tag}"')
print(f'Total number of tags: {sum(totaltags.values())}')

top_authors_data = sorted(quotecount.items(), key=lambda x: x[1], reverse=True)[:10]
top_author_names, top_author_quotes = zip(*top_authors_data)

authordata = [
    {
        "type": "bar",
        "x": top_author_names,
        "y": top_author_quotes,
        "marker": {
            "color": "rgb(255,192,203)",
            "line": {"width": 1.5, "color": "rgb(255,255,255)"},
        },
        "opacity": .8,
    }
    ]

top_authors_layout = {
    "title": "Top 10 Authors and their Quotes", 
    "xaxis": {"title": "Authors"}, 
    "yaxis": {"title": "Number of Quotes"}
    }

top_authors_fig = {"data": authordata, "layout": top_authors_layout}

offline.plot(top_authors_fig, filename='top_authors_quotes.html')

top_tags_data = sorted(totaltags.items(), key=lambda x: x[1], reverse=True)[:10]
top_tag_names, top_tag_counts = zip(*top_tags_data)

tagdata = [
    {
        "type": "bar",
        "x": top_tag_names,
        "y": top_tag_counts,
        "marker": {
            "color": "rgb(255,192,203)",
            "line": {"width": 1.5, "color": "rgb(255,255,255)"},
        },
        "opacity": .8,
    }
    ]

top_tags_layout = {
    "title": "Top 10 Tags", 
    "xaxis": {"title": "Tags"}, 
    "yaxis": {"title": "Number of Tags"}
    }

top_tags_fig = {"data": tagdata, "layout": top_tags_layout}

offline.plot(top_tags_fig, filename='top_tags.html')
