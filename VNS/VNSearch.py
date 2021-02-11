def create_first_claster(factory, count_mashine, count_part,  iter, max_count_clasters):
    clasters=list()
    left_machine_edge=0
    left_part_edge=0
    for i in range(iter):
        right_machine_edge=left_machine_edge+count_mashine//iter
        right_part_edge=left_part_edge+count_part//iter
        if(i==iter-1):
            right_machine_edge=count_machine
            right_part_edge=count_part
        claster = list()
        for j in range(left_machine_edge,right_machine_edge):
            machine = list()
            for k in factory[j]:
                if k>=left_part_edge and k<right_part_edge:
                    machine.append(k)
            claster.append(machine)
        left_machine_edge=right_machine_edge
        left_part_edge=right_part_edge
        clasters.append(claster)
    return clasters


def divide_clusters():
    pass


def merge_clusters():
    pass


def swap_machines():
   pass


def swap_parts():
    pass



def get_machines_and_parts_from_file(path):
    with open(path) as f:
        count_machine, count_part = [int(num) for num in f.readline().split()]
        factory = list()
        for i in range(count_machine):
            factory.append([int(num)-1 for num in f.readline().split()][1:])
    return factory, count_machine, count_part



# 2  - max_count_clusters

if __name__ == "__main__":
    factory, count_machine, count_part = get_machines_and_parts_from_file(
        "dataset/#1 - King and Nakornchai(1982)[Figure-1a] ")
    max_count_clasters = min(count_machine, count_part)
    print(factory)
    for count_clasters in range(2,max_count_clasters+1):
        clasters=create_first_claster(factory, count_machine, count_part, count_clasters, max_count_clasters)
        print(clasters)

# [[2, 4, 5, 6], [1, 3], [1, 3, 7], [2, 4, 6], [1, 7]]
#
# [[2]}, [1,3]]
# [[7]}, [4, 6]}, [7]]
#
# [[2,4], [1]]
# [[3,7], [6], [7]]



#[[1], [0,2]]
#[[6], [3,5], [6]]


#
#     0   1   2   3   4   5   6
# 0       #       #   #   #
# 1   #       #
# 2   #       #               #
# 3       #       #       #
# 4   #                       #

