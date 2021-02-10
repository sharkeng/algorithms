def shaking(factory, iter,max_claster):
    pass






def get_machines_and_parts_from_file(path):
    with open(path) as f:
        numbers_machine, numbers_part = [int(num) for num in f.readline().split()]
        factory = list()
        for i in range(numbers_machine):
            factory.append([int(num) for num in f.readline().split()][1:])
    return factory, numbers_machine, numbers_part


factory, numbers_machine, numbers_part = get_machines_and_parts_from_file(
    "dataset/#1 - King and Nakornchai(1982)[Figure-1a] ")
max_claster=min(numbers_machine,numbers_part)
shaking(factory,2,max_claster)

