import matplotlib.pyplot as plt

from utils import *
from Farm_Evaluator_Vec import *

from turbine import Turbine 
from population import Pop

if __name__ == "__main__":
    config = config()
    population = Pop(50)
    year = '2017'

    base = path.dirname(__file__)
    power_file = path.abspath(path.join(base, "..","Dataset/power_curve.csv"))
    wind_file_name = "Dataset/Wind Data/wind_data_" + year + ".csv"
    wind_file = path.abspath(path.join(base, "..",wind_file_name))

    power_curve   =  loadPowerCurve(power_file)
    wind_inst_freq =  binWindResourceData(wind_file)   
    n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t = preProcessing(power_curve)
    c = 1

    plt.ion()
    plt.show()

    while(True):
        turbo_coords = np.asarray(population.coords)
        AEP = getAEP(config['rad'], turbo_coords, power_curve, wind_inst_freq, n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t)
        plotPts(population.coords, AEP, 0.1)

        loss = getAvgLoss(config['rad'], turbo_coords, power_curve, wind_inst_freq, n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t)
        loss = loss * 100.0

        if c == 1:
            min_loss = loss
            max_coords = population.coords

        if(min_loss > loss).all():
            min_loss = loss

            max_coords = population.coords
        else:
            population.coords = max_coords

        population.losses = loss
        population.run(c)

        c += 1
        if AEP > 569.0:
            population.writeCSV(year + '_' + str(round(AEP,2)) + '.csv')
            break