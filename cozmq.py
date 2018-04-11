#! /usr/bin/env python3
#-*- coding: utf-8 -*-

'''
This is a simple example how to call Cozmo SDK functions triggered by incoming ZeroMQ messages.
A Cozmo device musts be connected to your mobile device, which has to be connected via USB to your host in
USB debugging mode.
'''


import sys

import zmq

import cozmo


PORT = 5556


class CoZMQ(object):
    def __init__(self, *args, **kwargs):
        super(CoZMQ, self).__init__(*args, **kwargs)

        self.__create_zmq_communication()

        while True:
            string = self.__word_socket.recv()
            print(string)
            cozmo.run_program(self.cozmo_say(string.decode('utf-8')))

    def __create_zmq_communication(self):
        context = zmq.Context()
        self.__word_socket = context.socket(zmq.SUB)
        self.__word_socket.connect('tcp://localhost:{p}'.format(p=PORT))
        self.__word_socket.setsockopt(zmq.SUBSCRIBE, b'')

    @staticmethod
    def cozmo_say(text):
        def program(robot):
            robot.say_text(text).wait_for_completed() 
        return program

    @staticmethod
    def cozmo_set_head_angle(angle):
        def program(robot):
            robot.set_head_angle(angle).wait_for_completed() 
        return program


if __name__ == '__main__':
    cozmq = CoZMQ()

