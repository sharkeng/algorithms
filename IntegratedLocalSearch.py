import math
from random import randint


def get_coords_from_console():
    n = int(input())
    coords = dict()
    for i in range(n):
        s = input().split(' ')
        coords[int(s[0])] = [int(float(s[1])), int(float(s[2]))]
    return coords


def get_coords_from_file():
    n = int(input())
    coords = dict()
    for i in range(n):
        s = input().split(' ')
        coords[int(s[0])] = [int(float(s[1])), int(float(s[2]))]
    return coords


coords = get_coords_from_console()

two_opt_swap = lambda r, i, k: r[0:i] + r[k:-len(r) + i - 1:-1] + r[k + 1:len(r)]


def calculate_total_distance(route):
    res = 0
    for p in range(1, len(route)):
        res += math.hypot(coords[route[p]][0] - coords[route[p-1]][0], coords[route[p]][1] - coords[route[p-1]][1])
    return res


def two_opt(route):
    existing_route = route
    current_dist = calculate_total_distance(route)
    for i in range(len(existing_route)):
        for k in range(i + 1, len(existing_route)):
            new_route = two_opt_swap(existing_route, i, k)
            new_dist = calculate_total_distance(new_route)
            if new_dist < current_dist:
                existing_route = new_route
                current_dist = new_dist
    return existing_route


def four_opt(route):
    rand_kek = lambda: randint(0, len(route) - 1) // 4
    x = rand_kek()
    y = x + rand_kek()
    z = y + rand_kek()
    return route[:x] + route[z:] + route[y:z] + route[x:y]


def greedy():
    route_best = []
    len_best = float('inf')
    for iter_index, iter in coords.items():
        route = [iter_index]
        len_route = 0
        new_index, new, distance = make_closer(iter, route)
        len_route += distance
        route.append(new_index)
        while len(route) < len(coords):
            newIndex, new, distance = make_closer(new, route)
            len_route += distance
            route.append(newIndex)
        if len_route < len_best:
            len_best = len_route
            route_best = route
    return route_best, len_best


def make_closer(coords_city, past_cities):
    dist_best = float('inf')
    for id, cs in coords.items():
        if id not in past_cities:
            distance = math.hypot(coords_city[0] - cs[0], coords_city[1] - cs[1])
            if distance < dist_best:
                dist_best = distance
                closer_city_id = id
                closer_city = cs
    return closer_city_id, closer_city, dist_best


def local_search(start_route):
    return two_opt(start_route)


def integrated_local_search():
    route, _ = greedy()
    print(_)
    route = local_search(route)
    min_distance = calculate_total_distance(route)
    max_ = (len(route) - 1 // 4 + 1) ** 6
    print("Distance after 2-Opt Approach:", min_distance)
    print(route, len(route))
    for i in range(1000):
        new_route = four_opt(route)
        new_route = local_search(new_route)
        new_distance = calculate_total_distance(new_route)
        if new_distance < min_distance:
            min_distance = new_distance
            route = new_route
    print("Distance after 4-Opt Approach:", min_distance)
    print(route, len(route))
    return route


integrated_local_search()
