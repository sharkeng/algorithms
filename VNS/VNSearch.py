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


def calc_swap_machines(clusters, part_in_clusters, clusters_in_machine, machine_number, cluster_number, n1_in, n0_in, n1):
    machine_belonging = clusters_in_machine[machine_number]

    if machine_belonging == cluster_number:
        return
    if len(machines_in_clusters[machine_belonging]) == 1:
        return

    len_old_machine_in_old_cluster = len(part_in_clusters[machine_belonging])
    old_n1_in = len(clusters[machine_belonging][machine_number])
    old_n0_in = len_old_machine_in_old_cluster - old_n1_in
    len_machine_in_cluster = len(part_in_clusters[cluster_number])

    new_n1_in = len(clusters[cluster_number][machine_number])
    new_n0_in = len_machine_in_cluster - n1_in
    new_value, n1_in, n0_in = get_new_value(old_n1_in, old_n0_in, new_n1_in, new_n0_in, n1_in, n0_in, n1)

    return new_value, n1_in, n0_in


# def swap_machines(factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part,
#                   machine_number, cluster_number, full_n1_in, full_n0_in, full_n1, old_value):
#     old_factory, old_clusters, old_machines_in_clusters, old_part_in_clusters, old_clusters_in_machine, old_clusters_in_part = factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part
#     olf_full_n1_in, old_full_n0_in = full_n1_in, full_n0_in
#     print("OLD", old_clusters)
#     machine_belonging = clusters_in_machine[machine_number]
#     if (machine_belonging == cluster_number):
#         # print(("OH Shit this is current cluster"))
#         return old_factory, old_clusters, old_machines_in_clusters, old_part_in_clusters, old_clusters_in_machine, old_clusters_in_part, olf_full_n1_in, old_full_n0_in, old_value, machine_number, cluster_number
#     if (len(machines_in_clusters[machine_belonging]) == 1):
#         # print("Null CLasters")
#         return old_factory, old_clusters, old_machines_in_clusters, old_part_in_clusters, old_clusters_in_machine, old_clusters_in_part, olf_full_n1_in, old_full_n0_in, old_value, machine_number, cluster_number
#     len_old_machine_in_old_cluster = len(part_in_clusters[machine_belonging])
#     old_n1_in = len(clusters[machine_belonging].pop(machine_number))
#     old_n0_in = len_old_machine_in_old_cluster - old_n1_in
#     machines_in_clusters[cluster_number].append(machine_number)
#     machines_in_clusters[machine_belonging].remove(machine_number)
#     clusters_in_machine[machine_number] = cluster_number
#     parts = list()
#     for part in factory[machine_number]:
#         if part in part_in_clusters[cluster_number]:
#             parts.append(part)
#     clusters[cluster_number][machine_number] = parts
#     len_machine_in_cluster = len(part_in_clusters[cluster_number])
#     n1_in = len(clusters[cluster_number][machine_number])
#     n0_in = len_machine_in_cluster - n1_in
#     # print(old_n0_in, old_n1_in, n0_in, n1_in)
#     # print(machines_in_clusters)
#     # print(part_in_clusters)
#     # print(clusters_in_machine)
#     # print(clusters_in_part)
#     # print(old_n1_in, old_n0_in, n1_in, n0_in, full_n1_in, full_n0_in, full_n1)
#     new_value, full_n1_in, full_n0_in = get_new_value(old_n1_in, old_n0_in, n1_in, n0_in, full_n1_in, full_n0_in,
#                                                       full_n1)
#     if new_value > old_value:
#         return factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, full_n1_in, full_n0_in, new_value, machine_number, cluster_number
#     else:
#         return old_factory, old_clusters, old_machines_in_clusters, old_part_in_clusters, old_clusters_in_machine, old_clusters_in_part, olf_full_n1_in, old_full_n0_in, old_value, machine_number, cluster_number


def swap_parts():
    pass


