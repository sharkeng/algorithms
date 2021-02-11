def create_first_cluster(factory, count_mashine, count_part, iter):
    left_machine_edge, left_part_edge = 0, 0
    clusters = list()
    machines_in_clusters = list()
    part_in_clusters = list()
    machine_number = 0
    clusters_in_machine = list()
    clusters_in_part = list()
    for i in range(iter):
        right_machine_edge = left_machine_edge + count_mashine // iter
        right_part_edge = left_part_edge + count_part // iter
        if i == iter - 1:
            right_machine_edge = count_machine
            right_part_edge = count_part
        cluster = {}
        one_machines_in_cluster = list()
        one_part_in_cluster = list()
        for j in range(left_part_edge, right_part_edge):
            one_part_in_cluster.append(j)
            clusters_in_part.append(i)
        part_in_clusters.append(one_part_in_cluster)
        for j in range(left_machine_edge, right_machine_edge):
            one_machines_in_cluster.append(j)
            parts = list()
            clusters_in_machine.append(i)
            for k in factory[j]:
                if left_part_edge <= k < right_part_edge:
                    parts.append(k)
            cluster[machine_number] = parts
            machine_number += 1
        left_machine_edge = right_machine_edge
        left_part_edge = right_part_edge
        machines_in_clusters.append(one_machines_in_cluster)
        clusters.append(cluster)
    return clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part


def get_value(clusters, machines_in_clusters, part_in_clusters, factory_len):
    n1_in = 0
    n0_in = 0
    for k in range(len(clusters)):
        x = sum(map(len, clusters[k].values()))
        n1_in += x
        n0_in += len(machines_in_clusters[k]) * len(part_in_clusters[k]) - x
    return n1_in / (factory_len + n0_in), n1_in, n0_in


def get_new_value(old_n1_in, old_n0_in, new_n1_in, new_n0_in, n1_in, n0_in, n1):
    new_full_n1_in = n1_in - old_n1_in + new_n1_in
    new_full_n0_in = n0_in - old_n0_in + new_n0_in
    return new_full_n1_in / (n1 + new_full_n0_in), new_full_n1_in, new_full_n0_in


def divide_clusters():
    pass


def merge_clusters():
    pass


def calc_swap_machines(clusters, part_in_clusters, clusters_in_machine, machine_number, cluster_number, n1_in, n0_in,
                       n1):
    machine_belonging = clusters_in_machine[machine_number]
    len_old_machine_in_old_cluster = len(part_in_clusters[machine_belonging])
    old_n1_in = len(clusters[machine_belonging][machine_number])
    old_n0_in = len_old_machine_in_old_cluster - old_n1_in
    len_machine_in_cluster = len(part_in_clusters[cluster_number])
    parts = list()
    for part in factory[machine_number]:
        if part in part_in_clusters[cluster_number]:
            parts.append(part)
    new_n1_in = len(parts)
    new_n0_in = len_machine_in_cluster - new_n1_in
    new_value, new_n1_in, new_n0_in = get_new_value(old_n1_in, old_n0_in, new_n1_in, new_n0_in, n1_in, n0_in, n1)

    return new_value, new_n1_in, new_n0_in


def swap_machines(factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part,
                  machine_number, cluster_number):
    machine_belonging = clusters_in_machine[machine_number]
    machines_in_clusters[cluster_number].append(machine_number)
    machines_in_clusters[machine_belonging].remove(machine_number)
    clusters_in_machine[machine_number] = cluster_number
    parts = list()
    for part in factory[machine_number]:
        if part in part_in_clusters[cluster_number]:
            parts.append(part)
    clusters[cluster_number][machine_number] = parts
    return factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part


def calc_swap_parts(clusters,machines_in_clusters,clusters_in_part,part_number,cluster_number, n1_in,n0_in, n1):
    part_belonging = clusters_in_part[part_number]
    len_old_part_in_old_cluster = len(machines_in_clusters[part_belonging])
    old_n1_in = len(clusters[part_belonging][part_number])
    old_n0_in = len_old_part_in_old_cluster - old_n1_in
    len_part_in_cluster = len(machines_in_clusters[cluster_number])
    parts = list()
    for part in factory_for_part[part_number]:
        if part in machines_in_clusters[cluster_number]:
            parts.append(part)
    new_n1_in = len(parts)
    new_n0_in = len_part_in_cluster - new_n1_in
    new_value, new_n1_in, new_n0_in = get_new_value(old_n1_in, old_n0_in, new_n1_in, new_n0_in, n1_in, n0_in, n1)

    return new_value, new_n1_in, new_n0_in

def swap_parts(factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part,
                  part_number, cluster_number):
    part_belonging = clusters_in_machine[part_number]
    part_in_clusters[cluster_number].append(part_number)
    part_in_clusters[part_belonging].remove(part_number)
    clusters_in_part[part_number] = cluster_number
    parts = list()
    for part in factory[part_number]:
        if part in part_in_clusters[cluster_number]:
            parts.append(part)
    clusters[cluster_number][part_number] = parts
    return factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part


