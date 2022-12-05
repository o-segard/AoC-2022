from heapq import heapify, heappop

def day_one():
    with open("AoC_input.txt") as fd:
        input = fd.read()
    elf_calories = [
        sum([-int(cal) for cal in cals.split("\n")]) 
        for cals in input.split("\n\n")
    ] # negative sum of the calories per elf 

    heapify(elf_calories) # transform in a min-heap
    res = 0
    for _ in range(3):
        res += -heappop(elf_calories)
    print(res)

def day_two():
    with open("AoC_day_two.txt") as fd:
        input = fd.read()
    strategy = [
        (ord(round.split(" ")[0])-64, round.split(" ")[1]) for round in input.split("\n")
    ] # transform in numbers: A->1, B->2, C->3

    res = 0
    for opp, strat in strategy:
        if strat == "X": # lose
            res += (opp + 1) % 3 + 1
        elif strat == "Y": # draw
            res += 3
            res += opp
        else: # win
            res += 6
            res += opp % 3 + 1
    print(res)

def day_three():
    with open("AoC_day_three.txt") as fd:
        input = fd.read()
    compartments = [
        (set(rucksack[:len(rucksack)//2]), set(rucksack[len(rucksack)//2:]))
        for rucksack in input.split("\n")
    ] # list of the rucksacks, each split in two compartments
    
    res = 0
    for (left, right) in compartments:
        item = (left & right).pop()
        if ord(item) > 90:
            res += ord(item)-96
        else:
            res += ord(item)-38
    print(res)

def day_three_b():
    with open("AoC_day_three.txt") as fd:
        input = fd.read()
    rucksacks = [
        set(rucksack) for rucksack in input.split("\n")
    ] # list of the rucksacks items, as hash tables

    res = 0
    for i in range(0, len(rucksacks), 3):
        item = (rucksacks[i] & rucksacks[i+1] & rucksacks[i+2]).pop()
        if ord(item) > 90:
            res += ord(item)-96
        else:
            res += ord(item)-38
    print(res)

def day_four():
    with open("AoC_day_four.txt") as fd:
        input = fd.read()
    pairs = [
        [
            (int(inter.split("-")[0]), int(inter.split("-")[1]))for inter in pair.split(",")
        ]
        for pair in input.split("\n")
    ] # pairs of intervals
    
    res = 0
    for [left, right] in pairs:
        # total overlap
        if left[0] >= right[0] and left[1] <= right[1]:
            res += 1
        elif right[0] >= left[0] and right[1] <= left[1]:
            res += 1
        # partial overlap
        elif left[0] <= right[0] and left[1] >= right[0]:
            res += 1
        elif left[0] <= right[1] and left[1] >= right[1]:
            res += 1
    print(res)

from collections import deque

def day_five():
    with open("AoC_day_five_columns.txt") as fd:
        columns = fd.read()
    with open("AoC_day_five_moves.txt") as fd:
        moves = fd.read()

    columns_data = [deque() for _ in range(len(columns.split("\n")[0])//4 + 1)]
    for row in columns.split("\n"):
        for i in range(0, len(row), 4):
            if row[i + 1] != " ":
                columns_data[i//4].append(row[i + 1])
    moves_data = [
        (int(move.split(" ")[1]), int(move.split(" ")[3]), int(move.split(" ")[-1]))
        for move in moves.split("\n")
    ]
    
    for (num, dep, arr) in moves_data:
        for _ in range(num):
            columns_data[arr-1].appendleft(columns_data[dep-1].popleft())

    res = ""
    for column in columns_data:
        res += column.popleft()
    print(res)

def day_five_b():
    with open("AoC_day_five_columns.txt") as fd:
        columns = fd.read()
    with open("AoC_day_five_moves.txt") as fd:
        moves = fd.read()

    columns_data = [deque() for _ in range(len(columns.split("\n")[0])//4 + 1)]
    for row in columns.split("\n"):
        for i in range(0, len(row), 4):
            if row[i + 1] != " ":
                columns_data[i//4].append(row[i + 1])
    moves_data = [
        (int(move.split(" ")[1]), int(move.split(" ")[3]), int(move.split(" ")[-1]))
        for move in moves.split("\n")
    ]
    
    for (num, dep, arr) in moves_data:
        moved = [columns_data[dep-1].popleft() for _ in range(num)]
        columns_data[arr-1].extendleft(reversed(moved))

    res = ""
    for column in columns_data:
        res += column.popleft()
    print(res)
