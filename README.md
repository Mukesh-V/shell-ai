# Shell AI Hackathon

### Genetic Algorithm
* I have used a primitive genetive algorithm with turbines as the individuals. The dna is a dictionary which contains the coordinates. 
* Speed loss is calculated first and at every run of the algorithm, fitness is calculated based on speed loss
* If speed loss is less than average of loses of all turbines, that turbine is killed and a new turbine is mutated by crossover.The crossover is a random weighted sum of the two parents and i know, its illogical to spawn based on coordinates ; lets try :P


##### Note : The wind data of 2017 has the highest AEP

```python
#install dependencies
pip3 install -r requirements.txt

#run the algorithm
python3 game.py
```
