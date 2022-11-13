#!/usr/bin/env python
from random import randint
import rospy
from std_msgs.msg import String
from glassbridge.srv import myService, myServiceResponse

class service:
    def generateSequence(self):
        mask = {0:'l', 1:'r'}
        array = [mask[randint(0,1)] for i in range(18)]
        print(array)
        return ''.join(array)
        
    def on_shutdown(self):
        print('game ended')
      
    def __init__(self):
        self.sequence = self.generateSequence()
        self.s = rospy.Service('myService', myService, self.callback)
        rospy.init_node('service')
        self.position = 0 
        self.publisher = rospy.Publisher('answerTopic', String, queue_size=10)
        self.subsriber = rospy.Subscriber('shutdownTopic', String, self.answer) 
        rospy.on_shutdown(self.on_shutdown)
        rospy.spin()
        
    def answer(self, data):
        rospy.signal_shutdown('dead')
        
    def callback(self, req):
        if self.sequence[self.position] == req.nextLetter:
            self.position+=1
            if self.position == 18:
                self.position = 0
                self.publisher.publish('win')
                return myServiceResponse('win')
            else:
                self.publisher.publish('move next')
                return myServiceResponse('move next')
        else:
            self.position+=1
            self.publisher.publish('dead')
            return myServiceResponse('dead')
            
            
if __name__ == '__main__':
    service = service()
