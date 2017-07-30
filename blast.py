from mastodon import Mastodon
import tracery
from tracery.modifiers import base_english
import json
import sys
import getopt
from html.parser import HTMLParser

#init mastodon
mastodon = Mastodon(
  #replace values/files with your own
  client_id = 'blast_clientcred.secret',
  access_token = 'blast_usercred.secret',
  api_base_url = 'https://botsin.space'
)

#init tracery
with open('names.json') as rules_file:
  rules = json.load(rules_file)
grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)

#init html parser
class MLStripper(HTMLParser):
  def __init__(self):
    super().__init__()
    self.reset()
    self.strict = False
    self.convert_charrefs= True
    self.fed = []
  def handle_data(self, d):
    self.fed.append(d)
  def get_data(self):
    return ''.join(self.fed)

def strip_tags(html):
  s = MLStripper()
  s.feed(html)
  return s.get_data()

def usage():
  print('usage:')
  print('-t, --toot: toots a name')
  print('-r, --reply: replies to mentions')
  print('-p, --print: prints name to console')
  
def blast_hardcheese():
  return grammar.flatten("#origin#")

def toot():
  mastodon.toot(blast_hardcheese())

def console():
  print(blast_hardcheese())

def reply():
  #get nofitications
  try:
    notifs = mastodon.notifications()
  except (KeyError):
    return
  #filter mentions
  mentions = list(filter(lambda x: x['type'] == 'mention', notifs))
  #iterate over them
  for status in mentions:
    msg = strip_tags(status['status']['content'])
    if 'name' in msg.lower():
      acct = status['status']['account']['acct']
      id = status['status']['id']
      toot = ''.join(['@', acct, ' ', blast_hardcheese()])
      print(toot)
      mastodon.status_post(toot, in_reply_to_id=id)
  #clear notifications
  mastodon._Mastodon__api_request('POST', '/api/v1/notifications/clear')

def main(argv):
  try:                                
    opts, args = getopt.getopt(argv, "trp", ["toot", "reply", "print"])
  except getopt.GetoptError:          
    usage()                         
    sys.exit(2)
  for opt, arg in opts:
    if opt in ('-t','--toot'):
      toot()
    elif opt in ('-r','--reply'):
      reply()
    elif opt in ('-p','--print'):
      console()

if __name__ == "__main__":
    main(sys.argv[1:])