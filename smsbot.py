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
    Verifies password for sending in order to prevent spamming
    Also loaded from 'server' config file.
"""
def authorize_to_send(sender):
    irc.send ('PRIVMSG ' + sender + ' :*** Enter Password ***\r\n')
    attempts = 3
    while attempts > 0:
        data = irc.recv(4096)
        print data
        if data.find(auth_password) != -1:
            irc.send ('PRIVMSG ' + sender + 
                        ' :*** Password Accepted ***\r\n')
            return
        else:
            attempts -= 1
            irc.send ('PRIVMSG ' + sender + 
                        ' :*** Invalid password, try again. (' + 
                         '%d) Attempts remaining. ***\r\n' % attempts)
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
  return message.group(1)

"""
    Uses pygooglevoice to send sms to list of numbers.
"""
def send_sms_message(target_contact_list, message):
   for i in target_contact_list:
      phoneNumber = i
      voice.send_sms(phoneNumber, message)
      time.sleep(2)
            
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
irc.connect((server, port))
print irc.recv(4096)
irc.send ('NICK smsbot\r\n')
irc.send ('USER smsbot smsbot smsbot :Python IRC\r\n')
irc.send ('JOIN ' + channel +'\r\n')
irc.send ('PRIVMSG ' + channel + ' :Hello World.\r\n')
while True:
  data = irc.recv(4096)
  sender = re.search("\:(\w+)\!", data)
  if data.find('PING') != -1:
    irc.send ('PONG ' + data.split() [1] + '\r\n')
  if data.find('KICK') != -1:
    irc.send ('JOIN ' + channel + '\r\n')
  if sender and sender.group(0) != 'smsbot':  
    if data.find('smsbot help') != -1:
      irc.send ('PRIVMSG ' + sender.group(1) + 
                ' :Hi! Send messages like this: sendsms [AddressBook]\r\n')
    if data.find('sendsms') != -1:
      contact_list = re.search("sendsms (\w+)", data)
      if contact_list:
        if sender: 
          irc.send ('PRIVMSG ' + channel + 
                    ' :Request received, see PM for instructions.\r\n')
          authorize_to_send(sender.group(1))
          target_contact_list = get_contact_list(contact_list.group(1))
          message = get_message(sender.group(1))
          send_sms_message(target_contact_list, message)
          irc.send ('PRIVMSG ' + sender.group(1) + 
                    ' :*** Message Sent ***\r\n')
      else:
        irc.send ('PRIVMSG ' + channel + 
                  ' :You must include an address book.\r\n')
  print data 
   


