#############################################################
# OCTOBER  2012                                             #
# Reading and unpacking routines from J.Brioude (NOAA)      #
# This routine is ready to provide concentration            #
# and dry and wet deposition independently via              #
# flex81.readgrid(header, filename, agec)                   #
# Limitations/peculiarities to be confirmed by J. Brioude:  #
# - age classes are not considered                          #
# - deos it read equally fwd/bwd runs?                      #
# - how does it deal with multiple releases?                #
#############################################################
 



import struct
import os
from numpy import array,zeros
from pylab import frange,close
#import math
#from math import *
def readheader(filename):
 f=open(filename,'rb')
# print filename
 calcarea=0
 readp=1
 nest=0
 #datespath=pathname
 
 header=dict()
 rl=struct.unpack('<i',f.read(4))
 header['open']=1
 header['ibdate']=struct.unpack('<i',f.read(4))
 header['ibtime']=struct.unpack('<i',f.read(4))
 toto=struct.unpack('ccccccccccccc',f.read(13))
 header['ver']=""
# print 'test1'
 for i in range(0,13):
         header['ver']=header['ver']+toto[i]
 
 junk=struct.unpack('<ii',f.read(8))
 header['loutstep']=struct.unpack('<i',f.read(4))
 header['loutaver']=struct.unpack('<i',f.read(4))
 header['loutsample']=struct.unpack('<i',f.read(4))
 junk=struct.unpack('<ii',f.read(8))
 header['outlon0']=struct.unpack('<f',f.read(4))
 header['outlat0']=struct.unpack('<f',f.read(4))
 header['numxgrid']=struct.unpack('<i',f.read(4))
 header['numygrid']=struct.unpack('<i',f.read(4))
 header['dxout']=struct.unpack('<f',f.read(4))
 header['dyout']=struct.unpack('<f',f.read(4))
 junk=struct.unpack('<ii',f.read(8))
 header['numzgrid']=struct.unpack('<i',f.read(4))
 form="<"
 for i in range(0,int(header['numzgrid'][0])):
         form=form+'f'
 
 header['outheight']=struct.unpack(form,f.read(4*int(header['numzgrid'][0])))
 junk=struct.unpack('<ii',f.read(8))
 header['jjjjmmdd']=struct.unpack('<i',f.read(4))
 header['hhmmss']=struct.unpack('<i',f.read(4))
 junk=struct.unpack('<ii',f.read(8))
 header['nspec']=struct.unpack('<i',f.read(4))[0]/3
 header['numpointspec']=struct.unpack('<i',f.read(4))
 junk=struct.unpack('<i',f.read(4))
 numzgrid=[]
 species=[]
 for i in range(0,header['nspec']):
         junk=struct.unpack('<i',f.read(4))
         one=struct.unpack('<i',f.read(4))
         wd=struct.unpack('cccccccccc',f.read(10))
         junk=struct.unpack('<ii',f.read(8))
         one=struct.unpack('<i',f.read(4))
         dd=struct.unpack('cccccccccc',f.read(10))
         junk=struct.unpack('<ii',f.read(8))
         numzgrid.append([struct.unpack('<i',f.read(4))])
         species.append([struct.unpack('cccccccccc',f.read(10))])
         junk=struct.unpack('<i',f.read(4))
 
#print header 
 header['species']=species
 junk=struct.unpack('<i',f.read(4))
#print junk
 header['numpoint']=struct.unpack('<i',f.read(4))
 junk=struct.unpack('<i',f.read(4))

# print header['numpoint']
 #header['ireleasestart']=zeros(header.numpoint,1);
 #ireleaseend=zeros(header.numpoint,1);
 #kindz=zeros(header.numpoint,1);
 #xp1=zeros(header.numpoint,1);
 #yp1=zeros(header.numpoint,1);
 #xp2=zeros(header.numpoint,1);
 #yp2=zeros(header.numpoint,1);
 #zpoint1=zeros(header.numpoint,1);
 #zpoint2=zeros(header.numpoint,1);
 #npart=zeros(header.numpoint,1);
 #xmass=zeros(header.numpoint,header.nspec);
 xp1=list()
 yp1=list()
 xp2=list()
 yp2=list()
 zpoint1=list()
 zpoint2=list()
 compoint=list()
 ireleasestart=list()
 ireleaseend=list()
 
