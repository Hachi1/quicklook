# encoding: utf-8
'''
@author:     Radek Hofman

configuration file for quick_look
'''
import matplotlib.pyplot as plt

#file suffixes to distinguish different outputs  
FILE_NAMES = ["",    #suffix for conc/residence times 
              "_dd",  #suffix for dry depo]
              "-wd",  #suffix for wet depo
              "_dwd"] #suffix for dry and wet depo

FIG_X = 10 # size of figure in x
FIG_Y =  8 # size of figure in y

MOTHER_MER_STEP = 10.0  # step of meridians for mother domain in degrees
MOTHER_PAR_STEP = 5.0  # step of meridians for mother domain in degrees

NESTED_MER_STEP = 10.0  # step of meridians for mother domain in degrees
NESTED_PAR_STEP = 10.0  # step of meridians for mother domain in degrees

PLOT_METHOD = "pcolormesh" # "contourf" | "imshow" | "pcolormesh"
ALPHA = 0.7 # transparency of 2d plots, 0 - 1, where 1 means no transparency at all 
LOG_FLAG = True #logarithmic scale, set false for linear scale

#log scale now assumes, that 1 step in levels is 1 order of magnitude
NUMBER_OF_ORDERS = 6  #number of orders to show in log scale, i.e. order_of_maximum - 6 -- order of maximum will be shown
LOG_LEVELS_MAX = -999 #maximum order of log levels, use -999 for real data maximum order

NUMBER_OF_LEVELS = 10 #number of levels for linear scale, equidistant levels LIN_LEVELS_MIN - maximum value 
LIN_LEVELS_MIN = -999 #minimum of linear levels, use -999 for real data minimum
LIN_LEVELS_MAX = -999 #maximum of linear levels, use -999 for real data maximum

C_MAP = plt.cm.jet # use matplotlib colormaps, list is avalibale at http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps

DATE_FORMAT_OUT = "%Y-%m-%d %H:%M" # format of date displayed in title of frames

TEXT_OFFSET = 0.2 # text offset for labeling POIs in degrees, applied in both lan and lot
POI_MARKER = 'bo' # marker and color of POI following matplotlib conventions
POI_MARKER_SIZE = 6 # size of POI MARKER

PNGS_FLAG = False # do we want to produce PNGs?
JPGS_FLAG = True # do we want to produce JPGs?
PDFS_FLAG = False # do we want to produce PDFs?

## Available map types (see http://matplotlib.org/basemap/users/geography.html for details):
# 0 - continents and oceans white, just borders
# 3 - filled oceans and continents
# 4 - NASA Bluemarble
# 5 - shaded relief
# 6 - etopo relief
MAP_TYPE = 0

BASEMAP_RESOLUTION = 'i' # resolution of map:  'c' (crude - fast), 'l' (low), 'i' (intermediate), 'h' (high), 'f' (full - slow) 
BASEMAP_AREA_THR = 10000 # basemap area threshold
