def create_first_claster(factory, count_mashine, count_part, iter, max_count_clasters):
    clasters = list()
    left_machine_edge = 0
    left_part_edge = 0
    machines_in_clusters = list()
    part_in_clusters = list()
    machine_number=0
    clasters_in_machine=list()
    clasters_in_part=list()
    for i in range(iter):
        right_machine_edge = left_machine_edge + count_mashine // iter
        right_part_edge = left_part_edge + count_part // iter
        if (i == iter - 1):
            right_machine_edge = count_machine
            right_part_edge = count_part
        claster = {}
        one_machines_in_claster = list()
        one_part_in_claster = list()
        for j in range(left_part_edge, right_part_edge):
            one_part_in_claster.append(j)
            clasters_in_part.append(i)
        part_in_clusters.append(one_part_in_claster)
        for j in range(left_machine_edge, right_machine_edge):
            one_machines_in_claster.append(j)
            parts = list()
            clasters_in_machine.append(i)
            for k in factory[j]:
                if k >= left_part_edge and k < right_part_edge:
                    parts.append(k)
            claster[machine_number]=parts
            machine_number+=1
        left_machine_edge = right_machine_edge
        left_part_edge = right_part_edge
        machines_in_clusters.append(one_machines_in_claster)
        clasters.append(claster)
    return clasters, machines_in_clusters, part_in_clusters,clasters_in_machine,clasters_in_part


def get_value(clasters, machines_in_clusters, part_in_clusters, factory_len):
    n1_in = 0
    n0_in = 0
    for k in range(len(clasters)):
        n1_in += len(clasters[k])
        n0_in += len(machines_in_clusters[k]) * len(part_in_clusters[k]) - len(clasters[k])
    return n1_in / (factory_len + n0_in),n1_in,n0_in


def divide_clusters():
    pass


def merge_clusters():
    pass


def swap_machines(factory,clasters,machines_in_clusters,part_in_clusters,clasters_in_machine,clasters_in_part,machine_number,claster_number):
    machine_belonging=clasters_in_machine[machine_number]
    if(machine_belonging==claster_number):
        print(("OH Shit this is current claster"))
        return
    if (len(clasters[machine_belonging])==1):
        print("Null CLasters")
        return
    dif_n=len(clasters[machine_belonging].pop(machine_number))
    machines_in_clusters[claster_number].append(machine_number)
    machines_in_clusters[machine_belonging].remove(machine_number)
    clasters_in_machine[machine_number]=claster_number
    parts=list()
    for part in factory[machine_number]:
        if part in part_in_clusters[claster_number]:
            parts.append(part)
    clasters[claster_number][machine_number]=parts
    print(clasters)
    print(machines_in_clusters)
    print(part_in_clusters)
    print(clasters_in_machine)
    print(clasters_in_part)

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
    max_count_clasters = min(count_machine, count_part)
    print(factory)
    factory_len = 0
    for i in factory:
        factory_len += len(i)
    clasters, machines_in_clusters, part_in_clusters,clasters_in_machine,clasters_in_part = create_first_claster(factory, count_machine, count_part,
                                                                            (max_count_clasters + 2) // 2,
                                                                            max_count_clasters)
    print(clasters, "\n", machines_in_clusters, "\n", part_in_clusters)
    print(clasters_in_machine,clasters_in_part)
    print(len(clasters[2]))
    value,n1_in,n0_in= get_value(clasters, machines_in_clusters, part_in_clusters, factory_len)
    print(value,n1_in,n0_in)

    factory=swap_machines(factory,clasters,machines_in_clusters,part_in_clusters,clasters_in_machine,clasters_in_part,2,2)
    print(factory)
# [[2, 4, 5, 6], [1, 3], [1, 3, 7], [2, 4, 6], [1, 7]]
#
# [[2]}, [1,3]]
# [[7]}, [4, 6]}, [7]]
#
# [[2,4], [1]]
# [[3,7], [6], [7]]


# [[1], [0,2]]
# [[6], [3,5], [6]]


#БЫЛО
# [[1, 3, 4, 5], [0, 2], [0, 2, 6], [1, 3, 5], [0, 6]]
# [[{0:[1]}], [{1:[2]}], [{2:[6]}, {3:[5]}, {4:[6]]]
#  [[0], [1], [2, 3, 4]]
#  [[0, 1], [2, 3], [4, 5, 6]]

# 3
# 0.22727272727272727


#СТАЛО
#[[{0:[1]},{2:[0]}],  [{1:[2]]}, [{3:[5], {4:[6]}]]
#[[0,2], [1], [3,4]]
#[[0,1], [2,3], [4,5,6]




#
#     0   1   2   3   4   5   6
# 0       #       #   #   #
# 1   #       #
# 2   #       #               #
# 3       #       #       #
# 4   #                       #
