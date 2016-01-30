from astropy.io import fits as pyfits
import numpy as np
import healpy as hp
import matplotlib.pyplot as plt
import math as ma
import os

import fonction as fct
plt.ion()

"""------------------------------------------------------------
   ---Program : Convolution using smooth function of healy to
                degraded HFI images of Planck before apply
                linear combinaison to study SZ effect
   ------------------------------------------------------------"""
   
unit_1 = open("filenames_HFI.txt")
FWMH = np.loadtxt("FWMH_HFI.txt")
i = 0
for line in unit_1 :
    fichier = line.strip()
    if "100" in fichier :
        continue
    if "143" in fichier :
        j = 1
    if "217" in fichier :
        j = 2
    if "353" in fichier :
        j = 3
    if "545" in fichier :
        j = 4
    if "857" in fichier :
        j = 5
        
    map_smooth, header = fct.smooth(fichier, ma.sqrt(FWMH[0,1]**2 - FWMH[j,1]**2))
    
    if "545" in fichier :
        map_smooth /= 58.04 # Jy to Tcmb convertion FIXME
    if "857" in fichier : 
        map_smooth /= 2.27  # Jy to Tcmb convertion FIXME

    i = i + 1
    path_1 = "maps_smooth/"
    if os.path.isfile(path_1 + fichier[10:]) == 1 :
        os.remove(path_1 + fichier[10:])
    hp.write_map("maps_smooth/" + fichier[10:],map_smooth, extra_header=(header))
        
for line in unit_1 :
    fichier = line.strip()
    if "100" in fichier :
        map,header = hp.read_map(filename,h=True)
        hp.write_map("maps_smooth/" + fichier[10:],map, extra_header=(header))
