from dsl import lesson, P, C, TIP, WARN, EX

PART = 2

lesson("p2-shape", PART, "What an MDP looks like in Python",
P("In the exam an MDP is given as `transitions`. It is **a list of lists of lists**, with 3 levels:"),
P("- Level 1, `transitions[s]`: all the **actions** of state `s`\n- Level 2, `transitions[s][a]`: all the **outcomes** of doing action `a` in state `s`\n- Level 3, one outcome: a tuple `(prob, next_state, reward, terminal)`"),
P("Here is the example MDP from the mock test. In **every exercise from now on, `EX` and `STUDY` already exist**, so you can use them without typing them."),
C('''EX = [
    [  # state 0
        [(0.8, 1, 2.0, False), (0.2, 2, 0.0, True)],   # action 0
        [(1.0, 2, 4.0, True)],                          # action 1
    ],
    [  # state 1
        [(1.0, 1, 0.0, True)],                          # action 0
    ],
    [  # state 2
        [(1.0, 2, 0.0, True)],                          # action 0
    ],
]'''),
P("Read state 0, action 0 out loud: *with probability 0.8 we go to state 1 and get reward 2, and the episode goes on; with probability 0.2 we go to state 2, get 0, and the episode ends.*"),
P("Now let's walk down the levels:"),
C('''print(len(EX))          # number of states
print(len(EX[0]))       # number of actions in state 0
print(EX[0][0])         # the outcomes of state 0, action 0
print(EX[0][0][1])      # the second outcome (a tuple)
print(EX[0][0][1][2])   # its reward'''),
TIP("`terminal` belongs to the **outcome**, not to the state. It means: *if this outcome happens, the episode is over, so there is no future value.*"),
P("The second MDP, `STUDY` (γ = 0.9), is used in many exercises:"),
C('''STUDY = [
    # state 0 = L (Lazy)
    [[(1.0, 0, 1.0, False)],                          # a0 Rest:   stay in L, +1
     [(1.0, 1, -1.0, False)]],                        # a1 Study:  go to S, -1
    # state 1 = S (Studying)
    [[(0.5, 2, 20.0, True), (0.5, 1, -1.0, False)],   # a0 Revise: 50% pass +20 (end), 50% stay -1
     [(1.0, 0, 0.0, False)]],                         # a1 Quit:   back to L, 0
    # state 2 = P (Passed)
    [[(1.0, 2, 0.0, True)]],
]'''),
EX("ex-shape-1", "n_states(transitions)",
   "Return the number of states.",
   "def n_states(transitions):\n    pass\n",
   "def n_states(transitions):\n    return len(transitions)\n",
   ["n_states(EX)", "n_states(STUDY)", "n_states([[[(1.0, 0, 0.0, True)]]])"],
   ["Level 1 is a list with one entry per state.", "`return len(transitions)`"]),
EX("ex-shape-2", "outcomes_of(transitions, s, a)",
   "Return the list of outcomes for state `s` and action `a`.",
   "def outcomes_of(transitions, s, a):\n    pass\n",
   "def outcomes_of(transitions, s, a):\n    return transitions[s][a]\n",
   ["outcomes_of(EX, 0, 0)", "outcomes_of(EX, 0, 1)", "outcomes_of(STUDY, 1, 1)"],
   ["Two indexes: first the state, then the action.", "`return transitions[s][a]`"]),
EX("ex-shape-3", "n_outcomes(transitions, s, a)",
   "Return how many outcomes action `a` has in state `s`.",
   "def n_outcomes(transitions, s, a):\n    pass\n",
   "def n_outcomes(transitions, s, a):\n    return len(transitions[s][a])\n",
   ["n_outcomes(EX, 0, 0)", "n_outcomes(EX, 0, 1)", "n_outcomes(STUDY, 1, 0)"],
   ["`len(...)` of the outcomes list.", "`return len(transitions[s][a])`"]),
)