# print header 
 if readp==1:
 
         for i in range(0,header['numpoint'][0]):
                 rl=struct.unpack('<i',f.read(4))
                 ireleasestart.append(struct.unpack('<i',f.read(4)))
                 ireleaseend.append(struct.unpack('<i',f.read(4)))
#                kindz=struct.unpack('<i',f.read(4))
                 kindz=struct.unpack('cc',f.read(2))
                 junk=struct.unpack('<ii',f.read(8))
                 xp1.append(struct.unpack('<f',f.read(4)))
                 yp1.append(struct.unpack('<f',f.read(4)))
                 xp2.append(struct.unpack('<f',f.read(4)))
                 yp2.append(struct.unpack('<f',f.read(4)))
#                 print i,ireleasestart
#                 print i,ireleaseend
#                 print i,kindz,xp1,
                 zpoint1.append(struct.unpack('<f',f.read(4)))
                 zpoint2.append(struct.unpack('<f',f.read(4)))
                 junk=struct.unpack('<ii',f.read(8))
                 npart=struct.unpack('<i',f.read(4))
                 mpart=struct.unpack('<i',f.read(4))
#                 print 'part',npart,mpart 
                 rl=struct.unpack('<ii',f.read(8))
                 compoint.append(''.join(struct.unpack('ccccccccccccccccccccccccccccccccccccccccccccc',f.read(45))))

#                 print compoint
                 rl=struct.unpack('<i',f.read(4))
                 for j in range(0,header['nspec']):
                         rl=struct.unpack('<i',f.read(4))
                         xmass=struct.unpack('<f',f.read(4))
                         junk=struct.unpack('<ii',f.read(8))
                         xmass=struct.unpack('<f',f.read(4))
                         junk=struct.unpack('<ii',f.read(8))
                         xmass=struct.unpack('<f',f.read(4))
                         rl=struct.unpack('<i',f.read(4))
 else:
         nb=int(119*header['numpoint'][0]+header['nspec']*36*header['numpoint'][0]+4)
#         print 'step2',nb,header
         #for i in range(0,int(nb)):
         for ii in range(0,int(nb/500.)):
          form=""
          for i in range(0,500):
                 form=form+'c'
          junk=struct.unpack(form,f.read(500))
         nb2=nb-int(nb/500.)*500
         form=""
         for i in range(0,nb2):
                form=form+'c'
         junk=struct.unpack(form,f.read(nb2))
          #junk=struct.unpack(form,f.read(int(nb)))
 
 header['xp1']=xp1
 header['yp1']=yp1
 header['xp2']=xp2
 header['yp2']=yp2
 header['zpoint1']=zpoint1
 header['zpoint2']=zpoint2
 header['compoint']=compoint
 header['ireleasestart']=ireleasestart
 header['ireleaseend']=ireleaseend
 rl=struct.unpack('<i',f.read(4))
 header['method']=struct.unpack('<i',f.read(4))
 header['lsubgrid']=struct.unpack('<i',f.read(4))
 header['lconvection']=struct.unpack('<i',f.read(4))
# print header
# print header['method'],header['lsubgrid'],header['lconvection']
# print rl
# if rl[0]==20:
 header['ind_source']=struct.unpack('<i',f.read(4))
 header['ind_receptor']=struct.unpack('<i',f.read(4))
 
 junk=struct.unpack('<ii',f.read(8))
 header['nageclass']=struct.unpack('<i',f.read(4))
# print header['nageclass'],header['ind_source'],header['ind_receptor']
 form="<"
 for i in range(0,int(header['nageclass'][0])):
         form=form+'i'
 
 lage=struct.unpack(form,f.read(4*int(header['nageclass'][0])))
 header['lage']=lage
 junk=struct.unpack('<i',f.read(4))
