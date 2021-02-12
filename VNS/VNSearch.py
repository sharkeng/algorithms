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


# def calc_divide_cluster(machines_in_clusters, part_in_clusters, clusters, num_cluster_to_change, n1_in, n0_in, n1):
#     m_cl = machines_in_clusters[num_cluster_to_change]
#     p_cl = part_in_clusters[num_cluster_to_change]
#     len_p_cl = len(p_cl)
#     len_m_cl = len(m_cl)
#     new_cl_id = len(clusters)
#
#     new_m_cl_left, new_m_cl_right = m_cl[len_m_cl // 2:], m_cl[:len_m_cl // 2]
#     new_p_cl_up, new_p_cl_down = p_cl[len_p_cl // 2:], p_cl[:len_p_cl // 2]
#
#     old_len = len_m_cl * len_p_cl
#     old_n1_in = sum(map(len, clusters[num_cluster_to_change].values()))
#     old_n0_in = old_len - old_n1_in
#
#     old_len = len_m_cl * len_p_cl
#     old_n1_in = sum(map(len, clusters[num_cluster_to_change].values()))
#     old_n0_in = old_len - old_n1_in

def merge_cluster(machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, clusters,
                  clusters_for_part, num_cl_1, num_cl_2, matrix):
    clusters[num_cl_1] = {}
    clusters_for_part[num_cl_1] = {}
    del clusters[num_cl_2]
    del clusters_for_part[num_cl_2]

    machines = machines_in_clusters[num_cl_1] + machines_in_clusters[num_cl_2]
    parts = part_in_clusters[num_cl_1] + part_in_clusters[num_cl_2]

    for m in machines:
        parts_for_every_m = []
        for p in parts:
            if matrix[m][p]:
                parts_for_every_m.append(p)
        clusters[num_cl_1][m] = parts_for_every_m

    for p in parts:
        machines_for_every_m = []
        for m in machines:
            if matrix[m][p]:
                machines_for_every_m.append(p)
        clusters_for_part[num_cl_1][p] = machines_for_every_m

    del machines_in_clusters[num_cl_2]
    del part_in_clusters[num_cl_2]
    machines_in_clusters[num_cl_1] = machines
    part_in_clusters[num_cl_1] = parts

    for i, x in enumerate(clusters_in_machine):
        if x == num_cl_2:
            clusters_in_machine[i] = num_cl_1

    for i, x in enumerate(clusters_in_part):
        if x == num_cl_2:
            clusters_in_part[i] = num_cl_1

    return machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, clusters, clusters_for_part


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
    # print(p_cl)

    new_m_cl_left, new_m_cl_right = m_cl[:len_m_cl // 2], m_cl[len_m_cl // 2:]
    new_p_cl_up, new_p_cl_down = p_cl[:len_p_cl // 2], p_cl[len_p_cl // 2:]

    machines_in_clusters[num_cluster_to_change] = new_m_cl_left
    part_in_clusters[num_cluster_to_change] = new_p_cl_up
    machines_in_clusters.append(new_m_cl_right)
    part_in_clusters.append(new_p_cl_down)
    # print("!!!!!!!!@@@@!!!!!!!!!")
    # print(clusters)
    # print(clusters_for_part, num_cluster_to_change, m_cl, p_cl)
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

    # print(clusters)
    # print(clusters_for_part, num_cluster_to_change, m_cl, p_cl)
    # print("!!!!!!!!!@@@@!!!!!!!!")

    # for m in m_cl:
    #     for p in p_cl:
    #         if m in new_m_cl_left and p in new_p_cl_up:
    #             clusters[num_cluster_to_change]
    #         x = clusters[num_cluster_to_change].pop(m)
    # clusters.append({})
    # for m in new_m_cl_right:
    #     clusters_in_machine[m] = new_cl_id
    #     try:
    #         x = clusters[num_cluster_to_change].pop(m)
    #         print(m)
    #         p_to_add = []
    #         for p in new_p_cl_down:
    #             if p in x:
    #                 p_to_add.append(p)
    #         if p_to_add:
    #             clusters[new_cl_id].update({m: p_to_add})
    #     except KeyError:
    #         continue
    # print(clusters, clusters_for_part, num_cluster_to_change)
    # print("!!!!!!!!!@@@@!!!!!!!!")
    # clusters_for_part.append({})
    # print("!!!!!!!!!!!!!!!!!")
    # print(clusters, clusters_for_part, num_cluster_to_change)
    # print(new_p_cl_down)
    # for p in new_p_cl_down:
    #     clusters_in_part[p] = new_cl_id
    #     print(p)
    #     try:
    #         x = clusters_for_part[num_cluster_to_change].pop(p)
    #         m_to_add = []
    #         for m in new_m_cl_right:
    #             if m in x:
    #                 m_to_add.append(m)
    #         if m_to_add:
    #             clusters_for_part[new_cl_id].update({p: m_to_add})
    #     except KeyError:
    #         continue

    # print(clusters, clusters_for_part, num_cluster_to_change)
    # print("!!!!!!!!!!!!!!!!!")
    return machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, clusters, clusters_for_part, value, n1_in, n0_in


def merge_clusters():
    pass


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
                # print("=======================")
                # print(clusters_for_part, cluster_number, part, machine_number)
                clusters_for_part[cluster_number][part] = [machine_number]
                # print(clusters_for_part, cluster_number, part, machine_number)
                # print("=======================")
        if part in part_in_clusters[machine_belonging]:
            try:
                # print("--------------")
                # print(clusters)
                # print(clusters_for_part, machine_belonging, part, machine_number)
                # print(part_in_clusters, cluster_number)
                # print(machines_in_clusters)
                # print('$$$$$$$$$')

                clusters_for_part[machine_belonging][part].remove(machine_number)
                # print(clusters_for_part, machine_belonging, part, machine_number)
                # print('------------')


            except KeyError:
                pass

    # print('DD', clusters)
    # print(parts)
    clusters[cluster_number][machine_number] = parts
    try:
        del clusters[machine_belonging][machine_number]
    except KeyError:
        pass
    # print('dsq', clusters)

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
    # print("CLASTER IN MACHIEN",clusters_in_machine)
    # print("OLD",part_in_clusters,cluster_number,part_number)
    part_in_clusters[cluster_number].append(part_number)
    # print("new",part_in_clusters,part_belonging,part_number)
    part_in_clusters[part_belonging].remove(part_number)
    clusters_in_part[part_number] = cluster_number
    machines = list()
    # print("fdffdfdf")
    for machine in factory_for_part[part_number]:
        if machine in machines_in_clusters[cluster_number]:
            machines.append(machine)
            try:
                # print("=----------------------")
                # print(clusters, cluster_number, machine, part_number)
                clusters[cluster_number][machine].append(part_number)
                # print(clusters, cluster_number, machine, part_number)
            except KeyError:
                clusters[cluster_number][machine] = [part_number]
        if machine in machines_in_clusters[part_belonging]:
            try:
                clusters[part_belonging][machine].remove(part_number)
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

                    print("NEW VALUE", value)
                    # print("NNNN", n1_in, n0_in)
                    changed = True
        if changed:
            clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part = swap_machines(
                factory, clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine,
                clusters_in_part,
                best_move[0], best_move[1])
            n1_in = new_n1_in
            n0_in = new_n0_in
        else:
            # print("HFHF",value)
            # print("CLASTER OLD",clusters,clusters_for_part)
            # print("NNNN", n1_in, n0_in)
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
                        print("NEW VALUE", value)
                        print("SUPERT")
                        # print("NNNN",n1_in,n0_in)
                        changed = True
            if changed:
                clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part = swap_parts(
                    factory_for_part, clusters, clusters_for_part, machines_in_clusters, part_in_clusters,
                    clusters_in_machine, clusters_in_part,
                    best_move[0], best_move[1])
                n1_in = new_n1_in
                n0_in = new_n0_in
            else:
                return clusters, clusters_for_part, machines_in_clusters, part_in_clusters, clusters_in_machine, clusters_in_part, n1_in, n0_in, value


if __name__ == "__main__":

    def main():
        factory, factory_for_part, count_machine, count_part = get_machines_and_parts_from_file(
            "dataset/cfp/zolf50.txt")
        max_count_clusters = min(count_machine, count_part)
        matrix = [[0 for j in range(count_part)] for i in range(count_machine)]
        for m_i, m in enumerate(factory):
            for p in m:
                matrix[m_i][p] = 1
        factory_len = sum(map(len, factory))
        (clusters, machines_in_clusters,
         part_in_clusters, clusters_in_machine,
         clusters_in_part) = create_first_cluster(factory, count_machine, count_part,
                                                  (max_count_clusters + 2) // 2)

        value, n1_in, n0_in = get_value(clusters, machines_in_clusters, part_in_clusters, factory_len)
        print(value, n1_in, n0_in)
        best_move = [0, 0]
        # print("factory", factory)
        # print("clusters", clusters)
        # print("machines_in_clusters", machines_in_clusters)
        # print("part_in_clusters", part_in_clusters)
        # print("clusters_in_machine", clusters_in_machine)
        # print("clusters_in_part", clusters_in_part)
        # print(factory_for_part)
        clusters_for_part = [{} for i in range(len(clusters))]
        # print(clusters_for_part)
        for i, num in enumerate(factory_for_part):
            list_machine = list()
            for j in num:
                if clusters_in_machine[j] == clusters_in_part[i]:
                    list_machine.append(j)
            if list_machine:
                clusters_for_part[clusters_in_part[i]][i] = list_machine
        # print("fdf", clusters_for_part)

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
            for i in range(len(clusters)):
                print(machines_in_clusters[i], part_in_clusters[i])
                if len(machines_in_clusters[i]) > 1 and len(part_in_clusters[i]) > 1:
                    d_machines_in_clusters, d_part_in_clusters, \
                    d_clusters_in_machine, d_clusters_in_part, \
                    d_clusters, d_clusters_for_part,\
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
                    print(d_value, value)
                    if d_value > value:
                        print(d_value)
                        r_clusters, r_clusters_for_part, \
                        r_machines_in_clusters, r_part_in_clusters, \
                        r_clusters_in_machine, r_clusters_in_part, \
                        r_n1_in, r_n0_in, r_value = \
                            deepcopy(d_clusters), deepcopy(d_clusters_for_part), \
                            deepcopy(d_machines_in_clusters), deepcopy(d_part_in_clusters), \
                            deepcopy(d_clusters_in_machine), deepcopy(d_clusters_in_part), \
                            deepcopy(d_n1_in), deepcopy(d_n0_in), deepcopy(d_value)

            if r_value > value:
                print(r_value)
                clusters, clusters_for_part, \
                machines_in_clusters, part_in_clusters, \
                clusters_in_machine, clusters_in_part, \
                n1_in, n0_in, value = \
                    r_clusters, r_clusters_for_part, \
                    r_machines_in_clusters, r_part_in_clusters, \
                    r_clusters_in_machine, r_clusters_in_part, \
                    r_n1_in, r_n0_in, r_value
                ch = True

        print("factory", factory)
        print("factory_for_part", factory_for_part)
        print("clusters", clusters)
        print("clusters_for_part", clusters_for_part)
        print("machines_in_clusters", machines_in_clusters)
        print("part_in_clusters", part_in_clusters)
        print("clusters_in_machine", clusters_in_machine)
        print("clusters_in_part", clusters_in_part)
        print(value)


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
