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

def day_six():
    with open("AoC_day_six.txt") as fd:
        input = fd.read()

    seen = deque(input[:14])
    for i in range(14, len(input)):
        if len(set(seen)) == 14:
            print(i)
            return
        seen.popleft()
        seen.append(input[i])
        
def day_seven():
    class Node:
        def __init__(self, name, size=0, parent=None, is_dir=False):
            self.name = name
            self.size = size
            self.parent = parent
            self.children = dict()
            self.is_dir = is_dir

    def build_tree():
        head = Node("/")
        current_node = head
        for line in input.split("\n"):
            if line == "$ ls":
                pass
            elif line == "$ cd /":
                current_node = head
            elif line == "$ cd ..":
                current_node = current_node.parent
            elif line[:5] == "$ cd ":
                current_node = current_node.children[line[5:]]
            elif line[:4] == "dir ":
                if line[4:] not in current_node.children:
                    current_node.children[line[4:]] = Node(line[4:], parent=current_node, is_dir=True)
            else:
                size, name = line.split(" ")
                if name not in current_node.children:
                    current_node.children[name] = Node(name, int(size), current_node)
                    temp = current_node
                    while temp is not None:
                        temp.size += int(size)
                        temp = temp.parent
        return head
    
    def find_directories_part_a(node):
        res = 0
        for child in node.children.values():
            if child.is_dir:
                if child.size <= 100000:
                    res += child.size
                res += find_directories_part_a(child)
        return res

    def find_directory_part_b(node, target):
        res = float("inf")
        for child in node.children.values():
            if child.is_dir and child.size >= target:
                if child.size < res:
                    res = child.size
                temp = find_directory_part_b(child, target)
                if temp < res:
                    res = temp
        return res
                

    with open("AoC_day_seven.txt") as fd:
        input = fd.read()
    head = build_tree()
    print(find_directories_part_a(head))

    current_unused = 70000000 - head.size
    target = 30000000 - current_unused
    print(find_directory_part_b(head, target))

def day_eight():
    with open("AoC_day_eight.txt") as fd:
        input = fd.read()

    lines = input.split("\n")
    res = set()

    max_left = [0 for _ in range(len(lines))]
    max_top = [0 for _ in range(len(lines[0]))]
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            visible = False
            if i == 0 or j == 0:
                visible = True
            if int(line[j]) > max_left[i]:
                visible = True
                max_left[i] = int(line[j])
            if int(line[j]) > max_top[j]:
                visible = True
                max_top[j] = int(line[j])
            if visible:
                res.add((i, j))
    max_right = [0 for _ in range(len(lines))]
    max_bottom = [0 for _ in range(len(lines[0]))]
    for i in range(len(lines)):
        line = lines[-i-1]
        for j in range(len(line)):
            visible = False
            if i == 0 or j == 0:
                visible = True
            if int(line[-j-1]) > max_right[-i-1]:
                visible = True
                max_right[-i-1] = int(line[-j-1])
            if int(line[-j-1]) > max_bottom[-j-1]:
                visible = True
                max_bottom[-j-1] = int(line[-j-1])
            if visible:
                res.add((len(lines)-i-1, len(line)-j-1))
                
    print(len(res))

def day_eight_part_b():
    with open("AoC_day_eight.txt") as fd:
        input = fd.read()
    lines = input.split("\n")
    
    def get_scenic_score(i, j):
        height = int(lines[i][j])

        k_i = i - 1
        ans_left = 1 if i > 0 else 0
        while k_i > 0 and int(lines[k_i][j]) < height:
            ans_left += 1
            k_i -= 1
        k_i = i + 1
        ans_right = 1 if i < len(lines) - 1 else 0
        while k_i < len(lines) - 1 and int(lines[k_i][j]) < height:
            ans_right += 1
            k_i += 1
        
        k_j = j - 1
        ans_top = 1 if j > 0 else 0
        while k_j > 0 and int(lines[i][k_j]) < height:
            ans_top += 1
            k_j -= 1
        k_j = j + 1
        ans_bottom = 1 if j < len(lines[0]) - 1 else 0
        while k_j < len(lines[0]) - 1 and int(lines[i][k_j]) < height:
            ans_bottom += 1
            k_j += 1
        
        return ans_top * ans_bottom * ans_right * ans_left
    
    res = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            temp = get_scenic_score(i, j)
            if temp > res:
                res = temp

    print(res)
    

    
day_eight_part_b()