def get_machines_and_parts_from_file(path):
    with open(path) as f:
        count_machine, count_part = [int(num) for num in f.readline().split()]
        factory = list()
        for i in range(count_machine):
            factory.append([int(num) - 1 for num in f.readline().split()][1:])
    return factory, count_machine, count_part


# 2  - max_count_clusters
def generate_clusters_for_part(factory_for_part,clusters):
    pass

if __name__ == "__main__":
    factory, count_machine, count_part = get_machines_and_parts_from_file(
        "dataset/#1 - King and Nakornchai(1982)[Figure-1a] ")
    max_count_clusters = min(count_machine, count_part)
    factory_len = sum(map(len, factory))
    (clusters, machines_in_clusters,
     part_in_clusters, clusters_in_machine,
     clusters_in_part) = create_first_cluster(factory, count_machine, count_part,
                                              (max_count_clusters + 2) // 2)

    value, n1_in, n0_in = get_value(clusters, machines_in_clusters, part_in_clusters, factory_len)
    print(value, n1_in, n0_in)
    best_move = [0, 0]
    print("factory", factory)
    print("clusters", clusters)
    print("machines_in_clusters", machines_in_clusters)
    print("part_in_clusters", part_in_clusters)
    print("clusters_in_machine", clusters_in_machine)
    print("clusters_in_part", clusters_in_part)
    factory_for_part=[[] for i in range (count_part)]
    for i in range(len(factory)):
        for j in factory[i]:
            factory_for_part[j].append(i)
    print(factory_for_part)
    clusters_for_part=[{} for i in range(len(clusters))]
    print(clusters_for_part)
    for i,num in enumerate(factory_for_part):
        list_machine=list()
        for j in num:
            if clusters_in_machine[j]==clusters_in_part[i]:
                print(i)
                print(clusters_in_part[i])
                list_machine.append(j)
        if(list_machine):
            clusters_for_part[clusters_in_part[i]][i]=list_machine
    print(clusters_for_part)

    changed = True
    while changed:
        changed = False
        for machine_number in range(count_machine):
            for cluster_number in range(len(clusters)):
                machine_belonging = clusters_in_machine[machine_number]
                if machine_belonging == cluster_number or len(machines_in_clusters[machine_belonging]) == 1:
                    continue
                new_value, new_n1_in, new_n0_in = calc_swap_machines(clusters=clusters,
                                                                     part_in_clusters=part_in_clusters,
                                                                     clusters_in_machine=clusters_in_machine,
                                                                     machine_number=machine_number,
                                                                     cluster_number=cluster_number, n1_in=n1_in,
                                                                     n0_in=n0_in, n1=factory_len)
                if new_value > value:
                    best_move[0] = machine_number
                    best_move[1] = cluster_number
                    value = new_value
                    n1_in = new_n1_in
                    n0_in = new_n0_in
                    changed = True
        if changed:
            factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part = swap_machines(
                factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part,
                best_move[0], best_move[1])
        else:
            for part_number in range(count_part):
                for cluster_number in range(len(clusters)):
                    part_belonging = clusters_in_part[part_number]
                    if part_belonging == cluster_number or len(part_in_clusters[part_belonging]) == 1:
                        continue
                    new_value, new_n1_in, new_n0_in = calc_swap_parts(clusters,
                                                                      machines_in_clusters,
                                                                      clusters_in_part,
                                                                      part_number,
                                                                      cluster_number, n1_in,
                                                                      n0_in, factory_len)
                    if new_value > value:
                        best_move[0] = part_number
                        best_move[1] = cluster_number
                        value = new_value
                        n1_in = new_n1_in
                        n0_in = new_n0_in
                        changed = True
            if changed:
                factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part = swap_parts(
                    factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part,
                    best_move[0], best_move[1])
    print("factory", factory)
    print("clusters", clusters)
    print("machines_in_clusters", machines_in_clusters)
    print("part_in_clusters", part_in_clusters)
    print("clusters_in_machine", clusters_in_machine)
    print("clusters_in_part", clusters_in_part)
    print(value)

# [[2, 4, 5, 6], [1, 3], [1, 3, 7], [2, 4, 6], [1, 7]]
#
# [[2]}, [1,3]]
# [[7]}, [4, 6]}, [7]]
#
# [[2,4], [1]]
# [[3,7], [6], [7]]


# [[1], [0,2]]
# [[6], [3,5], [6]]


# БЫЛО
# [[1, 3, 4, 5], [0, 2], [0, 2, 6], [1, 3, 5], [0, 6]]
# [[{0:[1]}], [{1:[2]}], [{2:[6]}, {3:[5]}, {4:[6]]]
#  [[0], [1], [2, 3, 4]]
#  [[0, 1], [2, 3], [4, 5, 6]]

# 3
# 0.22727272727272727


# СТАЛО
# [[{0:[1]},{2:[0]}],  [{1:[2]]}, [{3:[5], {4:[6]}]]
# [[0,2], [1], [3,4]]
# [[0,1], [2,3], [4,5,6]


#
#     0   1   2   3   4   5   6
# 0       #       #   #   #
# 1   #       #
# 2   #       #               #
# 3       #       #       #
# 4   #                       #
