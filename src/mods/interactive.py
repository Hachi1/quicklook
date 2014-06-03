# encoding: utf-8
'''
@author:     Radek Hofman
'''
from mods import data_tools

#how do we format date
DATE_FORMATTER = "%Y/%m/%d %H:%M"
ERR_PREFIX = "\n [ERROR]  "

def print_separator():
    """
    prints separation horizontal line...
    """
    print "=================================================================="

def print_menu(grids):
    """
    interactive parts of program
    """
    mcount = len(grids[0])
    ncount = len(grids[1])
    
    domain = print_menu_domains(mcount, ncount)
    
def print_menu_domains(grids):
    """
    prints the main menu for processing of Flexpart outputs
    """
    mcount = len(grids[0])
    ncount = len(grids[1])   
    
    print_separator()
    if (ncount == 0): #just the main domain is present
        print "No nested domain found, working with the main domain..."
    else: #even the nest domain is present
        print "Main and nested domains found, please select the domain:"
        print " 0 - main domain"
        print " 1 - nested domain"
        
    domain = int(raw_input("Choice: "))
    print_separator()
    return domain


def get_max_domain(header):
    """
    returns maximum available domain
    """
    return (header["outlon0"][0],
            header["outlat0"][0],
            header["outlon0"][0]+(header["numxgrid"][0]-1)*header["dxout"][0],
            header["outlat0"][0]+(header["numygrid"][0]-1)*header["dyout"][0])

def domain_info_short(header):
    """
    prints brief domain info (temporal and spatil) from header
    """
    print "Header info %s:" % header["ver"]
    #spatial domain
    print "Domain:"
    print "    Lon: %4.3f - %4.3f deg, step %4.3f deg" % (header["outlon0"][0], 
                                                                header["outlon0"][0]+(header["numxgrid"][0]-1)*header["dxout"][0], 
                                                                header["dxout"][0])
    print "    Lat:  %4.3f - %4.3f deg, step %4.3f deg" % (header["outlat0"][0], 
                                                                header["outlat0"][0]+(header["numygrid"][0]-1)*header["dyout"][0], 
                                                                header["dyout"][0])
    print "Output leves:"
    for i, lev in enumerate(header["outheight"]):
        print "    ", i, str(lev), "m"

    #temporal domain
    print "Run type:"
    if header["loutstep"][0] < 0:
        print "    Backward run"
    else:
        print "    Forward run"
    print "Output step:"
    print "    "+str(header["loutstep"][0])+" sec (%3.2f hours)" % (header["loutstep"][0] / 3600.)
    
    ibdate = header["ibdate"][0]
    ibtime = header["ibtime"][0]
    ireleaseend = header["ireleaseend"][0][0] 
    ireleasestart = header["ireleasestart"][0][0] 
    simul_end_date = data_tools.make_end_of_simulation_date(ibdate, str(ibtime)) 
    #in backward run, this times are sampling start and end
    rel_start, rel_end = data_tools.make_release_dates(simul_end_date, ireleasestart, ireleaseend)

    print "Release dates:"
    print "    From %s to %s" % (rel_start.strftime(DATE_FORMATTER), rel_end.strftime(DATE_FORMATTER))
    print_separator()
    
def select_domain(header):
    """
    user selects domain to plot
    """
    print "Select domain:"
    print "    |-----------lon1, lat1"
    print "    |               |"
    print "    |               |"
    print "lon0, lat0 ---------|"
    print ""
    lon0 = float(raw_input("lon0: "))
    lat0 = float(raw_input("lat0: "))
    lon1 = float(raw_input("lon1: "))
    lat1 = float(raw_input("lat1: "))
    print "\nSelect range of vertical levels (enter number of level, to select one level, z0=z1):"
    outheights = header["outheight"]
    for i in range(len(outheights)):
        print i,":",  outheights[i], "m"
    z0 = int(raw_input("z0 (from): "))
    z1 = int(raw_input("z1 (to): "))
    return lon0, lat0, lon1, lat1, z0, z1

def validate_domain(lon0, lat0, lon1, lat1, z0, z1, header):
    """
    validates if the selected domain is possible - if it is inside the output region
    """
    
    #computing the domain coordinates
    _lon0 = header["outlon0"][0]
    _lon1 = header["outlon0"][0]+(header["numxgrid"][0]-1)*header["dxout"][0]
    _lat0 = header["outlat0"][0]                                                        
    _lat1 = header["outlat0"][0]+(header["numygrid"][0]-1)*header["dyout"][0] 
    
    #now follows seried of different conditions on validitiy of user inputs...
    valid = True #we apriori assume, that the data are valid
    
    #testing of different conditions
    if lon0 > lon1:
        valid = False
        print ERR_PREFIX+"Lon0 must be greater than Lon1!"
    if lat0 > lat1:
        valid = False
        print ERR_PREFIX+"Lat0 must be greater than Lat1!"
    if lon0 < _lon0 or lon0 > _lon1:
        valid = False
        print ERR_PREFIX+"Lon0 outside plausible region!"
    if lat0 < _lat0 or lat0 > _lat1:
        valid = False
        print ERR_PREFIX+"Lat0 outside plausible region!"          
    if z1 < z0:
        valid = False
        print ERR_PREFIX+"z1 must be not be smaller z0"
        
    return valid
    
    