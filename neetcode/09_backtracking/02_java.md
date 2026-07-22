### 1. Restate the problem

We are given an array of unique integers and a target integer. We need to find all unique combinations of these integers that add up exactly to the target.

Key details:

* We can use the same number from the array as many times as we want.
* The order of numbers within a combination doesn't matter (e.g., `[2, 3]` is the same as `[3, 2]`).
* We must return a list of these combinations, and the overall order of the returned list does not matter.

### 2. Ask clarifying questions

Before writing code, I'd want to confirm a few assumptions:

* **Negative numbers:** Can the array contain negative numbers or zero? (Assumption: No. If `0` or negative numbers were allowed, we could reuse them infinitely to reach the same target, resulting in an infinite number of valid combinations. I will assume all numbers are strictly positive).
* **Input size:** How large is the array, and how large is the target? (Assumption: The input size is reasonably small, e.g., target $\le 40$ and array size $\le 30$. This matters because combinations grow exponentially, and we need to ensure the result fits in memory).
* **Return type:** Should I return `List<List<Integer>>`? (Assumption: Yes, this is the standard Java representation).

### 3. Work through an example by hand

Let's take `nums = [2, 3, 6, 7]` and `target = 7`.

1. Start with an empty combination: `[]`, target remaining = 7.
2. Try adding `2`: `[2]`, remaining = 5.
3. Try adding `2` again: `[2, 2]`, remaining = 3.
4. Try adding `2` again: `[2, 2, 2]`, remaining = 1.
5. Try adding `2` again: `[2, 2, 2, 2]`, remaining = -1. (Bust! Backtrack to step 4).
6. Try adding `3` (next available number) to `[2, 2, 2]`: `[2, 2, 2, 3]`, remaining = -2. (Bust! Backtrack).
7. Backtrack to step 3 (`[2, 2]`, remaining = 3). Try adding `3`: `[2, 2, 3]`, remaining = 0. **Match! Save this combination.**
8. Backtrack, try other paths. Eventually, we try `[3, 3]` (remaining 1) -> bust.
9. Try `[6]` (remaining 1) -> bust.
10. Try `[7]` (remaining 0) -> **Match!**

Final valid combinations: `[[2, 2, 3], [7]]`.

### 4. Brainstorm solutions aloud

**Approach 1: Dynamic Programming**
We could build an array of lists `dp`, where `dp[i]` stores all combinations that sum to `i`. We iterate through `i` from 1 to `target`. For each value, we try adding every number in `nums`.

* *Drawback:* To avoid duplicate combinations like `[2, 3]` and `[3, 2]`, we'd have to sort combinations and use a Set, or be very careful about the order of loops. It also consumes a lot of memory holding intermediate combinations that might never reach the target.

**Approach 2: Depth-First Search (DFS) with Backtracking**
This is the literal process from our manual example. We build a single list incrementally. At each step, we iterate through the available numbers. To prevent duplicate combinations, we enforce an order: once we move on to the next number in `nums` (e.g., from `2` to `3`), we never look back at the previous numbers (we never add a `2` after adding a `3`).

* *Data structures:* An `ArrayList` to represent the current path, and a `List<List<Integer>>` for the final results.
* *Why it works:* It exhaustively explores all valid paths and abandons (prunes) paths as soon as they exceed the target.
* *Time complexity:* Exponential, $\mathcal{O}(N^{(T/M)})$, where $N$ is the number of elements, $T$ is the target, and $M$ is the minimum value in the array.
* *Space complexity:* $\mathcal{O}(T/M)$ for the recursion stack and the current path.

### 5. Select the solution

I will use **DFS with Backtracking**. It is the standard, most memory-efficient approach for generating combinations. It cleanly avoids duplicate combinations by controlling the starting index of our choices at each recursive step.

I will use standard Java `ArrayList` collections. An `ArrayList` is perfect for the `currentCombo` because we need stack-like behavior (adding and removing from the end), and `ArrayList` does this in $\mathcal{O}(1)$ time while allowing fast iteration when we need to copy it to the results list.

### 6. Write the implementation outline

```java
List<List<Integer>> combinationSum(int[] candidates, int target) {
    /*
     * Reframe:
     * Systematically build combinations by trying to add numbers one by one.
     * To allow reuse, we can pick the current number again.
     * To prevent duplicate sets, once we skip a number, we never pick it again.
     *
     * State:
     * - results: List to store valid combinations.
     * - currentCombo: The current sequence of numbers we've built.
     * Chosen because: ArrayList allows O(1) appends and removals at the end.
     *
     * Invariant:
     * Elements in currentCombo always sum to (original target - remainingTarget).
     * We only ever append elements from candidates starting at `startIndex` to prevent duplicates.
     *
     * Helpers:
     * backtrack(candidates, remainingTarget, startIndex, currentCombo, results)
     * - Explores all valid additions to currentCombo.
     *
     * Core logic:
     * - Initiate backtracking with index 0.
     * - Inside backtrack:
     *   - If remainingTarget == 0, we found a valid combination. Copy and store it.
     *   - If remainingTarget < 0, this path is a dead end. Return.
     *   - Loop through candidates starting from `startIndex`.
     *   - Add the candidate to the combo.
     *   - Recurse with the new remaining target. (Pass the *same* index to allow reuse).
     *   - Remove the candidate (backtrack) to explore the next option.
     *
     * Edge cases:
     * - Empty array.
     * - Target is already 0.
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton and basic state setup**

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> results = new ArrayList<>();
    List<Integer> currentCombo = new ArrayList<>();
    
    // TODO: invoke backtracking helper
    
    return results;
}

// TODO: create backtracking helper

```

