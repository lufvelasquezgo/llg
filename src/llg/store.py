import fileinput
import pickle
import numpy

states = []

counter = 0
for line in fileinput.input():
    if counter >= 3:
        state = pickle.loads(eval(line))
        states.append(state)
    counter += 1

states = numpy.array(states)
print(states.shape)
