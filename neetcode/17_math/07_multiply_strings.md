### question
You are given two strings num1 and num2 that represent non-negative integers.

Return the product of num1 and num2 in the form of a string.

Assume that neither num1 nor num2 contain any leading zero, unless they are the number 0 itself.

Note: You can not use any built-in library to convert the inputs directly into integers.

## 1. Restate the problem

We have two strings, `num1` and `num2`, each representing a non-negative integer.

We need return their product as a **string**.

Constraint: we cannot directly do:

```python
int(num1) * int(num2)
```

So we need simulate multiplication manually.

---

## 2. Clarifying questions / assumptions

I would confirm:

1. Are both inputs valid digit strings?
   Assume yes.

2. Can either input be `"0"`?
   Yes.

3. Should output have leading zeroes?
   No. Output should be normal integer string.

4. Can numbers be very large?
   Yes, so we need avoid converting whole string to integer.

---

## 3. Example by hand

Example:

```python
num1 = "123"
num2 = "45"
```

Manual multiplication:

```text
      123
   x   45
   ------
      615   # 123 * 5
     4920   # 123 * 40
   ------
     5535
```

Return:

```python
"5535"
```

---

## 4. Brainstorm solutions

### Solution 1: Convert manually into integer

We could parse each digit and build number:

```python
value = value * 10 + digit
```

Then multiply.

But this still builds full integer. In Python it works because Python integers are arbitrary precision, but interview constraint usually wants us not to rely on integer conversion at all.

So avoid this.

### Solution 2: Repeated addition

Add `num1` to itself `num2` times.

Bad because if `num2` is huge, impossible.

Time would be proportional to numeric value of `num2`, not length.

### Solution 3: Grade-school multiplication

Use the same multiplication we do by hand.

If:

```python
len(num1) = m
len(num2) = n
```

The product can have at most:

```python
m + n
```

digits.

Example:

```text
99 * 99 = 9801
2 digits * 2 digits -> at most 4 digits
```

So create an array of size `m + n`.

Each digit pair contributes to some position in this result array.

This is the clean interview solution.

Time:

```text
O(m * n)
```

Space:

```text
O(m + n)
```

---

## 5. Key idea

For digits at positions:

```python
num1[i]
num2[j]
```

Their product contributes to:

```python
result[i + j + 1]
```

and carry goes to:

```python
result[i + j]
```

Because the result array has length `m + n`.

Example:

```text
num1 = "123"
num2 = "45"

result length = 3 + 2 = 5
```

Index mapping:

```text
          1   2   3
              4   5
result: [0,  0,  0,  0,  0]
index:   0   1   2   3   4
```

The rightmost multiplication contributes near the right side of the result.

---

## 6. Selected implementation outline

```python
def multiply(num1: str, num2: str) -> str:
    """
    Reframe: Simulate grade-school multiplication digit by digit.

    State:
        result array of size len(num1) + len(num2),
        chosen because multiplying an m-digit number by an n-digit number
        produces at most m + n digits.

    Invariant:
        After processing each digit-pair, result holds the partial product
        with carries pushed left.

    charToDigit(ch) = convert one digit character into its numeric value.

    buildString(result) = skip leading zeroes and join digits into final string.

    Core logic:
    - if either number is zero, return "0"
    - create a result array filled with zeroes
    - walk num1 from right to left
    - walk num2 from right to left
    - multiply the two current digits
    - add that product into the correct low position
    - keep the single digit there
    - carry the overflow into the position to its left
    - after all pairs are processed, remove leading zeroes
    - return remaining digits as a string

    Edge cases:
    - one input is "0"
    - product creates one extra leading digit, example "99" * "99"
    - product does not use first slot, example "12" * "3"
    - one-digit by one-digit
    - many carries, example "999" * "999"
    """
```

---

# 7. Iterative implementation

## Iteration 1: skeleton

```python
def multiply(num1: str, num2: str) -> str:
    if is_zero(num1, num2):
        return "0"

    result = make_result_array(num1, num2)

    fill_result_with_products(num1, num2, result)

    return build_answer(result)
```

This reads clearly, but helpers are not implemented yet.

---

## Iteration 2: implement easy helpers

