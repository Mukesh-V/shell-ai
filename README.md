# Shell AI Hackathon

### Genetic Algorithm v1
* I have used an algorithm close to GA with turbines as the individuals. The dna is a dictionary which contains the coordinates. 
* If speed loss is less than average loss, that turbine is killed and a new turbine is mutated by crossover.The crossover is a random weighted sum of the two parents and i know, its illogical to spawn based on coordinates ; lets try :P

### Genetic Algorithm v2
* I have used a primitive genetic algorithm with turbines as the individuals. The dna shape is lifespan * [x, y]
* At every timestep of life, speed loss is calculated first and fitness is calculated based on speed loss
* After a generation ends, selection is done based on a threshold on fitness.
* Less-fit turbines are mutated by a single-point crossover of two randomly selected turbines


##### Note : The wind data of 2015 has the highest AEP

```python
#install dependencies
pip3 install -r requirements.txt

#run algorithms : <algorithm> = v1, v2
python3 <algorithm>/game.py
```
