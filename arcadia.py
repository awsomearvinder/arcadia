# -*- coding: utf-8 -*-
#!/usr/bin/env python2
import fileinput
import json
import random
import socket
import thread #
import urllib2 #
import collections
import time
import traceback
import re
from decimal import Decimal as D
from datetime import datetime


import MySQLdb #
import math
username = 'Arcadia2'
oper_key = 'ee82aeb94474fcc21f05061043cb4' #This is not the actual key
#weather_api="http://api.openweathermap.org/data/2.5/weather?q="
#weather_api="http://api.openweathermap.org/data/2.5/find?q="
weather_api="http://api.openweathermap.org/data/2.5/find?APPID=c61b24ac1edeb6837b377df=" # This is not the actual key

API_KEY="&APPID=c61b24ac1edeb6837b377df" #This is not the actual key

CHANNEL = "#main"

# TODO: @Arcadia.msg_register(name: str, requires_auth: bool, secret: bool, floodrule: str)
#          @Arcadia.data_register(....)
#          would inspect function for name and arguments, and get docstring, to add as a response to !help.
#          would add the decoratee function as a msg or data callback.
# IDEA: floodrule is similar to unrealircd +f channel flag: [*]<attempts>:<seconds>

# TODO: Log !sudo commands to #opers (unless it's issued from #opers), or to file, or to /helpops or /globops or /chatops
#          Failed attempts should be logged unobtrusively, to file
# IDEA: Allow user to pipe the output of a command to another channel they are in.

class Connection: #This should work similarly to the singleton.
        __shared_state = {}
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        network = '192.102.0.203'
        port = 6667
        channel = CHANNEL
        #sock.connect((network, port))
        def __init__(self):
                self.__dict__ = self.__shared_state
        # and whatever else you want in your class -- that's all!
        def connect(self):
                self.sock.connect((self.network, self.port))

        def get_names_list(self, channel=None):
                if channel is None or not is_chan(channel):
                        channel = self.channel
                self.sendPacket ( 'names %s :' %(channel))
                all_names = []
                while True:  # I don't like having our own little recv loop here
                # but it's probably fine for IRC. Better solution would involve
                # moving to asyncio, threading and queues, or 'callback hell'.
                        data = self.sock.recv ( 1024 )
                        print("Listening for NAMES:", data)
                        for line in data.splitlines():
                                numeric = line.split(" ")[1]
                                if numeric == "353":  # line of NAMES response
                                        names_part = line.split(channel + " :")[1]
                                        for namemask in names_part.split(" "):
                                                name = namemask.split("!")[0].lstrip("&~@")
                                                all_names.append(name)
                                else:
                                        if numeric != "366":  # end of NAMES response
                                                print("Odd data received while listening for NAMES:", data)
                                        return all_names
                return all_names

        def get_names(self, channel=None):
                return " ".join(self.get_names_list(channel))

        def sendPacket(self, packet):
                self.sock.send ( packet + '\r\n' )

        def sendPacket_split(self, prefix, suffix, split_size=250):
                # TODO: Need a maximum number of lines to send, with possibly a !continue callback.
                # TODO: Need to delay or queue our output without disrupting comms. Would require a timer.
                for i in range(0, len(suffix), split_size):
                        self.sendPacket(prefix + suffix[i:i+split_size])

class Message:
        """
        Represents a message from a user in a channel or PM window.
        """
        def __init__(self, bot, data):
                self.timestamp = time.time()

                self.bot = bot
                self.server = bot.server
                self.data = data
                self.msgtxt = ':'.join(data.split(':')[2:])
                self.nick = data.split( '!' )[0].replace(':', '')
                self.channel = get_chan_from_data(data, self.nick)
                self.type = data.split(" ")[1]  # PRIVMSG, NOTICE, etc
                self.is_channel = is_chan(self.channel)
                self.msgparts = self.msgtxt.strip().split(' ')

        def reply(self, message, highlight=None):
                h = self.nick + ": "
                if highlight is None:
                        highlight = self.is_channel

                if is_badword(self.nick):
                        highlight = False
                prefix = "PRIVMSG %s : %s" % (self.channel, h*highlight)
                return self.server.sendPacket_split(prefix, message)

        def said(self, s):
                return self.msgtxt.lower().find(s.lower()) == 0

        def find_raw(self, s):
                return self.data.find(s)

