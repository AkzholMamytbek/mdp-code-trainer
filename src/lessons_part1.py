from dsl import lesson, P, C, TIP, WARN, EX

PART = 1

lesson("p1-variables", PART, "Variables and maths",
P("A **variable** is a named box that stores a value. You put something in the box with `=`. Later you use the name to get the value back."),
C('''x = 7
y = 2
print(x + y)     # add
print(x - y)     # subtract
print(x * y)     # multiply
print(x / y)     # divide (always gives a float)
print(x ** y)    # power: 7 to the power 2'''),
P("Numbers with a dot, like `0.9` or `2.0`, are called **floats**. Whole numbers like `7` are **ints**. Python mixes them without problems."),
TIP("`**` means *power*. You will use it for the discount: `gamma ** 2` means γ²."),
C('''gamma = 0.9
print(gamma ** 0)   # anything to the power 0 is 1
print(gamma ** 1)
print(gamma ** 2)'''),
P("You can change a variable by giving it a new value. A very common pattern is **adding to what is already there**:"),
C('''total = 0
total = total + 5
total += 3          # short way to write: total = total + 3
print(total)'''),
EX("ex-var-1", "Make three variables",
   "Create a variable `a` with value `5`, a variable `b` with value `3`, and a variable `total` that is `a + b` (use the names, not the number 8).",
   "# write your 3 lines here\n",
   "a = 5\nb = 3\ntotal = a + b\n",
   ["a", "b", "total"],
   ["Each line looks like `name = value`.", "The third line is `total = a + b`."]),
EX("ex-var-2", "Gamma squared",
   "Create `gamma` with value `0.9`. Then create `g2` that is gamma to the power 2 (use `**`).",
   "# gamma = ...\n# g2 = ...\n",
   "gamma = 0.9\ng2 = gamma ** 2\n",
   ["gamma", "g2"],
   ["Power in Python is `**`, not `^`.", "`g2 = gamma ** 2`"]),
EX("ex-var-3", "Running total",
   "Start with `total = 0`. Then, using `+=` three times, add `2`, then `-1`, then `10`. At the end `total` should be 11.",
   "total = 0\n# add 2, then -1, then 10 using +=\n",
   "total = 0\ntotal += 2\ntotal += -1\ntotal += 10\n",
   ["total"],
   ["`total += 2` adds 2 to total.", "Three lines: `total += 2`, `total += -1`, `total += 10`."]),
)

lesson("p1-functions", PART, "Functions and return",
P("A **function** is a small machine: you give it inputs (called **parameters**), it does some work, and it gives back an answer with `return`."),
C('''def add(a, b):        # def + name + (parameters) + colon
    result = a + b    # the body is indented by 4 spaces
    return result     # give the answer back

answer = add(2, 3)    # call the function
print(answer)'''),
P("The rules:\n- The first line is `def name(parameters):` and it **ends with a colon** `:`.\n- Everything inside the function is **indented by 4 spaces**.\n- `return` gives the answer back and **stops the function** immediately."),
WARN("**print is not return!** CodeRunner checks what your function *returns*. `print` only shows text on the screen. A function with no `return` gives back `None`."),
C('''def bad_add(a, b):
    print(a + b)       # shows 5 ... but returns nothing

x = bad_add(2, 3)
print("x is", x)       # x is None!'''),
EX("ex-fn-1", "double(x)",
   "Write a function `double(x)` that **returns** `x` times 2.",
   "def double(x):\n    # your code here\n    pass\n",
   "def double(x):\n    return x * 2\n",
   ["double(4)", "double(-1.5)", "double(0)"],
   ["Replace `pass` with a `return` line.", "`return x * 2`"]),
EX("ex-fn-2", "average_of_two(a, b)",
   "Write `average_of_two(a, b)` that returns the average of the two numbers.",
   "def average_of_two(a, b):\n    pass\n",
   "def average_of_two(a, b):\n    return (a + b) / 2\n",
   ["average_of_two(4, 6)", "average_of_two(1, 2)", "average_of_two(-3, 3)"],
   ["Average = sum divided by 2.", "Use brackets: `(a + b) / 2`. Without them Python does `b / 2` first."]),
EX("ex-fn-3", "discount(reward, gamma, steps)",
   "A reward that arrives `steps` steps in the future is worth `reward * gamma ** steps` today. Write `discount(reward, gamma, steps)` that returns that value.",
   "def discount(reward, gamma, steps):\n    pass\n",
   "def discount(reward, gamma, steps):\n    return reward * gamma ** steps\n",
   ["discount(10, 0.9, 0)", "discount(10, 0.9, 2)", "discount(5, 0.5, 3)"],
   ["Python does `**` before `*`, so you don't need brackets.", "`return reward * gamma ** steps`"]),
)

