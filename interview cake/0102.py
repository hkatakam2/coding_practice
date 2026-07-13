'''
Write a function that takes an integer flight_length (in minutes) and 
a list of integers movie_lengths (in minutes) and 
returns a boolean indicating whether there are two numbers 
in movie_lengths whose sum equals flight_length.

assumptions:
1. users will watch exactly two movies
2. don't make the users watch the same movie twice
3. optimize for runtime over memory
'''

'''
Breakdown:
how would we solve this by hand?
we might go through movie_lengths from beginning to end, 
treating each item as first_movie_length, and 
for each of those check if there's a second_movie_length equal to 
flight_length - first_movie_length.

how would we implement this in code?
We could nest two loops (the outer choosing first_movie_length, 
the inner choosing second_movie_length). 
That'd give us a runtime of O(n^2).

can we do better?
To bring our runtime down we'll probably need to replace that inner loop 
(the one that looks for a matching second_movie_length) with 
something faster.

Could we check for the existence of our second_movie_length in 
constant time?
What data structure gives us convenient constant-time lookups?

A set!
'''

'''
Solution:
We make one pass through movie_lengths, 
treating each item as the first_movie_length. At each iteration, we:
1. See if there's a matching_ second _movie_length we've seen already 
(stored in our movie_lengths_seen set) that is equal to 
flight_length - first_movie_length. If there is, we short-circuit and return True.
2. Keep our movie_lengths_ seen set up to date by throwing in the 
current first_movie_length.
'''

def can_two_movies_fill_flight(movie_lengths, flight_length):
    # movie lengths we have seen so far
    movie_lengths_seen = set()

    for first_movie_length in movie_lengths:
        matching_second_movie_length = flight_length - first_movie_length

        if matching_second_movie_length in movie_lengths_seen:
            return True
        # else add this first_movie_length to seen list
        movie_lengths_seen.add(first_movie_length)

    # we never found a match, so return false
    return False

'''
O(n) time
O(n) space

Bonus:
1. what if we wanted the movie lengths to sum to something close to 
the flight length (say, within 20 minutes)
2. what if we wanted to fill the flight length as nicely as possible
with any number of movies (not just 2)?
3. what if we knew that move_lengths was sorted? could we save some
space and/or time?

what we learned?
Using hash-based data structures, like dictionaries or sets, is 
so common in coding challenge solutions, it should always be your 
first thought. Always ask yourself, right from the start: 
"Can I save time by using a dictionary?"
'''
# bonus 1
def can_two_movies_fill_close_to_flight(movie_lengths, flight_length, tolerance = 20):
    movie_lengths_seen = set()

    for first_movie_length in movie_lengths:
        for delta in range(-tolerance, tolerance + 1):
            matching_second_movie_length = flight_length - first_movie_length + delta
            if matching_second_movie_length in movie_lengths_seen:
                return True
        movie_lengths_seen.add(first_movie_length)
    
    return False
# bonus 2
# this is a variation of subset sum problem; DP can be used
# this algorithm find the maximum sum of movie lengths that 
# does not exceed the flight length
# it finds the maximum total duration of movies that can fit within the 
# flight time, not necessarily the closest match to the flight duration
def maximum_total_duration_of_movies(movie_lengths, flight_length):
    dp = [0] * (flight_length + 1)

    for length in movie_lengths:
        for time in range(flight_length, length -1, -1):
            dp[time] = max(dp[time], dp[time - length] + length)

    return dp[flight_length]
# bonus 2
def closest_movies_to_flight(movie_lengths, flight_length):
    """
    Find combination of movies that comes closest to the flight length.
    
    Args:
        movie_lengths: List of movie durations
        flight_length: Target duration of the flight
    
    Returns:
        tuple: (best_total_time, difference_from_flight_length)
    """
    # Create DP array where each index represents a possible duration
    dp = [float('-inf')] * (flight_length * 2 + 1)  # Double size to handle sums > flight_length
    dp[0] = 0  # Base case: 0 duration is possible with no movies

    # Build up possible combinations
    for length in movie_lengths:
        for time in range(flight_length * 2, length - 1, -1):
            if dp[time - length] != float('-inf'):
                dp[time] = max(dp[time], dp[time - length] + length)
    
    # Find the duration closest to flight_length
    best_diff = float('inf')
    best_total = 0
    
    for total_time, possible in enumerate(dp):
        if possible != float('-inf'):
            diff = abs(total_time - flight_length)
            if diff < best_diff:
                best_diff = diff
                best_total = total_time

    return best_total, best_diff

# Example usage:
movie_lengths = [30, 45, 60, 75, 90, 120]
flight_length = 200
best_time, difference = closest_movies_to_flight(movie_lengths, flight_length)
print(f"Best total time: {best_time} minutes")
print(f"Difference from flight length: {difference} minutes")


# bonus 3
# If movie_lengths is sorted, we can use the two-pointer technique, 
# which is more efficient in terms of time and space compared to 
# using a set
def can_two_movies_fill_flight_sorted(movie_lengths, flight_length):
    left, right = 0, len(movie_lengths) - 1
    while left < right:
        current_sum = movie_lengths[left] + movie_lengths[right]
        if current_sum == flight_length:
            return True
        elif current_sum < flight_length:
            left += 1
        else:
            right -= 1
    return False
# O(n) time, O(1) space