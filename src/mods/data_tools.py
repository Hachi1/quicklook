# encoding: utf-8
'''
@author:     Radek Hofman
'''
import os
import datetime
from datetime import timedelta
import flex_81
import numpy

IDENT_NEST_BWD = "grid_time_nest"
IDENT_MAIN_BWD = "grid_time"

IDENT_NEST_FWD = "grid_conc_nest"
IDENT_MAIN_FWD = "grid_conc"

ERR =  "  [ERROR]"
INFO = "   [INFO]"
WRN =  "[WARNING]"

def laod_receptors(path_to_receptors):
    """
    loads receptors from receprors file
    format of receptor file:
    
    lon lat caption, i.e.
    
    139.08 36.30 JPX38
    """
    receptors = []
    
    #in path_to_receptors = None, nothing happens, we have with statement
    with open(path_to_receptors) as f:
        s = f.readlines()
    
        for line in s:
            spl = line.split()
            spl[:2] = map(float, spl[:2]) #mapping to float values
            if len(spl) < 3:
                spl += [""] #in no station name is entered
            receptors.append(spl)
            
    #aleays is something returned, even an empty array           
    return receptors 
        

def load_data(FLEXPART_output_dir, species=1, reverse=False):
    """
    loads data - both concentration data and header data for main (and nested domains, where applicable)
    """
    #list all files in FP output directory
    all_files = os.listdir(FLEXPART_output_dir)

    #only those files we are interested in (starting with the right label (grid_time_2 or grid_time_nest))
    nest_domain_files = []
    main_domain_files = []
    
    domain_files = []
    headers = []
    
    #we assume that there are output files for main domain
    header_main = read_header(FLEXPART_output_dir, "header")
    run_type = numpy.sign(header_main["loutstep"][0])
       
    
    if run_type == 1: #FWD run
       IDENT_MAIN = IDENT_MAIN_FWD 
       IDENT_NEST = IDENT_NEST_FWD
    elif run_type == -1: #BWD run
       IDENT_MAIN = IDENT_MAIN_BWD 
       IDENT_NEST = IDENT_NEST_BWD
           
    for file in all_files:
        if file.startswith(IDENT_MAIN) and (not IDENT_NEST in file) and file.endswith("%3.3d" % species):
            main_domain_files.append(file)
        elif file.startswith(IDENT_NEST) and file.endswith("%3.3d" % species):
            nest_domain_files.append(file)

    nest_domain_files.sort(reverse=reverse)
    main_domain_files.sort(reverse=reverse)

    domain_files.append(main_domain_files)
    headers.append(header_main)  
    
    header_nest = None
    
    #read header files
    if (len(nest_domain_files) > 0): #yes, there are outputs for the nested domain
        header_nest = read_header(FLEXPART_output_dir, "header_nest")   
        domain_files.append(nest_domain_files)
        headers.append(header_nest) 
        
    return domain_files, headers

def read_header(FP_output_dir, output_type):
    """
    reads output header
    """
    header = flex_81.readheader(FP_output_dir+os.sep+output_type)

    
    return header


def make_end_of_simulation_date(jjjjmmdd, hhmmss):
    """
    makes datetime from date and time
    """
    
    year = int(str(jjjjmmdd)[:4])
    month = int(str(jjjjmmdd)[4:6])
    day = int(str(jjjjmmdd)[6:8])
    #hack!!! sometimes hhmmss is just hmmss if h < 10
    if len(hhmmss) == 5:
        hhmmss = '0'+hhmmss
        
    hour = int(str(hhmmss)[:2])
    try:
        min = int(str(hhmmss)[2:4])
    except:
        min = 0
    try:
        sec = int(str(hhmmss)[4:6])
    except:
        sec = 0
    

    return datetime.datetime(year, month, day, hour, min, sec)
    
def make_release_dates(simul_end_date, ireleasestart, ireleaseend):
    """
    from simulation end date return release start and end date
    """ 
    time_to_start = timedelta(seconds=ireleasestart)
    time_to_end = timedelta(seconds=ireleaseend)
    rel_start = simul_end_date + time_to_start
    rel_end = simul_end_date + time_to_end

    return rel_start, rel_end


def get_min_max_of_data(grids, header, FLEXPART_output_dir, z0, z1, data_factor, data_type):
    """
    finds minimal and maximal values of data for better scaling of levels
    """
    min = 1.0E+100
    max = -1.0E+100
    
    agec = 1
    
    for file in grids:
        grid, wetdep, drydep  = flex_81.readgrid(header, FLEXPART_output_dir+os.sep+file, agec)
        
        if data_type == 0:
            data0 = grid * data_factor
        elif data_type == 1:
            data0 = drydep[:,:,:,0,0] * data_factor        
        elif data_type == 2:
            data0 = wetdep[:,:,:,0,0] * data_factor        
        elif data_type == 3:
            data0 = (drydep[:,:,:,0,0] + wetdep[:,:,:,0,0]) * data_factor
        
        if z0<z1:
            data = numpy.sum(data0[:,:,z0:z1+1], axis=2) 
        else: #just the values from one selected level
            data = data0[:,:,z0]
        if data.max() > max:
            max = data.max()
        if data.min() < min:
            min = data.min()
            
    print INFO+" -- Minimum date value = %5.4E" % min
    print INFO+" -- Maximum value of data = %5.4E" % max
    return min, max