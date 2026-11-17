class Solution(object):
    def minimumChanges(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        n = len(s)
        
        # Precompute proper divisors for each length from 1 to n
        divisors = [[] for _ in range(n + 1)]
        for length in range(1, n + 1):
            for d in range(1, length):
                if length % d == 0:
                    divisors[length].append(d)
        
        # Precompute cost[i][j]: min changes to make s[i...j] a semi-palindrome
        cost = [[float('inf')] * n for _ in range(n)]
        
        for i in range(n):
            for j in range(i + 1, n):
                length = j - i + 1
                min_changes = float('inf')
                for d in divisors[length]:
                    current_changes = 0
                    # Check each of the d groups
                    for start in range(d):
                        # Use two pointers directly on the string indices instead of building lists
                        left = i + start
                        right = i + start + (length - 1 // d) * d # or compute end of group
                        # A cleaner way to traverse the group:
                        # Collect characters for this group
                        group_start = i + start
                        # Fast loop to count palindrome mismatches for this group
                        l_idx = group_start
                        r_idx = i + start + ((length // d) - 1) * d
                        while l_idx < r_idx:
                            if s[l_idx] != s[r_idx]:
                                current_changes += 1
                            l_idx += d
                            r_idx -= d
                    min_changes = min(min_changes, current_changes)
                cost[i][j] = min_changes

        # DP table: dp[i][parts] = min changes for suffix s[i:] into `parts` semi-palindromes
        dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
        dp[n][0] = 0

        # Base case: 1 part for the remaining suffix
        for i in range(n - 1, -1, -1):
            dp[i][1] = cost[i][n - 1]

        # Fill DP table for partitions from 2 to k
        for parts in range(2, k + 1):
            for i in range(n - parts + 1):
                for j in range(i, n - parts + 1):
                    dp[i][parts] = min(dp[i][parts], cost[i][j] + dp[j + 1][parts - 1])

        return dp[0][k]