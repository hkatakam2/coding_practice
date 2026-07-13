'''
write a function merge_ranges() that takes a list of multiple meeting 
time ranges and returns a list of condensed ranges.

given [(0, 1), (3, 5), (4, 8), (10, 12), (9, 10)],

the function would return [(0, 1), (3, 8), (9, 12)].

Do not assume the meetings are in order. challenge is to merge meetings 
where start time and end time don't have an upper bound

'''

'''
each tuple is compared with each other tuple; O(n^2)
better to sort; O(nlog n)


how to we know if an interval is overlapping?
start time of next interval is <= end time of current interval


algorithm:
1. if start time of second interval is <= end time of first, we merge them.
The resulting interval start time is start time of first interval
end time is max(first end time, second end time)
'''

def merge_ranges(meetings):
    # sort by start time
    sorted_meetings = sorted(meetings)
    # initialize merged_meetings with the earliest meeting
    merged_meetings = [sorted_meetings[0]]

    for current_meeting_start, current_meeting_end in sorted_meetings[1:]:
        last_merged_meeting_start, last_merged_meeting_end = merged_meetings[-1]

        # if the current meeting overlaps with the last merged meeting,
        # use the later endtime of the two
        if (current_meeting_start <= last_merged_meeting_end):
            merged_meetings[-1] = (last_merged_meeting_start, 
                                   max(last_merged_meeting_end, current_meeting_end))
        else:
            # add the current meeting as it does not overlap
            merged_meetings.append((current_meeting_start, current_meeting_end))

    return merged_meetings

'''
O(nlog n) time
O(n) space; in the worst case none of the meetings overlap

bonus:
what if we have an upper bound on the input values? can we improve time and space?

If we have an upper bound (let's say k) on input values:
1. Can use counting/bucket sort instead - O(k) time
2. Can use a boolean array of size k to mark intervals - O(k) space
3. Final time would be O(k) instead of O(nlogn)
4. Trade-off: Only works for small k values, uses more space for sparse data
'''


'''
Bonus: can we utlitze the inplace algorithm to save space? what are the pros and cons?

learning: first simplify and relax the inplace requirement
'''
def merge_ranges_inplace(meetings):
    # Sort in place
    meetings.sort()
    
    # Keep track of write index
    write_idx = 0
    
    for i in range(1, len(meetings)):
        if meetings[i][0] <= meetings[write_idx][1]:
            # Merge by updating end time of previous meeting
            meetings[write_idx] = (meetings[write_idx][0], 
                                 max(meetings[write_idx][1], meetings[i][1]))
        else:
            # Move write index and copy current meeting
            write_idx += 1
            meetings[write_idx] = meetings[i]
    
    # Trim the list to remove unused elements
    del meetings[write_idx + 1:]
    return meetings

'''
Pros:
- O(1) extra space instead of O(n)
- No need to create new list

Cons:
- Modifies input list which can be unexpected
- Less flexible if input is immutable
- Not thread-safe if input is shared
'''

'''
what we learned? a greedy approch
why did we sort? we saw comparing with every interval is inefficient


you should be able to see the whole solution;
then we can attempt new questions. you need more revision. 
take one more month and revise them.

'''
