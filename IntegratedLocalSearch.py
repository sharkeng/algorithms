import math
import time
from random import randint
from tqdm import tqdm


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
        return {int(s.split()[0]): list(map(int, s.split()[1:])) for s in st if s}

two_opt_swap = lambda r, i, k: r[0:i] + r[k:-len(r) + i - 1:-1] + r[k + 1:len(r)]


class ILS:
    def __init__(self, filename):
        self.coords = get_coords_from_file(filename)
        self.old_i_dist, self.old_k_dist = 0, 0

    def get_dist(self, x, r):
        return math.hypot(self.coords[r[x-1]][0] - self.coords[r[x]][0], self.coords[r[x-1]][1] - self.coords[r[x]][1])

    def get_i_k_dists(self, i, k, route):
        try:
            new_k_dist = self.get_dist(k + 1, route)
        except:
            new_k_dist = 0
        try:
            new_i_dist = self.get_dist(i, route)
        except:
            new_i_dist = 0
        return new_i_dist, new_k_dist

    def calculate_total_distance(self, route, i=None, k=None, old_dist=None):
        if i and k and old_dist:
            return old_dist - self.old_i_dist - self.old_k_dist + sum(self.get_i_k_dists(i, k, route))
        else:
            res = 0
            for p in range(1, len(route)):
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

                    if current_dist - new_dist >= 1:
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

    def integrated_local_search(self, node, count):
        route, _ = self.greedy(node)
        print(_)
        route, min_distance = self.local_search(route)
        print("Distance after 2-Opt Approach:", min_distance)
        print(route, len(route))
        for i in tqdm(range(count)):
            new_route = self.four_opt(route)
            new_route, new_distance = self.local_search(new_route)
            if new_distance < min_distance:
                min_distance = new_distance
                route = new_route
        print("Distance after 4-Opt Approach:", min_distance)
        # print(route, len(route))
        return route, min_distance


# x, min_dist = ILS("datasets/ja_1000.txt").integrated_local_search(1, 300)

# print(" ".join(list(map(str, x))))
# print(f"Min dist: {min_dist}")

# # print(" ".join(list(map(str, x))))
#
# from multiprocessing.dummy import Pool as ThreadPool
#
# # Make the Pool of workers
# from os import walk
#
# _, _, filenames = next(walk("datasets"))
#
# x = {}
# for file in filenames:
#     x.update({file.split(".")[0]: ILS(f"datasets/{file}").integrated_local_search})
#
# pool = ThreadPool(len(filenames))
#
# # Open the URLs in their own threads
# # and return the results
# results = pool.map(urllib2.urlopen, urls)
#
# # Close the pool and wait for the work to finish
# pool.close()
# pool.join()

