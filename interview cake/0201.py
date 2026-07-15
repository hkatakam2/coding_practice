'''
given stock_prices find the max profit

stock_prices = [10,7,5,8,11,9]
get_max_profit(stock_prices) -> 6
buying for $5 and selling for $11

1. you can not sell before you buy
2. you can not buy and sell in the same time, at least 1 minute must pass
'''

"""
brute force: for each price, compare with all other prices
O(n^2) time and O(1) space

better: keep track of the min_price and max_profit
O(n) time and O(1) space
"""
# brute force O(n^2); this is wrong
def get_max_profit(stock_prices):
    max_profit = 0

    # go through every time
    for outer_time in range(len(stock_prices)):

        # for every time, go throguth every other time
        for inner_time in range(len(stock_prices)):
            # for each pair, find the earlier and later times
            earlier_time = min(outer_time, inner_time)
            later_time = max(outer_time, inner_time)

            # and use those to find the earlier and later prices
            earlier_price = stock_prices[earlier_time]
            later_price = stock_prices[later_time]

            # see what our profit would be if we bought at the 
            # earlier price and sold at the later price
            potential_profit = later_price - earlier_price

            # update max_profit if we can do better
            max_profit = max(max_profit, potential_profit)
    return max_profit

# in our inner loop we could just look at every price after the price in our outer loop
def get_max_profit(stock_prices):
    max_profit = 0

    # go through every price( with its index as the time)
    for earlier_time, earlier_price in enumerate(stock_prices):

        # and go through all the later prices
        for later_time in range(earlier_time+1, len(stock_prices)):
            later_price = stock_prices[later_time]

            # see what our profit would be if we bought at the 
            # earlier price and sold at the later price
            potential_profit = later_price - earlier_price

            # update max_profit if we do better
            max_profit = max(max_profit, potential_profit)
    return max_profit
# still O(n^2), can we do better?

"""
we need to loop through it only once; let's use a greedy approach

how do we know we've found a new max_profit?
at each iteration, our max_profit is either:
1. the same as the max_profit at the last step, or
2. the max profit we can get by selling at the current_price

how do we know we have a case 2?
the max profit we can get by selling at the current_price is simply
the difference between the current_price and the min_price from earlier in the day.

for every price, we'll need to:
1. keep track of the lowest price we've seen so far
2. see if we get a better profit
"""
def get_max_profit(stock_prices):
    min_price = stock_prices[0]
    max_profit = 0

    for current_price in stock_prices:
        # ensure min_price is the lowest price we've seen so far
        min_price = min(min_price, current_price)

        # see what our profit would be if we bought at the 
        # min price and sold at the current price
        potential_profit = current_price - min_price

        # update the max_profit if we can do better
        max_profit = max(max_profit, potential_profit)
    
    return max_profit
"""
are there any edge cases?
what if the price stays the same? -- our function works
what if the price goes down all day? -- our functions gives wrong answer?
it has two issues:
1. It allows buying and selling at the same time (index)
2. It returns 0 for declining prices when we should return the smallest loss

we can initialize max_profit = -stock_price[0]
but this creates a problem of buying and selling at the same time
change the order of calculation of min_price, max_profit
"""
def get_max_profit(stock_prices):
    if len(stock_prices) < 2:
        raise ValueError('Getting a profit requires at least 2 prices')
    
    # we'll greedily update min_price and max_profit, so we initialize
    # them to the first price and the first possible profit
    min_price = stock_prices[0]
    max_profit = stock_prices[1] - stock_prices[0]

    # start at the second index time
    # we ca't sell at the same time, we must buy first,
    for current_time in range(1, len(stock_prices)):
        current_price = stock_prices[current_time]

        # see what our profit would be if we bought at the min price and sold at the current price
        potential_profit = current_price- min_price

        # udpate max_profit if we can do better
        max_profit = max(max_profit, potential_profit)

        # update min_price so it's always the lowest price 
        # we've seen so far
        min_price = min(min_price, current_price)

    return max_profit
"""
what we learned?
how do we know if greedy works? try it out and see

ask yourself:
suppose we could come up with the answer in one pass through the input,
by simply updating the 'best answer so far' as we went. what additional
values would we need to keep updated as we looked at each item in our
input, in order to be able to update the best answer so far in const time?

"""



