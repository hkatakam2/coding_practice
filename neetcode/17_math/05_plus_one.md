### question
You are given an integer array digits, where each digits[i] is the ith digit of a large integer. It is ordered from most significant to least significant digit, and it will not contain any leading zero.

Return the digits of the given integer after incrementing it by one.

**1. Restating the Question**
Given array of digits representing integer. Most significant left, least right. No leading zeros. Add 1 to integer. Return resulting digit array.

**2. Clarifying Questions**

* Negative numbers? (Assume no).
* Can array be empty? (Assume no, minimum `[0]`).
* Language integer limits? (If using C++/Java, `[9]*100` overflows standard integer. Must manipulate array directly. Even in Python, array manipulation demonstrates algorithmic intent better than typecasting).
* In-place modification okay? (Assume yes, returns modified array).

**3. Example by Hand**

* Input: `[1, 2, 3]`
* Look at last digit: 3. Add 1 -> 4. No carry. Done. Return `[1, 2, 4]`.


* Input: `[1, 2, 9]`
* Last digit: 9. Add 1 -> 10. Write 0. Carry 1 to left.
* Next digit: 2. Add carry (1) -> 3. No carry. Done. Return `[1, 3, 0]`.


* Input: `[9, 9]`
* Last: 9+1=10 -> 0, carry 1.
* Next: 9+1=10 -> 0, carry 1.
* Out of digits. Create new digit 1 at front. Return `[1, 0, 0]`.



**4. Brainstorming & Complexity**

* *Idea A (Typecast):* Convert list to string, parse to int, add 1, convert back to list of ints. O(N) time, O(N) space. Skips core logic problem.
* *Idea B (Math Simulation):* Start rightmost digit. Add 1. If sum < 10, update and stop. If sum == 10, set to 0, move left. If loop exhausts, prepend 1. O(N) worst-case time, O(1) space (ignoring prepend resize).

**5. Suggest Solutions**
Prefer Idea B. Direct, simple, mirrors manual addition. Idea A feels like cheating the interview. We will implement Idea B.

**6. Outline**

```python
def plusOne(digits): 
    """
    Reframe: Simulate grade-school right-to-left addition by 1.
    State: current digit position, chosen because carries propagate right-to-left.
    Invariant: all digits to the right of current position are 0 and carry is correctly passed left.

    Core logic:
    - start at rightmost digit
    - check if digit can be incremented without overflowing 10
    - if yes, increment and return early
    - if no, digit must be 9. set to 0, move left to process carry
    
    Edge cases:
    - loop finishes but carry remains (all original digits were 9). prepend 1.
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton*

```python
def plusOne(digits):
    # loop from right to left
        # if current digit is less than 9:
            # increment it
            # return digits early
        
        # otherwise, digit is 9
        # set it to 0
    
    # TODO: edge case - what if all digits were 9?
    pass

```

*Iteration 2: Core Logic (Happy Path)*

```python
def plusOne(digits):
    # loop right to left
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            # increment and return early (e.g. 3 -> 4)
            digits[i] += 1
            return digits
            
        # digit is 9, overflows to 0. Carry naturally passes to next loop iteration.
        digits[i] = 0
        
    # TODO: handle all 9s edge case

```

*Iteration 3: Full Logic (Adding Edge Case)*

```python
def plusOne(digits):
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        
        digits[i] = 0
        
    # Edge case: Loop finished without returning. Means all digits were 9.
    # Array is currently all 0s. Prepend 1.
    return [1] + digits

```

**8. Complexity & Optimizations**

* **Time Complexity:** `O(N)`. Worst case, traverses entire array if all 9s. Best case `O(1)` if last digit < 9.
* **Space Complexity:** `O(1)` for happy path (in-place). `O(N)` worst case in Python to create new `[1] + digits` array.
* **Optimization:** `[1] + digits` creates new list. If memory is extremely tight or using languages like Java/C++, you'd allocate a new array of size `N+1`, set `arr[0] = 1`, and rest are `0` by default. Python handles this elegantly with list concatenation. No further logic optimization needed.