lesson("p1-if", PART, "if / elif / else",
P("`if` lets your code choose. Python checks the condition; if it is True, the indented block runs."),
C('''def describe(x):
    if x > 0:
        return "positive"
    elif x < 0:          # elif = "else if"
        return "negative"
    else:                # everything else
        return "zero"

print(describe(5))
print(describe(-2))
print(describe(0))'''),
P("Comparisons you can use:\n- `==` equal (two `=` signs!), `!=` not equal\n- `<`, `>`, `<=`, `>=`"),
TIP("`=` **stores** a value. `==` **compares** two values. Mixing them up is the most common beginner bug."),
P("This pattern is exactly what you will use for terminal states in MDPs:"),
C('''terminal = True
V_next = 7.5
if terminal:
    future = 0.0        # the episode ended: no future
else:
    future = V_next
print(future)'''),
P("A shorter one-line version does the same thing:"),
C('''terminal = False
V_next = 7.5
future = 0.0 if terminal else V_next
print(future)'''),
EX("ex-if-1", "sign(x)",
   "Write `sign(x)` that returns the string `\"positive\"`, `\"negative\"` or `\"zero\"`.",
   "def sign(x):\n    pass\n",
   "def sign(x):\n    if x > 0:\n        return \"positive\"\n    elif x < 0:\n        return \"negative\"\n    else:\n        return \"zero\"\n",
   ["sign(3)", "sign(-0.5)", "sign(0)"],
   ["Use `if`, `elif`, `else`, each ending with a colon.", "Copy the shape of `describe` above."]),
EX("ex-if-2", "bigger(a, b)",
   "Write `bigger(a, b)` that returns the larger number **without** using `max`. If they are equal, return `a`.",
   "def bigger(a, b):\n    pass\n",
   "def bigger(a, b):\n    if b > a:\n        return b\n    return a\n",
   ["bigger(3, 8)", "bigger(8, 3)", "bigger(-1, -5)", "bigger(4, 4)"],
   ["Only return `b` when `b` is strictly bigger.", "`if b > a: return b` then on the next line (not inside the if) `return a`."]),
EX("ex-if-3", "future_value(v_next, terminal)",
   "MDP preview! Write `future_value(v_next, terminal)`: if `terminal` is True return `0.0`, otherwise return `v_next`.",
   "def future_value(v_next, terminal):\n    pass\n",
   "def future_value(v_next, terminal):\n    if terminal:\n        return 0.0\n    return v_next\n",
   ["future_value(5.0, False)", "future_value(5.0, True)", "future_value(-2.0, False)"],
   ["`terminal` is already True/False, so you can write `if terminal:` directly.", "`return 0.0 if terminal else v_next` also works."]),
)

