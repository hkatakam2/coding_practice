class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s: return ""

        # initialize the global variable with first char
        self.longest = s[0]

        for i in range(len(s)):
            # case: odd length palindrome
            self.expand_and_update(s, i, i)

            # case: even length palindrome
            self.expand_and_update(s, i, i+1)

        return self.longest

    # TODO
    def expand_and_update(self, s, left, right):
        # expand as long as pointers are in bounds and characters match
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1

        # extract the palindrome; use left and right before exit from while loop
        # current_palindrome = s[left + 1 : right] this is slow

        # update the global maximum
        if (right - left -1) > len(self.longest):
            self.longest = s[left+1 : right]

sol = Solution()
print(sol.longestPalindrome("babad"))