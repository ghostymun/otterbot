import os

from requests_html import HTMLSession
from slackclient import SlackClient


class SlackError(Exception):
    pass


session = HTMLSession()

r = session.get("https://dailyotter.org/")

post = r.html.find("h2", first=True)
url = post.absolute_links

d = session.get(list(url)[0])
about = d.html.find("iframe", first=True)

if not about:
    about = d.html.find("img", first=True)

if about.element.tag == "img":
    img = d.html.find("img", first=True)
    text = img.attrs["data-src"]
elif about.element.tag == "iframe":
    iframe = d.html.find("iframe", first=True)
    text = iframe.attrs["src"]

slack_token = os.environ["SLACK_TOKEN"]
sc = SlackClient(slack_token)

resp = sc.api_call(
    "chat.postMessage",
    channel="#random",
    text=text,
    username="Daily Otter",
    icon_emoji=":otter-dance:",
)

if resp["ok"] is False:
    raise SlackError(f"chat.postMessage call failed: {resp['error']}")
