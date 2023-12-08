'''
Find a 'scrappable' cryptocurrencies website where you can scrape the top 5 cryptocurrencies 
and display as a formatted output one currency at a time. 
The output should display the name of the currency, the symbol (if applicable), 
the current price and % change in the last 24 hrs and corresponding price (based on % change)
Furthermore, for Ethereum, the program should alert you via text if the value gets above $2,000 
'''
from twilio.rest import Client
import keys
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = 'https://crypto.com/price'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers = headers)
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, 'html.parser')

table_rows = soup.findAll("tr")

for x in range(1,6):
    td = table_rows[x].findAll("td")
    name = td[2].text
    currentprice = float(td[3].text.split('$')[1].strip().replace(',', ''))
    percentchange = float(td[4].text.strip().replace('%', '')) / 100
    prevprice = currentprice - currentprice * percentchange
    percentvalue = float(td[4].text.strip().replace('%', ''))
    
    print(f'Currency Name: {name}')
    print(f'Current Price: ${currentprice:.2f}')
    print(f'Change in last 24 hours: {percentvalue:.2f}%')
    print(f'Previous Price: ${prevprice:.2f}')
    
    if name == 'EEthereumETH' and currentprice > 2000:
            client = Client(keys.accountSID, keys.authToken)
            TwilioNumber = "+18449683396"
            myCellPhone = '+14252395071'
            msg = "Ethereum price is above $2,000."
            txtmsg = client.messages.create(to = myCellPhone, from_ = TwilioNumber, body = msg)
            print('Notifictaion sent')
    input()
