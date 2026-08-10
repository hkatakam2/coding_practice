'''
making change:
write a function that, given:
1. an amount of money
2. a list of coin denominations
computes the number of ways to 
make the amount of money with coins of the available denominations

breakdown:
break this problem into sub problems

example:
amount=4, coins=[1,2,3]

Level 1: Using 1¢ coin (can use 0,1,2,3,4 times)
  └── Using 0 ones: 4¢ remaining, try [2,3]
      ├── Using 0 twos: 4¢ remaining, try [3]
      │   └── Using 1 three: 1¢ remaining → 0 ways
      └── Using 2 twos: 0¢ remaining → 1 way
  └── Using 1 one: 3¢ remaining, try [2,3]
      ├── Using 0 twos: 3¢ remaining, try [3]
      │   └── Using 1 three: 0¢ remaining → 1 way
      └── Using 1 two: 1¢ remaining, try [3] → 0 ways
  ...and so on          
'''
# as a recursive function
def change_possibilities_top_down(amount_left, denominations, current_index=0):
    if amount_left == 0: return 1      # Found a valid combination
    if amount_left < 0: return 0       # Invalid combination
    if current_index >= len(denominations): return 0  # No more coins to try

    current_coin = denominations[current_index]
    num_possibilities = 0

    # Try using current coin multiple times
    while amount_left >= 0:
        num_possibilities += change_possibilities_top_down(
            amount_left, denominations, current_index + 1
        )
        amount_left -= current_coin

    return num_possibilities
'''
there are some duplications;

we can memoize
'''
class Change(object):
    def __init__(self):
        self.memo = {}
    def change_possibilities_top_down(self, amount_left, denominations, current_index=0):
        # Check our memo and short-circuit if we've already solved this one
        memo_key = str((amount_left, current_index))
        if memo_key in self. memo:
            print("grabbing memo[%s]" % memo_key)
            return self.memo[memo_key]
        
        # Base cases:
        # We hit the amount spot on. yes!
        if amount_left == 0:
            return 1
        
        # We overshot the amount left (used too many coins)
        if amount_left < 0:
            return 0
        
        # We're out of denominations
        if current_index == len(denominations):
            return 0
            print("checking ways to make %i with %s" % (
            amount_left, denominations[current_index:],
            ))
        
        # Choose a current coin
        current_coin = denominations[current_index]
        
        # See how many possibilities we can get
        # for each number of times to use current_coin
        num_possibilities = 0
        while amount_left >= 0:
            num_possibilities += self.change_possibilities_top_down(
            amount_left, denominations,
            current_index + 1,
            )
            amount_left -= current_coin
        
        # Save the answer in our memo so we don't compute it again
        self.memo[memo_key] = num_possibilities
        return num_possibilities
'''
O(n*m) time
O(n*m) space

our method is recursive, so we are building up a large call stack O(m) size
how can we get O(n) additional space?

bottom up method

We can start by making a list ways_of_doing_n_cents, where 
the index is the amount and the value at each index is the number of 
ways of getting that amount.
This list will take O(n) space, where n is the size of amount.

ways_of_doing_n_cents_1_2[5] = ways_of_doing_n_cents_1[5] + ways_of_doing_n_cents_1_2[5-2]

Example:
Initial: ways = [1,0,0,0,0]  # ways[0] = 1

Using 1¢:
ways = [1,1,1,1,1]  # Can make any amount with 1¢

Using 2¢:
ways[2] += ways[0] → [1,1,2,1,1]
ways[3] += ways[1] → [1,1,2,2,1]
ways[4] += ways[2] → [1,1,2,2,3]

Using 3¢:
ways[3] += ways[0] → [1,1,2,3,3]
ways[4] += ways[1] → [1,1,2,3,4]

Final answer: 4 ways
1. 1¢ + 1¢ + 1¢ + 1¢
2. 1¢ + 1¢ + 2¢
3. 2¢ + 2¢
4. 1¢ + 3¢

'''
def change_possibilities_bottom_up(amount, denominations):
    ways = [0] * (amount + 1)  # Index represents amount
    ways[0] = 1  # Base case: one way to make zero

    for coin in denominations:
        for current_amount in range(coin, amount + 1):
            remainder = current_amount - coin
            ways[current_amount] += ways[remainder]
    
    return ways[amount]
'''
O(n*m) time
O(n) additional space

replaced code:
def change_possibilities_bottom_up(amount, denominations):
    ways_of_doing_n_cents = [0] * (amount + 1)
    ways_of_doing_n_cents[0] = 1

    for coin in denominations:
        for higher_amount in range(coin, amount + 1):
            higher_amount_remainder = higher_amount - coin
            ways_of_doing_n_cents[higher_amount] += (ways_of_doing_n_cents[higher_amount_remainder])
        
    return ways_of_doing_n_cents[amount]


learning:
this is the dynamic programming approach.

'''