```python
def multiply(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"

    result = [0] * (len(num1) + len(num2))

    fill_result_with_products(num1, num2, result)

    return build_answer(result)


def char_to_digit(ch: str) -> int:
    return ord(ch) - ord("0")


def build_answer(result: list[int]) -> str:
    first_non_zero = 0

    while first_non_zero < len(result) and result[first_non_zero] == 0:
        first_non_zero += 1

    digits = result[first_non_zero:]

    return "".join(str(digit) for digit in digits)
```

Still missing core multiplication.

---

## Iteration 3: implement core multiplication

```python
def multiply(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"

    result = [0] * (len(num1) + len(num2))

    for i in range(len(num1) - 1, -1, -1):
        for j in range(len(num2) - 1, -1, -1):
            digit1 = ord(num1[i]) - ord("0")
            digit2 = ord(num2[j]) - ord("0")

            product = digit1 * digit2

            low_position = i + j + 1
            high_position = i + j

            total = product + result[low_position]

            result[low_position] = total % 10
            result[high_position] += total // 10

    first_non_zero = 0

    while first_non_zero < len(result) and result[first_non_zero] == 0:
        first_non_zero += 1

    return "".join(str(digit) for digit in result[first_non_zero:])
```

This is already mostly complete.

But let’s check edge cases.

---

## 8. Edge case walkthrough

### Edge case 1: one input is `"0"`

```python
num1 = "0"
num2 = "123"
```

Our code returns:

```python
"0"
```

Good.

---

### Edge case 2: product creates full `m + n` digits

```python
num1 = "99"
num2 = "99"
```

Expected:

```python
"9801"
```

Result array length is `4`, exactly enough.

Good.

---

### Edge case 3: product does not use first slot

```python
num1 = "12"
num2 = "3"
```

Result array length is `3`.

Internal result may become:

```python
[0, 3, 6]
```

We skip leading zero and return:

```python
"36"
```

Good.

---

### Edge case 4: one-digit multiplication

```python
num1 = "8"
num2 = "9"
```

Expected:

```python
"72"
```

Result length is `2`.

Good.

---

### Edge case 5: many carries

```python
num1 = "999"
num2 = "999"
```

Expected:

```python
"998001"
```

The carry logic works because every digit-pair pushes overflow left.

Good.

---

# Final implementation

```python
def multiply(num1: str, num2: str) -> str:
    """
    Reframe: Simulate grade-school multiplication digit by digit.

    State:
        result array of size len(num1) + len(num2),
        chosen because multiplying an m-digit number by an n-digit number
        produces at most m + n digits.

    Invariant:
        After each digit-pair multiplication, the partial product is stored
        in result, with carry pushed one position left.

    Core logic:
    - if either number is zero, return "0"
    - create result array with enough room for all product digits
    - multiply every digit in num1 with every digit in num2
    - place the ones digit in the low position
    - add carry into the high position
    - skip leading zeroes
    - return the remaining digits as a string

    Edge cases:
    - one input is "0"
    - output has fewer than len(num1) + len(num2) digits
    - output uses all len(num1) + len(num2) digits
    - one-digit by one-digit
    - many carries
    """

    if num1 == "0" or num2 == "0":
        return "0"

    result = [0] * (len(num1) + len(num2))

    for i in range(len(num1) - 1, -1, -1):
        for j in range(len(num2) - 1, -1, -1):
            digit1 = ord(num1[i]) - ord("0")
            digit2 = ord(num2[j]) - ord("0")

            product = digit1 * digit2

            low_position = i + j + 1
            high_position = i + j

            total = product + result[low_position]

            result[low_position] = total % 10
            result[high_position] += total // 10

    first_non_zero = 0

    while first_non_zero < len(result) and result[first_non_zero] == 0:
        first_non_zero += 1

    return "".join(str(digit) for digit in result[first_non_zero:])
```

## Complexity

Let:

```python
m = len(num1)
n = len(num2)
```

The nested loop multiplies every digit of `num1` with every digit of `num2`.

```text
Time:  O(m * n)
Space: O(m + n)
```

The expensive section is:

```python
for i in range(len(num1) - 1, -1, -1):
    for j in range(len(num2) - 1, -1, -1):
```

That is necessary for grade-school multiplication. For interviews, this is the expected clean solution.
