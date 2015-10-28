"""

"""
import sys
import os #for later implementation of custom images
import pygame as pg
from pygame.locals import *

class PlayField(object):
    def __init__(self, screenLength, screenWidth, cellRows, cellSize, surface):
        self.cellSize = cellSize
        self.cellRows = cellRows
        self.cellCols = cellRows
        self.gridX = (screenLength/2) - (self.cellRows*cellSize)/2
        self.gridY = (screenWidth/2) - (self.cellCols*cellSize)/2
        self.model  = []
        self.model += [[1]*self.cellCols for row in xrange(self.cellRows)]
        #testCode
        self.modelWidth = self.cellSize*self.cellRows
        grey = pg.Color(192,192,192)
        slightlyDarkerGrey = (85,85,85)
        self.blockColor1 = grey
        self.blockColor2 = slightlyDarkerGrey
        #list of rectangle coordinates for later drawing
        self.rectList = []
        for row in xrange(self.cellRows):
            addend = []
            for col in xrange(self.cellCols):
                rect = pg.Rect(self.gridX+(cellSize*col), self.gridY+(cellSize*row), cellSize, cellSize)
                addend.append(rect)
            self.rectList.append(addend)
        self.surface = surface
        self.killzone = pg.Rect(0,800,1000, 200)

    def drawView(self):
        alt = 0
        for row in xrange(self.cellRows):
            for col in xrange(self.cellCols):
                if (self.rectList[row][col]):
                    if alt % 2 == 0:
                        color = self.blockColor1
                    else:
                        color =self.blockColor2
                    alt += 1    
                    pg.draw.rect(self.surface, color, self.rectList[row][col])
                else:
                    alt += 1
            alt +=1

    def transform(self, clockwise):
        n = self.cellRows
        #print self.model 
        if (clockwise):
            for row in xrange(self.cellRows/2):
                for col in xrange(self.cellCols/2):
                    tempModel = self.model[row][col]
                    tempRect = self.rectList[row][col]
                    self.model[row][col] = self.model[col][n-1-row]
                    self.rectList[row][col] = self.rectList[col][n-1-row]
                    self.model[col][n-1-row] = self.model[n-1-row][n-1-col]
                    self.rectList[col][n-1-row] = self.rectList[n-1-row][n-1-col]
                    self.model[n-1-row][n-1-col] = self.model[n-1-col][row]
                    self.rectList[n-1-row][n-1-col] = self.rectList[n-1-col][row]
                    self.model[n-1-col][row] = tempModel
                    self.rectList[n-1-col][row] = tempRect
        else:
            #possible improvement: actually do this in the opposite direction
            for iterations in xrange(3):
                for row in xrange(self.cellRows/2):
                    for col in xrange(self.cellCols/2):
                        tempModel = self.model[row][col]
                        tempRect = self.rectList[row][col]
                        self.model[row][col] = self.model[col][n-1-row]
                        self.rectList[row][col] = self.rectList[col][n-1-row]
                        self.model[col][n-1-row] = self.model[n-1-row][n-1-col]
                        self.rectList[col][n-1-row] = self.rectList[n-1-row][n-1-col]
                        self.model[n-1-row][n-1-col] = self.model[n-1-col][row]
                        self.rectList[n-1-row][n-1-col] = self.rectList[n-1-col][row]
                        self.model[n-1-col][row] = tempModel
                        self.rectList[n-1-col][row] = tempRect

    # def checkKeys(self, keys):#Modified from Sean J. McKiernan 'Mekire'
    #     if keys[pg.K_q]:
    #         self.transform(True)
    #     elif keys[pg.K_e]:
    #         self.transform(False)
    #     elif keys[pg.K_r]:
    #         self.reset()

    def reset(self):
        for row in xrange(self.cellRows):
            addend = []
            for col in xrange(self.cellCols):
                rect = pg.Rect(self.gridX+(self.cellSize*col), self.gridY+(self.cellSize*row), self.cellSize, self.cellSize)
                addend.append(rect)
            self.rectList.append(addend)

    def update(self):
        self.drawView()
        pg.draw.rect(self.surface, (255,20, 20), self.killzone)
