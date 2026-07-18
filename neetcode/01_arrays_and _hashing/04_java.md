### 1. Restate the problem

We are given an array of strings. We need to group strings that are anagrams of one another into separate lists and return all of these lists. An anagram is a word formed by rearranging the letters of another word, using all the original letters exactly once.

Essentially, we need to recognize when two strings have the exact same character frequencies and put them in the same "bucket". The order of the output groups, and the order of strings within those groups, does not matter.

### 2. Ask clarifying questions

Before writing any code, I would want to confirm a few details:

* **Input size:** What is the maximum number of strings, and what is the maximum length of a single string?
* **Character set:** Are all strings composed of only lowercase English letters, or do we need to handle uppercase, numbers, or Unicode characters?
* **Nulls and empties:** Can the input array be null? Can it be empty? Can the strings themselves be empty?
* **Return type:** Should I return a `List<List<String>>`?

*Assumption:* I will assume the input array is not null, but may be empty. The strings consist of lowercase English letters, and empty strings are possible. I will return a `List<List<String>>`.

### 3. Work through an example by hand

Let's trace the standard input: `strs = ["eat", "tea", "tan", "ate", "nat", "bat"]`

To group these, we need a standard way to identify an anagram. If we sort the characters of each string alphabetically, all anagrams will result in the exact same string.

* Process `"eat"` -> sorted is `"aet"`. Create a new bucket for `"aet"`: `["eat"]`
* Process `"tea"` -> sorted is `"aet"`. Add to `"aet"` bucket: `["eat", "tea"]`
* Process `"tan"` -> sorted is `"ant"`. Create a new bucket for `"ant"`: `["tan"]`
* Process `"ate"` -> sorted is `"aet"`. Add to `"aet"` bucket: `["eat", "tea", "ate"]`
* Process `"nat"` -> sorted is `"ant"`. Add to `"ant"` bucket: `["tan", "nat"]`
* Process `"bat"` -> sorted is `"abt"`. Create a new bucket for `"abt"`: `["bat"]`

Final Result: `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`

### 4. Brainstorm solutions aloud

**Approach 1: Brute Force**
I could compare every string against every other string to see if they are anagrams (by comparing character frequency counts). This would take O(N²) comparisons, which is highly inefficient and unnecessary.

**Approach 2: Sort and Map**
As I did in the manual example, I can use a `HashMap`. The key will be the alphabetically sorted version of the string, and the value will be a `List` of the original strings.

* **Time Complexity:** For `N` strings of maximum length `K`, sorting each string takes O(K log K). Doing this for all `N` strings takes O(N * K log K).
* **Space Complexity:** O(N * K) to store the map keys and the lists of strings.

**Approach 3: Character Count Array and Map**
If the strings are exceptionally long, sorting them might become a bottleneck. Since we know the input consists of lowercase English letters, we can create an integer array of size 26 to count character frequencies. We can then convert this array into a String (e.g., `"1#0#0...3#"`) and use *that* as the map key.

* **Time Complexity:** O(N * K) because counting characters takes linear time relative to string length.
* **Space Complexity:** O(N * K).

### 5. Select the solution

I will choose **Approach 2 (Sort and Map)**. While Approach 3 is technically faster for very long strings by avoiding the O(K log K) sort, words are generally short. Approach 2 is much easier to read, explain, and implement without introducing custom delimiter parsing or manual array-to-string conversions. It heavily leverages standard Java features and perfectly fits the requirement of "clear code over clever code".

### 6. Write the implementation outline

```java
List<List<String>> groupAnagrams(String[] strs) {
    /*
     * Reframe:
     * Transform each string into a consistent signature (sorted characters) 
     * and group strings with the same signature.
     *
     * State:
     * Map from a String (the sorted signature) to a List of Strings (the original anagrams).
     * Chosen because HashMaps provide expected O(1) grouping once the key is known.
     *
     * Invariant:
     * After processing index `i`, the map contains correct groupings for all strings
     * from index 0 to `i`.
     *
     * Helpers:
     * getSignature(String s)
     * - takes a string, sorts its characters, and returns the sorted string
     *
     * Core logic:
     * - create a HashMap to store the groupings
     * - iterate through each string in the input array
     * - get the sorted signature for the current string
     * - append the original string to the list associated with that signature
     * - return all the values in the map as a new list
     *
     * Edge cases:
     * - empty input array (should return an empty list)
     * - strings that are empty ("" -> signature is "")
     */
}

```

