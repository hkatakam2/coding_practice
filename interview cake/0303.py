'''
write a function that takes
1. a list of unsorted_scores
2. the highest_possible_score in the game

return a sorted list of scores in less than O(n lg n) time.

breakdown:
what are some common ways to get O(n) time?
greedy: but we're not looking to grab a specific value from the input list
(e.g. the 'largest' or the 'greatest difference') 

counting: we can build a list score_counts where the indices represent scores 
and the values represent how many times the score appears. 
Once we have that, we can generate a sorted list of scores?

'''
# counting sort
def sort_scores(unsorted_scores, highest_possible_score):
    # list of 0s at indices 0..highest_possible_score
    score_counts = [0] * (highest_possible_score)

    # populate score counts
    for score in unsorted_scores:
        score_counts[score] += 1

    # populate the final sorted list
    sorted_scores = []

    # for each item in score_counts
    for score in range(len(score_counts)-1, -1, -1):
        count = score_counts[score]

        # for the number of times the item occurs
        for time in range(count):
            sorted_scores.append(score)
    
    return sorted_scores
'''
O(n) time and O(n) space
by optimzing for time, we ended up incurring some space cost.

Bonus: can we optimize space by using inplace 
'''
def sort_scores_in_place(unsorted_scores, highest_possible_score):
    # List of 0s at indices 0..highest_possible_score
    score_counts = [0] * (highest_possible_score + 1)

    # Populate score_counts
    for score in unsorted_scores:
        score_counts[score] += 1

    # Repopulate unsorted_scores in place
    index = 0
    for score in range(len(score_counts) - 1, -1, -1):
        count = score_counts[score]
        for _ in range(count):
            unsorted_scores[index] = score
            index += 1
'''
Bucket sort:
Uses buckets that store actual scores instead of just counts
Uses extend() instead of multiple append() operations
More intuitive but uses more space

'''
def sort_scores_bucket(unsorted_scores, highest_possible_score):
    # Create buckets (0 to highest_possible_score)
    buckets = [[] for _ in range(highest_possible_score + 1)]
    
    # Put scores into buckets
    for score in unsorted_scores:
        buckets[score].append(score)
    
    # Collect scores from buckets in descending order
    sorted_scores = []
    for i in range(highest_possible_score, -1, -1):
        sorted_scores.extend(buckets[i])
        
    return sorted_scores
'''
Time complexity: O(n)
Space complexity: O(n)

However:

Counting sort is more space-efficient as it only stores counts
Bucket sort might be more intuitive and easier to modify if you need to store additional information with each score
Bucket sort would be more appropriate if scores had associated data (like player names)
'''
