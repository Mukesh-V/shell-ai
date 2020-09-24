from utils import *
from Farm_Evaluator_Vec import *
from turbine import Turbine 
from population import Pop

if __name__ == "__main__":
    config = config()
    population = Pop(50)
    year = '2017'
    power_curve   =  loadPowerCurve('./Dataset/power_curve.csv')
    wind_inst_freq =  binWindResourceData('./Dataset/Wind Data/wind_data_' + year + '.csv')   
    n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t = preProcessing(power_curve)
    c = 1

    while(True):
        turbo_coords = np.asarray(population.coords)
        loss = getAvgLoss(config['rad'], turbo_coords, power_curve, wind_inst_freq, n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t)
        loss = loss*100.0
        population.losses = loss
        population.run(c)
        AEP = getAEP(config['rad'], turbo_coords, power_curve, wind_inst_freq, n_wind_instances, cos_dir, sin_dir, wind_sped_stacked, C_t)
        print(AEP)
        c += 1
        if AEP > 565.0:
            population.writeCSV(year + '_' + str(round(AEP,2)) + '.csv')
            break