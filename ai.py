from copy import deepcopy
from math import exp
from const import *
from random import choice, uniform
from pygame.draw import rect, line

def sigmoid(z):
    return 1 / (1 + exp(-z))


class Neuron:
    def __init__(self, id, type="hidden"):
        self.id = id
        self.value = 0
        self.type = type


class Connection:
    def __init__(self, inp, out, id, weight=None):
        self.id = id
        self.inp = inp
        self.out = out
        if weight:
            self.weight = weight
        else:
            self.weight = uniform(-1, 1)
        self.value = 0
        self.enabled = True
    
    def forward(self):
        if not self.enabled : return
        self.value = self.weight * sigmoid(self.inp.value)
        self.out.value += self.value



class NeuralNetwork:
    """
    Entrées du réseau de neurone :
     - Distance à un obstacle (mur ou lui-même) dans les 8 directions
     - Distance à un fruit dans les 8 directions
     - 
    """    
    def __init__(self):

        self.fitness = 0
        self.neurons = []
        self.connections = []

        # Création des neurones
        for i in range(16):
            self.neurons.append(Neuron(i, type="in"))
        for i in range(16, 16 + 4):
            self.neurons.append(Neuron(i, type="out"))
        
        # Création des connexions
        """for i in range(16):
            for j in range(4):
                self.connections.append(Connection(self.neurons[i], self.neurons[MAP_WIDTH * MAP_HEIGHT + j], i*4+j))"""
    
    def copy(self):
        return deepcopy(self)
    
    def reset(self):
        for i in range(len(self.neurons)):
            self.neurons[i].value = 0
        for i in range(len(self.connections)):
            self.connections[i].value = 0

    def forward(self, inputs):
        self.reset()
        for i in range(len(inputs)):
            self.neurons[i].value = inputs[i]
        for connection in self.connections:
            connection.forward()
        outputs = []
        for neuron in self.neurons:
            if neuron.type == "out" : outputs.append(sigmoid(neuron.value))
        return outputs
    
    def mutate_weights(self):
        for co in self.connections:
            if uniform(0, 1) < WEIGHT_MUTATION_CHANCES:
                co.weight += uniform(-WEIGHT_MAX_CHANGES, WEIGHT_MAX_CHANGES)
            elif uniform(0, 1) < WEIGHT_RESET_CHANCES:
                co.weight = uniform(-1, 1)

    def add_connection(self):

        while True:

            n1, n2 = choice(self.neurons), choice(self.neurons)

            if n1.id == n2.id : continue

            if (n1.type == "in" and n2.type == "out") or (n1.type == "in" and n2.type == "hidden") or (n1.type == "hidden" and n2.type == "hidden"):
                
                ok = True

                for c in self.connections: 
                    if c.inp.id == n1.id and c.out.id == n2.id: 
                        ok = False
                        break
                
                if ok:
                    self.connections.append(Connection(n1, n2, len(self.connections)))
                    return

    def add_neuron(self):

        if len(self.connections) == 0 : return

        c = choice(self.connections)
        c.enabled = False
        new = Neuron(len(self.neurons))
        
        self.neurons.append(new)
        
        self.connections.append(Connection(c.inp, new, len(self.connections)))
        self.connections.append(Connection(new, c.out, len(self.connections)))
        
    def mutate(self):

        rand = uniform(0, 1)
        
        if rand < MUTATE_ADD_CONNECTION_CHANCE:
            self.add_connection()
        if rand < MUTATE_ADD_NEURON_CHANCE:
            self.add_neuron()
        if rand < MUTATE_WEIGHTS_CHANCE:
            self.mutate_weights()

    def child(self, network):
        
        best = self if self.fitness > network.fitness else network
        other = self if best != self else network
        new = best.copy()

        for i in range(len(new.connections)):
            for j in range(len(other.connections)):
                if new.connections[i].id == other.connections[j].id and uniform(0, 1) < OTHER_PARENT_WEIGHT_CHANCES:
                    new.connections[i].weight = other.connections[j].weight
        
        for i in range(MUTATION_AMOUNT):

            new.mutate()

        return new
    
    def paint(self, screen, pos):
        
        width, height = pos[2], pos[3]

        input_amount, hidden_amount, output_amount = 0, 0, 0
        neurons_pos = {}

        for neuron in self.neurons:
            if neuron.type == "in":
                input_amount += 1
            elif neuron.type == "out":
                output_amount += 1
            else:
                hidden_amount += 1
        
        input_origin = 0
        hidden_origin = width // 2 - HIDDEN_NEURON_SIZE // 2
        output_origin = width - OUTPUT_NEURON_SIZE

        input_remaining_space = height - input_amount * INPUT_NEURON_SIZE
        hidden_remaining_space = height - hidden_amount * HIDDEN_NEURON_SIZE
        output_remaining_space = height - output_amount * OUTPUT_NEURON_SIZE

        input_count, hidden_count, output_count = 0, 0, 0

        # neurons positions calculation

        for neuron in self.neurons:
            if neuron.type == "in":
                x, y = pos[0] + input_origin, pos[1] + input_remaining_space / (input_amount + 1) * (input_count + 1) + input_count * INPUT_NEURON_SIZE
                neurons_pos[neuron] = (x, y)
                input_count += 1
            elif neuron.type == "hidden":
                x, y = pos[0] + hidden_origin, pos[1] + hidden_remaining_space / (hidden_amount + 1) * (hidden_count + 1) + hidden_count * HIDDEN_NEURON_SIZE
                neurons_pos[neuron] = (x, y)
                hidden_count += 1
            elif neuron.type == "out":
                x, y = pos[0] + output_origin, pos[1] + output_remaining_space / (output_amount + 1) * (output_count + 1) + output_count * OUTPUT_NEURON_SIZE
                neurons_pos[neuron] = (x, y)
                output_count += 1
        
        # connections display
        
        for c in self.connections:

            color = NEGATIVE_SYNAPSE_COLOR if c.weight < 0 else POSITIVE_SYNAPSE_COLOR
            
            coef = min(1, abs(c.weight) / 2)

            color = tuple(coef * color[i] + (1 - coef) * BACKGROUND_COLOR[i] for i in range(3))

            inp_size = INPUT_NEURON_SIZE if c.inp.type == "in" else HIDDEN_NEURON_SIZE if c.inp.type == "hidden" else OUTPUT_NEURON_SIZE
            inp_pos = (neurons_pos[c.inp][0] + inp_size - 1, neurons_pos[c.inp][1] + inp_size//2)
            
            out_size = INPUT_NEURON_SIZE if c.out.type == "in" else HIDDEN_NEURON_SIZE if c.out.type == "hidden" else OUTPUT_NEURON_SIZE
            out_pos = (neurons_pos[c.out][0], neurons_pos[c.out][1] + out_size//2)
            
            line(screen, color, inp_pos, out_pos, SYNAPSE_THICKNESS)
        
        # neurons display

        for neuron in neurons_pos.keys():
            coef = sigmoid(neuron.value)
            color = tuple(coef * NEURON_POSITIVE_ACTIVATION[i] + (1 - coef) * NEURON_NEGATIVE_ACTIVATION[i] for i in range(3))
            x, y =  neurons_pos[neuron][0], neurons_pos[neuron][1]
            rect(screen, color, (x, y, INPUT_NEURON_SIZE, INPUT_NEURON_SIZE))
            
class Generation:
    def __init__(self):
        
        self.population = [NeuralNetwork() for i in range(POPULATION_SIZE)]
        self.current = 0

        for ind in self.population:
            for i in range(MUTATION_AMOUNT):
                ind.mutate()

    def select_elite(self):

        self.population.sort(key=lambda a: -a.fitness)

        self.population = self.population[:ELITE_COUNT]
    
    def gen_children(self):

        while len(self.population) < POPULATION_SIZE:

            parent1 = choice(self.population[:ELITE_COUNT])
            parent2 = choice(self.population[:ELITE_COUNT])

            if parent1 == parent2 : continue

            self.population.append(parent1.child(parent2))
    
    def next_generation(self):

        self.select_elite()

        self.gen_children()

    def get_current_ind(self):

        return self.population[self.current]
    
    def current_index(self):
        return self.current

    def next_ind(self):

        if self.current >= len(self.population)-1:

            self.next_generation()
            self.current = 0
        
        else:

            self.current += 1
        
        return self.get_current_ind()
