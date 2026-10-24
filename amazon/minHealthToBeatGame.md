# question
Minimum Health to Beat Game ([LeetCode 2214](https://leetcode.com/discuss/interview-question/6273626/)): Given an array damage[i] per level and a one-time armor shield that absorbs up to armor damage on a single level, return the minimum starting health $> 0$ needed to survive all levels

# clarifications
1. one time armour shiled, can only be used once; can absorb upto armour damage
2. min starting health to survive all levels
3. death is health <= 0

# ideas
1. for the game to win, they have to survive till the end
   1. if start with a small number they could die at a level before end
   2. they need max damage of a level; with armour max damage - armour shield as starting

# outline
minimumHealth(damage, armour):
    total = totalDamage(damage) # without armour
    saved = bestArmourSaving(damage, armour) # use it at the nastiest level
    return total - saved + 1 # +1 so health is > 0

```python
def minimumHealth(damage: list[int], armour: int) -> int:
    total = sum(damage)
    saved = min(max(damage), armour) # armour can save upto armour or level
    return total - saved + 1
```

# extensions
if there is healing then; only total matters logic will nto hold; 
we need prefix sum approach