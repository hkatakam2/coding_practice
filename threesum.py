class Solution:
    def threeSum(nums):
        nums.sort() 
        result = []
        n = len(nums)
        
        for i in range(n - 2):
            # 1. OPTIMIZATION: If the current number is positive, we can't sum to 0
            # because the array is sorted (remaining numbers are also positive).
            if nums[i] > 0:
                break
                
            # 2. DUPLICATE HANDLING (Outer Loop): 
            # If this number is the same as the previous one, skip it.
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            left = i + 1
            right = n - 1
            
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]
                
                if current_sum == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    
                    # 3. DUPLICATE HANDLING (Inner Loop):
                    # Skip all duplicates for the 'left' pointer
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # Skip all duplicates for the 'right' pointer
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                        
                    # Move pointers inward after skipping duplicates
                    left += 1
                    right -= 1
                    
                elif current_sum < 0:
                    left += 1
                else:
                    right -= 1
                    
        return result
    
    print(threeSum([-1, 0, 1, 2, -1, -4]))  # Example usage