lesson("p1-bool", PART, "True, False and comparing floats",
P("Conditions give **booleans**: `True` or `False`. You can combine them with `and`, `or`, `not`."),
C('''p = 0.3
print(p >= 0 and p <= 1)    # both must be True
print(p < 0 or p > 1)       # at least one True
print(not (p > 1))'''),
WARN("Floats are not exact! Computers store 0.1 slightly wrong. So never compare floats with `==`."),
C('''print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)               # False!!
print(abs((0.1 + 0.2) - 0.3) < 1e-9)  # True: "close enough"'''),
P("`abs(x)` is the absolute value (removes the minus). `1e-9` means 0.000000001. So `abs(a - b) < 1e-9` means *a and b are practically equal*. You need this to check that probabilities add up to 1."),
EX("ex-bool-1", "close(a, b)",
   "Write `close(a, b)` that returns `True` if `a` and `b` differ by at most `1e-9`, otherwise `False`.",
   "def close(a, b):\n    pass\n",
   "def close(a, b):\n    return abs(a - b) <= 1e-9\n",
   ["close(0.1 + 0.2, 0.3)", "close(1.0, 1.1)", "close(0.8 + 0.2, 1.0)", "close(5, 5)"],
   ["A comparison is already True/False, so you can return it directly.", "`return abs(a - b) <= 1e-9`"]),
EX("ex-bool-2", "is_valid_prob(p)",
   "Write `is_valid_prob(p)` that returns `True` if `p` is between 0 and 1 (both included).",
   "def is_valid_prob(p):\n    pass\n",
   "def is_valid_prob(p):\n    return p >= 0 and p <= 1\n",
   ["is_valid_prob(0.5)", "is_valid_prob(0)", "is_valid_prob(1)", "is_valid_prob(1.2)", "is_valid_prob(-0.1)"],
   ["Two conditions joined with `and`.", "`return p >= 0 and p <= 1` (Python also allows `0 <= p <= 1`)."]),
)

lesson("p1-lists", PART, "Lists",
P("A **list** keeps many values in order, inside square brackets. Each value has a position called an **index**. Indexes **start at 0**."),
C('''V = [4.0, 6.5, 0.0]
print(V[0])        # first item
print(V[2])        # third item
print(V[-1])       # last item (negative = count from the end)
print(len(V))      # how many items'''),
P("You can change an item, and add new items at the end with `append`:"),
C('''V = [4.0, 6.5, 0.0]
V[1] = 9.9          # replace the item at index 1
V.append(3.3)       # add to the end
print(V)'''),
P("Two tricks you will use **all the time** in MDP code:"),
C('''n = 4
V = [0.0] * n       # a list of n zeros
print(V)

empty = []           # empty list, fill it with append
empty.append(1)
empty.append(2)
print(empty)'''),
WARN("`new = V` does **not** copy a list. Both names point to the *same* list, so changing one changes the other. To copy, write `new = V[:]`, or build a fresh list with `[0.0] * n`."),
C('''V = [1, 2, 3]
same = V          # NOT a copy
copy = V[:]       # a real copy
V[0] = 100
print(same)       # changed too!
print(copy)       # safe'''),
EX("ex-list-1", "first_and_last(lst)",
   "Write `first_and_last(lst)` that returns a **new list** with two items: the first and the last item of `lst`.",
   "def first_and_last(lst):\n    pass\n",
   "def first_and_last(lst):\n    return [lst[0], lst[-1]]\n",
   ["first_and_last([5, 8, 2])", "first_and_last(['a', 'b'])", "first_and_last([7])"],
   ["First is `lst[0]`, last is `lst[-1]`.", "`return [lst[0], lst[-1]]`"]),
EX("ex-list-2", "zeros(n)",
   "Write `zeros(n)` that returns a list of `n` zeros (as floats: `0.0`).",
   "def zeros(n):\n    pass\n",
   "def zeros(n):\n    return [0.0] * n\n",
   ["zeros(3)", "zeros(1)", "zeros(0)"],
   ["Multiply a one-item list.", "`return [0.0] * n`"]),
EX("ex-list-3", "add_item(lst, x)",
   "Write `add_item(lst, x)` that appends `x` to the end of `lst` and returns `lst`.",
   "def add_item(lst, x):\n    pass\n",
   "def add_item(lst, x):\n    lst.append(x)\n    return lst\n",
   ["add_item([1, 2], 3)", "add_item([], 'hi')"],
   ["`lst.append(x)` changes the list but returns None, so return `lst` on the next line.", "Two lines: `lst.append(x)` then `return lst`."]),
)

