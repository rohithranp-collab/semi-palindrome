# 2911. Minimum Changes to Make K Semi-palindromes

![Difficulty](https://img.shields.io/badge/difficulty-hard-red)
![Language](https://img.shields.io/badge/language-python-blue)
![Topic](https://img.shields.io/badge/topic-dynamic%20programming-green)

LeetCode problem: [Minimum Changes to Make K Semi-palindromes](https://leetcode.com/problems/minimum-changes-to-make-k-semi-palindromes/)

## Problem

Given a string `s` and an integer `k`, partition `s` into `k` substrings so that the total number of letter changes needed to turn every substring into a **semi-palindrome** is minimized. Return that minimum.

A string of length `L` is a semi-palindrome if there is a divisor `d` of `L` with `1 <= d < L` such that, when the string is split into `d` groups (group `g` holds the characters at positions `g, g + d, g + 2d, ...`), every group is a palindrome.

**Example**

```
Input:  s = "abcac", k = 2
Output: 1
Explanation: "ab" + "cac". "cac" is already a semi-palindrome,
and "ab" needs one change ("aa").
```

**Constraints**

- `2 <= s.length <= 200`
- `1 <= k <= s.length / 2`
- `s` contains only lowercase English letters

## Approach

The solution uses two stages of dynamic programming.

### 1. Cost table

`cost[i][j]` is the minimum number of changes to make `s[i..j]` a semi-palindrome.

- For each substring of length `L`, try every proper divisor `d` of `L`.
- For a given `d`, split the substring into `d` groups. In each group, count mismatched pairs from both ends moving inward. That count is the number of changes the group needs.
- The cost for the substring is the minimum total over all valid `d`. Stop early if a divisor gives `0`.
- Proper divisors for every length are precomputed with a sieve.

A substring of length 1 has no valid divisor, so its cost stays infinite. This means every part must have length at least 2.

### 2. Partition DP

`dp[p][j]` is the minimum cost to split the first `j` characters into `p` parts.

```
dp[p][j] = min over i of ( dp[p-1][i] + cost[i][j-1] )
```

Optimizations that keep it within the time limit:

- Part `p` must end at `j >= 2p`, and it must leave room for the remaining `k - p` parts, so `j <= n - 2(k - p)`.
- A rolling array (`prev` / `cur`) replaces the full 2D DP table.
- Groups are extracted with string slicing (`sub[g::d]`), which runs in C.

## Complexity

| | Complexity |
|---|---|
| Time | `O(n^3 * D)` for the cost table (`D` = max number of divisors of a length, small for `n <= 200`) + `O(k * n^2)` for the DP |
| Space | `O(n^2)` for the cost table + `O(n)` for the rolling DP |

## Solution

See [`2911-minimum-changes-to-make-k-semi-palindromes.py`](./2911-minimum-changes-to-make-k-semi-palindromes.py).

```python
from solution import Solution

print(Solution().minimumChanges("abcac", 2))    # 1
print(Solution().minimumChanges("abcdef", 2))   # 2
print(Solution().minimumChanges("aabbaa", 3))   # 0
```

## Notes

- The hardest test case is `n = 200, k = 100`. A first version with a plain triple loop and `float('inf')` exceeded the time limit. Tightening the DP bounds, using integer infinity, and slicing groups fixed it.
