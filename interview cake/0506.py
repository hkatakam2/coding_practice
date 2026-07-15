'''
cake thief

there are unlimited number of cakes

Each type of cake has a weight and a value, stored in a tuple with two indices:
0. An integer representing the weight of the cake in kilograms
1. An integer representing the monetary value of the cake in British shillings

for example:
# Weighs 7 kilograms and has a value of 160 shillings
(7, 160)

write a function max_duffel_bag_value() 
for example:
cake_tuples = [(7, 160), (3, 90), (2, 15)]
capacity= 20
# Returns 555 (6 of the middle type of cake and 1 of the last type of cake)
max_duffel_bag_value(cake_tuples, capacity)

weights and values may be any non-negative integer. could be zero
'''

'''
Breakdown:
bruteforce: try every combinatin of cakes; it will be very inefficient

what if we just look at the highest value cakes? (greedy approach)
it will give wrong answer sometimes, why is it giving wrong answer?
because we did not think about weight of the cake.

what if we look at value/weight ratio? (this is also greedy approach)
even this could give wrong answer when the highest value/weight ratio
does not fit properly in the bag.

how can we ensure we get the optimal value we can carry?
try thinking small; what if the capacity is 1kg
what if the capacity is 2kg?

can we use the the answer at capcities 1kg and 2kg to calculate at 3kg?
"overlapping problems"
'''
def max_duffel_bag_value(cake_tuples, weight_capacity):
    # We make a list to hold the maximum possible value at every
    # duffel bag weight capacity from 0 to weight_capacity
    # starting each index with value 0
    max_values_at_capacities = [0] * (weight_capacity + 1)
    for current_capacity in range(weight_capacity + 1):
        # Set a variable to hold the max monetary value so far
        # for current_capacity
        current_max_value = 0
        for cake_weight, cake_value in cake_tuples:
            # If a cake weighs 0 and has a positive value the value of
            # our duffel bag is infinite!
            if cake_weight == 0 and cake_value != 0:
                return float('inf')
            # If the current cake weighs as much or less than the
            # current weight capacity it's possible taking the cake
            # would get a better value
            if cake_weight <= current_capacity:
                # So we check: should we use the cake or not?
                # If we use the cake, the most kilograms we can include in
                # addition to the cake we're adding is the current capacity
                # minus the cake's weight. We find the max value at that 
                # integer capacity in our list max_values_at_capacities
                max_value_using_cake = (
                            cake_value
                            + max_values_at_capacities[current_capacity - cake_weight]
                )
                # Now we see if it's worth taking the cake. how does the
                # value with the cake compare to the current_max_value?
                current_max_value = max(max_value_using_cake,
                                        current_max_value)
        # Add each capacity's max value to our list so we can use them
        # when calculating all the remaining capacities
        max_values_at_capacities[current_capacity] = current_max_value
    return max_values_at_capacities[weight_capacity]
'''
O(n*k) time and O(k) space

if there is an alarm in the vault and we need to move quickly then
greedy algorithms are better

it is not always better to be optimal. 

Bonus:
which cakes should we take, and how many?
'''
def max_duffel_bag_value_with_selection(cake_tuples, weight_capacity):
    max_values_at_capacities = [0] * (weight_capacity + 1)
    selected_cakes = [None] * (weight_capacity + 1)  # To track the cakes used

    for current_capacity in range(weight_capacity + 1):
        current_max_value = 0
        best_cake = None

        for cake_weight, cake_value in cake_tuples:
            if cake_weight == 0 and cake_value != 0:
                return float('inf'), None

            if cake_weight <= current_capacity:
                max_value_using_cake = (
                    cake_value
                    + max_values_at_capacities[current_capacity - cake_weight]
                )

                if max_value_using_cake > current_max_value:
                    current_max_value = max_value_using_cake
                    best_cake = (cake_weight, cake_value)

        max_values_at_capacities[current_capacity] = current_max_value
        selected_cakes[current_capacity] = best_cake

    # Reconstruct which cakes were used
    capacity = weight_capacity
    used_cakes = []
    while capacity > 0 and selected_cakes[capacity] is not None:
        cake = selected_cakes[capacity]
        used_cakes.append(cake)
        capacity -= cake[0]

    return max_values_at_capacities[weight_capacity], used_cakes

'''
Bonus: Common Denominator Optimization
If all the cake weights have a greatest common divisor (GCD) 
greater than 1, we can reduce the problem size by dividing 
all weights by their GCD. This reduces the number of iterations 
while preserving the relative capacities.
'''
from math import gcd
from functools import reduce

def find_gcd_of_weights(cake_tuples):
    weights = [cake[0] for cake in cake_tuples if cake[0] > 0]
    return reduce(gcd, weights)

# Before solving the problem, scale weights by their GCD
cake_tuples = [(w // gcd, v) for w, v in cake_tuples]
weight_capacity //= gcd

'''
Bonus: Dominance relation
We can filter out cakes that are dominated by others (i.e., heavier and less valuable). For this:
	1.	Sort cakes by  value / weight  in descending order.
	2.	Remove cakes that are dominated by another cake.
'''
def filter_dominated_cakes(cake_tuples):
    sorted_cakes = sorted(cake_tuples, key=lambda cake: cake[1] / cake[0], reverse=True)
    filtered_cakes = []
    max_value = 0

    for cake in sorted_cakes:
        if cake[1] > max_value:
            filtered_cakes.append(cake)
            max_value = cake[1]

    return filtered_cakes
'''
Bonus: 0/1 knapsack
If there is only one of each type of cake.
'''
def knapsack(cake_tuples, weight_capacity):
    dp = [0] * (weight_capacity + 1)

    for cake_weight, cake_value in cake_tuples:
        for capacity in range(weight_capacity, cake_weight - 1, -1):
            dp[capacity] = max(dp[capacity], dp[capacity - cake_weight] + cake_value)

    return dp[weight_capacity]