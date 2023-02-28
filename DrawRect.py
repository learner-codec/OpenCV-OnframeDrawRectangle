import cv2
import numpy as np
import math
import keyboard
# Define a callback function for mouse events
import json
class DrawRect:
    def __init__(self):
        self.rects={}
        self.points={}
        self.frame=None
        self.point_counter = 0
        self.rect_counter = 0
        self.default_color = (0,0,255)
        self.select_color = (0,255,0)
        self.selected_point = None
        self.file_name = "data.json"
    def pass_frame(self,frame):
        self.frame = frame
    def collect_point(self,points:list):
        self.point_counter += 1
        print("point counter", self.point_counter)
        print("rectangles = ", self.rects)
        self.points["point_{}".format(self.point_counter)] = [points, self.default_color]
        self.rects["rect_{}".format(self.rect_counter)] = self.points
        if self.point_counter % 4 == 0:
            self.point_counter = 0
            self.rect_counter+=1
            self.points = {}
    def draw_points(self):
        for rect in self.rects:
            if(len(self.rects[rect])>0):
                for points in self.rects[rect]:
                    cv2.circle(self.frame, tuple(self.rects[rect][points][0]), 5,  self.rects[rect][points][1], -1)
        return self.frame

    def draw_rect(self):
        # self.frame = self.draw_points()
        for rect_name, rect_points in self.rects.items():
            if len(rect_points)<4:
                print("rect name", rect_name,"rect len", len(rect_points))
                return self.frame
            keys = [key for key in rect_points]
            cv2.line(self.frame, rect_points[keys[0]][0], rect_points[keys[1]][0], (0, 255, 0), 2)
            cv2.line(self.frame, rect_points[keys[1]][0], rect_points[keys[2]][0], (0, 255, 0), 2)
            cv2.line(self.frame, rect_points[keys[2]][0], rect_points[keys[3]][0], (0, 255, 0), 2)
            cv2.line(self.frame, rect_points[keys[3]][0], rect_points[keys[0]][0], (0, 255, 0), 2)
        return self.frame
    def del_point(self):
        return None

    def check_selected(self,points):
        closest_dist = float('inf')
        closest_point = None
        closest_rect = None
        point_name_ = None

        for rect_name, rect_points in self.rects.items():
            print(rect_points)
            for point_name, point_data in rect_points.items():
                rect_point = point_data[0]
                dist = math.sqrt((points[0] - rect_point[0]) ** 2 + (points[1] - rect_point[1]) ** 2)
                if dist < 5.0:
                    closest_dist = dist
                    closest_point = rect_point
                    closest_rect = rect_name
                    point_name_ = point_name
        return closest_rect, point_name_
    def set_selected(self,points):
        rect, point_name = self.check_selected(points)
        self.selected_point = [rect,point_name]
    def move_selected(self,points):

        # print("the pointn ", self.rects[rect][point][0],"== ", points)
        if self.selected_point[0] and self.selected_point[1]:
            self.rects[self.selected_point[0]][self.selected_point[1]][0] = points
    def get_data(self):
        return self.rects
    def save(self,file_name = None):
        if file_name is None:
            file_name = self.file_name
        try:
            removable = []
            for rect_name, rect_points in self.rects.items():
                if len(rect_points) < 4:
                    removable.append(rect_name)
            for r in removable:
                print("insufficient points. removing rect=> ", r)
                del self.rects[r]
                self.points={}
                self.point_counter = 0
            with open(file_name, "w") as outfile:
                json.dump(self.rects, outfile)
            return True
        except Exception as e:
            print("error while writing file ", e)
        return False
    def load(self, file_name = None):
        if file_name is None:
            file_name = self.file_name
        try:
            with open("data.json", "r") as infile:
                self.rects = json.load(infile)
            return True
        except Exception as e:
            print("error loading file ", e)
        return False