lesson("p1-for", PART, "for loops over a list",
P("A `for` loop takes the items of a list **one by one**. The indented block runs once for each item."),
C('''rewards = [2, -1, 5]
for r in rewards:
    print("got reward", r)
print("done")      # not indented: runs once, after the loop'''),
P("The most important pattern: the **accumulator**. Make a variable *before* the loop, update it *inside*, use it *after*."),
C('''rewards = [2, -1, 5]
total = 0              # 1. start
for r in rewards:
    total += r         # 2. update for every item
print(total)           # 3. use the result'''),
P("You can also count, or put an `if` inside the loop:"),
C('''probs = [0.8, 0.0, 0.2]
count = 0
for p in probs:
    if p > 0:
        count += 1
print(count)'''),
P("**Early return**: inside a function you can stop as soon as you know the answer. This is exactly how `valid_mdp` works."),
C('''def has_negative(lst):
    for x in lst:
        if x < 0:
            return True     # found one -> stop now
    return False            # loop finished, none found

print(has_negative([3, 1, -2, 5]))
print(has_negative([3, 1]))'''),
WARN("Watch the indentation of the final `return`. If it is inside the loop, the function stops after the first item."),
EX("ex-for-1", "total(lst)",
   "Write `total(lst)` that returns the sum of all numbers in the list. Use a loop (don't use `sum`).",
   "def total(lst):\n    pass\n",
   "def total(lst):\n    t = 0\n    for x in lst:\n        t += x\n    return t\n",
   ["total([1, 2, 3])", "total([2.5, -1])", "total([])"],
   ["Accumulator: start at 0 before the loop.", "`t = 0`, then `for x in lst: t += x`, then `return t` (not indented under the for)."]),
EX("ex-for-2", "count_positive(lst)",
   "Write `count_positive(lst)` that returns how many numbers in the list are greater than 0.",
   "def count_positive(lst):\n    pass\n",
   "def count_positive(lst):\n    count = 0\n    for x in lst:\n        if x > 0:\n            count += 1\n    return count\n",
   ["count_positive([0.8, 0.0, 0.2])", "count_positive([-1, -2])", "count_positive([5, 5, 5])"],
   ["A counter starts at 0 and does `+= 1` when the `if` is True.", "Look at the `probs` example above: it is the same code."]),
EX("ex-for-3", "all_positive(lst)",
   "Write `all_positive(lst)` that returns `True` if every number is greater than 0, otherwise `False`. Use early return.",
   "def all_positive(lst):\n    pass\n",
   "def all_positive(lst):\n    for x in lst:\n        if x <= 0:\n            return False\n    return True\n",
   ["all_positive([1, 2, 3])", "all_positive([1, 0, 3])", "all_positive([-5])", "all_positive([])"],
   ["Look for a 'bad' item. As soon as you find one, `return False`.", "Same shape as `has_negative` above, but the condition is `x <= 0` and the answers are swapped."]),
)

lesson("p1-range", PART, "range and indexes",
P("Sometimes you need the **index** (position), not just the item. `range(n)` gives the numbers `0, 1, ..., n-1`."),
C('''for i in range(4):
    print(i)'''),
C('''V = [4.0, 6.5, 0.0]
for s in range(len(V)):        # s = 0, 1, 2
    print("state", s, "has value", V[s])'''),
P("`range` can also start somewhere else, and even count **backwards**: `range(start, stop, step)`. The stop number is never included."),
C('''print(list(range(2, 5)))          # 2, 3, 4
print(list(range(3, -1, -1)))     # 3, 2, 1, 0  (backwards)'''),
TIP("To walk a list **from the end**: `for t in range(len(lst) - 1, -1, -1):`. You need this to compute returns in RL."),
P("To repeat something k times when you don't need the number, write `_` as the variable name:"),
C('''x = 1
for _ in range(3):
    x = x * 2
print(x)'''),
EX("ex-range-1", "squares(n)",
   "Write `squares(n)` that returns `[0, 1, 4, 9, ...]`: the squares of 0 up to n−1.",
   "def squares(n):\n    pass\n",
   "def squares(n):\n    result = []\n    for i in range(n):\n        result.append(i ** 2)\n    return result\n",
   ["squares(4)", "squares(1)", "squares(0)"],
   ["Start with an empty list and `append` inside a `for i in range(n)` loop.", "`result.append(i ** 2)`"]),
EX("ex-range-2", "powers_of_gamma(gamma, n)",
   "Write `powers_of_gamma(gamma, n)` that returns `[gamma**0, gamma**1, ..., gamma**(n-1)]`.",
   "def powers_of_gamma(gamma, n):\n    pass\n",
   "def powers_of_gamma(gamma, n):\n    result = []\n    for i in range(n):\n        result.append(gamma ** i)\n    return result\n",
   ["powers_of_gamma(0.5, 4)", "powers_of_gamma(0.9, 3)", "powers_of_gamma(0.9, 0)"],
   ["Same as `squares`, but append `gamma ** i`.", "The first power is `gamma ** 0` = 1, so `range(n)` starting at 0 is exactly right."]),
EX("ex-range-3", "reverse_list(lst)",
   "Write `reverse_list(lst)` that returns a new list with the items in reverse order. Use a backwards `range` loop.",
   "def reverse_list(lst):\n    pass\n",
   "def reverse_list(lst):\n    result = []\n    for i in range(len(lst) - 1, -1, -1):\n        result.append(lst[i])\n    return result\n",
   ["reverse_list([1, 2, 3])", "reverse_list(['a'])", "reverse_list([])"],
   ["The last index is `len(lst) - 1`. Go down to 0, so stop at -1.", "`for i in range(len(lst) - 1, -1, -1): result.append(lst[i])`"]),
EX("ex-range-4", "repeat_double(x, k)",
   "Write `repeat_double(x, k)` that doubles `x` exactly `k` times and returns the result (k = 0 means return x unchanged).",
   "def repeat_double(x, k):\n    pass\n",
   "def repeat_double(x, k):\n    for _ in range(k):\n        x = x * 2\n    return x\n",
   ["repeat_double(1, 3)", "repeat_double(5, 0)", "repeat_double(0.5, 1)"],
   ["`for _ in range(k):` repeats k times.", "This is the same loop shape as `value_iteration` with k iterations!"]),
)

