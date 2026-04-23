# Interview Walkthrough: Turn-Based Combat Simulator

- **Target Level:** Senior Software Engineer
- **Duration:** 45-60 Minutes
- **Language Chosen:** Python (ideal for readable Object-Oriented Design)

---

## Phase 1: Clarification & Scoping (0-5 Minutes)

**Interviewer Prompt:**
"Design and implement a turn-based combat simulator where two monsters fight until one faints."

**Candidate:**
"Great, this sounds like a classic RPG battle system. Before I write any code, I want to scope this out so we don't over-engineer or miss critical requirements."

### Key Clarification Questions:
1. **Scale:** Is this strictly 1v1, or a team vs. team battle?
2. **Attributes:** What attributes do monsters have? Just HP, or also Attack, Defense, and Speed?
3. **Move Variety:** Are moves purely damage-based, or do we need to support healing, buffs/debuffs, and status effects like Poison?
4. **Turn Order:** How is the turn order decided? Speed stat, or coin flip?

**Interviewer Response:**
"Let's stick to 1v1 for now. Monsters have HP, Attack, Defense, and Speed. Turn order is determined by Speed. For moves, start with basic damage, but design it so we can easily add healing and status effects later."

> **Candidate Thought Process:**
> The interviewer specifically asked for extensibility ("easily add healing and status effects later"). I cannot use a giant if/else block for move logic. I need to use the **Strategy Pattern** for moves.

---

## Phase 2: High-Level Design & Interfaces (5-15 Minutes)

**Candidate:**
"I'll start by defining the core entities and their interfaces. We have three main components:"
- **Monster:** Holds state (stats, current HP).
- **Move (Strategy Pattern):** An interface for actions.
- **BattleEngine:** Manages the game loop and turn order.

### Initial Skeletal Structure

```python
from abc import ABC, abstractmethod

class Move(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, source: 'Monster', target: 'Monster'):
        pass

class Monster:
    def __init__(self, name: str, hp: int, attack: int, defense: int, speed: int, moves: list[Move]):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves

    def is_alive(self) -> bool:
        return self.current_hp > 0

class BattleEngine:
    def __init__(self, m1: Monster, m2: Monster):
        # Sort by speed descending
        self.fighters = sorted([m1, m2], key=lambda x: x.speed, reverse=True)

    def run_battle(self):
        pass
```

**Interviewer:**
"This looks clean. I like the use of the Abstract Base Class for `Move`. How would you implement a basic attack move?"

---

## Phase 3: Core Implementation - MVP (15-25 Minutes)

**Candidate:**
"I'll implement a `DamageMove`. To keep responsibilities clean, the math for damage calculation will live inside the move itself, and the `Monster` class will just have a `take_damage` method to encapsulate its HP state."

### Implementation Updates

```python
# Adding to Monster class
class Monster:
    # ... previous init ...
    def take_damage(self, amount: int):
        self.current_hp = max(0, self.current_hp - amount)
        print(f"{self.name} takes {amount} damage! HP: {self.current_hp}/{self.max_hp}")

# Implementing a concrete Move
class DamageMove(Move):
    def __init__(self, name: str, base_power: int):
        super().__init__(name)
        self.base_power = base_power

    def execute(self, source: Monster, target: Monster):
        # Simple damage formula: Power + (Attacker Atk - Defender Def)
        # Ensure damage is at least 1
        damage = max(1, self.base_power + (source.attack - target.defense))
        print(f"{source.name} uses {self.name}!")
        target.take_damage(damage)

# Implementing the game loop
class BattleEngine:
    # ... init ...
    
    def run_battle(self):
        print(f"Battle starts between {self.fighters[0].name} and {self.fighters[1].name}!")
        turn_number = 1
        
        while self.fighters[0].is_alive() and self.fighters[1].is_alive():
            print(f"\n--- Turn {turn_number} ---")
            for i in range(2):
                attacker = self.fighters[i]
                defender = self.fighters[1 - i]
                
                if not attacker.is_alive():
                    continue # Skip dead monsters
                
                # For simplicity, AI just picks a random move
                import random
                move = random.choice(attacker.moves)
                move.execute(attacker, defender)
                
                if not defender.is_alive():
                    print(f"{defender.name} fainted! {attacker.name} wins!")
                    return attacker
            turn_number += 1
```

