#!/usr/bin/env python
import sys
import rospy
from glassbridge.srv import myService

class player:
    def down(self):
        print('game over')
        self.flag = True
    def __init__(self):
        self.sequence = ''
        self.flag = False
        rospy.init_node('main')
        self.r = rospy.Rate(10)
        rospy.wait_for_service('myService')
        rospy.on_shutdown(self.down)
        try:
            self.s = rospy.ServiceProxy('myService', myService)

        except rospy.ServiceException:
            print('failed to connect to to service')

    def start(self):
        while len(self.sequence)<18:
            if self.flag:
                break
            self.Input()
        if not self.flag:
            rospy.loginfo('Congratulations')
    def Input(self):
        letter = ''
        while letter != 'l' and letter != 'r':
            letter = input().lower()
            if letter !='l' and letter !='r':
                print('Wrong input')
        response = self.s(letter, self.sequence)
        if response.answer == 'dead':
            rospy.signal_shutdown('dead')
        else:
            self.sequence+=letter
            rospy.loginfo('Move next')
if __name__ == '__main__':
    print('Welcome to the game. Use l or r letters to play')
    player = player()
    player.start()
