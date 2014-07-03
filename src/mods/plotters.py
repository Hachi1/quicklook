# encoding: utf-8
'''
@author:     Radek Hofman
'''
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy
import matplotlib.animation
import os
from mods import flex_81
from mods import data_tools
from matplotlib.colors import LogNorm, Normalize
import math
import datetime
import sys
sys.path.append("../")
import config as cf

DATE_FORMAT_IN = "%Y%m%d%H%M%S"

counter = 0

ERR = "[ERROR]"
INFO = " [INFO]"

def get_date_from_fname(fname):
    """
    extracts date from file name like grid_time_20131107120000_001
    the date is always second from the back
    """
    dtime = datetime.datetime.strptime(fname.split("_")[-2], DATE_FORMAT_IN)
    
    d = dtime.strftime(cf.DATE_FORMAT_OUT)
    return d

def get_frame(nframe, header, grids, data_factor, domain, FLEXPART_output_dir, lon0, lon1, lat0, lat1, z0, z1, m, x, y, min_d, max_d, receptors, unitlabel, imagedir, title, log_flag=True):
    """
    renders single frame of animation
    """
    global counter
    
    print INFO+" -- Processing file %d" % nframe, grids[nframe]
    plt.cla()
    agec = 1
    file_path = FLEXPART_output_dir+os.sep+grids[nframe]
    grid, wetdep, drydep = flex_81.readgrid(header, file_path, agec)
    grid = grid * data_factor
    
    if z0<z1: #we eant integral value over more vetical levels
        data = numpy.sum(grid[:,:,z0:z1+1], axis=2).transpose()
    else: #just the values from one selected level
        data = grid[:,:,z0].transpose()
                
    if cf.LOG_FLAG: #log scale
        if cf.LOG_LEVELS_MAX == - 999:
            cf.LOG_LEVELS_MAX = math.ceil(math.log10(max_d))
        orders = 10 #we go back 10 orders from maxima
        levels = numpy.logspace(cf.LOG_LEVELS_MAX-cf.NUMBER_OF_ORDERS, cf.LOG_LEVELS_MAX, cf.NUMBER_OF_ORDERS+1)
        if cf.PLOT_METHOD == "contourf":
            c1 = m.contourf(x, y, data, latlon=False, levels=levels, norm=LogNorm(), cmap=cf.C_MAP, alpha=cf.ALPHA)
        elif cf.PLOT_METHOD == "imshow":
            c1 = m.imshow(data, 
                          interpolation='nearest', 
                          extent=(lon0, lon1, lat0, lat1), 
                          origin='lower', 
                          alpha=cf.ALPHA, #transparency
                          cmap=cf.C_MAP, #colormap
                          norm=LogNorm(vmin=levels[0], vmax=levels[-1]))
        elif cf.PLOT_METHOD == "pcolormesh":
            c1 = m.pcolormesh(x, y, data, 
                              #shading='gouraud', 
                              norm=LogNorm(vmin=levels[0], vmax=levels[-1]), 
                              cmap=cf.C_MAP, 
                              alpha=cf.ALPHA)
        else:
            print ERR, "Wrong plot method %s , exiting..." % cf.PLOT_METHOD 
            sys.exit(1)                        
    else: #linear scale
        #small offset added to min to exclude zeros
        if cf.LIN_LEVELS_MAX == -999:
            cf.LIN_LEVELS_MAX = max_d
        if cf.LIN_LEVELS_MIN == -999:
            cf.LIN_LEVELS_MIN = min_d
             
        levels = numpy.linspace(cf.LIN_LEVELS_MIN, cf.LIN_LEVELS_MAX, cf.NUMBER_OF_LEVELS)
        if cf.PLOT_METHOD == "contourf":
            c1 = m.contourf(x, y, data, latlon=False, levels=levels, cmap=cf.C_MAP, alpha=cf.ALPHA)
        elif cf.PLOT_METHOD == "imshow":
            c1 = m.imshow(data, 
                          interpolation='nearest', 
                          extent=(lon0, lon1, lat0, lat1), 
                          origin='lower', 
                          alpha=cf.ALPHA,
                          cmap=cf.C_MAP,
                          norm=Normalize(vmin=levels[0], vmax=levels[-1]))
        elif cf.PLOT_METHOD == "pcolormesh":
            c1 = m.pcolormesh(x, y, data, 
                              #shading='gouraud', 
                              norm=Normalize(vmin=levels[0], vmax=levels[-1]), 
                              cmap=cf.C_MAP, 
                              alpha=cf.ALPHA)            
        else:
            print ERR, "Wrong plot method %s , exiting..." % cf.PLOT_METHOD
            sys.exit(1)
    if counter == 0:
        cbar = m.colorbar(c1, location="bottom", pad="7%")
        cbar.set_label(unitlabel)
    
    
    #parallels and meridians are generated over the whole globe but only those contained in
    #viewports are visible
    #draw parallels

    if domain == "nested":
        par_step = cf.NESTED_PAR_STEP
        mer_step = cf.NESTED_MER_STEP
    else:
        par_step = cf.MOTHER_PAR_STEP
        mer_step = cf.MOTHER_MER_STEP

    parallels = numpy.arange(-90.,90.,par_step)
    m.drawparallels(parallels,labels=[True,False,False,True],fontsize=10)

    # draw meridians
    meridians = numpy.arange(-180.0,180.0,mer_step)
    m.drawmeridians(meridians,labels=[True,False,False,True],fontsize=10)   
    
    m.drawcoastlines()
    #m.drawstates()
    m.drawcountries()
    
    if cf.MAP_TYPE == 3:
        m.drawmapboundary(fill_color='aqua')
        m.fillcontinents(color='coral',lake_color='aqua')
    elif cf.MAP_TYPE == 4:
        m.bluemarble()
    elif cf.MAP_TYPE == 5:
        m.shadedrelief()
    elif cf.MAP_TYPE == 6:
        m.etopo()
    
    #plotting of receptors:
    for receptor in receptors:
        #r_lon = receptor[0]
        #r_lat = receptor[1]
        r_lon, r_lat = m(receptor[0], receptor[1])
        m.plot(r_lon, r_lat, cf.POI_MARKER, markersize=cf.POI_MARKER_SIZE)
        plt.text(r_lon+cf.TEXT_OFFSET, r_lat+cf.TEXT_OFFSET, receptor[2])
    
    date_str = get_date_from_fname(grids[nframe])
    
    plt.title(title+" ("+date_str+")")
    counter += 1



    if cf.PDFS_FLAG: #pdfs will be also saved
        plt.savefig(imagedir+os.sep+domain+"_"+str(int(z0))+"-"+str(int(z1))+"_frame_%03d.pdf" % nframe)
  
    if cf.JPGS_FLAG: #produce JPGs?
        plt.savefig(imagedir+os.sep+domain+"_"+str(int(z0))+"-"+str(int(z1))+"_frame_%03d.jpg" % nframe)
        
    if cf.PNGS_FLAG: #produce PNGs?    
        plt.savefig(imagedir+os.sep+domain+"_"+str(int(z0))+"-"+str(int(z1))+"_frame_%03d.png" % nframe)


