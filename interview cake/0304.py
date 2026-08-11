'''
merge meeting times

given [(0, 1), (3, 5), (4, 8), (10, 12), (9, 10)]
output [(0, 1), (3, 8), (9, 12)]

do not assume the meetings are in order

Brute force:
check each pair with every other pair to see if it overlaps O(n^2) time

how do we do this with hand?
sort them with starting time;
if the starting time of the next meeting is <= end time of first meeting
then it overlaps

what is merged meeting time?
end time = max(current end time, next end time)

'''

def merge_ranges(meetings):
    # sort by start time
    sorted_meetings = sorted(meetings)

    # initialize merged_meetings with the earliest meeting
    merged_meetings = [sorted_meetings[0]]

    for current_meeting_start, current_meeting_end in sorted_meetings[1:]:
        last_merged_meeting_start, last_merged_meeting_end = merged_meetings[-1]

        # if the current meeting overlaps with the last merged meeting,
        # use the later end time of the two
        if (current_meeting_start <= last_merged_meeting_end):
            merged_meetings[-1] = (last_merged_meeting_start, max(last_merged_meeting_end, current_meeting_end))
        else:
            # add the current meeting since it does not overlap
            merged_meetings.append((current_meeting_start, current_meeting_end))

    return merged_meetings
'''
O(n lg n) time and 
O(n) space; in the worst case none of the meetings overlap

Bonus:
1. what if we could have an upper bound on the input values? 
will it reduce the time? what impact it will have on space?

Improvement in Runtime:
If we know the input values are bounded (e.g., all times are between 0 and 1000), 
we can use a counting sort or a bucket-based approach instead. A counting sort 
or bucket sort could bring the sorting step down to O(U + n), where U is 
the size of the range of values and n is the number of meetings. If U is much smaller than n \log n, this would result in a significant runtime improvement.

Cost in Memory:
This optimization would increase memory usage because we would need 
to allocate an array or buckets of size U to store counts or buckets 
of start and end times. If U is very large (e.g., millions), 
this could become impractical.
'''
def merge_ranges_bucket(meetings, max_time=24):  # assuming 24-hour clock
    """
    Merge meetings using bucket sort approach
    Time: O(max_time + n) where n is number of meetings
    Space: O(max_time)
    """
    # Create buckets for start and end times
    time_slots = [False] * (max_time + 1)
    end_times = [0] * (max_time + 1)
    
    # Mark start times and track latest end time for each start
    for start, end in meetings:
        time_slots[start] = True
        end_times[start] = max(end_times[start], end)
    
    merged_meetings = []
    current_start = None
    current_end = None
    
    # Scan through time slots to merge meetings
    for time in range(max_time + 1):
        if time_slots[time]:
            if current_start is None:
                # Start new meeting range
                current_start = time
                current_end = end_times[time]
            elif time <= current_end:
                # Extend current meeting if overlapping
                current_end = max(current_end, end_times[time])
            else:
                # Add previous meeting and start new one
                merged_meetings.append((current_start, current_end))
                current_start = time
                current_end = end_times[time]
    
    # Add last meeting if exists
    if current_start is not None:
        merged_meetings.append((current_start, current_end))
    
    return merged_meetings

def merge_ranges_counting(meetings, max_time=24):
    """
    Merge meetings using counting sort approach
    Time: O(max_time + n) where n is number of meetings
    Space: O(max_time)
    """
    # Create count arrays for start and end times
    start_counts = [0] * (max_time + 1)
    end_counts = [0] * (max_time + 1)
    
    # Count occurrences of start and end times
    for start, end in meetings:
        start_counts[start] += 1
        end_counts[end] += 1
    
    merged_meetings = []
    active_meetings = 0
    current_start = None
    
    # Scan through all time slots
    for time in range(max_time + 1):
        # Process end times first to handle back-to-back meetings correctly
        if end_counts[time] > 0:
            active_meetings -= end_counts[time]
            if active_meetings == 0 and current_start is not None:
                merged_meetings.append((current_start, time))
                current_start = None
        
        # Process start times
        if start_counts[time] > 0:
            if active_meetings == 0:
                current_start = time
            active_meetings += start_counts[time]
    
    return merged_meetings


