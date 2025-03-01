# encoding: utf-8

###########################################################################################################
#
#
#	Filter without dialog plug-in
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from math import sqrt

def getIntersection( x1,y1, x2,y2, x3,y3, x4,y4 ):
	px = ( (x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) ) 
	py = ( (x1*y2-y1*x2)*(y3-y4)-(y1-y2)*(x3*y4-y3*x4) ) / ( (x1-x2)*(y3-y4)-(y1-y2)*(x3-x4) )
	return px, py

def getDist(a, b):
	dist = sqrt( (b.x - a.x)**2 + (b.y - a.y)**2 )
	return dist

def remap( oldValue, oldMin, oldMax, newMin, newMax):
	try:
		oldRange = (oldMax - oldMin)  
		newRange = (newMax - newMin)  
		newValue = (((oldValue - oldMin) * newRange) / oldRange) + newMin
		return newValue
	except:
		pass

class GreenHarmony(FilterWithoutDialog):
	
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': 'Green Harmony',
			'de': 'Grüne Harmonie',
			'fr': 'Harmonie verte',
			'es': 'Harmonía verde',
			'cs': 'Zelená harmonie',
			'pt': 'Harmonia verde',
			'ru': 'Зелёная гармония',
			'jp': '緑の調和',
			'ko': '녹색 조화',
			'zh': '🌱绿色和谐',
			})

	@objc.python_method
	def filter(self, layer, inEditView, customParameters):
		# Based on algorithm suggestion by Simon Cozens:
		# https://gist.github.com/simoncozens/3c5d304ae2c14894393c6284df91be5b

		selectionCounts = bool(inEditView) and bool(layer.selection)
		if layer.shapes:
			for shape in layer.shapes:
				if type(shape) == GSPath:
					for node in shape.nodes:
						if not selectionCounts or node in layer.selection:
							if node.type == CURVE and node.smooth:
								if node.nextNode and node.prevNode and node.nextNode.type == OFFCURVE and node.prevNode.type == OFFCURVE:
									# adjacent handles:
									N = node.nextNode
									NN = node.nextNode.nextNode
									P = node.prevNode
									PP = node.prevNode.prevNode
								
									# find intersection of lines created by offcurves
									xIntersect, yIntersect = (
										getIntersection( 
											N.x, N.y, NN.x, NN.y,
											P.x, P.y, PP.x, PP.y,
											) 
										)
									intersection = NSPoint( xIntersect, yIntersect )
								
									# find ratios
									r0 = getDist( NN, N ) / getDist( N, intersection )
									r1 = getDist( intersection, P ) / getDist( P, PP )
									ratio = sqrt(r0 * r1)
								
									# set oncurve point position based on that ratio:
									t = ratio / (ratio+1)
									node.x = remap( t, 0, 1, N.x, P.x ) 
									node.y = remap( t, 0, 1, N.y, P.y )

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
