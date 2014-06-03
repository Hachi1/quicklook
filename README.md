# README #

QuickLook is a free command line tool for fast plotting of [FLEXPART](http://www.flexpart.eu) outputs.

## Licence ##

QuickLook is distributed under [GPL 2.0](http://www.gnu.org/licenses/gpl-2.0.html)

## Perquisites ##

To run QuickLook you need Python 2.7 and following libraries:

* Numpy
* Matplotlib
* Basemap

Reading of FLEXPART outputs is accomplished via *flex_81.py* module by J. Brioude (NOAA).

## How to use QuickLook? ##

It is quite easy:) QuickLook is a command line tool. To display a list of possible options, simply run

```bash
$ python quick_look.py -h
```

You shoule get something like this:

```bash
Usage: quick_look.py [options]

Created by Radek Hofman 2014

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -e EXP_PATH, --explore=EXP_PATH
                        Prints info abou Flexpart output at EXP_PATH
  -i INPUT, --input=INPUT
                        Flexpart output directory
  -d DOMAIN, --domain=DOMAIN
                        Coordinates of the domain: ll_lon, ll_lat, ur_lon,
                        ur_lat
  -m, --max_lat_lon     Takes maximum available lat-lon domain (overrides -d)
  -l LEVELS, --levels=LEVELS
                        Sets vertical level range: z0, z1 (z0,z1 >= 0, z0=z1
                        to select just one level)
  -t TYPE, --type=TYPE  Flexpart output type [mother|nested]
  -o OUTPUT, --output=OUTPUT
                        Images output directory
  -r RECEPTORS, --receptors=RECEPTORS
                        File with receptors
  -f DATAFACTOR, --datafactor=DATAFACTOR
                        Factor to multiply the data with
  -u UNITLABEL, --unitlabel=UNITLABEL
                        String containing units of visualized quantity
  -n FILENAME, --filename=FILENAME
                        Filename of resulting GIF
  -p, --pdf             Creates PDFs instead of PNGs of single frames (slower)
  -q, --reverse         Files are processes in reverse order
  -x TITLE, --title=TITLE
                        Title of images
  -z PROJECTION, --projection=PROJECTION
                        Map projection [cylindrical:cyl (default),
                        Marcator:merc]
```

### Explore FLEXPART outputs ###

To get started, let's explore some FLEXPART outputs. To do so, simply run
```bash
$ python quic_look.py -e <path_to_output>
```
where `<path_to_output>` is path to FLEXPART Output directory, e.g.

```bash
$ python quic_look.py -e /home/users/radek/run_1/Output
```

You should get something like:

```bash
==================================================================
DOMAIN TYPE: mother
Header info FLEXPART V9.0:
Domain:
    Lon: -179.000 - 179.000 deg, step 1.000 deg
    Lat:  -90.000 - 89.000 deg, step 1.000 deg
Output leves:
     0 100.0 m
     1 500.0 m
     2 1000.0 m
     3 1500.0 m
     4 2000.0 m
Run type:
    Backward run
Output step:
    -10800 sec (-3.00 hours)
Release dates:
    From 2013/04/07 18:54 to 2013/04/08 06:54
==================================================================
==================================================================
DOMAIN TYPE: nested
Header info FLEXPART V8.2:
Domain:
    Lon: 110.000 - 170.000 deg, step 0.250 deg
    Lat:  15.000 - 60.000 deg, step 0.200 deg
Output leves:
     0 100.0 m
     1 500.0 m
     2 1000.0 m
     3 1500.0 m
     4 2000.0 m
Run type:
    Backward run
Output step:
    -10800 sec (-3.00 hours)
Release dates:
    From 2013/04/07 18:54 to 2013/04/08 06:54
==================================================================
```

We see that we have a backward run of FLEXPART with mother and global mother and a smaller nested domain. The output time step is 3 hours and we have 5 vertical levels 0-4.