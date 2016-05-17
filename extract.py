"""This plugin extracts the main content of a webpage"""
"""e.g. extracting the article of a url of bbc.co.uk"""

from utils import add_cmd, add_handler
import utils
import requests
from bs4 import BeautifulSoup

name = "extract"
cmds = ["extract"]

def main(irc):
	if name not in irc.plugins.keys():
		irc.plugins[name] = {}

@add_cmd
def extract(irc, event, args):
	try:
		html = requests.get(args[0]).text
		soup = BeautifulSoup(html)
		for script in soup(["script", "style"]):
		    script.extract()
		text = soup.get_text()
		lines = (line.strip() for line in text.splitlines())
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		text = '\n'.join(chunk for chunk in chunks if chunk)
		text = text.encode('ascii', 'ignore')
		irc.reply(event, (text[:350] + '..') if len(text) > 350 else text)
	except IndexError:
		irc.reply(event, utils.gethelp("extract"))
	except:
		irc.reply(event, "Error extracting informations")


add_handler(extract, name)