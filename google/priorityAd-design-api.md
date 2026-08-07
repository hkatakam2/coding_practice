Priority Ad System Design

### question
Design an API for an advertisement server that manages ad selection based on scores:

InsertAd(adContent, score): Inserts a new advertisement with its content and an initial priority score.
GetAd(): Selects and returns the advertisement with the highest score.

Once an advertisement is served, its score decreases by 1.
Constraint: The exact same advertisement cannot be returned in two consecutive calls to GetAd(), regardless of whether it still holds the highest score.

## 1. Restate Question

Design Ad Server system supporting two methods:

* `InsertAd(adContent, score)`: adds ad with initial score.
* `GetAd()`: returns ad with highest score, then decrements its score by 1.
* **Constraint**: cannot return same ad twice in consecutive `GetAd()` calls.

---

## 2. Clarifying Questions & Assumptions

* **Scores**: Can scores be $\le 0$? *Assumption: score $> 0$ required to be served. Once score drops to 0, ad expires.*
* **Uniqueness**: Is `adContent` unique identifier? *Assumption: yes, string content uniquely identifies ad.*
* **Empty state / Invalid state**: What if no ad available or top ad violates consecutive rule and no alternative exists? *Assumption: return `None`.*
* **Tie-breaking**: How to break tie when scores equal? *Assumption: arbitrary tie-breaker (e.g. insertion order or string comparison).*

---

## 3. Example Walkthrough by Hand

**Operations**:
`InsertAd("A", 10)`, `InsertAd("B", 10)`, `InsertAd("C", 5)`

| Step | Call | Active Ads (Score) | Last Served | Action / Check | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | `GetAd()` | `[A:10, B:10, C:5]` | `None` | Max score 10 (`A`). `A != None` -> Serve `A`, score becomes 9. | `"A"` |
| 2 | `GetAd()` | `[B:10, A:9, C:5]` | `"A"` | Max score 10 (`B`). `B != "A"` -> Serve `B`, score becomes 9. | `"B"` |
| 3 | `GetAd()` | `[A:9, B:9, C:5]` | `"B"` | Max score 9 (`B`). `B == "B"` (invalid!). Pick 2nd max `A:9`. Serve `A`, score becomes 8. Re-insert `B:9`. | `"A"` |
| 4 | `GetAd()` | `[B:9, A:8, C:5]` | `"A"` | Max score 9 (`B`). `B != "A"` -> Serve `B`, score becomes 8. | `"B"` |

---

## 4. Brainstorming Solutions

### Solution A: Unsorted Array / Scan

* Store `(score, adContent)` in list.
* `InsertAd`: append to list — $O(1)$.
* `GetAd`: linear scan to find max score where `adContent != last_served` — $O(N)$.

### Solution B: Max-Heap (Priority Queue)

* Maintain max-heap ordered by `-score`.
* `InsertAd`: push tuple to heap — $O(\log N)$.
* `GetAd`: pop top element. If matches `last_served`, pop second top element, push top element back. Decrement score of served ad, re-push if score $> 0$ — $O(\log N)$.

---

## 5. Suggested Solution

**Solution B (Max-Heap)**: optimal time complexity $O(\log N)$, straightforward, standard pattern for dynamic max-tracking with exclusion constraints.

---

## 6. Implementation Outline

```python
class AdServer:
    def get_ad(self) -> str:
        """
        Reframe: Max-priority extraction with single-element immediate exclusion.
        State: Max-heap storing (-score, count, ad_content), string last_served.
        Invariant: Top of heap holds max score; last_served tracks output of immediately prior get_ad call.

        get_eligible_candidate() = pops top; if content == last_served, pops 2nd top, restores 1st top, returns 2nd top.

        Core logic:
        - extract highest eligible ad content & current score via helper
        - decrement score by 1
        - if decremented score > 0, re-insert ad into heap
        - update last_served to extracted ad
        - return ad content

        Edge cases:
        - heap is empty
        - top ad matches last_served and no 2nd ad exists in heap
        - decremented score reaches 0 (do not re-insert)
        """

```

---

## 7. Iterative Implementation

### Step 7a: Skeleton / Code Outline

```python
import heapq

class AdServer:
    def __init__(self):
        self.heap = []
        self.last_served = None
        self.counter = 0  # Tie-breaker for heap

    def insert_ad(self, ad_content: str, score: int) -> None:
        # TODO: Push (-score, counter, ad_content) to heap
        pass

    def _get_eligible_ad(self):
        # TODO Stub helper: extract best candidate not equal to last_served
        pass

    def get_ad(self) -> str:
        # Core logic plain English outline:
        # 1. Pop eligible ad and score from helper
        # 2. Decrement score
        # 3. If score > 0, re-insert
        # 4. Update last_served
        # 5. Return ad
        pass

```

---

### Step 7b: Core Logic Implementation (Iterative)

#### Iteration 1: Basic Insert & Happy Path GetAd (Ignoring Consecutive Rule)