lesson("p1-enumerate", PART, "enumerate and finding the best (argmax)",
P("`enumerate` gives you **index and item together**. It is shorter than `range(len(...))`."),
C('''actions = ["up", "down", "left"]
for i, name in enumerate(actions):
    print(i, name)'''),
P("**Argmax** = *the index of the biggest value*. In MDPs this is how you pick the best action. Learn this pattern by heart:"),
C('''Q = [3.0, 7.5, 7.5, 2.0]
best_i = 0
for i in range(1, len(Q)):
    if Q[i] > Q[best_i]:      # strictly bigger
        best_i = i
print(best_i)                 # 1, not 2'''),
TIP("Use `>` and **not** `>=`. With `>` a tie keeps the **first** (lowest) index. Tests usually expect the lowest index."),
P("To find the biggest **value** when numbers can be negative, start with `None`, not 0:"),
C('''values = [-3, -1, -7]
best = None
for v in values:
    if best is None or v > best:
        best = v
print(best)          # -1  (starting at 0 would wrongly give 0)'''),
EX("ex-enum-1", "index_of_max(lst)",
   "Write `index_of_max(lst)` that returns the index of the biggest number. If there is a tie, return the **first** index.",
   "def index_of_max(lst):\n    pass\n",
   "def index_of_max(lst):\n    best_i = 0\n    for i in range(1, len(lst)):\n        if lst[i] > lst[best_i]:\n            best_i = i\n    return best_i\n",
   ["index_of_max([3, 7, 2])", "index_of_max([5, 5, 1])", "index_of_max([-4, -2, -9])", "index_of_max([1, 2, 3, 3])"],
   ["Start with `best_i = 0` and compare every other item with `lst[best_i]`.", "Use `>` (strict) so ties keep the first index."]),
EX("ex-enum-2", "max_value(lst)",
   "Write `max_value(lst)` that returns the biggest number without using `max`. It must work for all-negative lists.",
   "def max_value(lst):\n    pass\n",
   "def max_value(lst):\n    best = None\n    for v in lst:\n        if best is None or v > best:\n            best = v\n    return best\n",
   ["max_value([4, 9, 1])", "max_value([-3, -1, -7])", "max_value([2.5])"],
   ["Start with `best = None`.", "`if best is None or v > best: best = v`"]),
EX("ex-enum-3", "positions_of(lst, target)",
   "Write `positions_of(lst, target)` that returns a list of all indexes where `lst` has the value `target`. Use `enumerate`.",
   "def positions_of(lst, target):\n    pass\n",
   "def positions_of(lst, target):\n    result = []\n    for i, x in enumerate(lst):\n        if x == target:\n            result.append(i)\n    return result\n",
   ["positions_of([1, 2, 1, 3, 1], 1)", "positions_of([5, 6], 9)", "positions_of([], 1)"],
   ["`for i, x in enumerate(lst):` gives index and value.", "Append `i` (the index), not `x`."]),
)

