
#!/usr/bin/env python

import rospy

from std_msgs.msg import String

class player:
    def down(self):
        self.publisher.publish('finish')
        if self.length<18:
            print('game over')
        else:
            print('Congratulations')
    def __init__(self):
        self.length = 1
        self.flag = False
        self.subsriber = rospy.Subscriber('answerTopic', String, self.callback)
        self.publisher = rospy.Publisher('shutdownTopic', String, queue_size = 10) 
        rospy.init_node('main')
        rospy.wait_for_service('myService')
        rospy.on_shutdown(self.down)
        rospy.spin()


    def callback(self, data):
        if data.data == 'dead':
            rospy.signal_shutdown('dead')
        elif data.data == 'move next':
            print('Move next')
        else:
            rospy.signal_shutdown('finish')
if __name__ == '__main__':
    print('Welcome to the game. Use l or r letters to play')
    player = player()
