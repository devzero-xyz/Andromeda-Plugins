from utils import add_cmd
import utils
import threading
import random
import time

name = "timebomb"
cmds = ["timebomb", "cut"]

def main(irc):
    if not name in irc.plugins.keys():
        irc.plugins["timebomb"] = {"exempts": [], "idle": 300}
        
    for channel in irc.channels.keys():
        if "timebomb" not in irc.channels[channel].keys():
            irc.channels[channel]["timebomb"] = {"disabled": True, "active": {}, "limit": 1}

def kick(irc, target, channel, noRemove=False):
    prepare_nicks = []
    reason = "BOOM"
    nicks = [target]

    already_op = irc.is_opped(irc.get_nick(), channel)
    gotop = utils.getop(irc, channel)
    if gotop:
        for nick in nicks:
            if reason:
                irc.kick(channel, nick, reason)
            else:
                irc.kick(channel, nick)
        
        if not already_op:
            irc.mode(channel, "-o {}".format(irc.get_nick()))

    if not noRemove:
        timeBomb.remove(irc, target, channel, colour="", message=False)

class time_bomb(object):
    def __init__(self):
        self.active = {}
        self.availableWires = ["green", "orange", "blue", "brown", "pink", "purple", "red", "yellow"]

    def add(self, irc, event, target):
        channel = event.target

        disabled = irc.channels[channel]["timebomb"].get("disabled", True)
        if disabled:
            irc.reply(event, "Sorry: This plugin isn't enabled for this channel")
            return        

        if channel not in self.active:
            self.active[channel] = {}

        limit = irc.channels[channel]["timebomb"].get("limit", 1)

        if len(irc.channels[channel]["timebomb"]["active"].keys()) >= limit:
            irc.reply(event, "Only an amount of {} timebombs can be active in this channel".format(str(limit)))
            return

        elif target in irc.channels[channel]["timebomb"]["active"]:
            irc.reply(event, "A user with that nick is already holding an active timebomb")
            return

        wires = []
        amountWanted = random.randint(2, len(self.availableWires))
        detonationTime = random.randint(60, 100)
        iteration = 0
        while True:
            if iteration == (amountWanted):
                break            

            colourToAdd = random.choice(self.availableWires)
            if colourToAdd in wires:
                continue

            wires.append(colourToAdd)
            iteration += 1
        
        probability = round(100 / len(wires)) # a * 100 / all (Amount of wires to cut will always be one)
        self.active[channel][target] = threading.Timer(detonationTime, kick, args=(irc, target, channel))
        self.active[channel][target].setDaemon(True)
        self.active[channel][target].start()
        irc.channels[channel]["timebomb"]["active"][target] = {"deployed": event.source.nick, "wires": wires, "toCut": random.choice(wires)}
        irc.reply(event, "{0}, a bomb was deployed near you. Your only choice is to disarm it. Use \"cut <wire>\" to disarm the bomb. Wires are: {1}. You have {2} seconds until detonation and a {3}% chance of cutting the correct wire."
            .format(target, ", ".join(wires), detonationTime, str(probability)))

    def remove(self, irc, target, channel, colour="", message=True):
        if message:
            if colour not in irc.channels[channel]["timebomb"]["active"][target]["wires"]:
                wires = irc.channels[channel]["timebomb"]["active"][target]["wires"]
                irc.privmsg(channel, "That is an invalid wire, the wires consist of {}".format(", ".join(wires)))
                return

            if colour.lower() != irc.channels[channel]["timebomb"]["active"][target]["toCut"].lower():
                correct = irc.channels[channel]["timebomb"]["active"][target]["toCut"]
                irc.privmsg(channel, "Wrong Wire! You should have cut {}".format(correct.upper()))
                kick(irc, target, channel, noRemove=True)

            else:
                irc.privmsg(channel, "Congratulations, you've defused the bomb!")

        try:
            self.active[channel][target].cancel()
        
        except:
            pass

        del(self.active[channel][target]) 
        del(irc.channels[channel]["timebomb"]["active"][target])

timeBomb = time_bomb()

@add_cmd
def timebomb(irc, event, args):
    channel = event.target

    if not irc.is_channel(channel):
        irc.reply(event, "This command has to be performed in a channel")
        return
    
    canBombSelf = False
    if "timebomb" in irc.channels[channel].keys():
        disabled = irc.channels[channel]["timebomb"].get("disabled", True)
        if disabled:
            irc.reply(event, "Sorry: This plugin isn't enabled for this channel")
            return
        
        canBombSelf = irc.channels[channel]["timebomb"].get("canBombSelf", False)

    if len(args) == 0:
        irc.reply(event, "You haven't specified a target")
        return
    
    elif args[0] == event.source.nick and not canBombSelf:
        irc.reply(event, "You can't bomb yourself!")
        return

    elif args[0] == irc.get_nick():
        irc.reply(event, "No chance")
        return

    elif args[0] not in irc.state["channels"][event.target]["names"]:
        irc.reply(event, "That nick isn't in this channel")
        return
    
    for item in irc.plugins["timebomb"]["exempts"]:
        if item.startswith("$a"):
            account = item[3:]
            if account == irc.state["users"][args[0]]["account"]:
                irc.reply(event, "You're not allowed to bomb that person")
                return

    allowed = False
    if "lastmsg" in irc.state["users"][args[0]].keys():
        if "time" in irc.state["users"][args[0]]["lastmsg"].keys():
            lasttime = irc.state["users"][args[0]]["lastmsg"]["time"]
            if lasttime >= int(time.time()) - irc.plugins[name]["idle"]:
                allowed = True

    if not allowed:
        irc.reply(event, "That person must of been active recently for you to timebomb them")
        return

    gotop = utils.getop(irc, channel)
    if gotop:
        timeBomb.add(irc, event, args[0])
    
    else:
        irc.reply(event, "Could not get channel op, canceling")

@add_cmd
def cut(irc, event, args):
    channel = event.target

    if "timebomb" in irc.channels[channel].keys():
        disabled = irc.channels[channel]["timebomb"].get("disabled", True)
        if disabled:
            irc.reply(event, "Sorry: This plugin isn't enabled for this channel")
            return

    if not irc.is_channel(channel):
        irc.reply(event, "This command has to be performed in a channel")
        return

    if len(args) == 0:
        irc.reply(event, "You haven't specified a wire to cut!")
        return
    
    elif args[0] == event.source.nick:
        irc.reply(event, "Try and cut a wire without cutting yourself")
        return

    if "timebomb" in irc.channels[channel].keys() and event.source.nick not in irc.channels[channel]["timebomb"]["active"].keys():
        irc.privmsg(channel, "You haven't been timebombed, there is no reason to cut {}".format("\"" + " ".join(event.arguments[0].split()[1:]) + "\"" if len(event.arguments) > 0 else "air"))
        return

    timeBomb.remove(irc, event.source.nick, channel, args[0])
