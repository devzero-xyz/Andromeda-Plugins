"""By Bowserinator: Insults people :D"""

from utils import add_cmd, add_handler
import utils
import random

name = "insult"
cmds = ["insult"]

insultPattern = [
    "That [REPLACE] just cut me off!",
    "My boss is a major [REPLACE]!",
    "Don't tell her I said this, but that dude she's with is a real [REPLACE]!",
    "Quit being such a [REPLACE]!",
    "The only people who would vote for that guy are total [REPLACE]s!",
    "What are you, some kind of [REPLACE]?",
    "Dude's a real [REPLACE], you know what I mean?",
    "He's got an ego like a [REPLACE]!",
    "She was being a real [REPLACE] at the store today!",
    "That [REPLACE] developer's code refuses to compile!",
    "Her kids are total [REPLACE]s!",
    "Whoever wrote this API documentation is a complete [REPLACE]!",
    "That guy has the personality of a [REPLACE]!",
    "I'm pretty sure I was a total [REPLACE] at the bar last night.",
    "What kind of [REPLACE] buys pre-ground coffee?",
    "I'd rather get a [REPLACE] to the eye than sit through this lecture.",
    "Wow, that [REPLACE] just went off the deep end.",
    "I may be a jerk, but at least I'm not like that [REPLACE] over there.",
    "I need that like I need a [REPLACE] on my elbow.",
    "What kind of [REPLACE] slows down to merge on the highway?",
    "You've got a face like a [REPLACE].",
    "Nothing personal, but you're a real [REPLACE].",
    "What a bunch of [REPLACE]s.",
    "That [REPLACE] is legally dead in 27 states - plus Guam.",
]

badwords = [
    'Ass',
    'Bitch',
    'Butt',
    'Cock',
    'Cum',
    'Cunt',
    'Dick',
    'Douche',
    'Fart',
    'Fuck',
    'Jizz',
    'Schlong',
    'Shit',
    'Slut',
    'Snatch',
    'Tit',
    'Twat',
    'Wang',
    'Wank',
    'Whore',
]

@add_cmd
def insult(irc, event, args):
  send = "\x02" + args[0] +", \x0f" + random.choice(insultPattern).replace("[REPLACE]",random.choice(badwords).lower())
  irc.reply(event, send)
  
add_handler(insult, name)
