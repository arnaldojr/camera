#!/usr/bin/env python
import rospy # Python library for ROS
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge, CvBridgeError
import cv2

class CameraPublisher(object):
    def __init__(self):
        self.setup_cam()
        self.loop()

    def setup_cam(self):
        """
        Publish the image from raspberry pi camera v2
        """

        # Tells rospy the name of the node.
        rospy.init_node('camera_publisher', anonymous=True)

        # Publishing to the "video_frames" topic using the message type Image

        self.pub = rospy.Publisher('/camera/image', Image, queue_size=10)
        print ("camera node inicializado")
    def loop(self):
        # go through the loop 120 times per second
        rate = rospy.Rate(9)

        # Create a VideoCapture object The argument '0' gets the default webcam.
       
        cap = cv2.VideoCapture(cv2.CAP_V4L2)
        bridge = CvBridge()
        print("criando pipline")
        

        while not rospy.is_shutdown():
            # Capture frame-by-frame
            # This method returns True/False as well as the video frame.
            ret, frame = cap.read()
            image_shape = None
            if ret == True:
                # Print debugging information to the terminal
                rospy.loginfo('publishing video frame')

                # converts an OpenCV image to a ROS image message
                frame = cv2.flip(frame,0)
                frame = cv2.flip(frame,1)
                img_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

                # Publish the image.
                self.pub.publish(img_msg)

                # Sleep just enough to maintain the desired rate
                rate.sleep()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        CameraPublisher()
    except rospy.ROSInterruptException:
        pass