### 7. Implement iteratively

**Iteration 1: Method skeleton**
I will set up the map, the main loop, and the return statement.

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();

    for (String current : strs) {
        // TODO: get sorted signature
        // TODO: add 'current' to the correct group in the map
    }

    return new ArrayList<>(groups.values());
}

```

*Notice:* I chose to use `current` instead of iterating by index because I don't need the index for anything. `new ArrayList<>(groups.values())` is a clean standard-library way to convert map values directly to the expected return type.

**Iteration 2: Adding the helper**
Now I will implement the logic to get the canonical signature of a string. I'll put this in a private helper method to keep the main loop readable.

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();

    for (String current : strs) {
        String signature = getSignature(current);
        
        // TODO: add 'current' to the correct group in the map
    }

    return new ArrayList<>(groups.values());
}

// Added: Helper to abstract away the character array manipulation
private String getSignature(String s) {
    char[] chars = s.toCharArray();
    Arrays.sort(chars);
    return new String(chars);
}

```

**Iteration 3: Complete the happy path**
Now I will use `computeIfAbsent` to cleanly initialize lists for new signatures and add the current string.

```java
public List<List<String>> groupAnagrams(String[] strs) {
    Map<String, List<String>> groups = new HashMap<>();

    for (String current : strs) {
        String signature = getSignature(current);
        
        // Added: Retrieve the list for this signature, creating it if it doesn't exist.
        groups.computeIfAbsent(signature, k -> new ArrayList<>()).add(current);
    }

    return new ArrayList<>(groups.values());
}

private String getSignature(String s) {
    char[] chars = s.toCharArray();
    Arrays.sort(chars);
    return new String(chars);
}

```

**Edge-case pass**
Let's check the edge cases identified earlier:

* *Empty array:* If `strs = []`, the loop doesn't run, `groups` is empty, and `new ArrayList<>(groups.values())` returns `[]`. This is correct.
* *Empty string:* If `strs = [""]`, `getSignature("")` returns `""`. The map creates a key `""` with the list `[""]`. Returns `[[""]]`. This is correct.
* *Duplicates:* If `strs = ["a", "a"]`, it adds `"a"` to the list twice. Returns `[["a", "a"]]`. This is correct.

No patches are required for these edge cases.

### 8. Analyze expensive sections and optimize

* **Time Complexity:** Let N be the number of strings and K be the maximum length of a string. We iterate N times. Inside the loop, we call `getSignature`, which takes `O(K log K)` to sort the character array. String creation and hash map insertion take `O(K)`. The total time complexity is **O(N * K log K)**.
* **Space Complexity:** The map stores N strings, and the keys are newly allocated strings taking up to K space each. The total space complexity is **O(N * K)**.

The `Arrays.sort` inside the loop is the most expensive operation. As discussed in the brainstorming phase, this is optimal for general use cases where word length is relatively small. I won't change this to a counting sort array unless specifically requested to handle extremely long strings, as sorting provides much better readability.

### Final Code

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> groups = new HashMap<>();

        for (String current : strs) {
            String signature = getSignature(current);
            groups.computeIfAbsent(signature, k -> new ArrayList<>()).add(current);
        }

        return new ArrayList<>(groups.values());
    }

    private String getSignature(String s) {
        char[] chars = s.toCharArray();
        Arrays.sort(chars);
        return new String(chars);
    }
}

```

### Brief test walkthrough

Let's run a test targeting empty strings, which can sometimes trip up string manipulation logic.

**Input:** `strs = ["", "b", ""]`

1. **Init:** `groups` is an empty HashMap.
2. **First element (`""`):**
* `getSignature("")` creates an empty `char[]`, sorts it, and returns `""`.
* `computeIfAbsent` puts key `""` with value `[]` in the map, then adds `""`. Map: `{ "": [""] }`.


3. **Second element (`"b"`):**
* `getSignature("b")` returns `"b"`.
* `computeIfAbsent` puts key `"b"` with value `[]`, then adds `"b"`. Map: `{ "": [""], "b": ["b"] }`.


4. **Third element (`""`):**
* `getSignature("")` returns `""`.
* `computeIfAbsent` finds key `""`. It retrieves the existing list and appends `""`. Map: `{ "": ["", ""], "b": ["b"] }`.


5. **Return:** Returns `[["", ""], ["b"]]`.

This exactly matches the expected output. The code safely handles missing lengths, multiple empty strings, and creates distinct groups properly.