def make_animation(header, grids, domain, data_factor, FLEXPART_output_dir, lon0, lon1, lat0, lat1, z0, z1, IMAGEDIR, receptors, filename, unitlabel, title, projection):
    """
    makes animation from an array of grids
    """
    """
    domain in ["mother", "nested"]
    
    creates single frame (from one flepart output file)
    time step is given by the file
    spatial domain is given by lon0, lon1, lat0, lat1, z0, z1
    
            |-----------------lon1, lat1
            |                     |
            |                     |
        lon0, lat0 ---------------| 
    
    z0 is lower vertica level, z1 is the upper
    
    
    Developer note..:
    
        For most map projections, the map projection region can either be specified by setting these keywords:
        
        Keyword    Description
        llcrnrlon    longitude of lower left hand corner of the desired map domain (degrees).
        llcrnrlat    latitude of lower left hand corner of the desired map domain (degrees).
        urcrnrlon    longitude of upper right hand corner of the desired map domain (degrees).
        urcrnrlat    latitude of upper right hand corner of the desired map domain (degrees).
        or these
        
        Keyword    Description
        width    width of desired map domain in projection coordinates (meters).
        height    height of desired map domain in projection coordinates (meters).
        lon_0    center of desired map domain (in degrees).
        lat_0    center of desired map domain (in degrees).    
    
    
        resolution:  c (crude), l (low), i (intermediate), h (high), f (full) 
    more at http://matplotlib.org/basemap/api/basemap_api.html
    """

    numxgrid = header["numxgrid"][0]
    numygrid = header["numygrid"][0]
    dxout = header["dxout"][0]
    dyout = header["dyout"][0]
    outlon0 = header["outlon0"][0]
    outlat0 = header["outlat0"][0]
        
    
    fig = plt.figure(figsize=(cf.FIG_X,cf.FIG_Y))
    m = Basemap(projection=projection,
                llcrnrlon = lon0, llcrnrlat = lat0,
                urcrnrlon = lon1, urcrnrlat = lat1,
                resolution=cf.BASEMAP_RESOLUTION, area_thresh=cf.BASEMAP_AREA_THR)    
         
    

    #this is better I think than the originla script
    lons0 = numpy.linspace(outlon0, outlon0+(numxgrid-1)*dxout, numxgrid)
    lats0 = numpy.linspace(outlat0, outlat0+(numygrid-1)*dyout, numygrid)
    lons, lats = numpy.meshgrid(lons0, lats0) 
    #now we create a mesh for plotting data
    x, y = m(lons, lats)
         
    #finding minimum and maximum values in the data to be able to make reasonale levels same for all frames
    min_d, max_d = data_tools.get_min_max_of_data(grids, header, FLEXPART_output_dir, z0, z1, data_factor)   
         
    a = matplotlib.animation.FuncAnimation(fig, 
                                   get_frame, 
                                   frames=len(grids), 
                                   #blit=True,
                                   fargs=(header, 
                                          grids, 
                                          data_factor, 
                                          domain,
                                          FLEXPART_output_dir, 
                                          lon0, 
                                          lon1, 
                                          lat0, 
                                          lat1, 
                                          z0, 
                                          z1, 
                                          m, 
                                          x, 
                                          y,
                                          min_d,
                                          max_d,
                                          receptors,
                                          unitlabel,
                                          IMAGEDIR,
                                          title),
                                    repeat=False)
    

    animpath = IMAGEDIR+os.sep+domain+"_"+str(int(z0))+"-"+str(int(z1))+"_"+filename
    print INFO+" - Creating animation %s" % animpath 
    a.save(animpath, writer='imagemagick')
    print "... Done!"

def make_frames(): 
    """
    makes signle frames from a sequence of data files, not an animation
    """

