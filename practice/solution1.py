#!/usr/bin/env python3

import sys

def takepizza(pizzas, key):
    ids = pizzas[key]
    ret = ids.pop()
    if not ids:
        # print('    took last {} pizza {} — deleting'.format(key, ret))
        del pizzas[key]
    return ret

with open(sys.argv[1]) as f:
    line1 = f.readline()
    m, t2, t3, t4 = [int(x) for x in line1.split()]

    pizzas = {} # dict of {ingredients}: [pizza IDs]

    for i in range(m):
        line = f.readline()

        pizza = frozenset(sorted(line.split()[1:]))
        pizzas.setdefault(pizza, []).append(i)

# TODO sort pizzas by descending number of toppings

orders = []
order_sizes = [(4, t4), (3, t3), (2, t2)]

for team_size, num_orders in order_sizes:
    # print('Filling {} orders for teams of {} from inventory {}'.format(num_orders, team_size, pizzas))
    for team in range(num_orders):
        if not pizzas:
            # print('No more pizzas :(')
            break

        pizza_keys = []
        all_toppings = set()
        last_toppings = set()
        for toppings in pizzas:

            # TODO decide stop or continue
            # num_new_toppings = len(toppings - all_toppings)
            if toppings != last_toppings:
                pizza_keys.append(toppings)
                all_toppings.update(toppings)
            last_toppings = toppings

            if len(pizza_keys) >= team_size:
                # print('  completed order: {}'.format(pizza_keys))
                break

        if len(pizza_keys) == team_size:
            pizza_ids = [takepizza(pizzas, k) for k in pizza_keys]
            orders.append(' '.join([str(i) for i in [team_size] + pizza_ids]))

    # TODO use up any remaining pizzas

print(len(orders))
[print(order) for order in orders]
