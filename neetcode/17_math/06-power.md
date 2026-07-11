### question

Pow(x, n) is a mathematical function to calculate the value of x raised to the power of n (i.e., x^n).

Given a floating-point value x and an integer value n, implement the myPow(x, n) function, which calculates x raised to the power n.

You may not use any built-in library functions.


**1. Restating the Question**
Need to implement a custom function to calculate `x` raised to the power of `n` ($x^n$). `x` is a float, `n` is an integer. No built-in math libraries allowed.

**2. Clarifying Questions & I/O Confirmations**

* Can `n` be negative? (Assuming yes, need to handle fractional results).
* Can `n` be zero? (Assuming yes, any non-zero `x` to power 0 is 1).
* Can `x` be zero? (Assuming yes, $0^n = 0$ for positive `n`. If $x=0$ and $n<0$, assume invalid/undefined or return infinity).
* Input: `x = 2.00000`, `n = 10`. Output: `1024.00000`.
* Input: `x = 2.00000`, `n = -2`. Output: `0.25000`.

**3. Example by Hand**
Let `x = 2.0`, `n = 5`.
Naively: $2 \times 2 \times 2 \times 2 \times 2 = 32$.
Smarter:
$2^5 = 2 \times 2^4$
$2^4 = (2^2)^2 = 4^2 = 16$
So $2^5 = 2 \times 16 = 32$.
We skip calculating $2 \times 2 \times 2 \times 2$ linearly by grouping into halves.

**4. Brainstorming & Complexity**

* *Idea 1: Brute Force.* Loop `n` times, multiply `result` by `x`.
*Time: $O(n)$. Space: $O(1)$.*
Bad if `n` is $2^{31}-1$. Will Time Out.
* *Idea 2: Binary Exponentiation (Divide & Conquer).* Break problem in half. $x^n = x^{n/2} \times x^{n/2}$. If `n` is odd, multiply by one more `x`.
*Time: $O(\log n)$. Space: $O(\log n)$ call stack.* Very fast.

**5. Suggested Solutions**
Prefer Idea 2 (Binary Exponentiation). It's mathematically straightforward, avoids timeout on large `n`, and the recursive tree is highly readable. The linear loop (Idea 1) is too slow for interview standards here.

**6. Outline**

```python
def myPow(x: float, n: int) -> float:
    """
    Reframe: Exponentiation can be halved recursively to reduce operations from n to log(n).
    State: current_power, chosen because dividing it by 2 rapidly shrinks the problem size.
    Invariant: the mathematical product of the recursive branches always equals x^n.

    is_even(power) = returns True if power is perfectly divisible by 2.
    compute_half(base, power) = recursively calls myPow for power // 2.

    Core logic:
    - base case: if power is zero, return 1.0.
    - get the result of compute_half for the base and power.
    - square that result (half * half).
    - if the power is NOT is_even, multiply the squared result by the base once more.
    - return the final computed value.

    Edge cases:
    - power is negative: invert the base (1/x) and make power positive, then proceed.
    - integer limits: in some languages, n = -2147483648 becomes overflow if simply negated. Python handles arbitrarily large ints, so no strict overflow here, but logically good to note.
    """

```

**7. Iterative Implementation**

*Iteration 1: Skeleton with dummies*

```python
def myPow(x: float, n: int) -> float:
    # TODO: handle edge cases later (negative n)
    
    # Base case
    if n == 0:
        return 1.0
        
    # Recursive step
    half_pow = compute_half(x, n)  # dummy
    result = half_pow * half_pow
    
    # Odd/Even adjustment
    if not is_even(n):  # dummy
        result = result * x
        
    return result

```

*Iteration 2: Fleshing out core logic (replacing dummies)*

```python
def myPow(x: float, n: int) -> float:
    # Base case
    if n == 0:
        return 1.0
        
    # Replace dummy 'compute_half' with actual recursion
    # Changed: n // 2 effectively halves the power
    half_pow = myPow(x, n // 2) 
    result = half_pow * half_pow
    
    # Replace dummy 'is_even' with modulo operator
    # Changed: check if n % 2 != 0 for odd
    if n % 2 != 0:
        result = result * x
        
    return result

```

*Iteration 3: Walking edge cases and patching code*
Now patching edge cases from the outline (Negative `n`).

```python
def myPow(x: float, n: int) -> float:
    # Patch: handle negative power edge case BEFORE core logic
    if n < 0:
        x = 1 / x
        n = -n
        
    # Core logic remains untouched
    if n == 0:
        return 1.0
        
    half_pow = myPow(x, n // 2)
    result = half_pow * half_pow
    
    if n % 2 != 0:
        result = result * x
        
    return result

```

**8. Complexity & Optimizations**
*Current Complexity:*
Time: $O(\log n)$ due to halving `n`.
Space: $O(\log n)$ due to recursive call stack.

*Optimization:*
To improve Space from $O(\log n)$ to $O(1)$, we convert recursion to iteration.

```python
def myPow(x: float, n: int) -> float:
    if n < 0:
        x = 1 / x
        n = -n
        
    result = 1.0
    current_product = x
    
    while n > 0:
        if n % 2 == 1:
            result = result * current_product
        current_product = current_product * current_product
        n = n // 2
        
    return result

```

*Commentary:* Iterative approach avoids stack overflow and uses purely $O(1)$ auxiliary space while keeping the $O(\log n)$ time efficiency. We just square the `current_product` at every step, and only multiply it into our `result` when the binary representation of `n` has a `1` (which corresponds to `n % 2 == 1`).