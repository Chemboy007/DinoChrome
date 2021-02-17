import random


def populate(size=10):
    initial = []
    for i in range(size):
        bot = [random.random(), random.random(), random.uniform(-2, 2)]
        initial.append(bot)
    return initial


def mutate(population):
    alpha = 1
    for person in population:
        for gene in enumerate(person.genes):
            person.genes[gene[0]] += random.uniform(-alpha, alpha)
    return population