lesson("p1-tuples", PART, "Tuples and unpacking",
P("A **tuple** is like a list, but with round brackets and it cannot be changed. MDP outcomes are tuples of 4 values."),
C('''outcome = (0.8, 1, 2.0, False)
print(outcome[0])     # 0.8
print(outcome[3])     # False
print(len(outcome))'''),
P("**Unpacking** gives every value its own name in one line. This is much easier to read than `outcome[2]`:"),
C('''outcome = (0.8, 1, 2.0, False)
prob, next_state, reward, terminal = outcome
print(prob, next_state, reward, terminal)'''),
P("And the super-useful combination: **unpack directly in the for loop**."),
C('''pairs = [("Ana", 7), ("Bo", 9), ("Cy", 4)]
for name, score in pairs:
    print(name, "scored", score)'''),
C('''# (probability, value) pairs: an expected value
pairs = [(0.5, 10), (0.5, 2)]
expected = 0.0
for p, v in pairs:
    expected += p * v
print(expected)'''),
TIP("The number of names on the left must equal the number of values in the tuple. An MDP outcome has **4**."),
EX("ex-tup-1", "product(pair)",
   "`pair` is a tuple of two numbers. Write `product(pair)` that unpacks it into `a, b` and returns `a * b`.",
   "def product(pair):\n    pass\n",
   "def product(pair):\n    a, b = pair\n    return a * b\n",
   ["product((3, 4))", "product((0.5, 10))", "product((-2, 2))"],
   ["`a, b = pair`", "Then `return a * b`."]),
EX("ex-tup-2", "total_score(pairs)",
   "`pairs` is a list of `(name, score)` tuples. Return the sum of all scores.",
   "def total_score(pairs):\n    pass\n",
   "def total_score(pairs):\n    t = 0\n    for name, score in pairs:\n        t += score\n    return t\n",
   ["total_score([('Ana', 7), ('Bo', 9)])", "total_score([])", "total_score([('X', -1)])"],
   ["`for name, score in pairs:`", "Accumulator: add `score` each time."]),
EX("ex-tup-3", "expected_value(pairs)",
   "`pairs` is a list of `(prob, value)` tuples. Return Σ prob × value. This is the 'expected value' used everywhere in MDPs.",
   "def expected_value(pairs):\n    pass\n",
   "def expected_value(pairs):\n    total = 0.0\n    for p, v in pairs:\n        total += p * v\n    return total\n",
   ["expected_value([(0.5, 10), (0.5, 2)])", "expected_value([(1.0, 4)])", "expected_value([(0.8, 2.0), (0.2, 0.0)])"],
   ["Copy the 'expected' example above into a function.", "`total += p * v` inside the loop."]),
EX("ex-tup-4", "outcome_reward(outcome)",
   "`outcome` is a 4-tuple `(prob, next_state, reward, terminal)`. Unpack it and return the **reward**.",
   "def outcome_reward(outcome):\n    pass\n",
   "def outcome_reward(outcome):\n    prob, next_state, reward, terminal = outcome\n    return reward\n",
   ["outcome_reward((0.8, 1, 2.0, False))", "outcome_reward((1.0, 2, -5.0, True))"],
   ["Four names on the left: `prob, next_state, reward, terminal = outcome`.", "Then `return reward`."]),
)

