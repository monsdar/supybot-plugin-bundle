###
# Copyright (c) 2013, Nils Brinkmann
# All rights reserved.
#
#
###

import os
import cPickle

import supybot.callbacks as callbacks
import supybot.conf as conf
import supybot.ircutils as ircutils
import supybot.plugins as plugins
import supybot.utils as utils
from supybot.commands import *

class BundleItem():
    def __init__(self, name=""):
        self.name = name
        self.commands = []

class Bundle(callbacks.Plugin):
    """Allows to define multiple commands which are executed altogether then."""
    def __init__(self, irc):
        self.__parent = super(Bundle, self)
        self.__parent.__init__(irc)
        
        #a dict is easier to search
        self.items = {}
    
        #read the items from file
        filepath = conf.supybot.directories.data.dirize('Bundle.db')
        if( os.path.exists(filepath) ):
            try:
                self.items = cPickle.load( open( filepath, "rb" ) )
            except EOFError as error:
                irc.reply("Error when trying to load existing data.")
                irc.reply("Message: " + str(error))
                
    def die(self):
        #Pickle the items to a file
        try:
            filepath = conf.supybot.directories.data.dirize('Bundle.db')
            cPickle.dump( self.items, open( filepath, "wb" ) )
        except cPickle.PicklingError as error:
            print("Info: Error when pickling to file...")
            print(error)
            
    
    def list(self, irc, msg, args):
        """takes no arguments
        
        Displays all the bundles"""
        if self.items:
            for name in self.items.keys():
                irc.reply( name )
        else:
            irc.reply( "There are no bundles stored" )
    list = wrap(list)
    
    def add(self, irc, msg, args, name, command):
        """<name> <command>

        Adds a command to the bundle <name>.
        The <name> must be without spaces.
        If there is no such bundle, it will be created
        """
        if( name in  self.items):
            item = self.items[name]
        else:
            item = BundleItem(name)
            
        item.append(command)
        self.items[name] = item
        irc.replySuccess()       
    add = wrap(add, ['somethingWithoutSpaces', 'text'])
    
    def remove(self, irc, msg, args, name):
        """<name>
        
        Removes the given <name> from the plugin."""
        if not( name in self.items ):
            irc.error('There is no such name as ' + name)
            return
    
        del self.items[name]
        irc.replySuccess()
    remove = wrap(remove, ['somethingWithoutSpaces'])

Class = Bundle


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
