## example 1
```python
def maxSubArray(nums: List[int]) -> int:
    if not nums: return None

    dp = [num for num in nums]
    for i, num in enumerate(nums[1:]):
        dp[i] = max(dp[i-1]+num, num)


    return max(dp)
```

there is a problem enumerate starts i from 0 instead of 1

```python
def maxSubArray(nums: List[int]) -> int:
        if not nums: 
            return 0 # Standard practice is to return 0 for an empty sum

        # A slightly cleaner way to copy the list
        dp = list(nums) 
        
        # Start at index 1 and go to the end of the array
        for i in range(1, len(nums)):
            dp[i] = max(dp[i-1] + nums[i], nums[i])

        return max(dp)
```
## revise list
- sorted rotated array; practice writing if else blocks
- search in sorted rotated array; finding which half using lies in between logic

- reversing linkedlist; only alter what is at the current step
- cycle detection; run through an example to find bugs; standard test cases
