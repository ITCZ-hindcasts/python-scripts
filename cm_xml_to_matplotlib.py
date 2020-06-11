#!/usr/bin/env python
#
## This script converts the .xml(ParaView compatible format) colormaps into Matplotlib or MATLAB format
import sys
import matplotlib as mpl
from lxml import etree

## load source xml file
def load_xml(xml):
	try:
		xmldoc = etree.parse(xml)
	except IOError as e:
		print('The input file is invalid. It must be a colormap xml file. Go to https://sciviscolor.org/home/colormaps/ for some good options')
		print('Go to https://sciviscolor.org/matlab-matplotlib-pv44/ for an example use of this script.')
		sys.exit()
	data_vals=[]
	color_vals=[]
	for s in xmldoc.getroot().findall('.//Point'):
		data_vals.append(float(s.attrib['x']))
		color_vals.append((float(s.attrib['r']),float(s.attrib['g']),float(s.attrib['b'])))
	return {'color_vals':color_vals, 'data_vals':data_vals}

## source of this function: http://schubert.atmos.colostate.edu/~cslocum/custom_cmap.html#code
def make_cmap(xml):
    vals = load_xml(xml)
    colors = vals['color_vals']
    position = vals['data_vals']
    if len(position) != len(colors):
        sys.exit('position length must be the same as colors')
    
    cdict = {'red':[], 'green':[], 'blue':[]}
    if position[0] != 0:
        cdict['red'].append((0, colors[0][0], colors[0][0]))
        cdict['green'].append((0, colors[0][1], colors[0][1]))
        cdict['blue'].append((0, colors[0][2], colors[0][2]))
    
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))
    if position[-1] != 1:
        cdict['red'].append((1, colors[-1][0], colors[-1][0]))
        cdict['green'].append((1, colors[-1][1], colors[-1][1]))
        cdict['blue'].append((1, colors[-1][2], colors[-1][2]))
    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap




