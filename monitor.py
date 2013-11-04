#!/usr/bin/python
#
# Airsoft Turret Target Tracking 
#
# Author: Adam Meyers (madboo@d0ubletap.net)
#
# This code leverages the OpenCV library to track a target using a webcam
# Borrowed from "http://stackoverflow.com/questions/3374828/how-do-i-track-motion-using-opencv-in-python"
#
#


# Import OpenCV and the fire_control.py controller
import cv
from fire_control import fire_control

class Target:

    def __init__(self):
# The init function will initiate the capture object which will by default capture from the first available webcam
        self.capture = cv.CaptureFromCAM(0) # Initialize capture object
        cv.NamedWindow("Target", 1) # Create a named Window to display webcam output
        self.firecontrol = fire_control() # Initiate the fire control object
        self.pos=[0,0] # Define the current position of the target

    def run(self):
        frame = cv.QueryFrame(self.capture) # Capture the first frame
        frame_size = cv.GetSize(frame) # Get the size of the frame in pixels e.g. 640x480
        color_image = cv.CreateImage(cv.GetSize(frame), 8, 3)
        grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
        moving_average = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)
        first = True

        while True:
            closest_to_left = cv.GetSize(frame)[0]
            closest_to_right = cv.GetSize(frame)[1]

            color_image = cv.QueryFrame(self.capture)

            # Smooth to get rid of false positives
            cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 3, 0)

            if first:
                difference = cv.CloneImage(color_image)
                temp = cv.CloneImage(color_image)
                cv.ConvertScale(color_image, moving_average, 1.0, 0.0)
                first = False
            else:
                cv.RunningAvg(color_image, moving_average, 0.020, None)

            # Convert the scale of the moving average.
            cv.ConvertScale(moving_average, temp, 1.0, 0.0)

            # Minus the current frame from the moving average.
            cv.AbsDiff(color_image, temp, difference)

            # Convert the image to grayscale.
            cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)

            # Convert the image to black and white.
            cv.Threshold(grey_image, grey_image, 70, 255, cv.CV_THRESH_BINARY)

            # Dilate and erode to get people blobs
            cv.Dilate(grey_image, grey_image, None, 18)
            cv.Erode(grey_image, grey_image, None, 10)

            storage = cv.CreateMemStorage(0)
            contour = cv.FindContours(grey_image, storage, cv.CV_RETR_CCOMP, cv.CV_CHAIN_APPROX_SIMPLE)
            points = []

            while contour:
                bound_rect = cv.BoundingRect(list(contour))
                contour = contour.h_next()

                pt1 = (bound_rect[0], bound_rect[1])
                pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])
                points.append(pt1)
                points.append(pt2)
                cv.Rectangle(color_image, pt1, pt2, cv.CV_RGB(255,0,0), 1)

            if len(points):
                center_point = reduce(lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), points)
                cv.Circle(color_image, center_point, 40, cv.CV_RGB(255, 255, 255), 1)
                cv.Circle(color_image, center_point, 30, cv.CV_RGB(255, 100, 0), 1)
                cv.Circle(color_image, center_point, 20, cv.CV_RGB(255, 255, 255), 1)
                cv.Circle(color_image, center_point, 10, cv.CV_RGB(255, 100, 0), 1)

                xangle = 0
                if center_point[0] < 320:
                  xangle = int(90 + ((center_point[0]-320)/22.857))
                elif center_point[0] == 320:
                  xangle = 90
                else:
                  xangle = int(90 + center_point[0] / 22.857)
                yangle = 0
                if center_point[1] < 240:
                  yangle = int(90 + center_point[1] /12) 
                elif center_point[1] == 240:
                  yangle = 93
                else:
                  yangle = int(90 - ((center_point[1] - 240)/12)) 

                print "Xangle = ",xangle
                self.firecontrol.sendcoord(0xff,xangle,yangle)
                current_position =center_point 
                self.firecontrol.fire(0xfe)
                print "Located at: ",current_position
#               fire_control.engage()
#               print "Fire: ", self.pos
                    

                self.pos = center_point
            cv.ShowImage("Target", color_image)
            # Listen for ESC key
            c = cv.WaitKey(7) % 0x100
            if c == 27:
                break

if __name__=="__main__":
    t = Target()
    t.run()
