import math
import time
from random import randint
from tqdm import tqdm


def to_list(r):
    return list(map(int, r.split()))


def to_str(r):
    return " ".join(list(map(str, r)))


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
        return {int(s.split()[0]): list(map(float, s.split()[1:])) for s in st if s}


two_opt_swap = lambda r, i, k: r[0:i] + r[k:-len(r) + i - 1:-1] + r[k + 1:len(r)]


class ILS:
    def __init__(self, filename):
        self.coords = get_coords_from_file(filename)
        self.old_i_dist, self.old_k_dist = 0, 0

    def get_dist(self, x, r):
        return math.hypot(self.coords[r[x - 1]][0] - self.coords[r[x]][0],
                          self.coords[r[x - 1]][1] - self.coords[r[x]][1])

    def get_i_k_dists(self, i, k, route):
        try:
            new_k_dist = self.get_dist(k + 1 if k + 1 < len(route) else 0, route)
        except KeyError:
            new_k_dist = 0
        try:
            new_i_dist = self.get_dist(i, route)
        except KeyError:
            new_i_dist = 0
        return new_i_dist, new_k_dist

    def calculate_total_distance(self, route, i=None, k=None, old_dist=None):
        if i and k and old_dist:
            return old_dist - self.old_i_dist - self.old_k_dist + sum(self.get_i_k_dists(i, k, route))
        else:
            res = 0
            for p in range(len(route)):
                res += self.get_dist(p, route)
        return res

    def two_opt(self, route):
        existing_route = route
        current_dist = self.calculate_total_distance(route)
        changed = True
        while changed:
            changed = False
            for i in range(len(existing_route)):
                for k in range(i + 1, len(existing_route)):
                    self.old_i_dist, self.old_k_dist = self.get_i_k_dists(i, k, existing_route)

                    new_route = two_opt_swap(existing_route, i, k)
                    new_dist = self.calculate_total_distance(new_route, i, k, current_dist)

                    if current_dist - new_dist >= 0.3:
                        # print(new_dist)
                        existing_route = new_route
                        current_dist = new_dist
                        changed = True
        return existing_route, current_dist

    def four_opt(self, route):
        rand_kek = lambda: randint(0, len(route) - 1) // 4
        x = rand_kek()
        y = x + rand_kek()
        z = y + rand_kek()
        return route[:x] + route[z:] + route[y:z] + route[x:y]

    def greedy(self, node=1):
        route_best = []
        len_best = float('inf')
        # for iter_index, iter in tqdm(coords.items()):
        route = [node]
        new_city_index, new_city_coords, distance = self.make_closer(self.coords[node], route)
        len_route = distance
        route.append(new_city_index)
        while len(route) < len(self.coords):
            new_city_index, new_city_coords, distance = self.make_closer(new_city_coords, route)
            len_route += distance
            route.append(new_city_index)
        if len_route < len_best:
            len_best = len_route
            route_best = route
        return route_best, len_best

    def make_closer(self, coords_city, past_cities):
        dist_best = float('inf')
        for id, cs in self.coords.items():
            if id not in past_cities:
                distance = math.hypot(coords_city[0] - cs[0], coords_city[1] - cs[1])
                if distance < dist_best:
                    dist_best = distance
                    closer_city_id = id
                    closer_city_coords = cs
        return closer_city_id, closer_city_coords, dist_best

    def local_search(self, start_route):
        return self.two_opt(start_route)

    def integrated_local_search(self, node, count=None, share_dict=None, wanted_distance=None, last_route=None):
        if share_dict:
            share_dict["found_new_route"] = False
            last_route = share_dict["route"]
            wanted_distance = share_dict["wanted_dist"]
        if last_route:
            route = last_route
        else:
            route, _ = self.greedy(node)
            print(_)
        route, min_distance = self.local_search(route)
        print("Distance after 2-Opt Approach:", min_distance)
        print(route, len(route))
        if count:
            for i in tqdm(range(count)):
                new_route = self.four_opt(route)
                new_route, new_distance = self.local_search(new_route)
                if new_distance < min_distance:
                    min_distance = new_distance
                    route = new_route
        elif wanted_distance:
            while min_distance > wanted_distance:
                if share_dict["found_new_route"]:
                    print("Restarting, because of new route!")
                    #loop.run_until_complete(tg_bot.close())
                    exit()

                new_route = self.four_opt(route)
                new_route, new_distance = self.local_search(new_route)
                # print(new_distance, new_distance-wanted_distance)
                if new_distance < min_distance:
                    print(new_route, "\n", new_distance, ">", wanted_distance)
                    #loop.run_until_complete(tg_bot.send_message("446162145", f"{to_str(new_route)} {new_distance} > {wanted_distance}"))
                    share_dict["found_new_route"] = True
                    share_dict["route"] = new_route
                    min_distance = new_distance
                    route = new_route
        print("Distance after 4-Opt Approach:", min_distance)
        # print(route, len(route))
        return route, min_distance

