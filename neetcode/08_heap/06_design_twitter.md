### question
Implement a simplified version of Twitter which allows users to post tweets, follow/unfollow each other, and view the 10 most recent tweets within their own news feed.

Users and tweets are uniquely identified by their IDs (integers).

Implement the following methods:

Twitter() Initializes the twitter object.
void postTweet(int userId, int tweetId) Publish a new tweet with ID tweetId by the user userId. You may assume that each tweetId is unique.
List<Integer> getNewsFeed(int userId) Fetches at most the 10 most recent tweet IDs in the user's news feed. Each item must be posted by users who the user is following or by the user themself. Tweets IDs should be ordered from most recent to least recent.
void follow(int followerId, int followeeId) The user with ID followerId follows the user with ID followeeId.
void unfollow(int followerId, int followeeId) The user with ID followerId unfollows the user with ID followeeId.

### 1. Restate

Design a simplified Twitter system. Users can post tweets, follow/unfollow others. Need to generate a news feed of the 10 most recent tweets from the user and their followees, sorted newest to oldest.

### 2. Clarify

* **Input:** Integers for user IDs and tweet IDs.
* **Output:** List of integers (tweet IDs) for the feed.
* **Missing info:** Are tweet IDs sequential/chronological? No guarantee. Need internal logical clock.
* **Self-following:** Can a user follow themselves? System should handle gracefully or ignore.
* **Unfollow:** If A unfollows B, B's past tweets vanish from A's feed? Yes, feed is computed dynamically.

### 3. Example by hand

* `postTweet(1, 5)` -> User 1 has Tweet 5 (time=1).
* `getNewsFeed(1)` -> gets `[5]`.
* `follow(1, 2)` -> User 1 follows User 2.
* `postTweet(2, 6)` -> User 2 has Tweet 6 (time=2).
* `getNewsFeed(1)` -> Check self (User 1: [5]) and followees (User 2: [6]). Sort by time desc. Return `[6, 5]`.
* `unfollow(1, 2)` -> User 1 stops following 2.
* `getNewsFeed(1)` -> Check self. Return `[5]`.

### 4. Brainstorming

* **Option A: Push model.** Each user maintains a pre-computed feed list. On post, push to all followers.
* *Complexity:* Post is O(F) [F = followers]. Feed is O(1). Hard to handle unfollows (requires finding and deleting tweets from feed).


* **Option B: Pull model.** Store tweets per user. On feed request, fetch tweets from self + followees, merge, sort.
* *Complexity:* Post O(1). Feed O(N * T log(N * T)) [N = followees, T = tweets]. Unfollows are trivial (just remove from set).


* **Option C: Pull model + Max-Heap.** Store tweets per user. Fetch *only* last 10 tweets from self + followees. Merge using Heap.
* *Complexity:* Feed O(N log 10) -> O(N).



### 5. Suggest Solutions

Prefer simple, clear implementations. Option B is easiest to explain and code correctly. Gather all tweets from user and followees, sort by internal timestamp, take top 10. Later, we can optimize the sorting step.

### 6. Outline

```python
class Twitter:
    def getNewsFeed(self, userId: int):
        """
        Reframe: Feed is max 10 most recent tweets from user and their followees.
        State: map of user->tweets, map of user->followees, global clock. Chosen because decoupling storage from feed generation makes follows/unfollows trivial.
        Invariant: Tweets in user map are strictly appended in chronological order.

        get_network(userId) = returns set of relevant users (self + followees)
        gather_tweets(users) = returns flat list of all tweets from these users
        sort_and_take_10(tweets) = sorts by time desc, returns top 10 ids

        Core logic:
        - get network of users for the current user
        - gather all tweets posted by this network
        - sort tweets from newest to oldest based on internal clock
        - return just the tweet IDs of the first 10
        Edge cases:
        - user requests feed but has no tweets and follows no one
        - user tries to follow themselves
        - user tries to unfollow themselves
        - user unfollows someone they don't follow
        - fewer than 10 tweets total in the network
        """

```

### 7. Iterative Implementation

**Iteration 1: Skeleton**

```python
class Twitter:
    def __init__(self):
        # TODO: init data structures
        pass

    def postTweet(self, userId: int, tweetId: int) -> None:
        # TODO: save tweet with timestamp
        pass

    def getNewsFeed(self, userId: int) -> List[int]:
        # TODO: use dummy helpers to execute core logic
        pass

    def follow(self, followerId: int, followeeId: int) -> None:
        # TODO: add to follow set
        pass

    def unfollow(self, followerId: int, followeeId: int) -> None:
        # TODO: remove from follow set
        pass

```

