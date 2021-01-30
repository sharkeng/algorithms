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


# x, min_dist = ILS("datasets/mona_1000.txt").integrated_local_search(1, 100)
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

x = "70 473 369 8 508 143 88 511 386 502 554 66 161 469 362 520 122 127 137 566 75 356 200 347 578 368 639 331 238 76 93 22 113 132 452 428 298 451 565 675 89 460 123 492 607 654 343 447 42 320 627 432 697 421 124 358 370 498 64 269 308 212 497 582 30 67 595 302 531 217 645 318 587 571 181 177 219 588 319 504 478 357 140 36 198 134 59 430 466 138 43 55 655 224 698 215 634 573 484 155 671 427 275 39 613 240 326 241 101 27 518 632 249 365 142 353 438 574 110 149 631 299 144 405 4 413 464 480 203 581 313 236 579 647 608 96 185 172 390 406 309 403 642 636 14 45 382 490 407 218 500 495 408 415 489 158 139 468 324 361 245 259 389 190 461 672 542 9 540 486 288 374 597 184 294 562 81 105 182 100 157 591 691 303 385 364 493 532 474 53 62 232 449 354 153 277 265 78 680 694 396 37 435 40 596 117 118 559 188 133 91 637 312 572 546 220 496 541 61 598 471 285 221 619 450 111 476 130 576 264 663 248 463 549 305 352 179 252 444 296 535 345 19 273 47 332 229 300 337 346 141 301 189 57 503 317 448 168 516 58 491 548 162 112 165 630 499 439 306 693 445 586 510 152 515 561 593 282 665 351 429 79 256 646 77 74 173 395 197 600 231 670 467 202 606 183 208 330 604 304 268 178 359 550 166 590 201 255 622 289 659 283 97 1 291 589 350 454 528 485 192 131 628 679 204 363 207 94 687 651 342 483 119 620 242 65 456 13 310 35 38 649 151 49 279 210 321 322 193 695 479 635 381 146 399 425 125 394 557 552 618 25 126 44 316 436 431 170 378 584 459 167 616 237 115 28 98 414 222 418 18 482 611 292 128 274 333 519 295 446 103 3 314 699 585 328 16 477 641 380 230 524 567 575 629 681 23 107 226 526 392 457 487 52 372 290 530 95 163 244 129 677 108 422 266 84 340 551 12 171 148 696 32 86 6 384 702 211 2 360 455 228 92 325 159 437 673 564 666 555 187 507 688 657 411 106 536 643 29 280 514 391 583 56 462 63 434 661 10 569 481 543 307 254 150 71 104 120 336 262 315 247 54 121 424 614 223 656 668 7 205 534 209 334 594 397 416 638 90 667 272 33 160 80 243 701 506 674 684 580 366 660 577 216 640 339 563 609 371 379 21 398 82 426 488 377 501 533 401 525 233 402 529 263 601 633 344 509 214 73 253 664 41 513 442 31 603 227 703 180 349 338 154 329 440 51 60 373 700 617 102 17 652 164 592 68 246 505 517 186 85 69 621 284 568 50 99 83 682 393 690 602 348 626 20 235 443 72 260 692 538 539 650 441 417 383 199 24 419 375 287 605 11 545 494 523 156 409 293 136 658 648 323 662 367 271 570 623 560 48 327 297 512 433 135 206 412 387 114 335 87 145 311 610 239 341 683 267 522 176 5 423 475 261 213 420 537 258 376 286 194 251 15 355 195 653 400 558 191 644 26 669 234 544 109 196 388 270 281 34 624 689 556 521 225 547 465 553 470 116 472 685 453 174 676 276 250 625 278 410 257 678 527 599 404 686 615 147 175 612 458 169 46"
# Min dist: 183086.7365476046
z = list(map(int, x.split()))

print(ILS("datasets/random_2.txt").calculate_total_distance(z))
