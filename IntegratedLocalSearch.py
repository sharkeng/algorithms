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
        return {int(s.split()[0]): list(map(float, s.split()[1:])) for s in st if s}


two_opt_swap = lambda r, i, k: r[0:i] + r[k:-len(r) + i - 1:-1] + r[k + 1:len(r)]


class ILS:
    def __init__(self, filename):
        self.coords = get_coords_from_file(filename)
        self.old_i_dist, self.old_k_dist = 0, 0

    def get_dist(self, x, r):
        return math.hypot(self.coords[r[x-1]][0] - self.coords[r[x]][0], self.coords[r[x-1]][1] - self.coords[r[x]][1])

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


# x, min_dist = ILS("datasets/mona_1000.txt").integrated_local_search(1, 2)
#
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

x = "207 633 850 845 94 859 296 958 30 440 12 685 478 93 897 779 833 818 953 300 803 501 981 806 561 828 299 629 481 532 365 488 133 891 180 311 49 289 444 977 61 201 153 668 910 766 139 930 725 53 615 262 156 849 569 542 751 753 173 932 368 587 870 586 351 856 1 832 423 862 373 334 874 424 63 505 357 576 533 150 206 908 225 657 952 588 827 24 755 113 391 397 752 652 563 20 73 973 140 861 171 123 966 78 98 301 965 945 388 969 307 385 705 541 723 163 104 203 26 336 624 122 97 38 579 508 621 421 894 573 479 468 968 537 985 161 54 398 912 264 378 224 64 376 721 837 175 130 674 776 783 194 951 582 167 471 707 608 272 144 136 497 898 286 794 354 918 127 147 913 425 638 520 820 447 983 328 135 396 466 892 800 146 409 975 50 129 991 18 745 905 777 860 333 500 48 821 314 854 791 498 655 281 268 640 160 782 192 3 8 52 82 670 483 748 927 372 492 667 625 578 214 32 389 491 811 959 291 970 530 74 798 276 404 240 489 758 212 946 817 617 106 234 807 810 938 428 540 571 899 627 401 222 200 785 495 742 377 165 277 689 601 232 4 204 35 802 116 528 823 847 643 406 851 518 125 884 546 417 217 606 531 6 344 936 181 347 39 671 934 239 485 198 565 538 620 706 220 356 184 282 630 808 298 921 361 835 221 332 306 605 432 11 649 367 596 238 352 294 205 926 318 558 384 448 252 493 174 216 316 529 864 364 353 326 678 434 885 684 189 320 117 245 442 796 190 111 199 81 631 813 719 661 273 829 410 550 574 88 526 710 470 5 769 229 143 476 236 773 92 330 290 940 436 168 744 566 210 693 902 553 244 33 841 507 429 235 395 786 121 720 650 694 857 188 169 516 152 602 695 733 737 137 266 580 310 848 654 91 770 916 477 816 994 258 700 183 961 407 947 43 883 729 781 944 622 517 374 746 115 844 804 838 193 325 453 768 696 957 750 663 405 594 254 680 544 524 731 889 616 858 185 159 767 825 321 903 342 433 950 131 379 375 270 226 437 513 865 338 304 933 772 400 114 292 974 822 162 308 260 279 101 499 567 915 929 41 669 697 176 967 632 242 348 369 418 730 37 726 358 564 218 880 522 774 863 340 990 830 58 112 233 557 208 100 581 677 247 790 597 313 31 56 415 589 688 302 219 896 819 676 872 109 55 614 75 702 555 430 879 445 842 867 734 521 648 738 179 792 942 452 322 155 105 243 922 598 760 458 683 487 256 712 585 128 427 426 881 708 893 793 283 120 151 87 868 231 871 275 27 960 89 462 709 686 119 570 103 263 66 682 996 609 607 172 381 126 939 157 187 834 149 882 7 467 548 76 19 660 412 901 604 514 84 612 717 13 399 419 956 80 906 95 907 664 62 309 339 68 25 14 512 635 735 971 223 853 789 653 110 411 230 197 675 613 390 280 269 658 972 414 382 987 599 666 765 646 775 611 704 724 464 297 482 878 65 998 469 826 628 761 764 703 634 690 511 107 590 295 554 455 900 474 124 715 556 931 539 642 713 762 265 402 743 21 324 227 408 869 461 9 824 502 534 370 948 456 740 274 911 255 319 148 177 457 506 887 943 34 420 895 312 154 17 459 202 920 435 805 568 997 70 164 989 443 327 928 662 28 132 797 919 383 665 463 584 839 718 343 687 801 465 659 875 877 799 186 852 191 504 935 57 722 728 438 142 509 923 716 647 45 988 986 993 494 380 727 886 626 79 178 22 23 855 701 982 480 403 962 10 980 15 562 600 2 964 473 949 475 422 843 749 449 96 293 525 341 754 645 484 40 496 551 812 623 337 756 795 366 285 241 523 118 651 577 992 656 386 451 355 914 995 739 261 527 560 692 251 42 287 145 763 711 253 108 472 963 331 941 387 636 69 371 490 16 46 545 209 535 134 559 924 86 77 215 937 917 362 815 771 925 536 413 732 431 1000 288 595 784 610 72 170 303 904 714 787 999 228 909 698 583 673 955 138 759 47 780 954 60 259 83 249 840 503 486 757 29 59 552 446 976 213 441 978 250 979 363 888 335 195 836 543 681 284 267 393 392 246 278 592 679 349 346 866 846 637 876 890 359 549 639 196 788 141 519 271 460 736 814 360 454 329 44 211 345 515 394 305 809 619 510 450 51 99 237 257 691 71 873 323 67 248 641 317 699 166 572 575 36 747 644 593 603 158 984 416 350 672 315 831 591 778 618 102 85 182 741 439 547 90"
# Min dist: 183086.7365476046
z = list(map(int, x.split()))

print(ILS("datasets/mona_1000.txt").calculate_total_distance(z))