class database:
        host = "localhost"
        user = "arcadia"
        passwd = "hoi22h33"
        db = "Arcadia"
        conn = None
        cursor = None

        def connect(self):
                self.conn = MySQLdb.connect(self.host, self.user, self.passwd, self.db)
                self.cursor = self.conn.cursor()

        def disconnect(self):
                self.cursor.close()
                self.conn.close()

        def escape(self, toclean):
                return MySQLdb.escape_string(toclean)
        def insert(self,query,params):
                self.cursor.execute(query, ( params ))

        def run(self, query):
                self.cursor.execute(query)
                row = self.cursor.fetchone()
                return row
        """def set_note(user,text):
        def get_note(user):
                return notes"""
"""class clue:
        db=database()
        db.connect()
        def get_location:
                db.connect()
                db.run("SELECT * FROM `locations` ORDER BY rand() LIMIT 1")
                db.disconnect()
        def add_location:

        def get_weapon:
        def add_weapon:"""
class brain:
        filename = "arcadias_brain.txt"
        def load(self):
                print("trying to load the brain")
                file = open(self.filename, "r")
                lines = file.readlines()
                print("I loaded the brain")
                return lines
        def save(self,lines):
                print("saving brain to file.")
                file = open(self.filename, "w")
                for line in lines:
                        file.write("%s\n" % line)
                file.close()
        def clean(self,lines):
                for lines in fileinput.FileInput(self.filename, inplace=1):
                        lines = lines.strip()
                        if lines == '': continue
                        print lines
                print("cleaned the brain")

def ago(past_timestamp):
        """
        Returns a string, the number of days, hours, minutes, or seconds ago a timestamp is.

        Example output:
        5h30m ago
        3d5h ago
        2m30s ago
        """
        time_diff = int(time.time() - past_timestamp)
        time_diff_units = []
        for unit, unitname in [(86400, "d"), (3600, "h"), (60, "m"), (1, "s")]:
                u = time_diff // unit
                if u > 0:
                        time_diff_units.append(str(u))
                        time_diff_units.append(unitname)
                        time_diff -= u * unit
                if len(time_diff_units) >= 4:
                        break
        return "".join(time_diff_units) + " ago"

class last_message:
        chans = collections.defaultdict(list)  # {"#chan": [(time, txt), (time, txt), ...], ...}
        def __init__(self, default_channel):
                self.default_channel = default_channel
        def push(self, timestamp, data, channel=None):
                if channel is None:
                        channel = self.default_channel
                arr = self.chans[channel]
                if len(arr) >5:
                        arr.pop(0)
                arr.append((timestamp, data.replace ( '\r\n', '' )))
        def pop(self, channel=None):
                if channel is None:
                        channel = self.default_channel
                arr = self.chans[channel]
                if len(arr) > 0:
                        return arr.pop(0)
                return (0, "")
        def pop_all(self, channel=None):
                if channel is None:
                        channel = self.default_channel
                return self.chans[channel]
"""class user_tracker:
        db = database()
        db.connect()
        #m = db.escape(message)
        def check_name(name):
                clean_name = self.db.escape(name)
                #print "Checking: " + word[:-4]
                query = "SELECT COUNT(*) from `users` WHERE `username` = '"+clean_name+"'"
                row = db.run(query)
                #print row[0]
                if(row[0] ==1):
                        return 1
                else:
                        return 0
        def insert_name(name):
                clean_name = self.db.escape(name)
                query = "INSERT INTO `users` VALUES('"+clean_name+"','9')"
                row = db.run(query)"""
