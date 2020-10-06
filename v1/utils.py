from shapely.geometry import Point            
from shapely.geometry.polygon import Polygon

import numpy as np
import matplotlib.pyplot as plt

def config():
    turbine =  {   
                     'Name': 'Anon Name',
                     'Vendor': 'Anon Vendor',
                     'Type': 'Anon Type',
                     'Dia (m)': 100,
                     'Rotor Area (m2)': 7853,
                     'Hub Height (m)': 100,
                     'Cut-in Wind Speed (m/s)': 3.5,
                     'Cut-out Wind Speed (m/s)': 25,
                     'Rated Wind Speed (m/s)': 15,
                     'Rated Power (MW)': 3
                }
    dia    =  turbine['Dia (m)']
    rad    =  dia/2

    configuration = {
        'specs': turbine,
        'dia'  : dia,
        'rad'  : rad
    }

    return configuration


def indivCheckConstraints(turbine, turb_coords, turb_diam):
    bound_clrnc      = 50
    
    farm_peri = [(0, 0), (0, 4000), (4000, 4000), (4000, 0)]
    farm_poly = Polygon(farm_peri)
    
    inp = np.asarray([turbine.dna['x'], turbine.dna['y']])
    turb = Point(inp)
    inside_farm   = farm_poly.contains(turb)
    correct_clrnc = farm_poly.boundary.distance(turb) >= bound_clrnc
    if (inside_farm == False or correct_clrnc == False):
        return 0
    
    for i,turb2 in enumerate(turb_coords):
        if (inp == turb2).all():
            continue
        if  np.linalg.norm(inp - turb2) < 4*turb_diam:
            return 0
    
    return 1

def searchSorted(lookup, sample_array):
    lookup_middles = lookup[1:] - np.diff(lookup.astype('f'))/2
    idx1 = np.searchsorted(lookup_middles, sample_array)
    indices = np.arange(lookup.shape[0])[idx1]
    return indices

def getAvgLoss(turb_rad, turb_coords, power_curve, wind_inst_freq, 
            n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t):

    n_turbs        =   turb_coords.shape[0]
    assert n_turbs ==  50, "Error! Number of turbines is not 50."

    rotate_coords   =  np.zeros((n_wind_instances, n_turbs, 2), dtype=np.float32)
    rotate_coords[:,:,0] =  np.matmul(cos_dir, np.transpose(turb_coords[:,0].reshape(n_turbs,1))) - \
                           np.matmul(sin_dir, np.transpose(turb_coords[:,1].reshape(n_turbs,1)))
    rotate_coords[:,:,1] =  np.matmul(sin_dir, np.transpose(turb_coords[:,0].reshape(n_turbs,1))) +\
                           np.matmul(cos_dir, np.transpose(turb_coords[:,1].reshape(n_turbs,1)))

    x_dist = np.zeros((n_wind_instances,n_turbs,n_turbs), dtype=np.float32)
    for i in range(n_wind_instances):
        tmp = rotate_coords[i,:,0].repeat(n_turbs).reshape(n_turbs, n_turbs)
        x_dist[i] = tmp - tmp.transpose()

    y_dist = np.zeros((n_wind_instances,n_turbs,n_turbs), dtype=np.float32)
    for i in range(n_wind_instances):
        tmp = rotate_coords[i,:,1].repeat(n_turbs).reshape(n_turbs, n_turbs)
        y_dist[i] = tmp - tmp.transpose()
    y_dist = np.abs(y_dist) 
 
    sped_deficit = (1-np.sqrt(1-C_t))*((turb_rad/(turb_rad + 0.05*x_dist))**2) 
    sped_deficit[((x_dist <= 0) | ((x_dist > 0) & (y_dist > (turb_rad + 0.05*x_dist))))] = 0.0
    sped_deficit_eff  = np.sqrt(np.sum(np.square(sped_deficit), axis = 2))

    avg_losses = np.mean(sped_deficit_eff, axis=0)
    return(avg_losses)

def plotPts(coords, AEP, interval):
    plot_pts = np.array(coords)
    x = plot_pts[:,0]
    y = plot_pts[:,1]
    plt.title('Wind Farm')
    plt.scatter(x,y)
    plt.draw()
    plt.figtext(0.5, 0.01, str(round(AEP,2)), ha="center", fontsize=18, bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.pause(interval)
    plt.clf()