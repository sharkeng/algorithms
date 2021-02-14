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


factory, factory_for_part, count_machine, count_part=get_machines_and_parts_from_file("dataset/cfp/corm37.txt")

matrix=list()

