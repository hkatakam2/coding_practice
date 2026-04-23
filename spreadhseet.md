## problem
Design a spreadsheet system that supports setting cell values (integers) and formulas (sum of other cells). The core challenge is maintaining a dependency graph where formulas automatically recompute when their dependencies change. For example, if cell C sums cells A and B, updating A should automatically propagate to C and any cells depending on C.

### 1. What is the actual question being asked?

At its core, the problem is asking you to build a **Reactive Key-Value Store**. 

Normally, a key-value store (like a dictionary or hash map) is static: you put a value in, it stays there until you change it. 
This problem asks for a system that is *dynamic*. Some values are static integers, but other values are mathematical functions (sums) of *other* keys. 
**The central challenge:** If you update Key A, any other Key that mathematically relies on Key A must automatically and accurately reflect that new reality when someone asks for its value.

---

### 2. Breaking the Problem Down into Familiar Patterns

When you face a complex problem, the best strategy is to map its behaviors to known computer science concepts. 

* **Pattern 1: The Standard Key-Value Store (Hash Map)**
    * *The Familiar Problem:* How do I quickly store and retrieve `A = 5`? 
    * *The Application:* You will definitely need a foundational map/dictionary to hold the final, computed integer values for instantaneous $O(1)$ lookups when `get_value` is called.
* **Pattern 2: The Directed Acyclic Graph (DAG)**
    * *The Familiar Problem:* Course prerequisites. You must take Math 101 before Math 201. 
    * *The Application:* Formulas create a flow of dependencies. If `C = A + B`, information flows from A to C, and B to C. Because the prompt guarantees "no circular dependencies," we know this is a DAG. This tells us that traversing the updates will behave like a tree search (DFS or BFS) moving strictly downstream.
* **Pattern 3: The Observer / Pub-Sub Pattern**
    * *The Familiar Problem:* When a YouTuber uploads a video, all their subscribers get a notification. 
    * *The Application:* Cells need to "subscribe" to the cells they depend on. `A` doesn't inherently care what its own value is, but it *must* maintain a list of its subscribers (like `C`) so it can "publish" a notification when its value changes.

---

### 3. Solving the Parts (Logical Assembly)

Now that we have our patterns, how do we think about connecting them into a working solution? 

