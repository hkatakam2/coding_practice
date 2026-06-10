# question
A string consisting of uppercase english characters can be encoded to a number using the following mapping:

'A' -> "1"
'B' -> "2"
...
'Z' -> "26"
To decode a message, digits must be grouped and then mapped back into letters using the reverse of the mapping above. There may be multiple ways to decode a message. For example, "1012" can be mapped into:

"JAB" with the grouping (10 1 2)
"JL" with the grouping (10 12)
The grouping (1 01 2) is invalid because 01 cannot be mapped into a letter since it contains a leading zero.
Given a string s containing only digits, return the number of ways to decode it. You can assume that the answer fits in a 32-bit integer.

**1. Restating the Question**
Given numeric string `s`. Find total valid ways to translate it to letters. 'A'=1 to 'Z'=26. No leading zeros allowed for mappings. Output: integer.

**2. Clarifying Questions**

* Can string be empty? (Assume no, length >= 1 per typical constraints).
* Can string start with '0'? (Yes, should return 0).
* Any non-digit characters? (No, pure digits).
* Output size limits? (Fits 32-bit integer).

**3. Hand Trace Example**
Input: `"226"`

* Take `2`, remaining `"26"`.
* Take `2`, remaining `"6"`.
* Take `6`, done. Path: `(2, 2, 6)` -> `BBF`.


* Take `26`, done. Path: `(2, 26)` -> `BZ`.


* Take `22`, remaining `"6"`.
* Take `6`, done. Path: `(22, 6)` -> `VF`.


* Total paths: 3.

**4. Brainstorming & Complexity**

* **Recursive DFS:** Try 1-digit, try 2-digit. Time: $O(2^n)$. Space: $O(n)$ for call stack. Too slow for large strings.
* **Memoized DFS:** Cache computed suffixes. Time: $O(n)$. Space: $O(n)$. Good.
* **Bottom-up DP:** Build ways iteratively left-to-right. Time: $O(n)$. Space: $O(n)$. Simple array.
* **Optimized DP:** Only need previous two states. Time: $O(n)$. Space: $O(1)$. Most efficient.

**5. Suggest Solutions**

1. **Recursive DFS (Manual trace):** Branch on 1 or 2 characters. Easy to grasp intuitively, mimics human logic.
2. **Top-Down Memoization:** Same as #1 but stores results to avoid redundant work.
3. **Bottom-Up DP:** Array tracks valid ways up to each index. Preferred for simplicity, avoids recursion stack depth issues, very clear state transitions. Will implement this.

**6. Implementation Outline**

```python
def numDecodings(s):
    """
    Reframe: Total ways to decode at current spot is sum of ways using valid 1-digit and valid 2-digit segments.
    State: List tracking valid decode combinations up to each segment, chosen because subproblems overlap perfectly.
    Invariant: Current ways depend exclusively on the immediate previous step and the step before that.

    isValidSingle(char) = true if char between '1' and '9'
    isValidDouble(chars) = true if string between "10" and "26"

    Core logic:
    - step through the string segment by segment
    - if current single digit is valid, carry forward combinations from one step back
    - if current two digits form a valid pair, add combinations from two steps back
    - return combinations accumulated at the very end

    Edge cases:
    - starting with '0'
    - encountering '0' that cannot pair with '1' or '2' (e.g., '30' or '00')
    """
    pass

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with plain English structure*

```python
def numDecodings(s):
    # init tracking array
    # set base states

    # loop through characters
        # ways for current step = 0
        
        # if isValidSingle:
        #   add ways from 1 step back
        
        # if isValidDouble:
        #   add ways from 2 steps back
        
        # save current step ways
        
    # return final step ways

```

*Iteration 2: Adding DP structure and loops*

```python
def numDecodings(s):
    # dp tracks ways up to length i
    dp = [0] * (len(s) + 1)
    
    # base states
    dp[0] = 1 # 1 way to decode empty string
    dp[1] = 1 # assume first char valid for now
    
    for i in range(2, len(s) + 1):
        ways = 0
        
        # placeholders for helpers
        # if isValidSingle(s[i-1]):
        #     ways += dp[i-1]
        
        # if isValidDouble(s[i-2 to i]):
        #     ways += dp[i-2]
            
        dp[i] = ways
        
    return dp[len(s)]

```

*Iteration 3: Filling in core logic helpers*

```python
def numDecodings(s):
    dp = [0] * (len(s) + 1)
    dp[0] = 1
    dp[1] = 1 

    for i in range(2, len(s) + 1):
        ways = 0
        
        # 1-digit check: just needs to not be '0'
        single_digit = s[i-1:i]
        if single_digit != "0":
            ways += dp[i-1]
            
        # 2-digit check: between 10 and 26
        double_digit = s[i-2:i]
        if "10" <= double_digit <= "26":
            ways += dp[i-2]
            
        dp[i] = ways
        
    return dp[len(s)]

```

*Iteration 4: Patching Edge Cases*
Edge case 1: String starts with '0'. `dp[1]` becomes 0.
Edge case 2: Impossible '0' later in string. Core logic actually handles this gracefully (ways remains 0, propagates 0).

```python
def numDecodings(s):
    # EDGE CASE: Empty string or leading zero
    if not s or s[0] == "0":
        return 0

    dp = [0] * (len(s) + 1)
    dp[0] = 1
    dp[1] = 1 # safe now, we checked s[0] == '0' above

    for i in range(2, len(s) + 1):
        ways = 0
        
        single_digit = s[i-1:i]
        if single_digit != "0":
            ways += dp[i-1]
            
        double_digit = s[i-2:i]
        if "10" <= double_digit <= "26":
            ways += dp[i-2]
            
        dp[i] = ways
        
    return dp[len(s)]

```

**8. Complexity & Optimizations**

* **Time Complexity:** $O(N)$ where $N$ is string length. Single pass.
* **Space Complexity:** $O(N)$ due to `dp` array.
* **Optimization:** Expensive section is memory allocation for long strings. We only ever look back 1 step (`dp[i-1]`) and 2 steps (`dp[i-2]`). Drop the $O(N)$ array and use two variables. $O(1)$ space.

*Optimized Code:*

```python
def numDecodings(s):
    if not s or s[0] == "0":
        return 0

    prev_two = 1 # equivalent to dp[i-2] (dp[0])
    prev_one = 1 # equivalent to dp[i-1] (dp[1])

    for i in range(2, len(s) + 1):
        current = 0
        
        single_digit = s[i-1:i]
        if single_digit != "0":
            current += prev_one
            
        double_digit = s[i-2:i]
        if "10" <= double_digit <= "26":
            current += prev_two
            
        # shift window forward
        prev_two = prev_one
        prev_one = current
        
    return prev_one

```