lesson("p2-outcome", PART, "One outcome: 4 values",
P("Take one outcome and unpack it. Always use the same 4 names, in this order:"),
C('''outcome = EX[0][0][0]
prob, next_state, reward, terminal = outcome
print("prob:", prob)
print("next_state:", next_state)
print("reward:", reward)
print("terminal:", terminal)'''),
TIP("Memorise the order: **prob, next_state, reward, terminal**. Say it like a song: *P – S – R – T*."),
EX("ex-out-1", "first_next_state(transitions, s, a)",
   "Return the `next_state` of the **first** outcome of `(s, a)`.",
   "def first_next_state(transitions, s, a):\n    pass\n",
   "def first_next_state(transitions, s, a):\n    prob, next_state, reward, terminal = transitions[s][a][0]\n    return next_state\n",
   ["first_next_state(EX, 0, 0)", "first_next_state(EX, 0, 1)", "first_next_state(STUDY, 0, 0)"],
   ["The first outcome is `transitions[s][a][0]`.", "Unpack it with the 4 names, then return `next_state`."]),
EX("ex-out-2", "is_first_terminal(transitions, s, a)",
   "Return `True` if the first outcome of `(s, a)` is terminal.",
   "def is_first_terminal(transitions, s, a):\n    pass\n",
   "def is_first_terminal(transitions, s, a):\n    prob, next_state, reward, terminal = transitions[s][a][0]\n    return terminal\n",
   ["is_first_terminal(EX, 0, 0)", "is_first_terminal(EX, 0, 1)", "is_first_terminal(STUDY, 1, 0)"],
   ["Same as the last exercise, but return the 4th value.", "`terminal` is already True/False: just return it."]),
)

lesson("p2-one-action", PART, "Loop over the outcomes of one action",
P("Most real tasks look at **all** outcomes of an action. Loop over `transitions[s][a]` and unpack right in the `for` line:"),
C('''for prob, next_state, reward, terminal in EX[0][0]:
    print(prob, next_state, reward, terminal)'''),
P("Now you can compute things over the outcomes, like the total probability:"),
C('''total = 0.0
for prob, next_state, reward, terminal in EX[0][0]:
    total += prob
print(total)'''),
EX("ex-oa-1", "sum_probs(transitions, s, a)",
   "Return the sum of the probabilities of all outcomes of `(s, a)`.",
   "def sum_probs(transitions, s, a):\n    pass\n",
   "def sum_probs(transitions, s, a):\n    total = 0.0\n    for prob, next_state, reward, terminal in transitions[s][a]:\n        total += prob\n    return total\n",
   ["sum_probs(EX, 0, 0)", "sum_probs(STUDY, 1, 0)", "sum_probs([[[(0.5, 0, 1.0, False), (0.3, 0, 0.0, True)]]], 0, 0)"],
   ["Accumulator + the loop from the example.", "Put the example inside a function and use `transitions[s][a]` instead of `EX[0][0]`."]),
EX("ex-oa-2", "next_states(transitions, s, a)",
   "Return a list of the `next_state` of every outcome of `(s, a)`, in order.",
   "def next_states(transitions, s, a):\n    pass\n",
   "def next_states(transitions, s, a):\n    result = []\n    for prob, next_state, reward, terminal in transitions[s][a]:\n        result.append(next_state)\n    return result\n",
   ["next_states(EX, 0, 0)", "next_states(STUDY, 1, 0)", "next_states(STUDY, 0, 1)"],
   ["Empty list + `append` inside the loop.", "`result.append(next_state)`"]),
EX("ex-oa-3", "terminal_prob(transitions, s, a)",
   "Return the total probability of the outcomes of `(s, a)` that are **terminal**.",
   "def terminal_prob(transitions, s, a):\n    pass\n",
   "def terminal_prob(transitions, s, a):\n    total = 0.0\n    for prob, next_state, reward, terminal in transitions[s][a]:\n        if terminal:\n            total += prob\n    return total\n",
   ["terminal_prob(EX, 0, 0)", "terminal_prob(EX, 0, 1)", "terminal_prob(STUDY, 0, 0)", "terminal_prob(STUDY, 1, 0)"],
   ["Like `sum_probs`, but only add when `terminal` is True.", "`if terminal: total += prob`"]),
EX("ex-oa-4", "rewards_of(transitions, s, a)",
   "Return a list of the rewards of all outcomes of `(s, a)`, in order.",
   "def rewards_of(transitions, s, a):\n    pass\n",
   "def rewards_of(transitions, s, a):\n    result = []\n    for prob, next_state, reward, terminal in transitions[s][a]:\n        result.append(reward)\n    return result\n",
   ["rewards_of(EX, 0, 0)", "rewards_of(STUDY, 1, 0)", "rewards_of(EX, 2, 0)"],
   ["Same as `next_states`, but append a different variable.", "`result.append(reward)`"]),
)

