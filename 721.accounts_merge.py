"""
given a list of accounts<name, emails>, merge accounts that belong to same person.
while returning, sort the emails


accounts = [
    ["John","johnsmith@mail.com","john_newyork@mail.com"],
    ["John","johnsmith@mail.com","john00@mail.com"],
    ["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]
]
Output: [
    ["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
    ["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]
]
"""

"""
Think of this as a graph relations
1. build a graph
a dictionary key=email, value=list of other emails it's connected to
a email_to_name map

2. find the clusters
iterate through every email w've seen, if we haven't visited it yet, it's a start of a new person
this collection is one merged account

3. sort and format before returning
<name, email1, email2...>
"""

from typing import List


def accounts_merge(accounts: List[List[str]]) -> List[List[str]]:
    from collections import defaultdict

    # 1. build graph
    graph = defaultdict(list)
    email_to_name = {}

    for account in accounts:  # name, email1, email2...
        name = account[0]
        first_email = account[1]

        for email in account[1:]:
            graph[first_email].append(email)
            graph[email].append(first_email)
            email_to_name[email] = name

    # 2. traverse (dfs)
    visited = set()
    result = []

    for email in graph:
        if email not in visited:
            stack = [email]
            visited.add(email)
            current_emails = []

            while stack:
                node = stack.pop()
                current_emails.append(node)

                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)

            # 3. format output
            current_emails.sort()
            result.append([email_to_name[email]] + current_emails)
    return result
