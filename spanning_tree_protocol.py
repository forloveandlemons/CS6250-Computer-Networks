# Project 2 for OMS6250
#
# This defines a Switch that can can send and receive spanning tree 
# messages to converge on a final loop free forwarding topology.  This
# class is a child class (specialization) of the StpSwitch class.  To 
# remain within the spirit of the project, the only inherited members
# functions the student is permitted to use are:
#
# self.switchID                   (the ID number of this switch object)
# self.links                      (the list of swtich IDs connected to this switch object)
# self.send_message(Message msg)  (Sends a Message object to another switch)
#
# Student code MUST use the send_message function to implement the algorithm - 
# a non-distributed algorithm will not receive credit.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2016 Michael Brown, updated by Kelly Parks
#           Based on prior work by Sean Donovan, 2015


from Message import *
from StpSwitch import *


class Switch(StpSwitch):
    def __init__(self, idNum, topolink, neighbors):
        # Invoke the super class constructor, which makes available to this object the following members:
        # -self.switchID                   (the ID number of this switch object)
        # -self.links                      (the list of swtich IDs connected to this switch object)
        super(Switch, self).__init__(idNum, topolink, neighbors)

        # TODO: Define a data structure to keep track of which links are part of / not part of the spanning tree.
        self.root = idNum
        self.distance = 0
        self.activeLinks = {}
        self.switchThrough = idNum
        for neighbor in self.links:
            self.activeLinks[neighbor] = False

    def send_initial_messages(self):
        # TODO: This function needs to create and send the initial messages from this switch.
        #      Messages are sent via the superclass method send_message(Message msg) - see Message.py.
        #      Use self.send_message(msg) to send this.  DO NOT use self.topology.send_message(msg)
        for neighbor in self.links:
            message = Message(self.root, self.distance, self.root, neighbor, False)
            self.send_message(message)
        return

    def process_message(self, message):
        # TODO: This function needs to accept an incoming message and process it accordingly.
        #      This function is called every time the switch receives a new message.
        if self.root > message.root or (self.root == message.root and message.distance + 1 < self.distance):
            self.root = message.root
            self.distance = message.distance + 1
            self.switchThrough = message.origin
            for neighbor in self.links:
                if neighbor == message.origin:
                    self.activeLinks[neighbor] = True
                    self.send_message(Message(self.root, self.distance, self.switchID, neighbor, True))
                else:
                    self.activeLinks[neighbor] = False
                    self.send_message(Message(self.root, self.distance, self.switchID, neighbor, False))
        elif self.root == message.root and message.distance + 1 == self.distance and message.origin < self.switchThrough:
            # disconnect from old switchThrough
            self.activeLinks[self.switchThrough] = False
            self.send_message(Message(self.root, self.distance, self.switchID, self.switchThrough, False))
            # update switchThrough to message origin and connect
            self.switchThrough = message.origin
            self.activeLinks[message.origin] = True
            self.send_message(Message(self.root, self.distance, self.switchID, message.origin, True))
        else:
            self.activeLinks[message.origin] = message.pathThrough

    def generate_logstring(self):
        # TODO: This function needs to return a logstring for this particular switch.  The
        #      string represents the active forwarding links for this switch and is invoked
        #      only after the simulaton is complete.  Output the links included in the
        #      spanning tree by increasing destination switch ID on a single line.
        #      Print links as '(source switch id) - (destination switch id)', separating links
        #      with a comma - ','.
        #
        #      For example, given a spanning tree (1 ----- 2 ----- 3), a correct output string
        #      for switch 2 would have the following text:
        #      2 - 1, 2 - 3
        #      A full example of a valid output file is included (sample_output.txt) with the project skeleton.
        l = []
        for active_link in sorted(self.activeLinks.iterkeys()):
            if self.activeLinks[active_link] == True:
                l.append('{} - {}'.format(self.switchID, active_link))
        return ', '.join(l)