lesson("p1-nested", PART, "Lists inside lists",
P("A list can contain other lists. Use **two indexes**: the first picks the inner list, the second picks the item inside it."),
C('''grid = [
    [1, 2, 3],     # row 0
    [4, 5],        # row 1  (rows can have different lengths!)
    [6],           # row 2
]
print(grid[0])         # the whole row 0
print(grid[0][2])      # row 0, item 2
print(grid[1][0])
print(len(grid))       # number of rows
print(len(grid[1]))    # length of row 1'''),
P("Read `grid[1][0]` **left to right**: first `grid[1]` is `[4, 5]`, then `[4, 5][0]` is `4`."),
TIP("MDPs are lists inside lists inside lists: `transitions[s][a]`. First pick the state, then the action. Same idea, one level deeper."),
EX("ex-nest-1", "get(grid, r, c)",
   "Write `get(grid, r, c)` that returns the item in row `r`, position `c`.",
   "def get(grid, r, c):\n    pass\n",
   "def get(grid, r, c):\n    return grid[r][c]\n",
   ["get([[1, 2, 3], [4, 5]], 0, 2)", "get([[1, 2, 3], [4, 5]], 1, 0)", "get([[9]], 0, 0)"],
   ["Two brackets, one after the other.", "`return grid[r][c]`"]),
EX("ex-nest-2", "row_lengths(grid)",
   "Write `row_lengths(grid)` that returns a list with the length of each row.",
   "def row_lengths(grid):\n    pass\n",
   "def row_lengths(grid):\n    result = []\n    for row in grid:\n        result.append(len(row))\n    return result\n",
   ["row_lengths([[1, 2, 3], [4, 5], [6]])", "row_lengths([[]])", "row_lengths([])"],
   ["`for row in grid:` gives you each inner list.", "Append `len(row)`."]),
EX("ex-nest-3", "row_sums(grid)",
   "Write `row_sums(grid)` that returns a list with the sum of each row.",
   "def row_sums(grid):\n    pass\n",
   "def row_sums(grid):\n    result = []\n    for row in grid:\n        s = 0\n        for x in row:\n            s += x\n        result.append(s)\n    return result\n",
   ["row_sums([[1, 2, 3], [4, 5], [6]])", "row_sums([[0.8, 0.2], [1.0]])", "row_sums([[]])"],
   ["For each row, run an accumulator. Reset it to 0 **for every row**.", "`s = 0` goes inside the outer loop, before the inner loop."]),
)

lesson("p1-nested-loops", PART, "Loops inside loops",
P("To visit **every** item in a list of lists, put one `for` inside another."),
C('''grid = [[1, 2, 3], [4, 5], [6]]
count = 0
for row in grid:          # outer loop: each row
    for x in row:         # inner loop: each item of that row
        count += 1
print(count)'''),
P("**Where you put the start value decides what you count.** Before both loops = one answer for everything. Inside the outer loop = one answer per row."),
C('''grid = [[1, -2], [3, 4], [-5]]
bad_rows = []
for i, row in enumerate(grid):
    for x in row:
        if x < 0:
            bad_rows.append(i)
            break          # stop the INNER loop: row i is already added
print(bad_rows)'''),
TIP("`break` stops only the loop it is in (the innermost one). Use it to avoid adding the same row twice. This is exactly how `stochastic_states` works."),
EX("ex-nl-1", "count_all(grid)",
   "Write `count_all(grid)` that returns the total number of items in all rows.",
   "def count_all(grid):\n    pass\n",
   "def count_all(grid):\n    count = 0\n    for row in grid:\n        for x in row:\n            count += 1\n    return count\n",
   ["count_all([[1, 2, 3], [4, 5], [6]])", "count_all([[], []])", "count_all([])"],
   ["Copy the first example into a function.", "`count = 0` before both loops; `return count` after both loops."]),
EX("ex-nl-2", "grid_max(grid)",
   "Write `grid_max(grid)` that returns the biggest number anywhere in the grid (numbers may be negative).",
   "def grid_max(grid):\n    pass\n",
   "def grid_max(grid):\n    best = None\n    for row in grid:\n        for x in row:\n            if best is None or x > best:\n                best = x\n    return best\n",
   ["grid_max([[1, 9], [4, 5]])", "grid_max([[-3], [-1, -8]])", "grid_max([[2.5]])"],
   ["Use the `best = None` pattern from the argmax lesson.", "The `if best is None or x > best` goes in the inner loop."]),
EX("ex-nl-3", "rows_with_negative(grid)",
   "Write `rows_with_negative(grid)` that returns the list of row indexes that contain at least one negative number (each index once).",
   "def rows_with_negative(grid):\n    pass\n",
   "def rows_with_negative(grid):\n    result = []\n    for i, row in enumerate(grid):\n        for x in row:\n            if x < 0:\n                result.append(i)\n                break\n    return result\n",
   ["rows_with_negative([[1, -2, -3], [3, 4], [-5]])", "rows_with_negative([[1], [2]])", "rows_with_negative([])"],
   ["`enumerate(grid)` gives you the row index `i`.", "After `result.append(i)` write `break` so the row is not added again."]),
EX("ex-nl-4", "rows_all_positive(grid)",
   "Write `rows_all_positive(grid)` that returns the indexes of rows where **every** number is > 0. (Hint: a flag variable.)",
   "def rows_all_positive(grid):\n    pass\n",
   "def rows_all_positive(grid):\n    result = []\n    for i, row in enumerate(grid):\n        ok = True\n        for x in row:\n            if x <= 0:\n                ok = False\n                break\n        if ok:\n            result.append(i)\n    return result\n",
   ["rows_all_positive([[1, 2], [3, -1], [5]])", "rows_all_positive([[0]])", "rows_all_positive([[1], [2]])"],
   ["For each row: set `ok = True`, then look for a bad number and set `ok = False`.", "After the inner loop (same indentation as the inner `for`): `if ok: result.append(i)`."]),
)