lesson("p2-one-state", PART, "Loop over the actions of one state",
P("`transitions[s]` is the list of actions of state `s`. Each action is itself a list of outcomes. Loop over them:"),
C('''for a, outcomes in enumerate(EX[0]):
    print("action", a, "has", len(outcomes), "outcomes")'''),
P("Or loop with `range` when you only need the action number:"),
C('''for a in range(len(STUDY[1])):
    print("action", a, ":", STUDY[1][a])'''),
P("Two loops = actions of one state, then the outcomes of each action:"),
C('''s = 1
for outcomes in STUDY[s]:
    for prob, next_state, reward, terminal in outcomes:
        print("  ->", next_state, "with p =", prob)'''),
EX("ex-os-1", "outcomes_per_action(transitions, s)",
   "Return a list: for each action of state `s`, how many outcomes it has.",
   "def outcomes_per_action(transitions, s):\n    pass\n",
   "def outcomes_per_action(transitions, s):\n    result = []\n    for outcomes in transitions[s]:\n        result.append(len(outcomes))\n    return result\n",
   ["outcomes_per_action(EX, 0)", "outcomes_per_action(STUDY, 1)", "outcomes_per_action(EX, 2)"],
   ["`for outcomes in transitions[s]:`", "Append `len(outcomes)`."]),
EX("ex-os-2", "total_outcomes_in_state(transitions, s)",
   "Return the total number of outcomes over all actions of state `s`.",
   "def total_outcomes_in_state(transitions, s):\n    pass\n",
   "def total_outcomes_in_state(transitions, s):\n    count = 0\n    for outcomes in transitions[s]:\n        for prob, next_state, reward, terminal in outcomes:\n            count += 1\n    return count\n",
   ["total_outcomes_in_state(EX, 0)", "total_outcomes_in_state(STUDY, 1)", "total_outcomes_in_state(STUDY, 2)"],
   ["Two loops: actions, then outcomes.", "`count += 1` in the inner loop. (Adding `len(outcomes)` in one loop also works.)"]),
EX("ex-os-3", "best_reward_action(transitions, s)",
   "Return the index of the action of state `s` with the highest **expected immediate reward** (Σ prob·reward). On a tie, the lowest index.",
   "def best_reward_action(transitions, s):\n    pass\n",
   "def best_reward_action(transitions, s):\n    best_a = 0\n    best_r = None\n    for a in range(len(transitions[s])):\n        r = 0.0\n        for prob, next_state, reward, terminal in transitions[s][a]:\n            r += prob * reward\n        if best_r is None or r > best_r:\n            best_a = a\n            best_r = r\n    return best_a\n",
   ["best_reward_action(EX, 0)", "best_reward_action(STUDY, 0)", "best_reward_action(STUDY, 1)", "best_reward_action(EX, 1)"],
   ["For each action compute its expected reward Σ prob·reward (like `expected_value` in Part 1), then use the argmax pattern.", "Keep `best_a` and `best_r`; update both when `r > best_r` (start `best_r = None`)."]),
)