"""class trivia_engine:
        db = database()
        db.connect()
        #m = db.escape(message)
        state = 0
        question_id =0
        players =[]
        def restart(self):
                self.players =[]
                self.state =0
        def question(self,message,nick):
                if self.state != 0:
                        return "A question was already asked: " +self.state
                m = self.db.escape(message)
                m = m.replace ( '\r\n', '' )
                parts = m.split(' ')
                bleh = parts[1::]
                #one_line = ' '.join([str(i) for i in bleh])[:-4:]
                #question = "Who was luke skywalker's father?"
                db = database()
                db.connect()
                m = db.escape(message)
                query ="SELECT count(*)FROM `trivia`;"
                row = db.run(query)
                count = row[0]
                next_id = str(random.randint(0,count-1))
                self.question_id = next_id
                print("Next_ID:"+ next_id)
                query ="SELECT `question` FROM `trivia` WHERE id="+next_id+";"
                row = db.run(query)
                self.state = row[0] # set the state to the current question.
                return self.state+" "+nick
        def answer(self,message,nick):
                if self.state ==0:
                        return "The game hasn't started yet."
                else:
                        if "darth vader" in message:
                                return "Good job."
                        else:
                                db = database()
                                db.connect()
                                m = db.escape(message)
                                query ="SELECT `id` from `trivia` WHERE `answer` LIKE '%"+m[3:-4:]+"%'"
                                print query
                                row = db.run(query)
                                if row is None:
                                        return "I'm sorry, wrong answer."
                                print("id: " + str(row[0]) +"Current question id: "+ str(self.question_id))

                                if(str(row[0]) == str(self.question_id)):
                                        self.state =0
                                        return "Good Job!"
                                else:
                                        return "Wrong answer"
                        return "I'm sorry, wrong answer."
"""

def get_weather(message):
        try:
                search = '%20'.join(message.msgparts[1:])
                if (search == 'hoth'):
                        search = 'Hell%20,MI'
                print(weather_api+search)
                try:
                        usock = urllib2.urlopen(weather_api+search)
                except urllib2.HTTPError as e:
                        return "Communication error (HTTP %s: %s). Try again later or notify developer." % (e.code, e.reason)
                data = usock.read()
                usock.close()
                weather = json.loads(data)
                try:
                        weather = weather['list'][0]
                except KeyError:
                        return "Error. You must provide a location. OpenWeatherMap says: %s (code %s)" % (weather['message'], weather['cod'])
                print(weather['weather'])
                status = weather['weather']
                temp = weather['main']['temp']
                location = str(weather['name']) + ', '+ str(weather['sys']['country'])
                print("Location" + location)
                return str(k2f(temp))+'°F|'+str(k2c(temp))+'°C, '+str(status[0]['description']) + ' | ' + location
        except:
                print "Unkown error in get_weather."
                traceback.print_exc()
                return "Unknown error."

def get_time(zone="-5"):
        return "Eastern: "+str(datetime.now().time())+" UTC: "+str(datetime.utcnow().time())
def k2f(K):
        F =(K - 273.15) *1.8000+32.00
        return F
def k2c(K):
        C= K- 273.15
        return C
def get_response(message):
#sendPacket ( 'PRIVMSG %s : %s' % (channel, 'Trying to respond to: '+message))
        db = database()
        db.connect()
        m = db.escape(message.msgtxt)
        parts = m.split(' ')
#       for part in parts:
                #print(part)
        #sendPacket ( 'PRIVMSG %s : %s' % (channel, 'filtered before db: '+m[:-4:]))
        row = db.run("SELECT `response` from `responses` WHERE `message`='"+m[:-4:]+"'")
        #db.disconnect()
        if(row != None):
                #sendPacket ( 'PRIVMSG %s : %s' % (channel, 'I found a response for: '+row))
                response = row[0]
                if "|names|" in response:
                        print (response)
                        #response = 'Bah Humbug! '#
                        response.replace("|names|", message.server.get_names(message.channel))
#                       response = ' '.join(response.split())
                        print (response)
                if "|nick|" in response:
                        response = response.replace("|nick|", message.nick)
                #if "||" in response:
                #       sendPacket("PRIVMSG %s : %s")
                if(response.startswith('|action|')):
                        return '\001ACTION ' + response.replace("|action|", "") + '\001'
                db.disconnect()
                return response
        else:
                return False