**Part A: State Separation (What are we actually storing?)**
You cannot store everything in one place. A cell fundamentally has three distinct identities that must be tracked separately:
1.  **Its Output:** The actual computed integer (e.g., `20`).
2.  **Its Blueprint:** The formula that defines it (e.g., `A + A + B`). You must save this because if `A` changes, you need the blueprint to recalculate `C`.
3.  **Its Subscribers:** The list of other cells waiting for it to change. (e.g., `A`'s subscriber list contains `C`).

**Part B: The "Set" Lifecycle (Handling Mutations)**
When a user updates a cell (either giving it a new static integer or a new formula), you have to think about the *destruction* of the old state before the *creation* of the new state.
* *Tear Down:* If `C` used to be `A + B`, but the user just overwrote `C` to be `100`, `C` is no longer a formula. You must logically sever the ties. `C` must "unsubscribe" from `A` and `B` so it stops receiving irrelevant updates.
* *Build Up:* If it's a new formula, you establish the new subscriptions.

**Part C: The Propagation Engine (The Ripple Effect)**
When a cell's value changes, how does the rest of the board update? You need a mechanism to traverse your DAG.
* If `A` changes, you look at `A`'s subscriber list. 
* You see `C`. You grab `C`'s blueprint (`A + B`) and re-calculate it using the new value of `A`.
* Now `C` has changed! So you look at `C`'s subscriber list... and the process continues downstream until no more subscribers are left.

**Part D: The Big Trade-off (Lazy vs. Eager Evaluation)**
You have to make a philosophical design choice on *when* to do the math:
* **Eager (Push):** Do all the heavy mathematical lifting and graph traversal the exact moment a `set` happens. `get` operations are incredibly fast because the answer is already computed.
* **Lazy (Pull):** When `set` happens, just mark the cell and its dependents as "dirty" (needs recalculation). Wait to do the actual math until someone actually asks for it via `get`. 

Both are conceptually valid, but they optimize for different scenarios. 

If we assume an Excel sheet where users might update a single cell 50 times in a minute before anyone ever checks the final total at the bottom, which evaluation strategy—Lazy or Eager—do you think would be more efficient, and why?

This is exactly how a senior candidate handles a system design or complex data structure interview. You don't just start writing code top-to-bottom. You build a "scaffold" first, explain the architecture to the interviewer to get their buy-in, and *then* fill in the bricks. 

This technique is called **"Signposting."** It proves you can think architecturally before getting lost in syntax.

Here is the game plan for how you would communicate this in an interview, setting up the logical flow step-by-step.

### Step 1: Declare the State (The "What")
First, you tell the interviewer you are going to initialize the three distinct layers of state we discussed earlier. You write the `__init__` method and clearly comment what each dictionary represents. 

```python
class ReactiveSpreadsheet:
    def __init__(self):
        # 1. The Evaluated State (The Output)
        # Maps a key to its final integer value. e.g., {"C": 20}
        self.values = {} 

        # 2. The Definitional State (The Blueprint)
        # Maps a formula cell to the list of cells it relies on. e.g., {"C": ["A", "A", "B"]}
        self.formulas = {} 

        # 3. The Relational State (The Subscribers)
        # Maps a cell to a SET of cells that are listening for its changes. e.g., {"A": {"C", "D"}}
        self.subscribers = {} 
```

### Step 2: Define the Public API and Helpers (The "Signposts")
Next, you write out the empty methods. You explicitly tell the interviewer: *"I'm going to define the public API, but I also know I'll need two private helper methods to handle the complex teardown and ripple effects."*

```python
    # --- PUBLIC API ---

    def get_value(self, key):
        """Returns the integer value, defaulting to 0 if not found."""
        pass

    def set_value(self, key, val):
        """Sets a cell to a static integer. Must destroy old formulas/subscriptions."""
        pass

    def set_sum(self, key, dependencies):
        """Sets a cell to be a formula. Must establish new subscriptions and calculate."""
        pass

    # --- PRIVATE ENGINE ---

    def _clear_old_subscriptions(self, key):
        """If this cell used to be a formula, it needs to unsubscribe from its old dependencies."""
        pass

    def _propagate_and_calculate(self, key):
        """The ripple effect. Recalculates this cell, then recursively updates its subscribers."""
        pass
```

### Step 3: Secure Interviewer Buy-In
At this point in the interview, you pause. You look at the interviewer and say: 

> *"Here is the overall flow: `get_value` will be an instant $O(1)$ lookup from `self.values`. The heavy lifting happens in the setters. Whether we call `set_value` or `set_sum`, the very first thing we must do is call `_clear_old_subscriptions` to prevent memory leaks or ghost updates. Then we update our state. Finally, we call `_propagate_and_calculate` to ripple the changes downstream. Does this architecture make sense before I implement the details?"*

(The interviewer will almost certainly smile and say "Yes, proceed.")

---

### Step 4: The Actual Implementation (Let's do this together)

Now it's time to fill in those empty blocks. Let's tackle the simplest public method first, relying on the fact that our helper methods *will* exist. 

If a user calls `set_value("C", 100)`, overwriting whatever "C" used to be with a brand new static integer, what are the specific steps you must take to update our three dictionaries (`values`, `formulas`, `subscribers`) before you trigger the final ripple effect?

Applying a first-principles approach here means we must handle the state mutations one dictionary at a time, ensuring total isolation between the old state and the new. It is the exact kind of systematic teardown you might emphasize when tutoring someone on preventing memory leaks or stale state. 

Here is exactly how you fill in that `set_value` brick while talking the interviewer through it:

### Step 4: Implementing `set_value` (The Teardown)

When a cell is forced to become a static integer, it immediately loses its identity as a formula. We have to scrub it from our definitional and relational states.

```python
    def set_value(self, key, val):
        # 1. Sever ties with the past. Stop listening to old dependencies.
        self._clear_old_subscriptions(key)
        
        # 2. Update the Output state with the new hardcoded integer.
        self.values[key] = val
        
        # 3. Destroy the Blueprint. It is no longer a formula.
        if key in self.formulas:
            del self.formulas[key]
            
        # 4. Ripple the new integer downstream to anyone who depends on this key.
        self._propagate_and_calculate(key)
```

By keeping the complex logic abstracted in the helper methods (`_clear_old_subscriptions` and `_propagate_and_calculate`), your core public API remains incredibly readable.

---

### Step 5: Implementing `set_sum` (The Build-Up)

Now we face the opposite scenario. The user calls `set_sum("C", ["A", "A", "B"])`. `C` is now a formula. 

Just like before, the very first thing we must do is call `self._clear_old_subscriptions("C")` to wipe the slate clean. Then, we update our blueprint state by saving `self.formulas["C"] = ["A", "A", "B"]`. 

But before we can trigger the ripple effect, we must build the *new* relational state. We have to wire up `self.subscribers` so that `A` and `B` know that `C` is listening to them.

To ensure `C` recalculates correctly when either `A` or `B` mutates, how exactly should we update the `self.subscribers` dictionary, and does the fact that `A` appears *twice* in the blueprint change how we register `C` as a subscriber?

The answer to the multiplicity challenge lies in the difference between **notification** and **calculation**. 

A publisher (like cell `A`) only needs to know *who* is listening so it can tap them on the shoulder and say, "Hey, I changed." It does not care *how many times* the subscriber plans to use that new information. Therefore, `self.subscribers` should use a `Set`. Adding `C` to `A`'s subscriber set multiple times is an idempotent operation—it safely resolves to a single subscription. The *calculation* phase will handle the multiplicity because `C` will read its own blueprint (`["A", "A", "B"]`) and fetch the value of `A` twice.

Here is how you explain and implement `set_sum`:

### Step 5: Implementing `set_sum` (The Build-Up)

```python
    def set_sum(self, key, dependencies):
        # 1. Sever ties with the past.
        self._clear_old_subscriptions(key)
        
        # 2. Save the new blueprint.
        self.formulas[key] = dependencies
        
        # 3. Establish new subscriptions (The Relational State).
        for dep in dependencies:
            if dep not in self.subscribers:
                self.subscribers[dep] = set()
            self.subscribers[dep].add(key) # Using a set naturally handles duplicates
            
        # 4. Ripple the changes downstream.
        self._propagate_and_calculate(key)
```

Now we have built the public API. In an interview, you would now say, *"With the state safely managed, we just need to build the private engine that handles the heavy lifting."*

---

### Step 6: The Private Engine (Teardown & Ripple)

The teardown is straightforward but critical to prevent memory leaks. If a cell stops being a formula, we must remove it from the subscriber lists of its old dependencies. 

```python
    def _clear_old_subscriptions(self, key):
        if key in self.formulas:
            old_dependencies = self.formulas[key]
            for dep in old_dependencies:
                if dep in self.subscribers and key in self.subscribers[dep]:
                    self.subscribers[dep].remove(key)
```

Finally, the engine itself: `_propagate_and_calculate`. Because we are guaranteed a Directed Acyclic Graph (DAG) with no circular dependencies, we can safely use a recursive Depth-First Search (DFS) to ripple the updates downstream.

```python
    def _propagate_and_calculate(self, key):
        # 1. Recalculate THIS cell's value (if it is a formula).
        if key in self.formulas:
            total = 0
            for dep in self.formulas[key]:
                # Recursive fetch or default to 0
                total += self.values.get(dep, 0) 
            self.values[key] = total
            
        # 2. Notify all subscribers that THIS cell has changed.
        if key in self.subscribers:
            for subscriber in self.subscribers[key]:
                self._propagate_and_calculate(subscriber)
```

And finally, our `get_value` is simply:

```python
    def get_value(self, key):
        return self.values.get(key, 0)
```

---

### The "Senior-Level" Pivot

If you lay out the code exactly like this, separating the state mutations from the graph traversal, an interviewer will recognize that you understand how to isolate concerns. 

However, we made a distinct, deliberate architectural choice here: **Eager Evaluation**. We chose to do all the mathematical heavy lifting during the `set` operation, making `get` an $O(1)$ operation. 

If the interviewer throws a curveball and says: *"Imagine a scenario where we have a massive, complex financial model. A script updates root cells thousands of times per second, but the user only checks the final `Total` cell once an hour."*

In that specific scenario, our Eager approach would waste massive amounts of CPU cycles recalculating intermediate states that no one ever looks at. How would you modify this architecture to use **Lazy Evaluation**, where the math only happens when `get_value` is explicitly called?

Switching from **Eager Evaluation** to **Lazy Evaluation** completely flips our performance profile. Instead of doing the heavy math on every `set` operation, we defer the cost to the `get` operation. 

This approach is heavily used in frontend frameworks (like React) and massive computational graphs (like TensorFlow or Excel) where state might mutate hundreds of times before anyone actually asks to see the result.

### The Lazy Evaluation Flow

To achieve this, we introduce a new piece of state: a **`dirty` cache**. 
* **The "Set" Phase (Invalidation):** When a cell is updated, we do *not* recalculate the math. We simply traverse the `subscribers` graph and tag every downstream cell as `dirty`. This is extremely fast because we are just flipping boolean flags, not doing arithmetic.
* **The "Get" Phase (Resolution):** When `get_value` is called, we check the `dirty` cache. If the cell is clean, we instantly return its cached value. If it is dirty, we recursively call `get_value` on its dependencies, do the math, cache the new value, and remove the `dirty` flag.

---

### The Complete Lazy Implementation

Here is the complete implementation with the missing pieces included:

```python
class LazyReactiveSpreadsheet:
    def __init__(self):
        # 1. Output State (Caches final computed values or static integers)
        self.values = {}       
        # 2. Definitional State (Formulas)
        self.formulas = {}     
        # 3. Relational State (Subscribers/Reverse Dependencies)
        self.subscribers = {}  
        # 4. The Invalidation State (Tracks which formulas need to be recalculated)
        self.dirty = set()     

    # --- PRIVATE ENGINE ---

    def _clear_old_subscriptions(self, key):
        """Sever ties with old dependencies when a formula changes."""
        if key in self.formulas:
            for dep in self.formulas[key]:
                if dep in self.subscribers and key in self.subscribers[dep]:
                    self.subscribers[dep].remove(key)

    def _invalidate_downstream(self, key):
        """
        The Lazy Ripple: We don't do math here. We just tag subscribers as 'dirty'.
        We use Depth-First Search to recursively invalidate all downstream dependents.
        """
        if key in self.subscribers:
            for sub in self.subscribers[key]:
                if sub not in self.dirty: # Prevent redundant traversals
                    self.dirty.add(sub)
                    self._invalidate_downstream(sub)

    # --- PUBLIC API ---

    def set_value(self, key, val):
        """O(V + E) for invalidation traversal, but O(1) math."""
        # Teardown
        self._clear_old_subscriptions(key)
        if key in self.formulas:
            del self.formulas[key]
        
        # Set new state
        self.values[key] = val
        self.dirty.discard(key) # A static value is inherently clean
        
        # Mark all dependent cells as dirty
        self._invalidate_downstream(key)

    def set_sum(self, key, dependencies):
        """O(V + E) for invalidation traversal, but O(1) math."""
        # Teardown
        self._clear_old_subscriptions(key)
        
        # Build up
        self.formulas[key] = dependencies
        for dep in dependencies:
            if dep not in self.subscribers:
                self.subscribers[dep] = set()
            self.subscribers[dep].add(key)
        
        # Mark THIS cell and all its dependents as dirty
        self.dirty.add(key)
        self._invalidate_downstream(key)

    def get_value(self, key):
        """O(N) for first call on dirty cells, O(1) for subsequent calls."""
        # Only do the heavy lifting if it's a formula AND it's marked as dirty
        if key in self.formulas and key in self.dirty:
            total = 0
            for dep in self.formulas[key]:
                # Recursively fetch values. This ensures upstream dirty cells 
                # are recalculated before we calculate our own value.
                total += self.get_value(dep)
            
            # Cache the computed result and mark as clean
            self.values[key] = total
            self.dirty.remove(key)
            
        return self.values.get(key, 0)
```

---

### The Missing Production Features

In an interview setting, providing the code above is the primary goal. However, mentioning what is *missing* for a true production system shows deep engineering maturity:

**1. Cycle Detection (The Infinite Loop Preventer)**
The constraints of this specific problem guarantee "no circular dependencies." In the real world, a user *will* inevitably set `A = B + C` and then maliciously or accidentally set `C = A`. In eager evaluation, this causes an infinite recursive loop that crashes the stack. In a production system, you would need to run a quick topological sort or a recursive DFS cycle-check during `set_sum` to raise an exception if a cycle is detected *before* saving the formula.

**2. Garbage Collection for Subscribers**
If `A` has an empty subscriber set, it is just sitting in the `self.subscribers` dictionary taking up memory. In a massive spreadsheet, you would occasionally want to prune keys from `self.subscribers` if their `set` length drops to `0`.

**3. DAG Depth Limits**
Python has a default recursion limit (usually 1,000). If you have a spreadsheet where `Cell 1001` depends on `Cell 1000` which depends on `Cell 999` all the way down to `Cell 1`, your `_invalidate_downstream` recursive call will trigger a `RecursionError`. A production system would implement the traversal iteratively using an explicit `while` loop and a stack array instead of relying on the call stack.