lesson("p2-triple", PART, "The triple loop: the whole MDP",
P("To look at **every** outcome in the MDP, use three loops. This is **template A**. Almost every mock question is this template plus one small idea."),
C('''for s, actions in enumerate(EX):                          # every state
    for a, outcomes in enumerate(actions):                # every action
        for prob, next_state, reward, terminal in outcomes:   # every outcome
            print("s =", s, "a =", a, "->", next_state, "p =", prob)'''),
P("If you don't need `s` and `a`, drop `enumerate`:"),
C('''count = 0
for actions in EX:
    for outcomes in actions:
        for prob, next_state, reward, terminal in outcomes:
            count += 1
print(count)'''),
TIP("Ask yourself: **is my answer about the whole MDP, about one state, or about one action?** Put the start value (`total = 0`, `found = set()`, ...) at that level of the loops."),
EX("ex-tri-1", "count_outcomes(transitions)",
   "Return the total number of outcomes in the whole MDP.",
   "def count_outcomes(transitions):\n    pass\n",
   "def count_outcomes(transitions):\n    count = 0\n    for actions in transitions:\n        for outcomes in actions:\n            for prob, next_state, reward, terminal in outcomes:\n                count += 1\n    return count\n",
   ["count_outcomes(EX)", "count_outcomes(STUDY)"],
   ["The second example above, inside a function.", "`count = 0` before all loops, `return count` after all loops."]),
EX("ex-tri-2", "min_reward(transitions)",
   "Return the **smallest** reward of any outcome in the MDP.",
   "def min_reward(transitions):\n    pass\n",
   "def min_reward(transitions):\n    best = None\n    for actions in transitions:\n        for outcomes in actions:\n            for prob, next_state, reward, terminal in outcomes:\n                if best is None or reward < best:\n                    best = reward\n    return best\n",
   ["min_reward(EX)", "min_reward(STUDY)"],
   ["The `best = None` pattern, but with `<`.", "`if best is None or reward < best: best = reward` in the innermost loop."]),
EX("ex-tri-3", "states_with_one_action(transitions)",
   "Return the list of states that have exactly **one** action.",
   "def states_with_one_action(transitions):\n    pass\n",
   "def states_with_one_action(transitions):\n    result = []\n    for s, actions in enumerate(transitions):\n        if len(actions) == 1:\n            result.append(s)\n    return result\n",
   ["states_with_one_action(EX)", "states_with_one_action(STUDY)"],
   ["You only need the state level here: `for s, actions in enumerate(transitions):`.", "`if len(actions) == 1: result.append(s)`"]),
EX("ex-tri-4", "terminal_targets(transitions)",
   "Return a sorted list of the unique `next_state`s that appear in a **terminal** outcome anywhere in the MDP.",
   "def terminal_targets(transitions):\n    pass\n",
   "def terminal_targets(transitions):\n    found = set()\n    for actions in transitions:\n        for outcomes in actions:\n            for prob, next_state, reward, terminal in outcomes:\n                if terminal:\n                    found.add(next_state)\n    return sorted(found)\n",
   ["terminal_targets(EX)", "terminal_targets(STUDY)"],
   ["Triple loop + a set.", "`if terminal: found.add(next_state)`, then `return sorted(found)`."]),
)