'''
Could we do this “in place” on the input list to save space?

First, sort the input list in place using meetings.sort().
Use a pointer or an index to track the position in the list where the merged ranges are stored.
Iterate through the list, merging as necessary, and overwrite the earlier indices with the merged ranges.
'''
def merge_ranges_in_place(meetings):
    # Sort the list in place
    meetings.sort()

    # Index to track position of merged ranges
    write_index = 0

    for i in range(1, len(meetings)):
        current_start, current_end = meetings[i]
        last_start, last_end = meetings[write_index]

        if current_start <= last_end:
            # Merge ranges
            meetings[write_index] = (last_start, max(last_end, current_end))
        else:
            # Move to next position
            write_index += 1
            meetings[write_index] = meetings[i]

    # Slice the list to retain only the merged ranges
    return meetings[:write_index + 1]
'''
reason through the example, you will understand the code:

meetings = [(1,3), (2,4), (5,7), (6,8)]
'''

'''
Bucket sort is most suitable when:

Input values have a known range (like times 0-24, scores 0-100)
Values are fairly uniformly distributed
You need O(n) time complexity instead of O(n log n)

The pattern:
1. create buckets
buckets = [[] for _ in range(max_value + 1)]

2. distribute items
for item in items:
    bucket_index = calculate_bucket_index(item)
    buckets[bucket_index].append(item)

3. process buckets
result = []
for bucket in buckets:
    process_bucket(bucket, result)

Example 1: Meeting Times (Your Current Problem)
'''
def merge_meetings_bucket(meetings, max_hour=24):
    # 1. Create buckets for each hour
    time_slots = [[] for _ in range(max_hour + 1)]
    
    # 2. Distribute meetings by start time
    for start, end in meetings:
        time_slots[start].append((start, end))
    
    # 3. Process buckets to merge meetings
    merged = []
    current_meeting = None
    
    for hour in range(max_hour + 1):
        if time_slots[hour]:
            for start, end in time_slots[hour]:
                if not current_meeting:
                    current_meeting = [start, end]
                elif start <= current_meeting[1]:
                    current_meeting[1] = max(current_meeting[1], end)
                else:
                    merged.append(tuple(current_meeting))
                    current_meeting = [start, end]
    
    if current_meeting:
        merged.append(tuple(current_meeting))
    
    return merged
'''
Example 2: Student Scores
'''
def group_scores(scores, max_score=100):
    # 1. Create buckets for each possible score
    score_buckets = [[] for _ in range(max_score + 1)]
    
    # 2. Distribute students by score
    for student, score in scores:
        score_buckets[score].append(student)
    
    # 3. Process buckets to group students
    grouped = {}
    for score, students in enumerate(score_buckets):
        if students:
            grouped[score] = students
    
    return grouped

'''
example 3: IP Address Sorting
'''
def sort_ips(ip_addresses):
    # 1. Create buckets for first octet (0-255)
    buckets = [[] for _ in range(256)]
    
    # 2. Distribute IPs by first octet
    for ip in ip_addresses:
        first_octet = int(ip.split('.')[0])
        buckets[first_octet].append(ip)
    
    # 3. Process buckets
    sorted_ips = []
    for bucket in buckets:
        if bucket:
            bucket.sort()  # Sort IPs within each bucket
            sorted_ips.extend(bucket)
    
    return sorted_ips

'''
Key Benefits
Linear time complexity O(n + k) where k is range
Works well with fixed-range integers
Can be modified for special cases
Good for counting and grouping

Limitations
Requires known value range
Uses extra space
Not efficient for small n or large ranges
Not suitable for non-numeric or widely scattered data
'''