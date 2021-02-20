#!/usr/bin/env python3

import collections
import sys

with open(sys.argv[1]) as f:
    m, t2, t3, t4 = [int(x) for x in f.readline().split()]

    pizzas = []
    for i in range(m):
        pizzas.append((i, frozenset(f.readline().split()[1:])))

open_orders = collections.deque()
completed_orders = []
order_sizes = [(4, t4), (3, t3), (2, t2)]

# create deque of (order size, [pizza IDs], {toppings}) (in descending order size)
for team_size, num_orders in order_sizes:
    for o in range(num_orders):
        open_orders.append((team_size, [], set()))

for pizza_id, toppings in pizzas:
    best_order = None
    best_new_toppings = -1
    for order in open_orders:
        order_size, ids, existing_toppings = order
        num_new_toppings = len(existing_toppings - toppings)

        if num_new_toppings > best_new_toppings:
            best_new_toppings = num_new_toppings
            best_order = order
            # print(f'new {best_order=} from {order=}')

        if num_new_toppings == len(toppings):
            # not going to find anywhere better than here
            break

    # print(f'{best_order=}')
    best_order[1].append(pizza_id)
    if len(best_order[1]) == best_order[0]:
        completed_orders.append([best_order[0]] + best_order[1])
        open_orders.remove(best_order)
    else:
        best_order[2].update(toppings)

# Finally, compress partially-completed orders

# First, delete trailing completely empty orders
while True:
    if not open_orders:
        break

    empty_order = open_orders.pop()
    if empty_order[1]:
        # not actually empty. Put it back, and end loop
        open_orders.append(empty_order)
        break

# Now fill leading orders with trailing orders
giver = None
while True:
    if len(open_orders) < 2:
        break

    taker = open_orders.popleft()

    while True:
        if not giver:
            giver = open_orders.pop()
        taker[1].append(giver[1].pop())
        if not giver[1]:
            # Have emptied this order
            giver = None
        if taker[1] == taker[0]:
            # Have completed this order
            break

print(len(completed_orders))
[print(' '.join([str(o) for o in order])) for order in completed_orders]
