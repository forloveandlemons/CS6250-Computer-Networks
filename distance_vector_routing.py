# Project 3 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *

class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        #TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data
        self.costs = {}
        self.costs[self.name] = 0


    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight '''

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        for each in self.incoming_links:
            self.send_msg((self, self.costs), each.name)


    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages
        update = False
        for (sender, msg) in self.messages:
            for node in msg:
                if node in self.costs:
                    if self.costs[node] > -99 and node != self.name:
                        if msg[node] == -99:
                            update = True
                            self.costs[node] = -99
                        elif self.costs[node] > msg[node] + int(self.get_outgoing_neighbor_weight(sender.name)):
                            update = True
                            self.costs[node] = max(-99, msg[node] + int(self.get_outgoing_neighbor_weight(sender.name)))
                else:
                    if msg[node] == -99:
                        self.costs[node] = -99
                    else:
                        self.costs[node] = max(-99, msg[node] + int(self.get_outgoing_neighbor_weight(sender.name)))
                    update = True

        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances
        if update:
            for neighbor in self.incoming_links:
                self.send_msg((self, self.costs), neighbor.name)


    def log_distances(self):
        ''' This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 '''
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.        
        # add_entry("A", "A0,B1,C2")
        log_str = []
        for each in self.costs:
            log_str.append('{}{}'.format(each, str(self.costs[each])))
        add_entry(self.name, ','.join(log_str))