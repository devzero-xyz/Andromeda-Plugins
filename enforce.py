"""This plugins allows a user to enforce modes set on channels"""
"""e.g. enforcing +o on nick"""

"""Requires admin"""

from utils import add_cmd, add_handler
import utils
from admin import deop

name = "enforce"
cmds = ["enforce"]

def main(irc):
    if name not in  irc.plugins.keys():
        irc.plugins[name] = {}
        
@add_cmd
def enforce(irc, event, args):
    """[<channel>] <modes> <nick>

    Enforces a mode to <nick> in the current channel if no channel argument is given.
    """
    
    message = event.arguments[0].split()

    try:
        if irc.is_channel(message[1]):
            unrecognised_modes = []
            unset_modes = []
            set_modes = []
            mode_diff = "+"
            for pos, mode in enumerate(message[2]):
                if mode in utils.argmodes["set"] or mode in utils.argmodes["unset"] or mode in ["+", "-"]:
                    pass
                else: # What on earth is that mode?
                    unrecognised_modes.append(mode)
            for mode in message[2]:
                if mode == "+":
                    mode_diff = "+"
                elif mode == "-":
                    mode_diff = "-"
                else:
                    if mode_diff == "+":
                        if mode in unset_modes:
                            irc.reply(event, "This mode {} is already set and could not be unset for {}".format(mode, message[3]))
                        else:
                            set_modes.append(mode)
                    elif mode_diff == "-": # else but who cares?
                        if mode in set_modes:
                            irc.reply(event, "This mode {} is already set and could not be set for {}".format(mode, message[3]))
                        else:
                            unset_modes.append(mode)
            if unrecognised_modes:
                irc.reply(event, "I could not recognise these modes: {}".format("".join(unrecognised_modes)))
            else:
                if len(message) >= 4:
                    if not "enforce" in irc.channels[message[1]]:
                        irc.channels[message[1]]["enforce"] = {}
                    irc.channels[message[1]]["enforce"][message[3]] = {
                        "set": set_modes or "",
                        "unset": unset_modes or ""
                    }
                else:
                    irc.reply(event, "You didn't specify a nick to enforce modes to")
    except IndexError:
        irc.reply(event, utils.gethelp("enforce"))
        
def on_mode(irc, conn, event): 
    modes = utils.split_modes(event.arguments)
    irc.notice("BWBellairs", str(modes))
    if "enforce" in irc.channels[event.target].keys():
        for mode in modes:
            subject = mode.split()[1]
            mode_type =  mode.split()[0]
            
            if subject in irc.channels[event.target]["enforce"].keys():
                modes_set = irc.channels[event.target]["enforce"][subject]
                
                if mode_type[0:2] == "+o" and mode_type[1] in modes_set["unset"]:
                    irc.notice("BWBellairs", "deop him!!!")
            

add_handler(on_mode, name)
        

 