def handle_badwords(message):
        print "handling badwords"
        msgtxt = message.msgtxt
        for l in ('"', "'", "\\"):
                msgtxt = msgtxt.replace(l, "")
        words = msgtxt.split(" ")
        for word in words:
                if is_badword(word) == 1:
                        print "Stop swearing!" + word
                        if not message.is_channel: #  Can't kick in a PM.
                                message.reply("Hey, watch your language")
                        else:
                                #sendPacket ( 'PRIVMSG %s : %s' % (channel, 'Hey, watch your language') )
                                kick = 'KICK %s %s %s' % (message.channel, message.nick, 'Hey, watch your language')
                                print(kick)
                                message.server.sendPacket(kick)
                                #Todo add a handling of the swearing, so it marks them saying it, and kicks them and stuff.
                        break



def is_badword(dirty_word):
		return #Currently, I haven't dumped the swearword database.
        db = database()
        db.connect()
        word = db.escape(dirty_word)
        #print "Checking: " + word[:-4]
        query = "SELECT COUNT(*) from `badwords`"
        query = query + " WHERE `words` = '" + word[:-4]+"'"
        query = query + " OR `words` = '"+word[:-4]+".'"
        query = query + " OR `words` = '"+word[:-4]+",'"
        query = query + " OR `words` = '"+word[:-4]+"!'"
        row = db.run(query)
        #print row[0]
        if(row[0] ==1):
                return 1
        else:
                return 0

def get_verse(message):
		return #Currently I haven't dumped the bible database.
        print('In get_verse')
        db = database()
        db.connect()
        m = db.escape(message.msgtxt)
        m = m.replace ('\r\n', '').replace("\\r\\n", '')
        parts = m.split(' ')
        for part in parts:
                print(part)
        print "Length: " + str(len(parts))
        #parts.pop(1)

        is_range = all(i.isdigit() for i in parts[-3:])

        if is_range:
                chapt = parts[-3]
                start = parts[-2]
                end = parts[-1]
                book = " ".join(parts[1:-3])

        else:
                chapt = parts[-2]
                start = end = parts[-1]
                book = " ".join(parts[1:-2])

        start = int(start)
        end = int(end)
        response = ""
        if end - start > 7:
                end = start + 7
                response += "[Limited verses: %s to %s] " % (start, end)
        print "Start: " + str(start) + " , END " + str(end)

        for i in range(start,end+1):
                query = "SELECT `VerseText` from `BibleKJV` WHERE `book`='" +book+"' AND `Chapter`='"+chapt+"' AND `Verse`='"+str(i)+"'"
                print query
                row = db.run(query)
                if row is None:
                        return 'Verse(s) not found. Format example (looking up 1 Corinthians 3:18-20): ".bible 1 Corinthians 3 18 20" -- Another (looking up John 3:16): ".bible John 3 16"'
                if len(row) > 0:
                        print "Multiverse"
                        for i in row:
                                print "verse: " + i
                                response += " " + i
                else:
                        response = row[0]
        print "response" + response
        return response
def AI_intel_response(message,storage):
        for word in message.split(' '):
                print("printing input word:"+ word)
                if word in ['hi','hello','yo','hey','greetings']:
                        matching = [s for s in storage if "hello" in s]
                        return random.choice(matching)
        return random.choice(storage)
def AI_response(message, storage_=None):
        global storage
        if storage_ is None:
                storage_ = storage
        db = database()
        db.connect()
        m = db.escape(message.msgtxt)
        m = m.replace ( '\r\n', '' )
        parts = m.split(' ')
        bleh = parts[1::]
        one_line = ' '.join([str(i) for i in bleh])[:-4:]
        print("storing:" + one_line)
        if "pug" not in one_line:
                storage.append(one_line)
        #return random.choice(storage_)#[:-4:]
        return AI_intel_response(one_line,storage_)


def arithmatic ( args ):
        args [ 0 ] = args [ 0 ].replace ( '\r\n', '' )
        for letter in 'abcdefghijklmnopqrstuvwxyz':
                args [ 0 ] = args [ 0 ].replace ( letter, '' )
        solution = str ( eval ( args [ 0 ], { '__builtins__' : {} } ) )
        return solution
def sine ( args ):
        solution = str ( math.sin ( float ( args [ 0 ] ) * ( 2 * math.pi ) / 360 ) )
        return solution
def cosine ( args ):
        solution = str ( math.cos ( float ( args [ 0 ] ) * ( 2 * math.pi ) / 360 ) )
        return solution