**Iteration 2: Adding the helper with base cases**

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> results = new ArrayList<>();
    List<Integer> currentCombo = new ArrayList<>();
    
    // Added: kick off the recursion
    backtrack(candidates, target, 0, currentCombo, results);
    
    return results;
}

private void backtrack(int[] candidates, int remainingTarget, int startIndex, 
                       List<Integer> currentCombo, List<List<Integer>> results) {
    
    // Added: Base case for a successful combination
    if (remainingTarget == 0) {
        results.add(new ArrayList<>(currentCombo)); // Deep copy the current state
        return;
    }
    
    // Added: Base case for exceeding the target
    if (remainingTarget < 0) {
        return;
    }
    
    // TODO: recursive branching logic
}

```

**Iteration 3: Completing the recursive branching**

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> results = new ArrayList<>();
    List<Integer> currentCombo = new ArrayList<>();
    backtrack(candidates, target, 0, currentCombo, results);
    return results;
}

private void backtrack(int[] candidates, int remainingTarget, int startIndex, 
                       List<Integer> currentCombo, List<List<Integer>> results) {
    
    if (remainingTarget == 0) {
        results.add(new ArrayList<>(currentCombo));
        return;
    }
    
    if (remainingTarget < 0) {
        return;
    }
    
    // Added: Loop through candidates from the current starting point
    for (int i = startIndex; i < candidates.length; i++) {
        currentCombo.add(candidates[i]);
        
        // Recurse: subtract the current number from target.
        // We pass 'i' as the startIndex to allow reusing the current number,
        // but prevent going backwards to previous numbers.
        backtrack(candidates, remainingTarget - candidates[i], i, currentCombo, results);
        
        // Backtrack: remove the last added element to try the next one in the loop
        currentCombo.remove(currentCombo.size() - 1);
    }
}

```

**Edge-case pass**

* *Empty array:* If `candidates` is empty, the `for` loop inside `backtrack` simply won't execute, and it correctly returns an empty list. No patch needed.
* *Target is 0:* The first call to `backtrack` hits `remainingTarget == 0` and adds an empty list to results. This is mathematically correct, though typically problems ask for positive targets.
* *Negative targets / numbers:* Handled by our assumption that inputs are strictly positive. If the target itself starts negative, the `< 0` check catches it immediately.

### 8. Analyze expensive sections and optimize

Looking at the code, we are doing a lot of recursive calls where `remainingTarget < 0` is only caught at the *top* of the next recursive call.

If we **sort the array** first, we can break out of the `for` loop entirely the moment we encounter a number that exceeds the `remainingTarget`. Because the array is sorted, all subsequent numbers will be even larger and will also exceed the target.

This pruning optimization significantly cuts down the number of recursive calls, saving both time and stack space.

Let's apply this optimization.

### 9. Final Code

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Solution {
    
    public List<List<Integer>> combinationSum(int[] candidates, int target) {
        List<List<Integer>> results = new ArrayList<>();
        List<Integer> currentCombo = new ArrayList<>();
        
        // Sort to allow early pruning in the backtracking loop
        Arrays.sort(candidates);
        
        backtrack(candidates, target, 0, currentCombo, results);
        
        return results;
    }

    private void backtrack(int[] candidates, int remainingTarget, int startIndex, 
                           List<Integer> currentCombo, List<List<Integer>> results) {
        
        if (remainingTarget == 0) {
            results.add(new ArrayList<>(currentCombo));
            return;
        }
        
        for (int i = startIndex; i < candidates.length; i++) {
            // Pruning optimization: if the current candidate exceeds the remaining target,
            // subsequent larger candidates will also exceed it. We can stop this branch.
            if (candidates[i] > remainingTarget) {
                break;
            }
            
            currentCombo.add(candidates[i]);
            
            backtrack(candidates, remainingTarget - candidates[i], i, currentCombo, results);
            
            currentCombo.remove(currentCombo.size() - 1);
        }
    }
}

```

### 10. Complexity

* **Time Complexity:** Let $N$ be the length of the array, $T$ be the target, and $M$ be the smallest element in the array. The maximum depth of the recursion tree is $T/M$. The number of nodes in the tree is bounded by $\mathcal{O}(N^{(T/M)})$. Sorting takes $\mathcal{O}(N \log N)$, which is dominated by the recursive generation. The total time complexity is loosely bounded by $\mathcal{O}(N^{(T/M)})$. In practice, the early pruning drastically reduces the constant factor.
* **Space Complexity:** The maximum depth of the call stack will be $T/M$. The `currentCombo` list will also hold at most $T/M$ elements. Therefore, the auxiliary space complexity is $\mathcal{O}(T/M)$. (This excludes the space required to store the final output).

### 11. Brief test walkthrough

Let's test `candidates = [2, 3]`, `target = 5`.

1. `Arrays.sort` gives `[2, 3]`.
2. `backtrack` called with remaining=5, index=0.
3. `i=0` (candidate 2). `2 <= 5`. Add 2. Combo: `[2]`.
4. Recurse: remaining=3, index=0.
5. `i=0` (candidate 2). `2 <= 3`. Add 2. Combo: `[2, 2]`.
6. Recurse: remaining=1, index=0.
7. `i=0` (candidate 2). `2 > 1`. Break loop! (Pruning works).
8. Backtrack to step 4 (remaining 3). `currentCombo.remove` -> Combo: `[2]`. Loop continues to `i=1` (candidate 3).
9. `3 <= 3`. Add 3. Combo: `[2, 3]`.
10. Recurse: remaining=0, index=1. **Match! Result added.**
11. Returns correctly.

The logic holds up perfectly, and the pruning optimization avoids unnecessary deeper recursive calls.