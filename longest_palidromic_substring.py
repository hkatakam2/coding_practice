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

    def expand_and_update(self, s, left, right):
        pass