def tangent ( args ):
        solution = str ( math.tan ( float ( args [ 0 ] ) * ( 2 * math.pi ) / 360 ) )
        return solution


def send_last_msgs(bot, nick, channel, show_error=False):
        server = bot.server
        if not is_chan(channel):
                channel = server.channel

        channel_nicks = server.get_names_list(channel)
        if nick not in channel_nicks:
                server.sendPacket ( 'NOTICE %s : %s' % (nick, 'You must be in a channel to see its last messages.') )
        elif "[m]" in nick:
                print("ignoring matrix")
        else:
                response = bot.last.pop_all(channel)
                print(response)
                if len(response) > 0:
                        server.sendPacket ( 'NOTICE %s : %s %s:' % (nick, 'Last messages on channel', channel) )
                        for timestamp, text in response:
                                server.sendPacket ( 'NOTICE %s : %s %s' % (nick, ago(timestamp), text) )
                elif show_error:
                        server.sendPacket ( 'NOTICE %s : %s %s.' % (nick, 'I don\'t remember any previous messages on the channel', channel) )


def is_chan(channel):
        return (channel.startswith("&") or channel.startswith("#"))

def get_chan_from_data(data, nick):
        channel = data.split(" ")[2]  # may be our own nick in a PM.
        if not is_chan(channel):
                return nick
        return channel

def procss_data(bot, data, msgtxt, nick, b, last):
        if data.find ( 'PING' ) != -1:
                bot.server.sendPacket ( 'PONG ' + data.split() [ 1 ] )
#       elif data.find( 'NICK') != -1:
#               if "has changed his/her nickname to" in message:
#               print  data
#               new_nick = message.split(':')
#               server.sendPacket ( 'PRIVMSG %s : %s' % (server.channel, nick + ' Changed to: '+message.split(':')[1]))
        else:
                not_blocked = bot.run_callbacks(data)
                if not_blocked:
                        if data.find("JOIN :#")!= -1:   #:Bart_Roberts!bartrobert@fanta.net JOIN :#main"
                                if "Arcadia" not in data:
                                        channel = data.split('JOIN :')[1].rstrip()
                                        join_nick = data.split (':')[1].split('!')[0]
                                        send_last_msgs(bot, join_nick, channel)
                        elif data.find('PRIVMSG') != -1:
                                procss_privmsg(Message(bot, data))

