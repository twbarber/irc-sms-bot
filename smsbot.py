import socket
import time
import re
from googlevoice import Voice
from googlevoice.util import input

""" 
    Reads server and login info in from config file...
    *** DO NOT PUSH THAT CONFIG FILE EVER YOU IDIOT ***
"""
def get_server_info():
  with open('server') as f:
      settings = f.read().splitlines()
      return settings

def connect_to_server(server, port, channel):
  irc.connect((server, port))
  print irc.recv(4096)
  irc.send ('NICK smsbot\r\n')
  irc.send ('USER smsbot smsbot smsbot :Python IRC\r\n')
  irc.send ('JOIN ' + channel +'\r\n')
  irc.send ('PRIVMSG ' + channel + ' :Hello World.\r\n')

""" 
    Reads numbers from file...
    *** DO NOT PUSH THAT NUMBER FILE EVER YOU IDIOT ***
"""
def get_contact_list(contact_list):
  try:
    with open('lists/' + contact_list) as f:
      numbers = f.read().splitlines()
      return numbers
  except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)

"""
    Runs through sequence of sending a message
"""   
def new_message_sequence(current_channel, sender, number_list):
  irc.send ('PRIVMSG ' + current_channel + 
                  ' :Request received, see PM for instructions.\r\n')
  verified = authorize_to_send(sender)
  target_number_list = get_contact_list(number_list)
  message = get_message(sender)
  send_sms_message(target_number_list, message)
  irc.send ('PRIVMSG ' + sender + 
            ' :*** Message Sent ***\r\n')

"""
    Verifies password for sending in order to prevent spamming
    Also loaded from 'server' config file.
"""
def authorize_to_send(initiator):
  irc.send ('PRIVMSG ' + initiator + ' :*** Enter Password ***\r\n')
  attempts = 3
  while attempts > 0:
    data = irc.recv(4096)
    message_sender = re.search('\:(\w+)\!', data)
    if message_sender and message_sender.group(1) == initiator:
      if data.find(auth_password) != -1:
        irc.send ('PRIVMSG ' + initiator + 
                ' :*** Password Accepted ***\r\n')
        return True
      else:
        attempts -= 1
        irc.send ('PRIVMSG ' + initiator + 
                ' :*** Invalid password, try again. (' + 
                 '%d) Attempts remaining. ***\r\n' % attempts)
  return False
"""
    Used to get desired message from user
"""              
def get_message(initiator):
  irc.send ('PRIVMSG ' + initiator + ' :*** Enter Message ***\r\n')
  message = ''
  while message == '':
    data = irc.recv(4096)
    sender = re.search('\:(\w+)\!', data)
    if sender and sender.group(1) == initiator:
      print sender.group(1)
      message = re.search('PRIVMSG smsbot :(.*)' ,data) 
  print message.group(1)
  return message.group(1)

"""
    Uses pygooglevoice to send sms to list of numbers.
"""
def send_sms_message(target_contact_list, message):
  for i in target_contact_list:
    phoneNumber = i
    voice.send_sms(phoneNumber, message)
    time.sleep(2)

"""
    Sends help dialog via PM to user
"""
def send_help_dialog(requester):
  irc.send ('PRIVMSG ' + sender.group(1) + 
  ' :Hi! Send messages like this: sendsms [AddressBook]\r\n')
            
# Populate vars with info needed to make connection
server_info = get_server_info()
server= server_info[0]
port = int(server_info[1])
channel = server_info[2]
auth_password = server_info[3]
print 'Server: ' + server + ':' + str(port)

# Connects to GVoice
voice = Voice()
voice_username = server_info[4]
voice_password = server_info[5]
voice.login(voice_username, voice_password, '')

# Connect to IRC
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_to_server(server, port, channel)

while True:
  data = irc.recv(4096)
  sender = re.search("\:(\w+)\!", data)
  
  # Replies to remian connected to server
  if data.find('PING') != -1:
    irc.send ('PONG ' + data.split() [1] + '\r\n')
  
  # Auto joins if kicked
  if data.find('KICK') != -1:
    irc.send ('JOIN ' + channel + '\r\n')
  
  # Help Requested
  if sender and sender.group(1) != 'smsbot':  
    if data.find('smsbot help') != -1:
      send_help_dialog(sender.group(1))
  
  # New request to send message 
  if data.find('sendsms') != -1:
    number_list = re.search("sendsms (\w+)", data)
    if  number_list:
      print sender.group(1)
      print number_list.group(0)
      new_message_sequence(channel, sender.group(1),  number_list.group(1))    
    else:
      irc.send ('PRIVMSG ' + channel + 
                  ' :You must include an address book.\r\n')

  # Prints data received from IRC Channel
  print data 
   


