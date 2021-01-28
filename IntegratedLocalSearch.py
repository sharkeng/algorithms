import math
import time
from random import randint
from tqdm import tqdm


def get_coords_from_console():
    n = int(input())
    coords = dict()
    for i in range(n):
        s = input().split(' ')
        coords[int(s[0])] = [int(float(s[1])), int(float(s[2]))]
    return coords


def get_coords_from_file(filename):
    with open(filename, "r") as f:
        st = f.read().split("\n")[1:]
        return {int(s.split()[0]): list(map(int, s.split()[1:])) for s in st}


coords = get_coords_from_file("mona_1000.txt")
old_i_dist, old_k_dist = 0, 0
print(coords)

two_opt_swap = lambda r, i, k: r[0:i] + r[k:-len(r) + i - 1:-1] + r[k + 1:len(r)]


# def calculate_total_distance(route):
#     res = 0
#     for p in range(1, len(route)):
#         res += math.hypot(coords[route[p]][0] - coords[route[p-1]][0], coords[route[p]][1] - coords[route[p-1]][1])
#     return res
def get_dist(x, r):
    return math.hypot(coords[r[x-1]][0] - coords[r[x]][0], coords[r[x-1]][1] - coords[r[x]][1])


def get_i_k_dists(i, k, route):
    try:
        new_k_dist = get_dist(k + 1, route)
    except:
        new_k_dist = 0
    try:
        new_i_dist = get_dist(i, route)
    except:
        new_i_dist = 0
    return new_i_dist, new_k_dist


def calculate_total_distance(route, i=None, k=None, old_dist=None):
    if i and k and old_dist:
        return old_dist - old_i_dist - old_k_dist + sum(get_i_k_dists(i, k, route))
    else:
        res = 0
        for p in range(1, len(route)):
            res += get_dist(p, route)
    return res


def two_opt(route):
    global old_i_dist, old_k_dist
    existing_route = route
    current_dist = calculate_total_distance(route)
    for i in range(len(existing_route)):
        for k in range(i + 1, len(existing_route)):
            old_i_dist, old_k_dist = get_i_k_dists(i, k, existing_route)

            new_route = two_opt_swap(existing_route, i, k)
            new_dist = calculate_total_distance(new_route, i, k, current_dist)

            if new_dist < current_dist:
                existing_route = new_route
                current_dist = new_dist
    return existing_route, current_dist


def four_opt(route):
    rand_kek = lambda: randint(0, len(route) - 1) // 4
    x = rand_kek()
    y = x + rand_kek()
    z = y + rand_kek()
    return route[:x] + route[z:] + route[y:z] + route[x:y]


def greedy(node=1):
    route_best = []
    len_best = float('inf')
    # for iter_index, iter in tqdm(coords.items()):
    route = [node]
    new_city_index, new_city_coords, distance = make_closer(coords[node], route)
    len_route = distance
    route.append(new_city_index)
    while len(route) < len(coords):
        new_city_index, new_city_coords, distance = make_closer(new_city_coords, route)
        len_route += distance
        route.append(new_city_index)
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
                closer_city_coords = cs
    return closer_city_id, closer_city_coords, dist_best


def local_search(start_route):
    return two_opt(start_route)


def integrated_local_search():
    route, _ = greedy()
    print(_)
    route, min_distance = local_search(route)
    print("Distance after 2-Opt Approach:", min_distance)
    print(route, len(route))
    for i in tqdm(range(100)):
        new_route = four_opt(route)
        new_route, new_distance = local_search(new_route)
        if new_distance < min_distance:
            min_distance = new_distance
            route = new_route
    print("Distance after 4-Opt Approach:", min_distance)
    print(route, len(route))
    return route


s_t = time.time()
integrated_local_search()
print(time.time() - s_t)