lesson("p2-mock", PART, "The 5 mock-test questions",
P("You now know everything needed for the real mock test. Try each one yourself. The hints show the idea step by step."),
P("**Discounted return**: G = r₀ + γ·r₁ + γ²·r₂ + ... The first reward gets γ⁰ = 1."),
C('''rewards = [1, 2, 3]
gamma = 0.5
print(1 + 0.5 * 2 + 0.25 * 3)'''),
EX("ex-mock-1", "discounted_return(rewards, gamma)",
   "Return the discounted return of the list `rewards` with discount `gamma`.",
   "def discounted_return(rewards, gamma):\n    pass\n",
   "def discounted_return(rewards, gamma):\n    total = 0.0\n    for i, r in enumerate(rewards):\n        total += (gamma ** i) * r\n    return total\n",
   ["discounted_return([1, 2, 3], 0.5)", "discounted_return([-1, -1, -1, 10], 0.9)", "discounted_return([5], 0.9)", "discounted_return([], 0.9)"],
   ["`enumerate` gives you `i`, the step number, starting at 0.", "`total += (gamma ** i) * r`"]),
EX("ex-mock-2", "valid_mdp(transitions)",
   "Return `True` if, for **every** state and action, the outcome probabilities add up to 1 (within `1e-9`). Otherwise `False`.",
   "def valid_mdp(transitions):\n    pass\n",
   "def valid_mdp(transitions):\n    for actions in transitions:\n        for outcomes in actions:\n            total = 0.0\n            for prob, next_state, reward, terminal in outcomes:\n                total += prob\n            if abs(total - 1.0) > 1e-9:\n                return False\n    return True\n",
   ["valid_mdp(EX)", "valid_mdp(STUDY)", "valid_mdp([[[(0.5, 0, 1.0, False), (0.4, 0, 0.0, True)]]])", "valid_mdp([[[(1.0, 1, 0.0, True)]], [[(0.7, 0, 0.0, False), (0.7, 1, 0.0, True)]]])"],
   ["The sum is about **one action**, so `total = 0.0` goes inside the action loop, before the outcome loop.", "After the outcome loop: `if abs(total - 1.0) > 1e-9: return False`. After all loops: `return True`."]),
EX("ex-mock-3", "count_terminal_outcomes(transitions)",
   "Return how many outcomes in the whole MDP have `terminal == True`.",
   "def count_terminal_outcomes(transitions):\n    pass\n",
   "def count_terminal_outcomes(transitions):\n    count = 0\n    for actions in transitions:\n        for outcomes in actions:\n            for prob, next_state, reward, terminal in outcomes:\n                if terminal:\n                    count += 1\n    return count\n",
   ["count_terminal_outcomes(EX)", "count_terminal_outcomes(STUDY)"],
   ["Triple loop + counter.", "`if terminal: count += 1`"]),
EX("ex-mock-4", "reachable_states(transitions, state)",
   "Return a sorted list (no duplicates) of the states you can reach in **one step** from `state`, using any action, through outcomes with `prob > 0`.",
   "def reachable_states(transitions, state):\n    pass\n",
   "def reachable_states(transitions, state):\n    found = set()\n    for outcomes in transitions[state]:\n        for prob, next_state, reward, terminal in outcomes:\n            if prob > 0:\n                found.add(next_state)\n    return sorted(found)\n",
   ["reachable_states(EX, 0)", "reachable_states(STUDY, 1)", "reachable_states(STUDY, 0)", "reachable_states([[[(0.0, 1, 0.0, False), (1.0, 0, 0.0, False)]], [[(1.0, 1, 0.0, True)]]], 0)"],
   ["Only one state: loop over `transitions[state]` (2 loops, not 3).", "Collect into a `set()`, only when `prob > 0`, and `return sorted(found)`."]),
EX("ex-mock-5", "stochastic_states(transitions)",
   "Return the list of states that have **at least one** action with 2 or more outcomes with `prob > 0`. Each state at most once.",
   "def stochastic_states(transitions):\n    pass\n",
   "def stochastic_states(transitions):\n    result = []\n    for s, actions in enumerate(transitions):\n        for outcomes in actions:\n            positive = 0\n            for prob, next_state, reward, terminal in outcomes:\n                if prob > 0:\n                    positive += 1\n            if positive >= 2:\n                result.append(s)\n                break\n    return result\n",
   ["stochastic_states(EX)", "stochastic_states(STUDY)", "stochastic_states([[[(1.0, 0, 0.0, False)], [(0.5, 0, 0.0, False), (0.5, 0, 1.0, True)]], [[(1.0, 1, 0.0, True), (0.0, 0, 0.0, False)]]])"],
   ["Count positive outcomes **per action** (`positive = 0` inside the action loop).", "When `positive >= 2`: `result.append(s)` then `break` (like `rows_with_negative`)."]),
)
