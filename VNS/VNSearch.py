def shaking(factory, count_mashine, count_part,  iter, max_count_clasters):
    pass


def get_machines_and_parts_from_file(path):
    with open(path) as f:
        count_machine, count_part = [int(num) for num in f.readline().split()]
        factory = list()
        for i in range(count_machine):
            factory.append([int(num)-1 for num in f.readline().split()][1:])
    return factory, count_machine, count_part


def make_clusters(factory, count_m, count_p, count_clusters):

# 2  - max_count_clusters

if __name__ == "__main__":
    factory, count_machine, count_part = get_machines_and_parts_from_file(
        "dataset/#1 - King and Nakornchai(1982)[Figure-1a] ")
    max_count_clasters = min(count_machine, count_part)
    shaking(factory, count_machine, count_part, 2, max_count_clasters)

    print(factory)
# [[2, 4, 5, 6], [1, 3], [1, 3, 7], [2, 4, 6], [1, 7]]
#
# [{1:[2]}, {2:[1,3]}]
# [{3:[7]}, {4:[4, 6]}, {5:[7]}]
#
# [[2,4], [1]]
# [[3,7], [6], [7]]
#
#     1   2   3   4   5   6   7
# 1       #       #   #   #
# 2   #       #
# 3   #       #               #
# 4       #       #       #
# 5   #                       #