x = [538, 109, 963, 290, 464, 275, 585, 980, 299, 861, 22, 82, 427, 799, 185, 30, 695, 657, 351, 338, 754, 269, 817, 106, 957, 796, 704, 100, 751, 455, 284, 809, 69, 62, 913, 256, 802, 417, 374, 888, 428, 170, 97, 561, 951, 521, 777, 865, 639, 152, 151, 596, 575, 259, 540, 981, 145, 588, 189, 153, 236, 78, 16, 50, 577, 768, 915, 781, 384, 6, 519, 844, 926, 370, 415, 985, 210, 785, 693, 550, 559, 59, 347, 615, 911, 784, 463, 646, 247, 141, 967, 960, 681, 919, 331, 984, 373, 989, 421, 769, 382, 531, 500, 837, 759, 551, 140, 853, 433, 711, 815, 130, 608, 857, 624, 686, 643, 86, 978, 663, 830, 360, 489, 923, 362, 84, 379, 74, 965, 191, 666, 111, 613, 148, 238, 221, 159, 263, 28, 460, 414, 413, 302, 2, 138, 558, 665, 901, 226, 698, 533, 589, 925, 680, 968, 273, 60, 40, 394, 102, 996, 98, 468, 425, 350, 687, 446, 775, 389, 619, 532, 896, 726, 677, 879, 167, 994, 161, 11, 323, 480, 490, 411, 731, 747, 554, 38, 786, 793, 340, 288, 92, 204, 117, 855, 892, 881, 630, 932, 744, 916, 479, 825, 587, 125, 887, 943, 387, 767, 843, 312, 341, 330, 703, 356, 113, 7, 380, 286, 852, 976, 821, 188, 311, 233, 688, 735, 72, 99, 49, 891, 494, 67, 938, 445, 459, 162, 683, 574, 21, 885, 583, 231, 88, 225, 132, 811, 93, 448, 133, 971, 391, 720, 670, 626, 808, 44, 317, 63, 358, 713, 637, 171, 627, 858, 917, 548, 897, 664, 223, 303, 51, 653, 560, 871, 478, 618, 860, 690, 667, 76, 876, 746, 77, 186, 877, 488, 377, 32, 339, 197, 555, 430, 73, 227, 990, 365, 763, 864, 376, 530, 848, 121, 859, 845, 969, 791, 701, 771, 65, 134, 503, 987, 883, 178, 222, 296, 198, 849, 997, 68, 486, 258, 741, 24, 45, 434, 1, 372, 835, 300, 367, 291, 634, 675, 410, 315, 208, 506, 10, 593, 650, 661, 979, 512, 709, 495, 562, 469, 34, 762, 89, 511, 329, 403, 899, 234, 471, 281, 36, 947, 937, 395, 172, 992, 516, 515, 928, 333, 525, 873, 787, 803, 778, 250, 614, 147, 549, 931, 239, 27, 39, 600, 716, 510, 404, 568, 884, 914, 563, 5, 610, 673, 685, 398, 544, 371, 304, 94, 893, 700, 177, 719, 572, 576, 738, 878, 135, 649, 935, 143, 128, 251, 974, 518, 805, 451, 285, 647, 298, 906, 283, 54, 625, 353, 316, 543, 513, 822, 237, 439, 423, 465, 638, 999, 306, 820, 757, 123, 889, 633, 656, 792, 875, 541, 736, 366, 689, 742, 797, 224, 880, 927, 473, 602, 396, 644, 721, 545, 104, 674, 907, 355, 669, 96, 254, 868, 682, 838, 761, 342, 349, 491, 15, 696, 381, 120, 322, 770, 676, 565, 536, 320, 705, 292, 789, 476, 801, 168, 272, 737, 131, 163, 83, 58, 697, 920, 332, 454, 493, 230, 598, 262, 119, 270, 832, 740, 828, 400, 756, 710, 41, 156, 242, 401, 982, 779, 765, 386, 908, 112, 648, 282, 659, 654, 909, 788, 806, 18, 956, 193, 566, 392, 592, 150, 375, 898, 662, 124, 508, 810, 309, 276, 578, 684, 496, 232, 952, 594, 723, 945, 310, 526, 636, 975, 201, 912, 79, 753, 603, 155, 929, 462, 187, 29, 81, 895, 988, 278, 862, 407, 182, 211, 57, 729, 995, 438, 748, 209, 8, 867, 839, 245, 216, 348, 390, 43, 450, 485, 458, 4, 26, 279, 122, 55, 959, 823, 115, 941, 144, 165, 724, 645, 492, 567, 652, 268, 557, 357, 14, 668, 482, 190, 364, 804, 573, 733, 368, 582, 986, 405, 672, 813, 90, 816, 606, 660, 612, 790, 37, 850, 599, 429, 114, 537, 214, 419, 706, 950, 874, 520, 749, 517, 949, 435, 818, 699, 229, 277, 166, 962, 289, 921, 641, 934, 457, 766, 328, 569, 426, 547, 75, 609, 930, 953, 20, 149, 194, 176, 46, 903, 946, 47, 487, 905, 553, 702, 658, 734, 629, 586, 760, 556, 831, 157, 301, 632, 195, 308, 447, 206, 774, 856, 694, 252, 85, 314, 847, 255, 126, 101, 95, 1000, 127, 345, 527, 539, 56, 146, 399, 958, 902, 507, 542, 692, 717, 9, 942, 834, 983, 628, 798, 61, 107, 846, 966, 924, 505, 192, 424, 764, 794, 287, 623, 12, 514, 595, 894, 579, 453, 691, 184, 334, 678, 993, 605, 378, 203, 118, 712, 552, 620, 116, 305, 955, 964, 327, 621, 466, 346, 755, 420, 722, 725, 866, 219, 449, 202, 836, 64, 318, 220, 71, 752, 904, 773, 174, 826, 900, 886, 655, 535, 266, 31, 326, 477, 730, 461, 470, 528, 745, 872, 750, 869, 780, 581, 431, 437, 933, 265, 361, 456, 240, 452, 160, 591, 772, 235, 267, 181, 743, 23, 584, 87, 800, 354, 264, 580, 524, 502, 441, 597, 497, 814, 422, 48, 108, 484, 196, 213, 406, 812, 180, 164, 13, 534, 19, 607, 25, 383, 295, 385, 977, 642, 244, 207, 472, 179, 444, 783, 651, 523, 136, 795, 475, 948, 509, 739, 274, 474, 335, 758, 129, 33, 571, 91, 319, 436, 241, 344, 443, 970, 183, 402, 819, 944, 501, 961, 70, 728, 205, 293, 142, 671, 35, 248, 139, 991, 105, 827, 280, 336, 842, 257, 782, 212, 52, 972, 169, 727, 158, 154, 175, 863, 882, 253, 215, 481, 890, 228, 432, 393, 936, 53, 343, 718, 807, 324, 564, 321, 829, 483, 604, 617, 622, 679, 388, 313, 337, 499, 854, 260, 631, 442, 137, 409, 249, 732, 973, 918, 397, 851, 66, 570, 271, 42, 352, 824, 359, 707, 910, 418, 440, 715, 998, 173, 546, 200, 17, 199, 3, 708, 110, 611, 498, 522, 103, 616, 940, 870, 601, 504, 80, 261, 939, 640, 325, 776, 590, 307, 954, 408, 833, 635, 297, 529, 840, 294, 246, 363, 841, 467, 714, 416, 243, 922, 217, 369, 412, 218]
from multiprocessing import Process, Manager

if __name__ == '__main__':
    manager = Manager()
    shared_dict = manager.dict()
    shared_dict["wanted_dist"] = 194000
    shared_dict["route"] = x
    shared_dict["found_new_route"] = False
    processes = []
    for i in range(0, 3):
        p = Process(target=ILS("datasets/ja_1000.txt").integrated_local_search, args=(1, None, shared_dict))
        processes.append(p)
        p.start()

    while True:
        for i, process in enumerate(processes):
            if not process.is_alive():
                processes[i] = Process(target=ILS("datasets/ja_1000.txt").integrated_local_search, args=(1, None, shared_dict))
                processes[i].start()
        for i, process in enumerate(processes):
            if process.is_alive():
                process.join()


