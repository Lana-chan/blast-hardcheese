from mastodon import Mastodon
import tracery
from tracery.modifiers import base_english
import json

with open('names.json') as rules_file:
  rules = json.load(rules_file)
  
grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
msg = grammar.flatten("#origin#")

mastodon = Mastodon(
    client_id = 'blast_clientcred.secret',
    access_token = 'blast_usercred.secret',
    api_base_url = 'https://botsin.space'
)

mastodon.toot(msg)