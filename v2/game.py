import matplotlib.pyplot as plt
from os import path

from utils import *
from Farm_Evaluator_Vec import *

from turbine import Turbine 
from population import Pop

if __name__ == "__main__":

    year = '2017'
    gen  = 50
    life = 15

    base = path.dirname(__file__)
    power_file = path.abspath(path.join(base, "..","Dataset/power_curve.csv"))
    wind_file_name = "Dataset/Wind Data/wind_data_" + year + ".csv"
    wind_file = path.abspath(path.join(base, "..",wind_file_name))

    config = config()
    power_curve    =  loadPowerCurve(power_file)
    wind_inst_freq =  binWindResourceData(wind_file)   
    n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t = preProcessing(power_curve)

    plt.ion()
    plt.show()

    population = Pop()

    for itr in range(0, gen):
        c = 0
        population.idx = 0
        while(True):  
            print('Running iteration : ' + str(itr) + " , " + str(c)) 
            if c == life:
                break
            population.init()
            population.run()

            turbo_coords = np.asarray(population.coords)
            AEP = getAEP(config['rad'], turbo_coords, power_curve, wind_inst_freq, n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t)
            plotPts(population.coords, AEP, 0.1)

            loss = getAvgLoss(config['rad'], turbo_coords, power_curve, wind_inst_freq, n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t)
            loss = loss * 100.0
            population.losses = loss

            population.eval()
            c += 1
            population.idx = c
            population.coords = []

            if AEP > 569.0:
                population.writeCSV(year + '_' + str(round(AEP,2)) + '.csv')

        population.selection()
        population.crossover()
        population.nullify()