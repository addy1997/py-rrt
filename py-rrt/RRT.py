# Author: Adwait Naik @addy1997 | Created on: 9/01/2019
#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import sys
import pygame
import random
from math import *
from pygame import *


class RRT(object):

    def __init__(self, point, parent):
        super(RRT, self).__init__()
        self.point = point
        self.parent = parent

XDIM = 640
YDIM = 480
windowSize = [XDIM, YDIM]
EPS = 10.0
GAME_LEVEL = 1
GOAL_RADIUS = 10
MIN_DISTANCE_TO_ADD = 1.0
NUMNODES = 5000
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode(windowSize)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)
cyan = (0, 100, 78)

count = 0
rectObs = []

def calculate_distance(x, y):  # distance between two points
    return sqrt((x[0] - y[0]) * (x[0] - y[0]) + (x[1] - y[1]) * (x[1]
                - y[1]))
                
def point_circle_collision(x, y, radius):
    distance = calculate_distance(x, y)
    if distance <= radius:
        return True
    return False

def distance_between_nodes(x, y):
    if calculate_distance(x, y) < EPS:
        return y
    else:
        theta = atan2(y[1] - x[1], y[0] - x[0])
        return (x[0] + EPS * cos(theta), x[1] + EPS * sin(theta))

def collides(p):  # check if point collides with the obstacle
    for rect in rectObstacles:
        if rect.collidepoint(p) == True:
            return True
    return False

def get_random_clear():
    while True:
        p = (random.random() * XDIM, random.random() * YDIM)
        noCollision = collides(p)
        if noCollision == False:
            return p

def init_obstacles(configNum=0):  # initialized the obstacle
    global rectObstacles
    rectObstacles = []
    print('config ' + str(configNum))
    if configNum == 0:
        rectObstacles.append(pygame.Rect((100, 50), (200, 150)))
        rectObstacles.append(pygame.Rect((400, 200), (200, 100)))
    if configNum == 1:
        rectObstacles.append(pygame.Rect((XDIM / 2.0 - 50, YDIM / 2.0
                             - 100), (100, 200)))
        rectObstacles.append(pygame.Rect((100, 50), (200, 150)))
        rectObstacles.append(pygame.Rect((400, 200), (200, 100)))
    if configNum == 2:
        rectObstacles.append(pygame.Rect((100, 50), (200, 150)))
    if configNum == 3:
        rectObstacles.append(pygame.Rect((100, 50), (200, 150)))

    for rect in rectObstacles:
        pygame.draw.rect(screen, black, rect)

def reset():
    global count
    screen.fill(white)
    init_obstacles(GAME_LEVEL)
    count = 0

def Start_the_Game():

    global count

    initialPoseSet = False
    initialPoint = RRT(None, None)
    goalPoseSet = False
    goalPoint = RRT(None, None)
    currentState = 'init'

    nodes = []
    reset()

    while True:
        if currentState == 'init':
            print('goal point not yet set')
            pygame.display.set_caption('Select Starting Point and then Goal Point'
                    )
            fpsClock.tick(10)
        elif currentState == 'goalFound':
            currentNode = goalNode.parent
            pygame.display.set_caption('Goal Reached')
            print('Goal Reached')

            while currentNode.parent != None:
                pygame.draw.line(screen, red, currentNode.point,
                                 currentNode.parent.point)
                currentNode = currentNode.parent
            optimizePhase = True
        elif currentState == 'optimize':
            fpsClock.tick(0.5)
            pass
        elif currentState == 'buildTree':
            count = count + 1
            pygame.display.set_caption('Performing RRT')
            if count < NUMNODES:
                foundNext = False
                while foundNext == False:
                    rand = get_random_clear()
                    parentNode = nodes[0]
                    for p in nodes:
                        if calculate_distance(p.point, rand) \
                            <= calculate_distance(parentNode.point,
                                rand):
                            newPoint = distance_between_nodes(p.point,
                                    rand)
                            if collides(newPoint) == False:
                                parentNode = p
                                foundNext = True

                newnode = distance_between_nodes(parentNode.point, rand)
                nodes.append(RRT(newnode, parentNode))
                pygame.draw.line(screen, cyan, parentNode.point,
                                 newnode)

                if point_circle_collision(newnode, goalPoint.point,
                        GOAL_RADIUS):
                    currentState = 'goalFound'

                    goalNode = nodes[len(nodes) - 1]
            else:

                print('Ran out of nodes... :(')
                return

        # handle events

        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYUP and e.key == K_ESCAPE:
                sys.exit('Exiting')
            if e.type == MOUSEBUTTONDOWN:
                print('mouse down')
                if currentState == 'init':
                    if initialPoseSet == False:
                        nodes = []
                        if collides(e.pos) == False:
                            print('initiale point set: ' + str(e.pos))

                            initialPoint = RRT(e.pos, None)
                            nodes.append(initialPoint)  # Start in the center
                            initialPoseSet = True
                            pygame.draw.circle(screen, red,
                                    initialPoint.point, GOAL_RADIUS)
                    elif goalPoseSet == False:
                        print('goal point set: ' + str(e.pos))
                        if collides(e.pos) == False:
                            goalPoint = RRT(e.pos, None)
                            goalPoseSet = True
                            pygame.draw.circle(screen, green,
                                    goalPoint.point, GOAL_RADIUS)
                            currentState = 'buildTree'
                else:
                    currentState = 'init'
                    initialPoseSet = False
                    goalPoseSet = False
                    reset()

        pygame.display.update()
        fpsClock.tick(10000)

if __name__ == '__main__':
    Start_the_Game()