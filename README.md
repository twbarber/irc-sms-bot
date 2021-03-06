##IRC SMS Bot

#####An IRC bot written in Python 2 that sends SMS messages to a desired list of numbers.<br>
A **Google Voice account** and **Linux OS** are requierd. Configuration of server and data files
are also necessary to run after downloading.

Uses **pygooglevoice** library by Joe McCall & Justin Quick<br>
**GitHub:** https://github.com/pettazz/pygooglevoice<br>
**Full Documentation:** http://sphinxdoc.github.com/pygooglevoice/

### Setup

You need to run the general setup for pygooglevoice before you
can run this bot. I will look into a fix for this soon.

After pygooglevoice is installed, there are 2 files that need to be created for smsbot to run...

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
    
### Generating your Number Lists 

The numbers you wish to text are also stored as plain text in a file named
whatever you'd like in the irc-sms-bot/lists directory as follows:

    Number1
    Number2
    Number3
    
    Example:
    
        8005551234
        1234567891
        1231231234
      
### Commands

    Send SMS - sendsms [NumberList]
    Get Active Number Lists - smsbot lists
    Help - smsbot help
      
**TODO:**

    - Passwords unique to address book
    - Change timeout function to work outside of linux
    - Improve overall stability
    - Make it so pygooglevoice doesn't have to be installed on the machine