**Interviewer:**
"Good. The loop works, and it handles the case where the first monster kills the second one so the second one doesn't get to attack from beyond the grave. Now, let's make it harder. How would you add a 'Poison' status effect that does 5 damage at the end of every turn?"

---

## Phase 4: Iteration & Handling Complexity (25-35 Minutes)

> **Candidate Thought Process:**
> This is the Senior check. I cannot just hack `if self.is_poisoned` into the `BattleEngine`. I need an extensible Status Effect system. Status effects usually trigger at specific phases (start of turn, end of turn).

**Candidate:**
"To support status effects without polluting the `Monster` or `BattleEngine` classes with edge cases, I'll introduce an `Effect` interface. The `Monster` will maintain a list of active effects. The `BattleEngine` will simply notify the monsters when a turn ends, and the monster will process its effects."

### Status Effect Implementation

```python
class Effect(ABC):
    def __init__(self, duration: int):
        self.duration = duration

    @abstractmethod
    def apply_end_of_turn(self, target: 'Monster'):
        pass

class PoisonEffect(Effect):
    def __init__(self, duration: int, damage: int = 5):
        super().__init__(duration)
        self.damage = damage

    def apply_end_of_turn(self, target: 'Monster'):
        print(f"{target.name} is hurt by poison!")
        target.take_damage(self.damage)
        self.duration -= 1

# Refactoring Monster to handle effects
class Monster:
    def __init__(self, ...):
        # ... previous init ...
        self.effects: list[Effect] = []

    def add_effect(self, effect: Effect):
        self.effects.append(effect)
        
    def process_end_of_turn_effects(self):
        for effect in self.effects:
            effect.apply_end_of_turn(self)
        # Remove expired effects
        self.effects = [e for e in self.effects if e.duration > 0]

# Refactoring BattleEngine loop
class BattleEngine:
    # ... 
    def run_battle(self):
        # ... 
        while self.fighters[0].is_alive() and self.fighters[1].is_alive():
            # ... standard turn logic ...
            
            # New phase: End of turn processing
            for fighter in self.fighters:
                if fighter.is_alive():
                    fighter.process_end_of_turn_effects()
                    
            # Check for deaths from poison
            if not self.fighters[0].is_alive() or not self.fighters[1].is_alive():
                break 
```

**Interviewer:**
"Excellent. And how does a monster get poisoned?"

**Candidate:**
"We simply create a new move type: `StatusMove`."

```python
class StatusMove(Move):
    def __init__(self, name: str, effect_factory):
        super().__init__(name)
        self.effect_factory = effect_factory

    def execute(self, source: Monster, target: Monster):
        print(f"{source.name} uses {self.name}!")
        target.add_effect(self.effect_factory())
        print(f"{target.name} was inflicted with a status effect!")

# Usage example:
# poison_powder = StatusMove("Poison Powder", lambda: PoisonEffect(duration=3))
```

---

## Phase 5: Edge Cases & Wrap-Up (35-45 Minutes)

**Interviewer:**
"This architecture is very solid. We have a few minutes left. Let's just talk through some edge cases."

**Tie-Breaking (Same Speed):**
- **Candidate:** "Right now, Python's `sorted` is stable, so whoever was passed as `m1` wins the tie. That's unfair. I would update the sorting logic in `BattleEngine.__init__` to shuffle the list first, or include a random float in the sort key if speeds are equal."

**Infinite Battles (Healing Spam):**
- **Candidate:** "Ah, the infinite battle. We could solve this by implementing a hard turn limit in the `BattleEngine`. If it reaches turn 100, we declare a draw. Alternatively, we could introduce 'Move Points' (PP in Pokemon) or Mana, so they eventually run out of heals and have to use a basic attack."

---

## Key Takeaways

1. **Strategic Scoping:** Never jump straight into coding. 5 minutes of scoping saves 20 minutes of refactoring.
2. **Open/Closed Principle:** The candidate designed `Move` and `Effect` so new mechanics can be added by creating new classes, not by modifying existing engine logic.
3. **Encapsulation:** The `BattleEngine` doesn't subtract numbers from HP directly; it asks the `Monster` to `take_damage()`.
4. **Iterative Delivery:** The candidate built a working MVP first (Phase 3), then added complexity (Phase 4). Interviewers prefer seeing working code early over a "perfect" architecture that never gets implemented.