#def procss_data(server,data,message,nick,b,trivia,last):
def procss_privmsg(msg):
        global storage
        server = msg.bot.server
        brain = msg.bot.brain
        print "nick: " + msg.nick
        print "channel: " + msg.channel
        print "message: " + msg.msgtxt
        #sendPacket ( 'JOIN :#main')
        handle_badwords(msg) # This will handle the swear words stuff.
        if msg.said('you\'re lame'):
                msg.reply("Hey", False)
        elif msg.said('!main'):
                server.sendPacket('JOIN ' + CHANNEL)
                server.sendPacket ('PRIVMSG %s : %s' % (CHANNEL, 'I\'m Back '))
        elif msg.said('.bible'):
                response = get_verse(msg)
                msg.reply(response, False)
        elif msg.said('arcadia'):
                response = AI_response(msg)
                msg.reply(" " + response, False)
        elif msg.said("!last"):
                try:
                        channel = msg.msgparts[1]
                except IndexError:
                        channel = msg.channel
                send_last_msgs(msg.bot, msg.nick, channel, show_error=True)
        elif msg.said('!save'):
                authed_function_call(msg, brain.save, storage)
        elif msg.said('!load'):
                def f():
                        global storage
                        storage = brain.load()
                authed_function_call(msg, f)
        elif msg.said('!clean' or '!fixbrain'):
                def f():
                        global storage
                        brain.clean(storage)
                        storage = brain.load()
                authed_function_call(msg, f)
        elif msg.said('!timeout'):
                command = 'SAJOIN ' + msg.msgparts[1] + ' #timeout'
                print(command)
                authed_function_call(msg, server.sendPacket, command)
        elif msg.said('!t_DISABLED'):
                print("In trivia: " +msg.msgtxt)
                server.sendPacket ( 'PRIVMSG %s : %s' % (server.channel, ' ') )
                #if "start" in msg:
                        #response = trivia.question(message,nick)
                        #server.sendPacket ( 'PRIVMSG %s : %s' % (server.channel, ' '+response) )
                #else:
                        #response = trivia.answer(message,nick)
                        #server.sendPacket ( 'PRIVMSG %s : %s' % (server.channel, ' '+response) )
        elif msg.said('!sudo'):
                print("Igot:" + msg.msgtxt)
                t = " ".join(msg.msgparts[1:]).replace('/msg','PRIVMSG ')
                authed_function_call(msg, server.sendPacket, t)
        elif msg.said('!f2c'):
                f = D(msg.msgparts[1])
                c = (f - 32) * D(5/9.)
                msg.reply('%1.2f' % c)
        elif msg.said('!c2f'):
                c = D(msg.msgparts[1])
                f = D(9/5.) * c + 32
                msg.reply('%1.2f' % f)
        elif msg.said('!time'):
                msg.reply(get_time())
        elif msg.said('!h7777777777'):
                msg.reply('Hello room, and hello ' + msg.nick, False)
        elif msg.said('!me'):
                server.sendPacket('PRIVMSG %s :%s' % (msg.channel, '\001ACTION waves.\001'))
                #sendPacket ( 'names %s :' %(channel))
                #data = server.sock.recv ( 1024 )
                server.sendPacket('PRIVMSG %s : %s' % (msg.channel, 'Response: ' + server.get_names(msg.channel)))
        else:
                if msg.said('!id'):
                        global oper_key
                        server.sendPacket ( 'OPER admin '+ oper_key)
                response = get_response(msg)
                if msg.said('!weather'):
                        response = get_weather(msg)
                if(response != False):
                        if msg.said('!test'):
                                data = server.sock.recv ( 1024 )
                                print "HERE"
                        elif msg.said('!joinbart'):
                                server.sendPacket ( response)
                                data = server.sock.recv ( 1024 )
                                print "HERE"
                        else:
                                msg.reply(response, False)

        if ("!id" not in msg.msgtxt and "NOTICE" not in msg.data) and msg.is_channel:
                #store the last 5 things said/did.
                if msg.msgtxt.startswith("\001ACTION "):
                        action = msg.msgtxt.replace("\001ACTION ", "", 1).rstrip("\001")
                        topush = "*"+msg.nick+" "+action
                else:
                        topush = "<"+msg.nick+">"+msg.msgtxt
                msg.bot.last.push(msg.timestamp, topush, msg.channel)

def authed_function_call(trig_msg, function, *args, **kwargs):
        t = time.time()
        timeout = t + 10

        def cb(whois_code, rest):
                if time.time() > timeout or whois_code == "318":
                        trig_msg.reply("Auth failed. Make sure that you're OPER'd (and that I'm OPER'd).")  # TODO: When we have timers, we can make this error message occur always.
                        return True
                elif whois_code in ("320", "313"):
                        function(*args, **kwargs)
                        return True
                return False

        whois(trig_msg.bot, trig_msg.nick, cb, ["320", "318", "313"])

def whois(bot, target_nick, cb, target_codes=None):
        """

        :param bot:
                An Arcadia instance.
        :param target_nick:
                The nick we have to whois. WHOIS responses from the server pertaining to
                any other nick are ignored.
        :param cb:
                A callable taking two strings, first is the WHOIS RPL numeric code,
                second is the string the server put at the end.
                If the server responds:

                ```
                :domainname.com 671 username1 username2 :is using a Secure Connection
                ```

                `cb` gets:

                ```
                cb("671", ":is using a Secure Connection")
                ```

        :param target_codes:
                The WHOIS RPL numeric codes we should watch out for, others will be ignored.
                If argument is not passed, we'll watch out for all known WHOIS numerics.
        """
        if target_codes is None:
                target_codes = [
                        "311",  # hostname (start)
                        "379",  # modes
                        "378",  # "is connecting from"
                        "307",  # "is identified"
                        "319",  # channels
                        "312",  # server in the net user is connected to
                        "313",  # server operator
                        "310",  # available for help
                        "671",  # using ssl
                        "320",  # is root
                        "317",  # idle time and signon time
                        "318",  # end
                        "401"  # no such user
                ]
        def whois_cb(bot, data):
                try:
                        servername, code, me, you, rest = data.split(" ", 4)
                except ValueError:  # not a whois reply.
                        return False, False
                else:
                        print("whois_cb:", servername, code, me, you, rest)
                        cbresult = None
                        if code in target_codes and you.lower() == target_nick.lower():
                                cbresult = cb(code, rest)
                        if code == "318" and you == target_nick:
                                # When we get to the end of the relevant WHOIS message, this function
                                # is removed from the list of callbacks in Arcadia.
                                return True, False
                        return cbresult, False

        bot.callbacks.append(whois_cb)

        bot.server.sendPacket(" WHOIS {0} {0}".format(target_nick))