# print header['lage']
 oro=list()
 form="<"
 for i in range(0,int(header['numygrid'][0])):
         form=form+'f'
 
 for i in range(0,int(header['numxgrid'][0])-1):
         junk=struct.unpack('<i',f.read(4))
         oro.append(struct.unpack(form,f.read(4*int(header['numygrid'][0]))))
         junk=struct.unpack('<i',f.read(4))
 
 oro.append(struct.unpack(form,f.read(4*int(header['numygrid'][0]))))
 header['oro']=array(oro)
 f.close()
 header['lonp']=frange(header['outlon0'][0]+header['dxout'][0]/2,header['outlon0'][0]+header['dxout'][0]*header['numxgrid'][0],header['dxout'][0])
 header['latp']=frange(header['outlat0'][0]+header['dyout'][0]/2,header['outlat0'][0]+header['dyout'][0]*header['numygrid'][0],header['dyout'][0])
 toto1=(header['outheight'])
 toto2=[0,]
 toto2.extend(toto1[0:-1])
 toto1=array(toto1)
# print toto1,toto2
 #print toto1.shape,toto2.shape
 header['zp']=0.5*(toto1+toto2)
 return header

def readgrid(header,filename,agec):
 f=open(filename,'rb')
 unit=1
 nest=0
 if nest==1:
  unit=unit+4
 
 
 
 formx="<"
 for i in range(0,int(header['numxgrid'][0])):
         formx=formx+'f'
 
 formy="<"
 for i in range(0,int(header['numygrid'][0])):
         formy=formy+'f'
 
 formz="<"
 for i in range(0,int(header['numzgrid'][0])):
         formz=formz+'f'
 
 wetdep=zeros([int(header["numxgrid"][0]),int(header["numygrid"][0]),int(1),int(header["nageclass"][0]),int(header['nspec'])])
 drydep=zeros([int(header["numxgrid"][0]),int(header["numygrid"][0]),int(1),int(header["nageclass"][0]),int(header['nspec'])])
 grid2=zeros([int(header["numxgrid"][0]),int(header["numygrid"][0]),int(header["numzgrid"][0])])
 grid=zeros([int(header["numxgrid"][0]),int(header["numygrid"][0]),int(header["numzgrid"][0])])
 #grid=zeros([int(header["numxgrid"][0]),int(header["numygrid"][0]),int(header["numzgrid"][0]),int(header["nageclass"][0]),int(header['nspec'])])
#print 'dim',int(header["numxgrid"][0]),int(header["numygrid"][0]),int(1),int(header["nageclass"][0]),int(header['nspec']) 
 rl=struct.unpack('<i',f.read(4))
 itime=struct.unpack('<i',f.read(4))
 rl=struct.unpack('<ii',f.read(8))
 kp_cnt=0
 agec=int(agec)
 if agec==0:
  age=header['nageclass'][0]
 else:
  age=agec 
# for kp in range(0,header['numpointspec'][0]):
 for kp in range(0,1):
  #for nage in range(0,header['nageclass'][0]):
  for nage in range(0,age):
   nage_read=1
   kp_read=1
 # wetgrid
   sp_count_i=struct.unpack('<i',f.read(4))
   sp_count_i=sp_count_i[0]
   rl=struct.unpack('<ii',f.read(8))
   form="<"
   for i in range(0,sp_count_i):
           form=form+'i'
   sparse_dump_i=struct.unpack(form,f.read(4*sp_count_i))
   rl=struct.unpack('<ii',f.read(8))
   sp_count_r=struct.unpack('<i',f.read(4))
   sp_count_r=sp_count_r[0]
   rl=struct.unpack('<ii',f.read(8))
   form="<"
   for i in range(0,sp_count_r):
           form=form+'f'
   sparse_dump_r=struct.unpack(form,f.read(4*sp_count_r))
#  print 'taille wet',len(sparse_dump_r)
   rl=struct.unpack('<ii',f.read(8))
