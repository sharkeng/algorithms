from copy import deepcopy


def create_first_cluster(factory, count_machine, count_part, iter):
    left_machine_edge, left_part_edge = 0, 0
    clusters = list()
    machines_in_clusters = list()
    part_in_clusters = list()
    machine_number = 0
    clusters_in_machine = list()
    clusters_in_part = list()
    for i in range(iter):
        right_machine_edge = left_machine_edge + count_machine // iter
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


def merge_cluster(machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, clusters,
                  clusters_for_part, num_cl_1, num_cl_2, matrix, n1_in, n0_in, n1):
    len_old = (len(machines_in_clusters[num_cl_1]) * len(part_in_clusters[num_cl_1])) + (
                len(machines_in_clusters[num_cl_2]) * len(part_in_clusters[num_cl_2]))

    old_n1_in = sum(map(len, clusters[num_cl_1].values())) + sum(map(len, clusters[num_cl_2].values()))
    old_n0_in = len_old - old_n1_in
    clusters[num_cl_1] = {}
    clusters_for_part[num_cl_1] = {}
    del clusters[num_cl_2]
    del clusters_for_part[num_cl_2]

    machines = machines_in_clusters[num_cl_1] + machines_in_clusters[num_cl_2]
    parts = part_in_clusters[num_cl_1] + part_in_clusters[num_cl_2]
    new_n1_in, new_n0_in = 0, 0
    for m in machines:
        parts_for_every_m = []
        for p in parts:
            if matrix[m][p]:
                new_n1_in += 1
                parts_for_every_m.append(p)
            else:
                new_n0_in += 1
        if parts_for_every_m:
            clusters[num_cl_1][m] = parts_for_every_m

    for p in parts:
        machines_for_every_m = []
        for m in machines:
            if matrix[m][p]:
                machines_for_every_m.append(m)
        if machines_for_every_m:
            clusters_for_part[num_cl_1][p] = machines_for_every_m
    del machines_in_clusters[num_cl_2]
    del part_in_clusters[num_cl_2]
    machines_in_clusters[num_cl_1] = machines
    part_in_clusters[num_cl_1] = parts


    for i, x in enumerate(clusters_in_machine):
        if x > num_cl_2:
            clusters_in_machine[i]-=1
        if x == num_cl_2:
            clusters_in_machine[i]=num_cl_1

    for i, x in enumerate(clusters_in_part):
        if x > num_cl_2:
            clusters_in_part[i]-=1
        if x==num_cl_2:
            clusters_in_part[i]=num_cl_1



    value, n1_in, n0_in = get_new_value(old_n1_in, old_n0_in, new_n1_in, new_n0_in, n1_in, n0_in, n1)
    return machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, clusters, clusters_for_part, value, n1_in, n0_in


