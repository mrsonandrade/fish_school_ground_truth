#!/usr/bin/env python
import rospy
import tf
import numpy as np

import pyswarming.behaviors as pb
from utils import ensure_negative_pi_to_pi

from std_msgs.msg import ColorRGBA
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class HeroExample(object):
    """ docstring for HeRo Example """

    def __init__(self,
                 robot_id="2"):

        self.robot_id = robot_id

        rospy.init_node('hero_demo', anonymous=True)

        # getting the pose from the neighbors
        topics = [topic[0] for topic in rospy.get_published_topics("/")]
        self.odoms = {}
        namespaces = []
        for topic in topics:
            if "odom" in topic:
                namespaces.append(topic.split("/")[1])

        rospy.loginfo("Founded robots:")
        for namespace in namespaces:
            rospy.loginfo(">> " + namespace)
        self.robots = {}
        for namespace in namespaces:
            pub_cmd = rospy.Publisher(
                '/'+namespace+"/cmd_vel", Twist, queue_size=1)
            pub_color = rospy.Publisher(
                '/'+namespace+"/led", ColorRGBA, queue_size=1)
            self.robots[namespace] = [pub_cmd, pub_color, None]
            rospy.Subscriber('/'+namespace + "/odom",
                             Odometry, self.odom_cb, namespace)
        
    def odom_cb(self, msg, namespace):
        w = (msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
             msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)
        euler = tf.transformations.euler_from_quaternion(w)
        row, pitch, yaw = euler
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        self.robots[namespace][2] = np.array([x, y, yaw])

    def run(self):
        rate = rospy.Rate(5)
        rospy.loginfo("[HeRo Example]: Running!")

        vel = Twist()

        robot_names = list(self.robots.copy().keys())
        r_i_index = robot_names.index("hero_"+self.robot_id)

        r_leader_index = robot_names.index("hero_0")

        alfa_beta_dict = {'v_i':   [1.14, 3.17],
                          'a_A_si':[0.08, 0.18],
                          'a_R_si':[0.16, 0.08],
                          'a_T_si':[0.27, 0.32]}

        while not rospy.is_shutdown():

            if np.any(np.asarray([self.robots[r][2] for r in robot_names]) == None):
                rate.sleep()
                continue
            
            try:
                robot_positions = np.asarray([[self.robots[r][2][0],
                                           self.robots[r][2][1], 0] for r in robot_names])

                leader = robot_positions[r_leader_index]
                distance = np.linalg.norm(leader - robot_positions[r_i_index])

                r_i = robot_positions[r_i_index]
                r_j = np.delete(robot_positions, np.array([r_i_index]), axis=0)
                
                #
                a_R_i =  np.random.beta(a=1.25, b=4.28, size=None)*(325.0/720.0)*2.0
                d_i =    2
                
                v_i =    np.random.beta(a=alfa_beta_dict['v_i'][0],    b=alfa_beta_dict['v_i'][1],    size=None)*33.0
                a_A_si = np.random.beta(a=alfa_beta_dict['a_A_si'][0], b=alfa_beta_dict['a_A_si'][1], size=None)
                a_R_si = np.random.beta(a=alfa_beta_dict['a_R_si'][0], b=alfa_beta_dict['a_R_si'][1], size=None)
                a_T_si = np.random.beta(a=alfa_beta_dict['a_T_si'][0], b=alfa_beta_dict['a_T_si'][1], size=None)
        
                r_cn = v_i*(a_A_si*pb.aggregation(r_i, r_j)
                            + a_R_si*pb.repulsion(r_i, r_j, a_R_i, d_i)
                            + a_T_si*pb.target(r_i, leader))
                #

                vel.linear.x = max(min(0.08, distance), 0.04) #hero
                vel.angular.z = ensure_negative_pi_to_pi(np.arctan2(r_cn[1], r_cn[0])
                                                         - self.robots["hero_"+self.robot_id][2][2])

                print("Error: {} - u: [{},{}]".format(
                    distance, vel.linear.x, vel.angular.z))
                self.robots["hero_"+self.robot_id][0].publish(vel)
                color = ColorRGBA()
                color.r = 0.0
                color.g = 1.0
                color.b = 0.0
                color.a = 1.0
                self.robots["hero_"+self.robot_id][1].publish(color)
            except Exception as e:
                print(e)

            rate.sleep()

# Main function
if __name__ == '__main__':
    try:
        demo = HeroExample()
        demo.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("[HeRo Example]: Closed!")