x = "485 450 43 390 458 4 26 245 216 348 839 862 407 182 211 748 209 8 867 438 995 729 57 278 988 895 81 310 945 723 594 975 636 929 462 526 187 29 155 603 753 79 912 201 952 232 496 684 578 276 309 810 279 122 508 124 662 898 375 150 592 392 566 55 959 823 144 115 941 165 724 645 492 567 652 268 557 357 14 612 790 660 606 37 850 599 429 114 537 214 419 706 816 668 482 190 364 804 813 90 672 405 368 733 573 582 986 874 520 749 950 725 722 420 755 346 517 949 435 699 229 818 252 694 856 277 166 962 921 641 289 553 905 702 487 47 946 903 934 766 328 569 457 426 547 75 46 176 194 609 930 953 20 149 556 760 586 157 301 632 831 629 658 734 447 195 308 206 774 314 85 621 466 327 964 752 71 220 318 64 836 866 219 202 449 886 900 826 174 773 904 955 305 116 847 255 126 101 95 620 1000 127 345 527 539 712 552 118 203 378 605 993 678 334 184 691 453 894 579 869 750 780 581 872 745 528 655 535 266 31 326 730 477 470 461 502 524 580 441 597 497 814 422 48 108 484 196 213 406 812 180 164 13 534 19 607 25 383 295 385 977 267 181 743 23 584 87 264 354 800 240 452 361 456 265 431 437 933 591 160 772 235 642 244 207 472 179 444 783 651 523 136 107 846 966 924 505 192 424 764 794 287 595 514 623 12 146 56 399 958 902 507 542 692 717 9 942 834 983 628 798 61 474 335 274 758 129 33 571 91 319 739 509 795 475 948 436 241 344 443 970 183 402 819 944 501 961 70 728 205 293 142 671 35 248 139 991 105 827 280 336 842 257 782 418 440 715 998 173 546 200 3 17 199 708 110 611 498 522 103 616 940 870 796 957 106 455 751 100 704 62 913 256 802 417 561 639 152 151 596 575 359 910 707 442 631 260 212 52 972 169 727 158 154 175 863 882 253 215 481 890 228 432 393 936 53 343 718 271 570 66 851 807 324 564 321 829 483 604 617 622 679 388 313 337 499 854 137 409 249 732 973 918 397 42 352 824 259 540 981 145 588 189 153 236 78 16 50 577 915 768 519 6 384 781 777 865 521 951 97 170 428 888 374 69 809 284 269 817 844 926 370 415 985 210 785 693 550 754 338 351 657 695 30 185 861 299 601 504 80 261 939 640 980 585 275 325 776 590 307 954 408 833 635 297 529 840 294 246 363 841 467 714 416 243 922 217 369 412 218 538 109 963 290 464 703 356 330 341 312 843 767 22 82 427 799 479 916 744 825 387 943 887 587 125 446 775 389 619 532 896 994 161 167 11 879 726 677 613 111 323 480 490 411 731 747 554 38 786 793 340 92 288 117 630 932 881 892 855 204 59 559 347 615 911 784 463 646 247 141 967 960 681 919 331 984 373 989 421 769 382 531 500 837 759 551 140 853 433 711 815 608 857 686 624 130 191 666 148 965 74 379 84 978 86 643 663 830 360 489 923 362 238 221 159 263 28 460 414 302 413 687 350 425 976 852 286 380 113 7 821 188 311 233 688 735 72 99 49 891 968 273 60 40 394 98 468 996 102 533 589 925 680 494 67 938 445 459 162 683 574 21 885 583 231 88 225 132 811 93 448 317 713 223 303 560 653 51 544 398 685 673 478 871 618 860 667 690 76 876 746 77 186 877 488 377 32 339 197 555 147 614 250 227 73 430 990 864 376 530 848 835 121 859 845 763 365 771 701 969 791 65 134 503 987 178 222 883 296 198 849 997 68 486 258 741 1 372 24 45 434 300 367 291 634 675 410 315 208 506 10 593 650 661 979 512 709 495 562 469 34 762 89 511 329 403 899 234 471 281 36 947 937 395 172 992 516 515 928 333 525 873 787 803 778 931 549 239 27 39 600 716 510 404 568 884 914 563 5 610 572 719 576 738 451 518 805 878 135 649 935 143 128 974 251 644 721 545 104 674 907 396 602 355 669 96 349 491 15 696 342 761 838 682 868 254 689 742 797 224 880 473 927 285 647 700 177 893 94 304 371 917 664 897 548 858 627 171 637 358 63 44 808 626 670 133 971 720 391 353 625 54 283 298 906 316 543 513 822 237 439 423 465 638 999 366 736 541 875 306 820 757 123 889 633 656 792 381 120 322 770 676 565 536 320 705 292 789 476 801 168 272 737 131 163 83 58 454 332 920 697 665 901 226 558 138 698 2 493 230 598 262 119 270 832 740 828 400 756 710 41 156 242 401 982 779 765 282 654 659 386 908 648 112 909 788 806 18 956 193"
# Min dist: 183086.7365476046
z = x.split()

print(ILS("datasets/ja_1000.txt").calculate_total_distance(z))
