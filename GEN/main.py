import math
from random import randint, sample, random
import numpy as np
from tqdm import tqdm
from sympy import isprime


class GenAlgTSP:
    def __init__(self, generations_count=100, population_size=1000, tournament_size=4,
                 elitism_rate=0.1, mutation_rate=0.1, latest_route=None, filename="dataset/cities.csv"):
        self.tournament_size = tournament_size
        self.population_size = population_size
        self.generations_count = generations_count
        self.elitism_rate = elitism_rate
        self.mutation_rate = mutation_rate
        self.coords = self.get_coords_from_file(filename)

    @staticmethod
    def get_coords_from_file(filename):
        with open(filename, "r") as f:
            st = f.read().split("\n")[1:]
            return {int(s.split(",")[0]): list(map(float, s.split(",")[1:])) for s in st if s}

    def greedy(self, node=0):
        route_best = []
        len_best = float('inf')
        route = [node]
        new_city_index, new_city_coords, distance = self.make_closer(self.coords[node], route)
        len_route = distance
        route.append(new_city_index)
        while len(route) < len(self.coords):
            new_city_index, new_city_coords, distance = self.make_closer(new_city_coords, route)
            len_route += distance
            route.append(new_city_index)
        if len_route < len_best:
            len_best = len_route
            route_best = route
        return route_best, len_best

    def make_closer(self, coords_city, past_cities):
        dist_best = float('inf')
        for id, cs in self.coords.items():
            if id not in past_cities:
                distance = math.hypot(coords_city[0] - cs[0], coords_city[1] - cs[1])
                if distance < dist_best:
                    dist_best = distance
                    closer_city_id = id
                    closer_city_coords = cs
        return closer_city_id, closer_city_coords, dist_best

    def four_opt(self, route):
        rand_kek = lambda: randint(1, len(route) - 1) // 4
        x = rand_kek()
        y = x + rand_kek()
        z = y + rand_kek()
        return route[:x] + route[z:] + route[y:z] + route[x:y]

    def get_dist(self, x, r):

        d = math.hypot(self.coords[r[x - 1]][0] - self.coords[r[x]][0],
                       self.coords[r[x - 1]][1] - self.coords[r[x]][1])
        if (x % 9 == 0 and x != 0 and isprime(r[x])) or (x % 9 != 0 or x == 0):
            return d
        return d * 1.1

    def get_i_k_dists(self, i, k, route):
        try:
            new_k_dist = self.get_dist(k + 1 if k + 1 < len(route) else 0, route)
        except KeyError:
            new_k_dist = 0
        try:
            new_i_dist = self.get_dist(i, route)
        except KeyError:
            new_i_dist = 0
        return new_i_dist, new_k_dist

    def calculate_total_distance(self, route, i=None, k=None, old_dist=None):
        if i and k and old_dist:
            return old_dist - self.old_i_dist - self.old_k_dist + sum(self.get_i_k_dists(i, k, route))
        else:
            res = 0
            for p in range(len(route)):
                res += self.get_dist(p, route)
        return res

    def make_first_population(self):
        route, len_route = self.greedy()
        population = []
        for i in tqdm(range(self.population_size)):
            population.append([new_route := self.four_opt(route), self.calculate_total_distance(new_route)])
        return population

    def get_random_indexes(self, parent1):
        return (left_ind := randint(1, len(parent1) - 1)), randint(left_ind, len(parent1))

    def get_random_indexes_lt_half(self, parent1):
        left_ind, right_ind = self.get_random_indexes(parent1)
        while right_ind - left_ind > len(parent1) / 2:
            left_ind, right_ind = self.get_random_indexes(parent1)
        return left_ind, right_ind

    def crossover(self, parent1, parent2):
        child = [-1 for i in range(len(parent1))]
        l_i, r_i = self.get_random_indexes_lt_half(parent1)
        child[l_i: r_i] = parent1[l_i: r_i]
        len_child = self.calculate_total_distance(child[l_i: r_i])
        available_index = list(range(0, l_i)) + list(range(r_i, len(parent1)))
        for city in parent2:
            if not available_index:
                break
            if city not in child:
                id = available_index.pop(0)
                child[id] = city
                if id != 0:
                    len_child += self.get_dist(id, child)
        len_child += self.get_dist(0, child)
        return [child, len_child]

    def optimize(self):
        population = self.make_first_population()
        elitism_offset = math.ceil(self.population_size * self.elitism_rate)
        last_route_len = float("inf")
        for i in tqdm(range(self.generations_count)):
            new_population = []

            population = sorted(population, key=lambda x: x[1])
            if population[0][1] < last_route_len:
                print(f'Fittest Route: {population[0][0]} ({population[0][1]})')

            if elitism_offset:
                elites = population[:elitism_offset]
                [new_population.append(i) for i in elites]
            for gen in range(elitism_offset, self.population_size):
                parent1 = self.tournament_selection(population)
                parent2 = self.tournament_selection(population)
                child = self.crossover(parent1[0], parent2[0])
                new_population.append(child)

            for gen in range(elitism_offset, self.population_size):
                new_population[gen] = self.mutate(new_population[gen])

            population = new_population
            last_route_len = population[0][1]
        return population[0]

    def mutate(self, genome):
        if random() < self.mutation_rate:
            left_ind, right_ind = self.get_random_indexes_lt_half(genome[0])
            genome[0] = self.two_opt_swap(genome[0], left_ind, right_ind)
            genome[1] = self.calculate_total_distance(genome[0])
        return genome

    two_opt_swap = lambda self, r, i, k: r[0:i] + r[k:-len(r) + i - 1:-1] + r[k + 1:len(r)]

    def tournament_selection(self, population):
        fighters = sample(population, k=self.tournament_size)
        return sorted(fighters, key=lambda x: x[1])[0]


if __name__ == "__main__":
    g = GenAlgTSP(population_size=1000, generations_count=20)
    # print(g.calculate_total_distance(g.greedy(0)[0]))
    print(g.optimize())
