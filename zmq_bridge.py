#! /usr/bin/env python
#-*- coding: utf-8 -*-

'''
This is a simple example how to translate ROS messages into ZeroMQ messages.
'''

import random
import sys
import time

import zmq

import rospy
from std_msgs.msg import String


PORT = 5556


class ZMQBridge(object):
    def __init__(self, *args , **kwargs):
        super(ZMQBridge, self).__init__(*args, **kwargs)
        rospy.init_node('zmq_bridge')

        self.__create_ros_communication()
        self.__create_zmq_communication()

    def __create_ros_communication(self):
        self.__word_sub = rospy.Subscriber('/word', String, self.receive_ros_word)

    def __create_zmq_communication(self):
        context = zmq.Context()
        self.__word_socket = context.socket(zmq.PUB)
        self.__word_socket.bind('tcp://*:{p}'.format(p=PORT))

    def publish_zmq_word(self, word):
        print('Publishing')
        self.__word_socket.send(word)
        
    def receive_ros_word(self, word):
        self.publish_zmq_word(word.data)


if __name__ == '__main__':
    zmq_bridge = ZMQBridge()

    rospy.spin()
    
