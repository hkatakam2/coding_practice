def threeSumSimple(nums):
    nums.sort()  # Sorting is O(N log N)
    result = []
    n = len(nums)
    
    # Iterate through the array, stopping 2 elements before the end
    for i in range(n - 2):
        
        # Standard Two-Pointer approach
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                # Since inputs are unique, we just move both pointers 
                # to look for other pairs
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1  # Need a larger sum
            else:
                right -= 1 # Need a smaller sum
                
    return result


print(threeSumSimple([ -1, 0, 1, 2, -1, -4]))