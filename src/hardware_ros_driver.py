#!/usr/bin/env python	
# -- coding: utf-8 --	
# license removed for brevity	

import serial
import json
import time
import rospy
from uwb_hardware_driver.msg import AnchorScan

port = "/dev/ttyACM1"
baud_rate = 19200

ser = serial.Serial(port, baud_rate)

def init_anchors():

    anchor_info = {
        0: [2.675, -0.09, 1.94],        # S
        1: [3.42, 4.58, 2.07],	        # C
        2: [12.475, -0.015, 2.4],	    # B
        3: [12.473, 4.543, 2.35] 	    # A
    }

    return anchor_info


def pub():

    rospy.init_node("hardware_ros_driver", anonymous = True)
    pub = rospy.Publisher('IPS', AnchorScan, queue_size = 2)
    rate = rospy.Rate(5)

    anchor_info = init_anchors()
    anchor_id = list(anchor_info.keys())
    anchor_coords = list(anchor_info.values())

    anchor_coords_x = list()
    anchor_coords_y = list()
    anchor_coords_z = list()

    for item in anchor_coords:
        anchor_coords_x.append(item[0])
        anchor_coords_y.append(item[1])
        anchor_coords_z.append(item[2])


    while not rospy.is_shutdown():

        msg = AnchorScan()

        msg.header.stamp = rospy.Time.now()
        msg.AnchorID = anchor_id
        msg.x = anchor_coords_x
        msg.y = anchor_coords_y
        msg.z = anchor_coords_z
        
        data = ser.readline()

        if data[0] == "{":
            parsed_data = (json.loads(data))
            print(json.dumps(parsed_data)) #, indent=4))
            #print(parsed_data)

            msg.tdoa_of_anchors = [float(parsed_data["DCS"])/100, float(parsed_data["DBS"])/100, float(parsed_data["DAS"])/100]
        
        pub.publish(msg)	
        rate.sleep()	


if __name__ == '__main__':	
    try:		
        pub()	
    except rospy.ROSInterruptException:	
        pass
