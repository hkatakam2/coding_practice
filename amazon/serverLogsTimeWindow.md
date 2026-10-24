# question
Server/Skill Request Logs in a Sliding Time Window: Given numSkills, a 2D array requestLogs = [skill_id, timestamp], a timeWindow $X$, and an array of queryTimes, return how many skills received zero requests in the interval $[t - X, t]$ for each query time $t$

# clarifications:
1. skills 0 indexed? No 1 indexed
2. interval is inclusive of both ends? Yes
3. are logs sorted? queries sorted? No both

# ideas
1. brute force: for each query, scan every log, collect distinct skill ids that are in the interval. return numSkills - len(set). O(Q.L)
2. sort logs and find out which skills are used in the interval; return unsed
3. sort both logs and queries; use sliding window to add and remove used kissls; optimized

# outline simple
count_idle_skills(numSkills, logs, X, queries):
    sort the logs by timestamp
    for each query t:
        window = logs with timestamp in [t-X, X]
        used = distnct skill ids in window
        answer.append(numSkills - len(used))
    return answer

```python
def count_idle_skills(numSkills, requestLogs, X, queryTimes):
    logs = sorted(requestLogs, key=lamda x:x[1])
    times = [ts for _, ts in logs] # seperated so bisect can run

    answer = []
    for t in queryTimes:
        lo = bisect_left(times, t-X) # first log with ts >= t-X
        hi = bisect_right(times, X) # first log with ts > X

        used = {logs[i][0] for i in range(lo, hi)} # set to dedup
        answer.append(numSkills - len(used))

    return answer
```

# optimize: instead of rescaning for each query; we can sort queries and do a slidning window
count_idle_skills(numSkills, logs, X, queryTimes):
    sort logs by timestamp
    sort queries by time(remember original positions)

    window = empty
    active_cells = 0

    for each query (t, original_index) in time order:
        admit all logs with time <= t
        remove all logs with time < t-X
        answer[original_index] = numSkills - activeSkills

    return answer

```python
def count_idle_skills(numSkills, skillLogs, X, queryTimes):
    logs = sorted(skillLogs, key=lambda x:x[1])
    ordered_queries = sorted((t, i) for i, t in enumerated(queryTimes))

    count = [0]* (numSKills - 1)
    actuve = 0
    left = right = 0
    answer = [0] * len(queryTimes)
    for t, idx in ordered_queries:
        # admit logs with ts <= t
        while right < len(logs) and logs[right][1] <= t:
            skill = logs[right][0]
            count[skill] += 1
            if count[skill] == 1:
                active += 1
            right += 1

        # remvoe logs with ts < t-X
        while left < right and logs[left][1] < t-X:
            skill = logs[left][0]
            count[skill] -= 1
            if count[skill] == 0:
                active -= 1
            left += 1

        answer[idx] = numSkills - active


    return answer
```
Complexity: Time is O(L log L + Q log Q), since each log is admitted and evicted at most once and sorting dominates. Space is O(numSkills + L + Q).

Follow-ups I’d expect:

Online queries (can’t sort them)? Group timestamps per skill and binary-search each, or use a persistent/segment-tree structure.
Streaming logs? Keep a deque window and evict by time as new logs arrive.