lesson("p1-sets-dicts", PART, "Sets, sorted and dictionaries",
P("A **set** keeps only **unique** values (no duplicates). `sorted(...)` returns a sorted list."),
C('''found = set()
for s in [2, 1, 2, 2, 0]:
    found.add(s)
print(found)
print(sorted(found))      # a sorted LIST'''),
P("A **dictionary** maps a **key** to a **value**: `d[key] = value`. Keys can be numbers, strings or tuples."),
C('''counts = {}
counts["up"] = 3
counts[(0, 1)] = 5        # a tuple as the key
print(counts["up"], counts[(0, 1)])
print(counts.get("down", 0))   # .get(key, default): no crash if missing'''),
P("Counting with a dictionary (you need this to estimate T in model-based RL):"),
C('''counts = {}
for x in ["a", "b", "a", "a"]:
    counts[x] = counts.get(x, 0) + 1
print(counts)'''),
EX("ex-sd-1", "unique_sorted(lst)",
   "Write `unique_sorted(lst)` that returns the unique values of `lst` as a sorted list.",
   "def unique_sorted(lst):\n    pass\n",
   "def unique_sorted(lst):\n    found = set()\n    for x in lst:\n        found.add(x)\n    return sorted(found)\n",
   ["unique_sorted([2, 1, 2, 2, 0])", "unique_sorted([5])", "unique_sorted([])"],
   ["Put every item in a `set()`.", "`return sorted(found)`"]),
EX("ex-sd-2", "count_items(lst)",
   "Write `count_items(lst)` that returns a dictionary: item → how many times it appears.",
   "def count_items(lst):\n    pass\n",
   "def count_items(lst):\n    counts = {}\n    for x in lst:\n        counts[x] = counts.get(x, 0) + 1\n    return counts\n",
   ["count_items(['a', 'b', 'a', 'a'])", "count_items([1, 1])", "count_items([])"],
   ["Start with `counts = {}`.", "`counts[x] = counts.get(x, 0) + 1`"]),
EX("ex-sd-3", "average_by_key(pairs)",
   "`pairs` is a list of `(key, value)`. Return a dict: key → the **average** of its values. (Use two dicts: one for sums, one for counts.)",
   "def average_by_key(pairs):\n    pass\n",
   "def average_by_key(pairs):\n    sums = {}\n    counts = {}\n    for k, v in pairs:\n        sums[k] = sums.get(k, 0) + v\n        counts[k] = counts.get(k, 0) + 1\n    result = {}\n    for k in sums:\n        result[k] = sums[k] / counts[k]\n    return result\n",
   ["average_by_key([('a', 2), ('b', 10), ('a', 4)])", "average_by_key([('x', 5)])", "average_by_key([])"],
   ["First loop: fill `sums` and `counts`. Second loop (`for k in sums:`): divide.", "`result[k] = sums[k] / counts[k]`"]),
)