class Arcadia:
        server = Connection()
        # Callbacks are called with an Arcadia object, and a string with the data
        # that was received. They are called every time we receive data, before the
        # normal hardcoded commands are tried.
        # Callbacks return two values.
        # (whether_to_remove_me, whether_to_block_callbacks_to_my_right)
        # If the second value equals 2, we cease processing the message and hardcoded
        # commands won't be tried (meaning, they will be tried if it isn't 2).
        callbacks = []

        def run_callbacks(self, data):
                return self._run_callbacks(self.callbacks, self, data)
        def _run_callbacks(self, cbs, *args):
                to_remove = []
                block = None
                for f in cbs:
                        remove, block = f(*args)
                        if remove:
                                to_remove.append(f)
                        if block:
                                break
                for f in to_remove:
                        while f in cbs:
                                cbs.remove(f)
                return (block != 2)
        def Arcadia_run(self):
                global running
                global username
                print(running)
                while running==1:
                        self.server.connect()
                        self.server.sendPacket ( 'NICK %s' % (username) )
                        self.server.sendPacket ( 'USER %s %s %s: %s' % ('Arcadia', 'Arcadia', 'Arcadia', 'Arcadia') )
                        trash = self.server.sock.recv ( 1024 )
                        self.server.sendPacket ( 'JOIN %s' % (self.server.channel) )
                        self.server.sendPacket ( 'PRIVMSG %s : %s' % (self.server.channel, 'Hey') )
                        #Other commands: !hiwizard,!easter, !sleep, !good, !whee,
                        # !purple, !batman, !grapefruit, !ben, !friday, !secret, !gps, !christmas. !bunny, !monday, !pirate, !sandwich, !sandvich
                        self.brain = brain() # load arcadia's brain
                        #trivia = trivia_engine()
                        self.last = last_message(self.server.channel)
                        while True:
                                data = self.server.sock.recv ( 1024 )
                                for line in data.splitlines(True):
                                        message = ':'.join ( line.split ( ':' ) [ 2: ] )
                                        nick = line.split ( '!' ) [ 0 ].replace ( ':', '' )
                                        print "Raw: " +line
        #                               procss_data(self.server,data,message,nick,b,trivia,last)
                                        procss_data(self, line, message, nick, self.brain, self.last)

running=1
storage = []
arcadia = Arcadia()
try:
        thread.start_new_thread( arcadia.Arcadia_run, () )
except:
        traceback.print_exc()
        print "Error: unable to start thread"

try:
        while 1:
                user_input = raw_input("enter something: ")
                if user_input.startswith("#EVAL#"):
                        user_input = user_input[len("#EVAL#"):]
                        try:
                                try:
                                        result = eval(user_input)
                                        print "Eval result:"
                                        print result
                                        print "-----"
                                except SyntaxError:
                                        exec(user_input)
                                        print "(Executed)"
                        except:
                                traceback.print_exc()
                else:
                        if "/join" in user_input:
                                arcadia.server.sendPacket ( 'JOIN %s' % (user_input[6::]) )
                                print("trying to")
                        elif user_input == "/start":
                                arcadia.server.sendPacket ( 'OPER ntw1103 '+ oper_key)
                                brain = arcadia.brain
                                global storage
                                storage = brain.load()
                                brain.clean(storage)
                        else:
                                arcadia.server.sendPacket ( 'PRIVMSG %s : %s' % (CHANNEL, ' ' +user_input) )
                print user_input
except KeyboardInterrupt:
                running = "stopped"
                print "done"