##
   if (nage_read==1) and  (kp_read==1):
    fact=1
    ii=0
    a1=(header['numxgrid'][0]*header['numygrid'][0])
    a2=header["numxgrid"][0]
    for ir in range(0,len(sparse_dump_r)):
     a3=sparse_dump_r[ir]

     if a3*fact>0:
             n=sparse_dump_i[ii]
             fact=fact*-1
             ii=ii+1
     else:
             n=n+1

     jy=int(n/a2)
     ix=n-a2*jy
#    print 'wet',ix,jy,nage,kp
     wetdep[ix,jy,0,nage,kp]=-fact*a3
##
   # drygrid
   sp_count_i=struct.unpack('<i',f.read(4))
#  print 'check',sp_count_i
   sp_count_i=sp_count_i[0]
   rl=struct.unpack('<ii',f.read(8))
#  print 'check',rl
   form="<"
   for i in range(0,sp_count_i):
           form=form+'i'
   sparse_dump_i=struct.unpack(form,f.read(4*sp_count_i))
#  print 'taille dry',len(sparse_dump_i)
   rl=struct.unpack('<ii',f.read(8))
   sp_count_r=struct.unpack('<i',f.read(4))
   sp_count_r=sp_count_r[0]
   rl=struct.unpack('<ii',f.read(8))
   form="<"
   for i in range(0,sp_count_r):
           form=form+'f'
   sparse_dump_r=struct.unpack(form,f.read(4*sp_count_r))
   rl=struct.unpack('<ii',f.read(8))
##
   if (nage_read==1) and  (kp_read==1):
    fact=1
    ii=0
    a1=(header['numxgrid'][0]*header['numygrid'][0])
    a2=header["numxgrid"][0]
    for ir in range(0,len(sparse_dump_r)):
     a3=sparse_dump_r[ir]

     if a3*fact>0:
#            print 'line',ii
             n=sparse_dump_i[ii]
             fact=fact*-1
             ii=ii+1
     else:
             n=n+1

     jy=int(n/a2)
     ix=n-a2*jy
#    print 'dry',ix,jy,nage,kp
     drydep[ix,jy,0,nage,kp]=-fact*a3
##
 
   #concentration
   sp_count_i=struct.unpack('<i',f.read(4))
   sp_count_i=sp_count_i[0]
   rl=struct.unpack('<ii',f.read(8))
   form="<"
   for i in range(0,sp_count_i):
           form=form+'i'
   sparse_dump_i=struct.unpack(form,f.read(4*sp_count_i))
   rl=struct.unpack('<ii',f.read(8))
   sp_count_r=struct.unpack('<i',f.read(4))
   sp_count_r=sp_count_r[0]
   #print sp_count_r,sp_count_i
   rl=struct.unpack('<ii',f.read(8))
   form="<"
   for i in range(0,sp_count_r):
           form=form+'f'
   sparse_dump_r=struct.unpack(form,f.read(4*sp_count_r))
   try:
    rl=struct.unpack('<ii',f.read(8))
   except:
    pass #print 'end of file'
   if (nage_read==1) and  (kp_read==1):
         fact=1
         ii=0
	 a1=(header['numxgrid'][0]*header['numygrid'][0])
	 a2=header["numxgrid"][0]
         for ir in range(0,len(sparse_dump_r)):
		 a3=sparse_dump_r[ir]
                 if a3*fact>0:
                         n=sparse_dump_i[ii]
                         fact=-fact
                         ii=ii+1
                 else:
                         n=n+1
			 #print a3
                 #kz=int(n/(header['numxgrid'][0]*header['numygrid'][0]))
                 #jy=int((n-kz*(header["numxgrid"][0]*header["numygrid"][0]))/header["numxgrid"][0])
                 #ix=n-kz*(header["numxgrid"][0]*header["numygrid"][0])-jy*header["numxgrid"][0]
                 kz=int(n/a1)
                 jy=int((n-kz*a1)/a2)
                 ix=n-kz*a1-jy*a2
                 #grid[ix,jy,kz,nage,kp]=-a3
                 grid2[ix,jy,kz-1]=-fact*a3
 
 
   grid=grid+grid2
 
 
 f.close()
 return grid,wetdep,drydep

