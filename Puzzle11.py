# %%
from typing import List, Dict 

class Monkey:
    def __init__(self, _6_lines : List[str], part_A):
        self.number = int
        self.items = []
        self.activity = 0
        self.common_divisor = 0
        self.part_A = part_A

        self.test_results = {}
        for x in _6_lines:
            x = x.strip('\r\n')
            if x.startswith("Monkey"):
                self.number = x.split(' ')[1].strip(':')
            if x.startswith('  Starting items:'):
                self.items = eval("[" + x.split(':')[1].strip(' ') + "]")
            if x.startswith('  Operation:'):
                self.operation = x.split(':')[1].strip(' ')
                self.operation_func = self.operation.split(' = ')[1].strip()
            if x.startswith('  Test:'):
                self.test = x.split(':')[1].strip(' ')
                self.divisor = int(self.test.split(' ')[-1])
                self.test_func = lambda x: x % self.divisor
            if x.startswith('    If true'):
                self.test_results[True] = x.split(':')[1].strip(' ').split(' ')[-1]
            if x.startswith('    If false'):
                self.test_results[False] = x.split(':')[1].strip(' ').split(' ')[-1]

    def recieve_item(self, item):
        self.items.append(item)

    def do_turn(self, monkeys: Dict[str, "Monkey"]):
        new = 0
        for old in self.items:
            self.activity += 1
            #- print(f"Worry level: {old}")
            #- print(f"Worry level operation: {self.operation}")
            # exec(self.operation, {}, {"old": old, "new": new})
            new = eval(self.operation_func.replace('old', str(old)))
            #- print(f'Worry level is now: {new}')
            
            # Part A .. Part B doesn't divide by 3
            if self.part_A:
                new = new // 3
            #- print(f'Worry has calmed down to: {new}')
            # pass_to = self.test_results[self.test_func(new)]
            pass_to = self.test_results[new % self.divisor == 0]

            new = new % self.common_divisor
            monkeys[pass_to].recieve_item(new)
        self.items = []

# %%
def load_data(part_A):
    data = [x.strip('\n') for x in open('Puzzle11_input.txt', 'r').readlines()]

    monkeys = {}
    start = 0
    while True:
        monkey = Monkey(data[start:start + 6], part_A)
        monkeys[monkey.number] = monkey
        del monkey
        start += 7
        if start >= len(data):
            break

    common_divisor = 1
    for x in monkeys:
        common_divisor *= monkeys[x].divisor

    for x in monkeys:
        monkeys[x].common_divisor = common_divisor

    def do_output(monkeys, answer):
        top_monkeys = sorted([monkeys[x].activity for x in monkeys], reverse=True)
        shenanigans = top_monkeys[0] * top_monkeys[1]
        print(f"Monkey Buisness: {shenanigans} - ({answer})")

    rounds = 10000
    if part_A:
        rounds = 20
    # Part A - 20, Part B - 10000
    # for round in range(20):
    for round in range(rounds):
        # print(f"Round {round}")
        for n in monkeys:
            x = monkeys[n]
            # print(f"    -- Monkey {x.number} -- Items: {x.items} -- Item: {len(x.items)}")
            x.do_turn(monkeys)
            # print(f"                -- Items: {x.items} -- Item: {len(x.items)}")

    if part_A:
        do_output(monkeys, 182293)
    else:
        do_output(monkeys, 54832778815)
# %%

load_data(True)
load_data(False)