def divide_cluster(machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, clusters,
                   clusters_for_part, num_cluster_to_change, matrix, n1_in, n0_in, n1):
    m_cl = machines_in_clusters[num_cluster_to_change]
    p_cl = part_in_clusters[num_cluster_to_change]
    len_p_cl = len(p_cl)
    len_m_cl = len(m_cl)


    len_old = len_m_cl * len_p_cl
    old_n1_in = sum(map(len, clusters[num_cluster_to_change].values()))

    old_n0_in = len_old - old_n1_in

    new_cl_id = len(clusters)

    new_m_cl_left, new_m_cl_right = m_cl[:len_m_cl // 2], m_cl[len_m_cl // 2:]
    new_p_cl_up, new_p_cl_down = p_cl[:len_p_cl // 2], p_cl[len_p_cl // 2:]

    machines_in_clusters[num_cluster_to_change] = new_m_cl_left
    part_in_clusters[num_cluster_to_change] = new_p_cl_up
    machines_in_clusters.append(new_m_cl_right)
    part_in_clusters.append(new_p_cl_down)
    len_cl = len(clusters)

    parts = []
    cl = {}
    clusters[num_cluster_to_change] = {}
    clusters_for_part[num_cluster_to_change] = {}

    new_n1_in, new_n0_in = 0, 0

    for m in new_m_cl_left:
        for p in new_p_cl_up:
            if matrix[m][p]:
                new_n1_in += 1
                parts.append(p)
                if not cl.get(p):
                    cl[p] = [m]
                else:
                    cl[p].append(m)
            else:
                new_n0_in += 1
        if parts:
            clusters[num_cluster_to_change].update({m: parts})
    clusters_for_part[num_cluster_to_change].update(cl)


    parts = []
    cl = {}
    clusters.append({})
    clusters_for_part.append({})
    for m in new_m_cl_right:
        clusters_in_machine[m] = len_cl
        for p in new_p_cl_down:
            clusters_in_part[p] = len_cl
            if matrix[m][p]:
                new_n1_in += 1
                parts.append(p)
                if not cl.get(p):
                    cl[p] = [m]
                else:
                    cl[p].append(m)
            else:
                new_n0_in += 1
        if parts:
            clusters[-1].update({m: parts})

    clusters_for_part[-1].update(cl)
    value, n1_in, n0_in = get_new_value(old_n1_in, old_n0_in, new_n1_in, new_n0_in, n1_in, n0_in, n1)
    return machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, clusters, clusters_for_part, value, n1_in, n0_in


def calc_swap_machines(factory, clusters, part_in_clusters, clusters_in_machine, machine_number, cluster_number, n1_in,
                       n0_in,
                       n1):
    machine_belonging = clusters_in_machine[machine_number]
    len_old_machine_in_old_cluster = len(part_in_clusters[machine_belonging])
    try:
        old_n1_in = len(clusters[machine_belonging][machine_number])
    except KeyError:
        old_n1_in = 0
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


def swap_machines(factory, clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine,
                  clusters_in_part,
                  machine_number, cluster_number):
    machine_belonging = clusters_in_machine[machine_number]
    machines_in_clusters[cluster_number].append(machine_number)
    machines_in_clusters[machine_belonging].remove(machine_number)
    clusters_in_machine[machine_number] = cluster_number
    parts = list()
    for part in factory[machine_number]:
        if part in part_in_clusters[cluster_number]:
            parts.append(part)
            try:
                clusters_for_part[cluster_number][part].append(machine_number)
            except KeyError:
                clusters_for_part[cluster_number][part] = [machine_number]
        if part in part_in_clusters[machine_belonging]:
            try:
                clusters_for_part[machine_belonging][part].remove(machine_number)
                if not clusters_for_part[machine_belonging][part]:
                    del clusters_for_part[machine_belonging][part]
            except KeyError:
                pass

    clusters[cluster_number][machine_number] = parts
    try:
        del clusters[machine_belonging][machine_number]
    except KeyError:
        pass
    return clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part


def calc_swap_parts(factory_for_part, clusters_for_part, machines_in_clusters, clusters_in_part, part_number,
                    cluster_number, n1_in, n0_in, n1):
    part_belonging = clusters_in_part[part_number]
    len_old_part_in_old_cluster = len(machines_in_clusters[part_belonging])
    try:
        old_n1_in = len(clusters_for_part[part_belonging][part_number])
    except KeyError:
        old_n1_in = 0
    old_n0_in = len_old_part_in_old_cluster - old_n1_in
    len_part_in_cluster = len(machines_in_clusters[cluster_number])
    machines = list()
    for machine in factory_for_part[part_number]:
        if machine in machines_in_clusters[cluster_number]:
            machines.append(machine)
    new_n1_in = len(machines)
    new_n0_in = len_part_in_cluster - new_n1_in
    new_value, new_n1_in, new_n0_in = get_new_value(old_n1_in, old_n0_in, new_n1_in, new_n0_in, n1_in, n0_in, n1)

    return new_value, new_n1_in, new_n0_in


def swap_parts(factory_for_part, clusters, clusters_for_part, machines_in_clusters, part_in_clusters,
               clusters_in_machine, clusters_in_part,
               part_number, cluster_number):
    part_belonging = clusters_in_part[part_number]
    part_in_clusters[cluster_number].append(part_number)
    part_in_clusters[part_belonging].remove(part_number)
    clusters_in_part[part_number] = cluster_number
    machines = list()
    for machine in factory_for_part[part_number]:
        if machine in machines_in_clusters[cluster_number]:
            machines.append(machine)
            try:
                clusters[cluster_number][machine].append(part_number)
            except KeyError:
                clusters[cluster_number][machine] = [part_number]
        if machine in machines_in_clusters[part_belonging]:
            try:
                clusters[part_belonging][machine].remove(part_number)
                if not clusters[part_belonging][machine]:
                    del clusters[part_belonging][machine]
            except KeyError:
                pass

    clusters_for_part[cluster_number][part_number] = machines
    try:
        del clusters_for_part[part_belonging][part_number]
    except KeyError:
        pass

    return clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part


def get_machines_and_parts_from_file(path):
    with open(path) as f:
        count_machine, count_part = [int(num) for num in f.readline().split()]
        factory = list()
        for i in range(count_machine):
            factory.append([int(num) - 1 for num in f.readline().split()][1:])
    factory_for_part = [[] for i in range(count_part)]
    for i in range(len(factory)):
        for j in factory[i]:
            factory_for_part[j].append(i)
    return factory, factory_for_part, count_machine, count_part


def vns(factory, factory_for_part, clusters, clusters_for_part, machines_in_clusters, part_in_clusters,
        clusters_in_machine, clusters_in_part, count_machine, count_part, n1_in, n0_in, factory_len, value):
    best_move = [0, 0]
    changed = True
    new_n1_in, new_n0_in = 0, 0
    while changed:
        changed = False
        nice_n1_in = n1_in
        nice_n0_in = n0_in
        for machine_number in range(count_machine):
            for cluster_number in range(len(clusters)):
                machine_belonging = clusters_in_machine[machine_number]
                if machine_belonging == cluster_number or len(machines_in_clusters[machine_belonging]) == 1:
                    continue
                new_value, new_n1_in, new_n0_in = calc_swap_machines(factory=factory, clusters=clusters,
                                                                     part_in_clusters=part_in_clusters,
                                                                     clusters_in_machine=clusters_in_machine,
                                                                     machine_number=machine_number,
                                                                     cluster_number=cluster_number, n1_in=n1_in,
                                                                     n0_in=n0_in, n1=factory_len)
                if new_value > value:
                    best_move[0] = machine_number
                    best_move[1] = cluster_number
                    value = new_value
                    nice_n1_in=new_n1_in
                    nice_n0_in=new_n0_in
                    changed = True
        if changed:
            n1_in = nice_n1_in
            n0_in = nice_n0_in

            clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part = swap_machines(
                factory, clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine,
                clusters_in_part,
                best_move[0], best_move[1])



        else:


            for part_number in range(count_part):
                for cluster_number in range(len(clusters_for_part)):
                    part_belonging = clusters_in_part[part_number]
                    if part_belonging == cluster_number or len(part_in_clusters[part_belonging]) == 1:
                        continue
                    new_value, new_n1_in, new_n0_in = calc_swap_parts(factory_for_part, clusters_for_part,
                                                                      machines_in_clusters,
                                                                      clusters_in_part,
                                                                      part_number,
                                                                      cluster_number, n1_in,
                                                                      n0_in, factory_len)
                    if new_value > value:
                        best_move[0] = part_number
                        best_move[1] = cluster_number
                        value = new_value
                        nice_n1_in = new_n1_in
                        nice_n0_in = new_n0_in
                        changed = True
            if changed:

                n1_in = nice_n1_in
                n0_in = nice_n0_in
                clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part = swap_parts(
                    factory_for_part, clusters, clusters_for_part, machines_in_clusters, part_in_clusters,
                    clusters_in_machine, clusters_in_part,
                    best_move[0], best_move[1])


            else:
                return clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, n1_in, n0_in, value


if __name__ == "__main__":

    def main():
        factory, factory_for_part, count_machine, count_part = get_machines_and_parts_from_file(
            "dataset/cfp/corm37.txt")
        max_count_clusters = min(count_machine, count_part)
        matrix = [[0 for j in range(count_part)] for i in range(count_machine)]
        for m_i, m in enumerate(factory):
            for p in m:
                matrix[m_i][p] = 1
        factory_len = sum(map(len, factory))
        super_value=0
        for first_create_param in range(2, max_count_clusters + 1):

            (clusters, machines_in_clusters,
             part_in_clusters, clusters_in_machine,
             clusters_in_part) = create_first_cluster(factory, count_machine, count_part,
                                                      first_create_param)

            value, n1_in, n0_in = get_value(clusters, machines_in_clusters, part_in_clusters, factory_len)

            clusters_for_part = [{} for i in range(len(clusters))]
            for i, num in enumerate(factory_for_part):
                list_machine = list()
                for j in num:
                    if clusters_in_machine[j] == clusters_in_part[i]:
                        list_machine.append(j)
                if list_machine:
                    clusters_for_part[clusters_in_part[i]][i] = list_machine

            clusters, clusters_for_part, \
            machines_in_clusters, part_in_clusters, \
            clusters_in_machine, clusters_in_part, \
            n1_in, n0_in, value = vns(
                factory, factory_for_part, clusters, clusters_for_part, machines_in_clusters, part_in_clusters,
                clusters_in_machine, clusters_in_part, count_machine, count_part, n1_in, n0_in, factory_len, value)

            r_clusters, r_clusters_for_part, \
            r_machines_in_clusters, r_part_in_clusters, \
            r_clusters_in_machine, r_clusters_in_part, \
            r_n1_in, r_n0_in, r_value = \
                clusters, clusters_for_part, \
                machines_in_clusters, part_in_clusters, \
                clusters_in_machine, clusters_in_part, \
                n1_in, n0_in, value

            ch = True
            while ch:
                ch = False
                len_clf = len(clusters)
                for i in range(len_clf):
                    if len(machines_in_clusters[i]) > 1 and len(part_in_clusters[i]) > 1:
                        d_machines_in_clusters, d_part_in_clusters, \
                        d_clusters_in_machine, d_clusters_in_part, \
                        d_clusters, d_clusters_for_part, \
                        d_value, d_n1_in, d_n0_in = \
                            divide_cluster(
                                deepcopy(machines_in_clusters),
                                deepcopy(part_in_clusters),
                                deepcopy(clusters_in_machine),
                                deepcopy(clusters_in_part),
                                deepcopy(clusters),
                                deepcopy(clusters_for_part), i, matrix, deepcopy(n1_in), deepcopy(n0_in), factory_len)
                        d_clusters, d_clusters_for_part, \
                        d_machines_in_clusters, d_part_in_clusters, \
                        d_clusters_in_machine, d_clusters_in_part, \
                        d_n1_in, d_n0_in, d_value = vns(
                            factory, factory_for_part,
                            d_clusters, d_clusters_for_part,
                            d_machines_in_clusters, d_part_in_clusters,
                            d_clusters_in_machine, d_clusters_in_part,
                            count_machine, count_part,
                            d_n1_in, d_n0_in, factory_len, d_value)
                        if d_value > value:
                            r_clusters, r_clusters_for_part, \
                            r_machines_in_clusters, r_part_in_clusters, \
                            r_clusters_in_machine, r_clusters_in_part, \
                            r_n1_in, r_n0_in, r_value = \
                                deepcopy(d_clusters), deepcopy(d_clusters_for_part), \
                                deepcopy(d_machines_in_clusters), deepcopy(d_part_in_clusters), \
                                deepcopy(d_clusters_in_machine), deepcopy(d_clusters_in_part), \
                                deepcopy(d_n1_in), deepcopy(d_n0_in), deepcopy(d_value)
                if r_value > value:
                    clusters, clusters_for_part, \
                    machines_in_clusters, part_in_clusters, \
                    clusters_in_machine, clusters_in_part, \
                    n1_in, n0_in, value = \
                        r_clusters, r_clusters_for_part, \
                        r_machines_in_clusters, r_part_in_clusters, \
                        r_clusters_in_machine, r_clusters_in_part, \
                        r_n1_in, r_n0_in, r_value
                    ch = True
                else:
                    len_clf=len(clusters)
                    for i in range(len_clf-1):
                        for j in range(i+1,len_clf):
                            d_machines_in_clusters, d_part_in_clusters, \
                            d_clusters_in_machine, d_clusters_in_part, \
                            d_clusters, d_clusters_for_part, \
                            d_value, d_n1_in, d_n0_in = merge_cluster(deepcopy(machines_in_clusters),
                                                                      deepcopy(part_in_clusters),
                                                                      deepcopy(clusters_in_machine),
                                                                      deepcopy(clusters_in_part),
                                                                      deepcopy(clusters),
                                                                      deepcopy(clusters_for_part), i, j, matrix, deepcopy(n1_in),
                                                                      deepcopy(n0_in), factory_len)

                            d_clusters, d_clusters_for_part, \
                            d_machines_in_clusters, d_part_in_clusters, \
                            d_clusters_in_machine, d_clusters_in_part, \
                            d_n1_in, d_n0_in, d_value = vns(
                                factory, factory_for_part,
                                d_clusters, d_clusters_for_part,
                                d_machines_in_clusters, d_part_in_clusters,
                                d_clusters_in_machine, d_clusters_in_part,
                                count_machine, count_part,
                                d_n1_in, d_n0_in, factory_len, d_value)
                            if d_value > value:
                                r_clusters, r_clusters_for_part, \
                                r_machines_in_clusters, r_part_in_clusters, \
                                r_clusters_in_machine, r_clusters_in_part, \
                                r_n1_in, r_n0_in, r_value = \
                                    deepcopy(d_clusters), deepcopy(d_clusters_for_part), \
                                    deepcopy(d_machines_in_clusters), deepcopy(d_part_in_clusters), \
                                    deepcopy(d_clusters_in_machine), deepcopy(d_clusters_in_part), \
                                    deepcopy(d_n1_in), deepcopy(d_n0_in), deepcopy(d_value)

                if r_value > value:
                    clusters, clusters_for_part, \
                    machines_in_clusters, part_in_clusters, \
                    clusters_in_machine, clusters_in_part, \
                    n1_in, n0_in, value = \
                        r_clusters, r_clusters_for_part, \
                        r_machines_in_clusters, r_part_in_clusters, \
                        r_clusters_in_machine, r_clusters_in_part, \
                        r_n1_in, r_n0_in, r_value

                    ch = True
            if(value>super_value):
                print(" ".join(map(str,clusters_in_machine)))
                print(" ".join(map(str,clusters_in_part)))
                print(value)
                super_value=value

    main()

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
