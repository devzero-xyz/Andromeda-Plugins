from utils import add_cmd, add_handler
import utils

name = "relay"
cmds = ["relay add", "relay remove", "relay modify"]

show_channel_prefix = True # Default
channel_prefix = "#" # Default

def main(irc):
	if not name in irc.plugins:
		irc.plugins[name] = {"channels": []}

@add_cmd
def relay(irc, event, args):
	"""<add|remove|modify> [channel] [type] [channel]

	For commands add,  modify, a type of link and channels have to be specified.
	types include: !, >, <, =. For remove only the two channels need specifying
	"""

	if len(args) == 0:
		irc.reply(event, utils.gethelp("relay"))

	if args[0] == "add":
		if len(args) == 1:
			irc.reply(event, "\x034You need to specify a mode and a two channels to link together. Modes are: ! (Silent), >, < (One Way) and = (Two Way)")
		elif len(args) == 2:
			irc.reply(event, "\x034You need to specify a mode and a another channel to link to. Modes are: ! (Silent), >, < (One Way) and = (Two Way)")
		elif len(args) == 3:
			if args[1] in [">", "<", "=", "!"]:
				irc.reply(event, "\x034You need to specify a channel to link to the first one.")
			else:
				irc.reply(event, "\x034You need to specify a relay mode before the second channel. Modes are: ! (Silent), >, < (One Way) and = (Two Way)")
		elif args[2] not in [">", "<", "=", "!"]:
			irc.reply(event, "\x034Invalid mode of relay. Modes are: ! (Silent), >, < (One Way) and  = (Two Way)")
		elif args[1] == args[3]:
			irc.reply(event, "\x034You can't relay the same channel.")

		else:
			success = True
			compare1 = [args[1], args[3]]
			compare1.sort()
			for connection_id, connection in enumerate(irc.plugins[name]["channels"]):
				compare2 = [irc.plugins[name]["channels"][connection_id]["channel-1"],irc.plugins[name]["channels"][connection_id]["channel-2"]]
				compare2.sort()
				if compare1 == compare2:
					success = False
					break

			if success:
				irc.plugins[name]["channels"].append({
					"channel-1": args[1],
					"channel-2": args[3],
					"mode": args[2],
				})

				irc.reply(event, "\x033Success!\x0f Relay between \"{0}\" and \"{1}\" has been initialized".format(args[1], args[3]))
			else:
				irc.reply(event, "\x034A connection between those two channels already exists. Maybe you meant to modify it?")

	elif args[0] == "remove":
		if len(args) == 1:
			irc.reply(event, "\x034You need to specify both channels to remove the relay between them")
		elif len(args) == 2:
			irc.reply(event, "\x034You need to specify another channel")
		elif args[1] == args[2]:
			irc.reply(event, "\x034Invalid relay. The channels can't be the same")
		
		success = False
		
		compare1 = [args[1], args[2]]
		compare1.sort()
		for connection_id, connection in enumerate(irc.plugins[name]["channels"]):
			compare2 = [irc.plugins[name]["channels"][connection_id]["channel-1"],irc.plugins[name]["channels"][connection_id]["channel-2"]]
			compare2.sort()
			if compare1 == compare2:
				irc.plugins[name]["channels"].pop(connection_id)
				irc.reply(event, "\x033Success!\x0f Deleted the link between \"{0}\"".format(" and ".join(compare1)))
				success = True
				break
				
		if not success:
			irc.reply(event, "\x034Could not find that relay")
			
	elif args[0] == "modify":
		if len(args) == 1:
			irc.reply(event, "\x034You need to specify a mode and a two channela to successfuly modify the relay. Modes are: ! (Silent), >, < (One Way) and = (Two Way)")
		elif len(args) == 2:
			irc.reply(event, "\x034You need to specify a mode and a another channel to link to successfuly modify the relay. Modes are: ! (Silent), >, < (One Way) and = (Two Way)")
		elif len(args) == 3:
			if args[1] in [">", "<", "=", "!"]:
				irc.reply(event, "\x034You need to specify another channel to successfuly modify the relay.")
			else:
				irc.reply(event, "\x034You need to specify a relay mode before the second channel. Modes are: ! (Silent), >, < (One Way) and = (Two Way)")
		elif args[2] not in [">", "<", "=", "!"]:
			irc.reply(event, "\x034Invalid mode of relay. Modes are: ! (Silent), >, < (One Way) and  = (Two Way)")
		elif args[1] == args[3]:
			irc.reply(event, "\x034You can't have two of the same channel.")
			
		else:
			success = False
			found = False
			new_mode = args[2]
			
			compare1 = [args[1], args[3]]
			compare1.sort()
			for connection_id, connection in enumerate(irc.plugins[name]["channels"]):
				compare2 = [irc.plugins[name]["channels"][connection_id]["channel-1"],irc.plugins[name]["channels"][connection_id]["channel-2"]]
				compare2.sort()
				if compare1 == compare2:
					if args[1] != irc.plugins[name]["channels"][connection_id]["channel-1"]:
						irc.plugins[name]["channels"][connection_id]["channel-1"] == args[3]
						irc.plugins[name]["channels"][connection_id]["channel-1"] == args[1]
				
					old_mode = irc.plugins[name]["channels"][connection_id]["mode"]
					if old_mode == new_mode:
						found = True
						break
					else:
						irc.plugins[name]["channels"][connection_id]["mode"] = new_mode
						irc.reply(event, "\x033Success!\x0f The link's mode between \"{0}\" has been updated from \"{1}\" to \"{2}\"".format(" and ".join(compare1), old_mode, new_mode))
						irc.plugins[name]["channels"][connection_id]["mode"] = new_mode
						success = True
						found = True
						break
						
			if found and not success:
				irc.reply(event, "\x034The mode of relay hasn't changed.")
			elif not found:
				irc.reply(event, "\x034The relay could not be found")
	
def on_pubmsg(irc, conn, event):
	message = " ".join(event.arguments)
	channel = event.target
	
	for connection_id, connection in enumerate(irc.plugins[name]["channels"]):
		data = irc.plugins[name]["channels"][connection_id]
		
		if not show_channel_prefix:
			data["channel-1"] = data["channel-1"].replace(channel_prefix, "")
			data["channel-2"] = data["channel-2"].replace(channel_prefix, "")
		
		if channel in [data["channel-1"], data["channel-2"]] and data["mode"] == "!":
			pass # Don't send anything
		elif channel == data["channel-1"] and data["mode"] in ["<", "="]:
			irc.privmsg(data["channel-2"], "<{0}@{1}> {2}".format(event.source.nick, data["channel-1"], message))
		elif channel == data["channel-2"] and data["mode"] in [">", "="]:
			irc.privmsg(data["channel-1"], "<{0}@{1}> {2}".format(event.source.nick, data["channel-2"], message))
add_handler(on_pubmsg, name)	