def get_machines_and_parts_from_file(path):
    with open(path) as f:
        count_machine, count_part = [int(num) for num in f.readline().split()]
        factory = list()
        for i in range(count_machine):
            factory.append([int(num) - 1 for num in f.readline().split()][1:])
    return factory, count_machine, count_part

# 2  - max_count_clusters


if __name__ == "__main__":
    factory, count_machine, count_part = get_machines_and_parts_from_file(
        "dataset/#1 - King and Nakornchai(1982)[Figure-1a] ")
    max_count_clusters = min(count_machine, count_part)
    print(factory)
    factory_len = sum(map(len, factory))
    (clusters, machines_in_clusters,
     part_in_clusters, clusters_in_machine,
     clusters_in_part) = create_first_cluster(factory, count_machine, count_part,
                                              (max_count_clusters + 2) // 2)

    value, n1_in, n0_in = get_value(clusters, machines_in_clusters, part_in_clusters, factory_len)
    print(value, n1_in, n0_in)
    current_value = value
    best_move_machine = 0
    best_move_cluster = 0
    # new_factory, new_clusters, new_machines_in_clusters, new_part_in_clusters, new_clusters_in_machine, new_clusters_in_part, new_n1_in, new_n0_in, new_value, new_best_move_machine, new_best_move_cluster = swap_machines(
    #     factory, clusters, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part,
    #     4,
    #     0, n1_in, n0_in, factory_len, current_value)
    # print("NEW------$@$@$@$@$$@$@-------------")
    # print(new_clusters)
    # print(new_machines_in_clusters)
    # print(new_part_in_clusters)
    # print(new_best_move_machine, current_best_move_cluster)
    # print(current_n1_in, current_n0_in)
    # print(new_value)
    # print("=----------@#KJKJKJKJKJKJKJ-----------------------")

    for machine_number in range(count_machine):
        for cluster_number in range(len(clusters)):
            pass
            # print("AMACH",machine_number,"CLSDATER",cluster_number)
    #         new_factory, new_clusters, new_machines_in_clusters, new_part_in_clusters, new_clusters_in_machine, new_clusters_in_part, new_n1_in, new_n0_in, new_value, new_best_move_machine, new_best_move_cluster = swap_machines(
    #             current_factory, current_clusters, current_machines_in_clusters, current_part_in_clusters,
    #             current_clusters_in_machine, current_clusters_in_part, machine_number, cluster_number, current_n1_in,
    #             current_n0_in, factory_len, current_value)
    #         # print(clusters)
    #         # print("NEW-------------------")
    #         # print(new_clusters)
    #         # print(new_machines_in_clusters)
    #         # print(new_part_in_clusters)
    #         # print(new_best_move_machine, current_best_move_cluster)
    #         # print(current_n1_in, current_n0_in)
    #         # print("=---------------------------------")
    #
    #         if new_value > value:
    #             # print("NEw", new_clusters)
    #             # print("Current", current_clusters)
    #             # print("OLD", clusters)
    #             current_factory, current_clusters, current_machines_in_clusters, current_part_in_clusters, current_clusters_in_machine, current_clusters_in_part, current_n1_in, current_n0_in, value, current_best_move_machine, current_best_move_cluster = new_factory, new_clusters, new_machines_in_clusters, new_part_in_clusters, new_clusters_in_machine, new_clusters_in_part, new_n1_in, new_n0_in, new_value, new_best_move_machine, new_best_move_cluster
    #             # print(current_clusters)
    #             # print(current_machines_in_clusters)
    #             # print(current_part_in_clusters)
    #             # print(current_best_move_machine, current_best_move_cluster)
    #             # print(current_n1_in, current_n0_in)
    #
    # print(value)
    print("factory", factory)
    print("clusters", clusters)
    print("machines_in_clusters", machines_in_clusters)
    print("part_in_clusters", part_in_clusters)
    print("clusters_in_machine", clusters_in_machine)
    print("clusters_in_part", clusters_in_part)
    print("best_move_machine", "best_move_cluster", best_move_machine, best_move_cluster)

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
