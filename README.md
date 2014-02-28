IRC SMS Bot - Written for Python 2
==================================


Uses **pygooglevoice** library by Joe McCall & Justin Quick
**GitHub:** https://github.com/pettazz/pygooglevoice
**Full Documentation:** http://sphinxdoc.github.com/pygooglevoice/

You need to run the general setup for pygooglevoice before you
can run this bot. I will look into a fix for this soon.

After pygooglevoice is installed, there are 2 files that need to be created for testbot.py to run...

    server
    ./lists/<numberLists>

Currently uses config file 'server' in irc-sms-bot directory to
configure server. Format is as follows:

    Server.Address
    PortNumber
    Channel
    MasterPassw0rd
    gmail_account@gmail.com
    PlainTextGmailPassword
    
    Example:
    
        mywebsite.com
        6667
        #l337h4x0r5
        hunter2*
        testemail@gmail.com
        hunter2**
    
    * Using 'hunter2' as a password is not advisable.
    ** Duplicating passwords, especially 'hunter2' is also not advisable.
    
The numbers you wish to text are also stored as plain text in a file named
whatever you'd like in the irc-sms-bot/lists directory as follows:

    Number1
    Number2
    Number3
    
    Example:
    
        8005551234
        1234567891
        1231231234
      
**TODO:**

    - Passwords unique to address book
    - Improve overall stability
    - Make it so pygooglevoice doesn't have to be installed on the machine
