# koko eatinting bananas/ minimum processing rate
we have a list of shipment batches, workers can process at K rate, K items/hour. If the batch has fewer than K items, remaining time is wasted. the work has to be finished within H hours. choose a minimum K that satisfies

# restate
batches = [3, 6, 7, 11], deadline = 8, so the answer is 4

# clarify

# ideas
1. brute force: we can try 1, 2, 3 .. and return the first rate that finishes before deadline. each check cost O(n), and the number of rates tried could be as large as the biggest batch, so this is O(n · max_batch). Too slow if batches are huge
2. binary search: lowest rate 1, highest rate = largest batch size 
   1. binary search over rates, with a helper that checks whether a candidate rate meets the deadline. Complexity is O(n · log(max_batch)).
# outline
min_rate_to_finish(batches, deadline):
    lowest_rate = 1
    highest_rate = max(batches)

    while lowest_rate < highest_rate:
        candidate_rate = middle of lowest and highest
        if can_finish(batches, candidate_rate, deadline):
            highest_rate = candidate_rate  #works, so try slower
        else:
            lowest_rate = candidate_rate + 1 # too slow, go faster
    return lowest_rate

can_finish(batches, rate, deadline):
    return hours_needed(batches, rate) <= deadline

hours_needed(batches, rate):
    return sum of hours_for(batch, rate) over every batch

hours_for(batch, rate):
    return batch divided by rate, rounded up

```python
def min_rate_to_finish(batches, deadline):
    # lowest_rate  = 1
    lowest_rate = 1
    # highest_rate = largest batch
    highest_rate = max(batches)

    # while lowest_rate < highest_rate:
    while lowest_rate < highest_rate:
        # candidate_rate = middle of lowest_rate and highest_rate
        candidate_rate = (lowest_rate + highest_rate) // 2

        # if can_finish(batches, candidate_rate, deadline):
        if can_finish(batches, candidate_rate, deadline):
            # highest_rate = candidate_rate   (works, so try slower)
            highest_rate = candidate_rate
        else:
            # lowest_rate = candidate_rate + 1   (too slow, so go faster)
            lowest_rate = candidate_rate + 1

    # return lowest_rate
    return lowest_rate


def can_finish(batches, rate, deadline):
    # return hours_needed(batches, rate) <= deadline
    return hours_needed(batches, rate) <= deadline


def hours_needed(batches, rate):
    # return sum of hours_for(batch, rate) over every batch
    return sum(hours_for(batch, rate) for batch in batches)


def hours_for(batch, rate):
    # return batch divided by rate, rounded up
    return (batch + rate - 1) // rate   # integer ceiling, no floats
```