```python
import heapq

class AdServer:
    def __init__(self):
        self.heap = []
        self.last_served = None
        self.counter = 0

    def insert_ad(self, ad_content: str, score: int) -> None:
        # Iteration 1: Standard max-heap insertion using negative score
        self.counter += 1
        heapq.heappush(self.heap, (-score, self.counter, ad_content))

    def _get_eligible_ad(self):
        # Iteration 1 stub: just pop top of heap
        neg_score, _, content = heapq.heappop(self.heap)
        return -neg_score, content

    def get_ad(self) -> str:
        # Iteration 1 core logic happy path
        score, ad = self._get_eligible_ad()
        
        new_score = score - 1
        if new_score > 0:
            self.insert_ad(ad, new_score)
            
        self.last_served = ad
        return ad

```

#### Iteration 2: Realizing Helper Logic (Consecutive Exclusion Rule)

```python
import heapq

class AdServer:
    def __init__(self):
        self.heap = []
        self.last_served = None
        self.counter = 0

    def insert_ad(self, ad_content: str, score: int) -> None:
        self.counter += 1
        heapq.heappush(self.heap, (-score, self.counter, ad_content))

    def _get_eligible_ad(self):
        # Iteration 2: pop top; if top == last_served, pop 2nd top and restore 1st top
        top_neg_score, top_count, top_ad = heapq.heappop(self.heap)
        
        if top_ad == self.last_served:
            # Need second best
            second_neg_score, second_count, second_ad = heapq.heappop(self.heap)
            # Restore top back to heap
            heapq.heappush(self.heap, (top_neg_score, top_count, top_ad))
            return -second_neg_score, second_ad
        
        return -top_neg_score, top_ad

    def get_ad(self) -> str:
        # Core logic fully realized
        score, ad = self._get_eligible_ad()
        
        new_score = score - 1
        if new_score > 0:
            self.insert_ad(ad, new_score)
            
        self.last_served = ad
        return ad

```

---

### Step 7c: Patching Edge Cases

Now test edge cases identified in Step 6 against core logic:

#### Edge Case 1: Heap is completely empty

* Current behavior: `heapq.heappop` raises `IndexError`.
* Patch: Check `if not self.heap:` -> return `None`.

#### Edge Case 2: Top ad matches `last_served`, but heap has no 2nd ad

* Current behavior: 2nd `heapq.heappop` raises `IndexError`.
* Patch: After popping top, if `top_ad == last_served` and heap is empty, re-push top and return `None`.

#### Edge Case 3: Decremented score reaches 0

* Current behavior: `new_score > 0` condition skips re-insertion. Correct behavior, no patch needed.

#### Final Complete Code (Post Edge Case Patches):

```python
import heapq
from typing import Optional

class AdServer:
    def __init__(self):
        self.heap = []
        self.last_served = None
        self.counter = 0

    def insert_ad(self, ad_content: str, score: int) -> None:
        if score <= 0:
            return
        self.counter += 1
        heapq.heappush(self.heap, (-score, self.counter, ad_content))

    def _get_eligible_ad(self) -> Optional[tuple[int, str]]:
        # Edge Case 1: Empty heap
        if not self.heap:
            return None
            
        top_neg_score, top_count, top_ad = heapq.heappop(self.heap)
        
        # Check consecutive rule violation
        if top_ad == self.last_served:
            # Edge Case 2: No second ad available
            if not self.heap:
                heapq.heappush(self.heap, (top_neg_score, top_count, top_ad))
                return None
                
            second_neg_score, second_count, second_ad = heapq.heappop(self.heap)
            # Restore 1st candidate
            heapq.heappush(self.heap, (top_neg_score, top_count, top_ad))
            return -second_neg_score, second_ad
            
        return -top_neg_score, top_ad

    def get_ad(self) -> Optional[str]:
        eligible = self._get_eligible_ad()
        if not eligible:
            return None
            
        score, ad = eligible
        
        # Decrement score and re-insert if still active
        new_score = score - 1
        if new_score > 0:
            self.insert_ad(ad, new_score)
            
        self.last_served = ad
        return ad

```

---

## 8. Complexity & Optimization Analysis

### Time Complexity

* `InsertAd`: $O(\log N)$ where $N$ is number of active ads in heap.
* `GetAd`:
* Worst case pops 2 elements and pushes 2 elements back -> $4 \times O(\log N) = O(\log N)$.
* Amortized / Average case: $O(\log N)$.



### Space Complexity

* $O(N)$ auxiliary space for max-heap storing active ads.

### Potential Optimization

* **Stale Heap Cleanups / Batch Heap Updates**: If same ad inserted multiple times with updated score, store scores in HashMap (`{ad: score}`) + Heap (`(-score, ad)`). Lazy delete stale entries upon `GetAd` popping. Cuts heap churn when frequent score updates occur.

## follow up
Cooldown/Delay Constraint: Each advertisement now has an additional parameter, delay. Once an advertisement is returned by GetAd(), it cannot be served again for the next delay calls to GetAd(). How would you modify your data structures (e.g., combining a Max-Heap with a Min-Heap/Queue indexed by available time step) to efficiently support this cool-down period?





