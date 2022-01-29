import re
import sys


def domino_fits(domino, start):
    (a, b) = domino
    return a == start or b == start


def get_fitting_direction(domino, start):
    (a, b) = domino
    if a == start:
        return (a, b)
    elif b == start:
        return (b, a)
    else:
        raise(Exception(
            "Trying to find direction of unfitting domino: (%d,%d) to %d!" % (a, b, start)))


def solve_rec(dominos, start):
    max_length = 0
    max_train = []
    if start == None:
        fitting_dominos = dominos
    else:
        # Filter for fitting
        fitting_dominos = list(
            filter(lambda d: domino_fits(d, start), dominos))
        # Rotate to fit
        fitting_dominos = list(
            map(lambda d: get_fitting_direction(d, start), fitting_dominos))

    if len(fitting_dominos) == 0:
        return (0, [])
    else:
        for (a, b) in fitting_dominos:
            (length, train) = solve_rec(
                list(filter(lambda d: d != (a, b) and d != (b, a), dominos)), b)
            if length + 1 > max_length:
                max_length = length + 1
                max_train = [(a, b)] + train

        return (max_length, max_train)


def solve(instance, start):
    return solve_rec(instance, start)


def run():
    start = None
    while(True):
        print("Enter starting number, if none press enter")
        start_in = input()
        if re.match(r"[0-9]+", start_in):
            start = int(start_in)
            break
        elif start_in == "":
            break
        else:
            print("Badly formatted! Try again!")

    print("Enter one domino at a time in the format n,m")
    instance = []
    reading = True
    while reading:
        curr_in = input()
        if curr_in == "":
            reading = False
            break
        elif re.match(r'^[0-9]+,[0-9]+$', curr_in):
            [a_str, b_str] = curr_in.split(',')
            a = int(a_str)
            b = int(b_str)
            if (a, b) not in instance and (b, a) not in instance:
                instance.append((a, b))
            else:
                print("Domino is already in set!")
        else:
            print("Badly formatted input! Try again!")

    if len(instance) == 0:
        print("Empty instance! Exiting...")
        sys.exit()

    print("Solving...")
    [length, train] = solve(instance, start)
    print("Solution found!")
    print("Length: %d" % length)
    print("Train: ", end="")
    first = True
    for (a, b) in train:
        if first:
            first = False
        else:
            print(",", end="")
        print("(%d,%d)" % (a, b), end="")

    print()


run()