**Iteration 2: Core Data Structures & Simple Methods**

```python
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.time = 0 # global clock
        self.tweets = defaultdict(list) # userId -> list of (time, tweetId)
        self.following = defaultdict(set) # userId -> set of followeeIds

    def postTweet(self, userId: int, tweetId: int) -> None:
        # store negative time so default sorting is descending (newest first)
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        # discard used instead of remove to avoid KeyError if not following
        self.following[followerId].discard(followeeId)
        
    def getNewsFeed(self, userId: int) -> list[int]:
        pass # next iteration

```

**Iteration 3: Core Logic for Feed (Plain English mapping)**

```python
    def getNewsFeed(self, userId: int) -> list[int]:
        # get network
        network = self._get_network(userId)
        
        # gather tweets
        all_tweets = self._gather_tweets(network)
        
        # sort and take 10
        return self._sort_and_take_10(all_tweets)

```

**Iteration 4: Implement Helpers (Happy Path realized)**

```python
    def _get_network(self, userId: int) -> set:
        # include followees
        network = set(self.following[userId])
        # include self
        network.add(userId)
        return network

    def _gather_tweets(self, network: set) -> list:
        all_tweets = []
        for user in network:
            all_tweets.extend(self.tweets[user])
        return all_tweets

    def _sort_and_take_10(self, tweets: list) -> list:
        # sort by time descending. Since time increments, larger time = newer.
        tweets.sort(key=lambda x: x[0], reverse=True)
        
        # extract just the IDs, limit to 10
        top_10 = []
        for i in range(min(10, len(tweets))):
            top_10.append(tweets[i][1])
        return top_10

```

**Iteration 5: Edge Cases Walkthrough & Patching**

* *User has no tweets/follows no one:* Handled. Network = `{userId}`, tweets = `[]`, returns `[]`.
* *Fewer than 10 tweets:* Handled by `min(10, len(tweets))`.
* *User follows/unfollows themselves:* If `follow(1, 1)` occurs, it's added to set. Doesn't break `_get_network` since sets hold unique values. But let's patch to prevent useless work.
* *Unfollow someone not followed:* Handled by `set.discard()`.

*Patching `follow` and `unfollow` in final merged code:*

```python
from collections import defaultdict

class Twitter:
    def __init__(self):
        self.time = 0 
        self.tweets = defaultdict(list) 
        self.following = defaultdict(set) 

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def follow(self, followerId: int, followeeId: int) -> None:
        # EDGE CASE PATCH: prevent following self
        if followerId != followeeId:
            self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        # EDGE CASE PATCH: prevent unfollowing self
        if followerId != followeeId:
            self.following[followerId].discard(followeeId)

    def getNewsFeed(self, userId: int) -> list[int]:
        network = self.following[userId].copy() # avoid mutating original
        network.add(userId)
        
        all_tweets = []
        for user in network:
            # OPTIMIZATION: only grab last 10 tweets per user to save memory/sort time
            all_tweets.extend(self.tweets[user][-10:])
            
        all_tweets.sort(key=lambda x: x[0], reverse=True)
        
        return [tweetId for time, tweetId in all_tweets[:10]]

```

### 8. Complexity & Optimization

**Current Complexity:**

* `postTweet`, `follow`, `unfollow`: O(1) time.
* `getNewsFeed`: O(N) where N is number of followees. We extract max 10 tweets per followee, so list size is bounded by 10N. Sorting takes O(10N log(10N)).

**Optimization (K-way Merge / Min-Heap):**
Sorting `10N` elements is slightly wasteful if N is large (e.g., following 1000 people = sorting 10,000 tweets).
Because each user's tweet list is *already sorted* chronologically, this is essentially a "Merge K Sorted Lists" problem. We can use a heap to pull just the top 10 efficiently.

*Alternative heap approach (Python `heapq.nlargest`):*

```python
import heapq

    # Inside getNewsFeed:
    # Instead of pulling all and sorting, yield directly into nlargest
    def getNewsFeed(self, userId: int) -> list[int]:
        network = self.following[userId].copy()
        network.add(userId)
        
        # Generator expression avoids building large intermediate lists
        # heapq.nlargest is O(K log 10) where K is total tweets inspected.
        recent_tweets = heapq.nlargest(
            10, 
            (tweet for user in network for tweet in self.tweets[user][-10:]),
            key=lambda x: x[0]
        )
        return [tweetId for time, tweetId in recent_tweets]

```

This reduces the feed generation space complexity to O(10) [for the heap] and time complexity closer to O(N log 10), which scales much better for users following thousands of accounts.