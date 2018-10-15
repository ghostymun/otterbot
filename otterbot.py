from requests_html import HTMLSession
from slackclient import SlackClient
import os

session = HTMLSession()

r = session.get('https://dailyotter.org/')

img = r.html.find('div', first=True)
text = 'https://dailyotter.org/'+img.attrs['href']

# if "thumbnail" in thing.attrs['class']:
#     text = 'https://dailyotter.org/'+thing.attrs['href']

# else:
#     img = r.html.find('img', first=True)
#     text = img.attrs['data-src']

slack_token = os.environ['SLACK_TOKEN']
sc = SlackClient(slack_token)

sc.api_call(
    "chat.postMessage",
    channel="#random",
    text=text,
    username="Daily Otter",
    icon_emoji=":otter-dance:"
    )
