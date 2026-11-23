from dsl import lesson, P, C, TIP, WARN, EX

PART = 3

QV = '''def q_value(transitions, V, s, a, gamma):
    total = 0.0
    for prob, next_state, reward, terminal in transitions[s][a]:
        future = 0.0 if terminal else V[next_state]
        total += prob * (reward + gamma * future)
    return total
'''

lesson("p3-outcome-value", PART, "The Bellman piece for one outcome",
P("Every MDP formula is built from one small piece. For **one outcome**:"),
P("**prob × ( reward + γ × V(next_state) )**, and if the outcome is terminal, V(next_state) is replaced by **0**."),
P("In words: *the reward now, plus the discounted value of the place where I land, weighted by how likely this outcome is.*"),
C('''V = [10.0, 9.0, 0.0]
gamma = 0.9
prob, next_state, reward, terminal = (0.5, 1, -1.0, False)
future = 0.0 if terminal else V[next_state]
print(prob * (reward + gamma * future))     # 0.5 * (-1 + 0.9 * 9)'''),
WARN("Use **V of next_state** (where you land), never V of the state you are in. This is the most common mistake when solving by hand."),
EX("ex-ov-1", "outcome_value(prob, next_state, reward, terminal, V, gamma)",
   "Return `prob * (reward + gamma * future)`, where `future` is `0.0` if `terminal`, otherwise `V[next_state]`.",
   "def outcome_value(prob, next_state, reward, terminal, V, gamma):\n    pass\n",
   "def outcome_value(prob, next_state, reward, terminal, V, gamma):\n    future = 0.0 if terminal else V[next_state]\n    return prob * (reward + gamma * future)\n",
   ["outcome_value(0.5, 1, -1.0, False, [10.0, 9.0, 0.0], 0.9)",
    "outcome_value(0.5, 2, 20.0, True, [10.0, 9.0, 5.0], 0.9)",
    "outcome_value(1.0, 0, 1.0, False, [10.0, 9.0, 0.0], 0.9)"],
   ["First compute `future` with an if (or the one-line `0.0 if terminal else V[next_state]`).", "Then `return prob * (reward + gamma * future)`."]),
)

lesson("p3-q", PART, "Q-value: how good is action a in state s?",
P("Q(s, a) = the sum of the outcome pieces over **all outcomes** of `(s, a)`. It is the expected value of doing `a` in `s` and then having value `V` afterwards."),
P("Q(s,a) = Σ prob × ( reward + γ × V(s′) ),   with V(s′) = 0 for terminal outcomes."),
P("Example by hand, STUDY, V = (10, 9, 0), γ = 0.9, state 1, action 0 (Revise):\n- outcome 1: 0.5 × (20 + 0) = 10 (terminal, so no future)\n- outcome 2: 0.5 × (−1 + 0.9 × 9) = 3.55\n- Q = 13.55"),
C(QV + '''
print(q_value(STUDY, [10.0, 9.0, 0.0], 1, 0, 0.9))
print(q_value(STUDY, [10.0, 9.0, 0.0], 0, 0, 0.9))
print(q_value(EX, [0.0, 0.0, 0.0], 0, 0, 0.9))'''),
TIP("**This is the heart of the whole MDP topic.** Value iteration = max of Q. Policy evaluation = Q of the policy's action. Policy extraction = argmax of Q. Learn `q_value` by heart."),
EX("ex-q-1", "q_value(transitions, V, s, a, gamma)",
   "Write `q_value` yourself (don't copy, type it!).",
   "def q_value(transitions, V, s, a, gamma):\n    pass\n",
   QV,
   ["q_value(STUDY, [10.0, 9.0, 0.0], 1, 0, 0.9)", "q_value(STUDY, [10.0, 9.0, 0.0], 1, 1, 0.9)",
    "q_value(EX, [0.0, 0.0, 0.0], 0, 0, 0.9)", "q_value(EX, [0.0, 5.0, 7.0], 0, 0, 0.5)", "q_value(STUDY, [0.0, 0.0, 0.0], 0, 1, 0.9)"],
   ["Accumulator over `transitions[s][a]` + the outcome piece from the last lesson.", "Inside the loop: `future = 0.0 if terminal else V[next_state]` and `total += prob * (reward + gamma * future)`."]),
EX("ex-q-2", "q_table(transitions, V, gamma)",
   "Return a list of lists: `table[s][a]` = Q(s, a). `q_value` is already given in the box.",
   QV + "\ndef q_table(transitions, V, gamma):\n    pass\n",
   QV + "\ndef q_table(transitions, V, gamma):\n    table = []\n    for s in range(len(transitions)):\n        row = []\n        for a in range(len(transitions[s])):\n            row.append(q_value(transitions, V, s, a, gamma))\n        table.append(row)\n    return table\n",
   ["q_table(STUDY, [10.0, 9.0, 0.0], 0.9)", "q_table(EX, [0.0, 0.0, 0.0], 0.9)"],
   ["Outer loop over states builds one `row` per state; inner loop over actions appends Q values.", "`row = []` goes inside the state loop; `table.append(row)` after the action loop."]),
)

lesson("p3-backup", PART, "Bellman backup: the best Q",
P("The **Bellman update** for one state: try every action, take the **largest** Q."),
P("V_new(s) = max over a of Q(s, a)"),
C(QV + '''
V = [10.0, 9.0, 0.0]
for a in range(len(STUDY[0])):
    print("Q(L, a=%d) =" % a, q_value(STUDY, V, 0, a, 0.9))'''),
P("So V_new(L) = max(10.0, 7.1) = 10.0."),
TIP("Start the best value with `None` (or `float('-inf')`), not 0: all Q values can be negative."),
EX("ex-bb-1", "bellman_backup(transitions, V, s, gamma)",
   "Return the maximum Q(s, a) over all actions `a` of state `s`. `q_value` is given.",
   QV + "\ndef bellman_backup(transitions, V, s, gamma):\n    pass\n",
   QV + "\ndef bellman_backup(transitions, V, s, gamma):\n    best = None\n    for a in range(len(transitions[s])):\n        q = q_value(transitions, V, s, a, gamma)\n        if best is None or q > best:\n            best = q\n    return best\n",
   ["bellman_backup(STUDY, [10.0, 9.0, 0.0], 0, 0.9)", "bellman_backup(STUDY, [10.0, 9.0, 0.0], 1, 0.9)",
    "bellman_backup(EX, [0.0, 0.0, 0.0], 0, 0.9)", "bellman_backup([[[(1.0, 0, -5.0, True)], [(1.0, 0, -2.0, True)]]], [0.0], 0, 0.9)"],
   ["Loop `for a in range(len(transitions[s]))`, compute `q` with `q_value`, keep the max.", "`if best is None or q > best: best = q`"]),
EX("ex-bb-2", "best_action(transitions, V, s, gamma)",
   "Return the **action index** with the largest Q(s, a). Ties → lowest index. `q_value` is given.",
   QV + "\ndef best_action(transitions, V, s, gamma):\n    pass\n",
   QV + "\ndef best_action(transitions, V, s, gamma):\n    best_a = 0\n    best_q = None\n    for a in range(len(transitions[s])):\n        q = q_value(transitions, V, s, a, gamma)\n        if best_q is None or q > best_q:\n            best_a = a\n            best_q = q\n    return best_a\n",
   ["best_action(STUDY, [10.0, 9.0, 0.0], 0, 0.9)", "best_action(STUDY, [14.5, 17.3, 0.0], 0, 0.9)",
    "best_action(EX, [0.0, 0.0, 0.0], 0, 0.9)", "best_action([[[(1.0, 0, 1.0, True)], [(1.0, 0, 1.0, True)]]], [0.0], 0, 0.9)"],
   ["Same as `bellman_backup`, but also remember `best_a`.", "Update both `best_a = a` and `best_q = q` inside the if. Use `>` so ties keep the first action."]),
)

lesson("p3-sweep", PART, "One sweep over all states (batch update)",
P("One iteration of value iteration updates **every** state. The rule from the lectures: V_{k+1} is computed **only from V_k**. So we build a **new list** and only replace V at the end."),
C(QV + '''
V = [0.0, 0.0, 0.0]          # V_0
new_V = [0.0] * len(V)
for s in range(len(STUDY)):
    best = None
    for a in range(len(STUDY[s])):
        q = q_value(STUDY, V, s, a, 0.9)   # uses the OLD V
        if best is None or q > best:
            best = q
    new_V[s] = best
print(new_V)                 # V_1'''),
WARN("Do **not** write the new value straight into `V[s]`. Then state 1 would already see the new value of state 0, which is a different algorithm, and the tests won't match."),
EX("ex-sw-1", "vi_sweep(transitions, V, gamma)",
   "Return a **new list** with the Bellman backup of every state, computed from `V`. Do not change `V` itself. `q_value` is given.",
   QV + "\ndef vi_sweep(transitions, V, gamma):\n    pass\n",
   QV + "\ndef vi_sweep(transitions, V, gamma):\n    new_V = [0.0] * len(transitions)\n    for s in range(len(transitions)):\n        best = None\n        for a in range(len(transitions[s])):\n            q = q_value(transitions, V, s, a, gamma)\n            if best is None or q > best:\n                best = q\n        new_V[s] = best\n    return new_V\n",
   ["vi_sweep(STUDY, [0.0, 0.0, 0.0], 0.9)", "vi_sweep(STUDY, [1.0, 9.5, 0.0], 0.9)",
    "(lambda V: (vi_sweep(STUDY, V, 0.9), V))([1.0, 9.5, 0.0])", "vi_sweep(STUDY, [30.0, 0.0, 0.0], 0.9)", "vi_sweep(EX, [0.0, 0.0, 0.0], 0.9)"],
   ["Make `new_V = [0.0] * len(transitions)` first. Fill `new_V[s]`, read only from `V`.", "The example above is the answer; put it in a function and return `new_V`. (The 3rd test checks that `V` was not changed.)"]),
)

lesson("p3-vi", PART, "Value iteration: repeat the sweep k times",
P("Value iteration = start with all zeros (V_0) and do the sweep **k times**. V_k is the best value with k steps left."),
P("Trace on STUDY, γ = 0.9:\n- V_0 = (0, 0, 0)\n- V_1 = (1, 9.5, 0)\n- V_2 = (7.55, 13.775, 0)\n- ... it converges to (14.55, 17.27, 0)"),
C(QV + '''
def vi_sweep(transitions, V, gamma):
    new_V = [0.0] * len(transitions)
    for s in range(len(transitions)):
        best = None
        for a in range(len(transitions[s])):
            q = q_value(transitions, V, s, a, gamma)
            if best is None or q > best:
                best = q
        new_V[s] = best
    return new_V

V = [0.0, 0.0, 0.0]
for k in range(1, 4):
    V = vi_sweep(STUDY, V, 0.9)
    print("V_%d =" % k, V)'''),
TIP("Check yourself: with k = 0 you must get all zeros back. `range(k)` runs exactly k times."),
EX("ex-vi-1", "value_iteration(transitions, gamma, k)",
   "Start from V = all zeros, apply the sweep `k` times, return V. `q_value` is given. You may write the sweep inside, or write a helper.",
   QV + "\ndef value_iteration(transitions, gamma, k):\n    pass\n",
   QV + "\ndef value_iteration(transitions, gamma, k):\n    n = len(transitions)\n    V = [0.0] * n\n    for _ in range(k):\n        new_V = [0.0] * n\n        for s in range(n):\n            best = None\n            for a in range(len(transitions[s])):\n                q = q_value(transitions, V, s, a, gamma)\n                if best is None or q > best:\n                    best = q\n            new_V[s] = best\n        V = new_V\n    return V\n",
   ["value_iteration(STUDY, 0.9, 0)", "value_iteration(STUDY, 0.9, 1)", "value_iteration(STUDY, 0.9, 2)",
    "value_iteration(STUDY, 0.9, 3)", "value_iteration(EX, 0.9, 2)", "value_iteration(STUDY, 0.9, 200)"],
   ["Structure: `V = [0.0] * n`, then `for _ in range(k):` containing the whole sweep, then `V = new_V` at the end of each iteration.", "`V = new_V` is inside the `for _` loop but after the `for s` loop."]),
EX("ex-vi-2", "value_iteration_until(transitions, gamma, theta)",
   "Challenge: repeat sweeps until the biggest change `max |new_V[s] − V[s]|` is **smaller than** `theta`, then return the new V. `q_value` is given.",
   QV + "\ndef value_iteration_until(transitions, gamma, theta):\n    pass\n",
   QV + "\ndef value_iteration_until(transitions, gamma, theta):\n    n = len(transitions)\n    V = [0.0] * n\n    while True:\n        new_V = [0.0] * n\n        for s in range(n):\n            best = None\n            for a in range(len(transitions[s])):\n                q = q_value(transitions, V, s, a, gamma)\n                if best is None or q > best:\n                    best = q\n            new_V[s] = best\n        delta = 0.0\n        for s in range(n):\n            delta = max(delta, abs(new_V[s] - V[s]))\n        V = new_V\n        if delta < theta:\n            return V\n",
   ["value_iteration_until(STUDY, 0.9, 1e-10)", "value_iteration_until(EX, 0.9, 1e-10)"],
   ["Use `while True:` and `return V` when the change is small enough.", "After each sweep: `delta = max(abs(new_V[s] - V[s]) for s in range(n))`, then `V = new_V`, then `if delta < theta: return V`."]),
)

lesson("p3-policy", PART, "Policy extraction: the best action in every state",
P("A **policy** is a list: `policy[s]` = the action to take in state `s`. Policy extraction builds it from V: in every state pick the action with the biggest Q (argmax)."),
C(QV + '''
V = [10.0, 9.0, 0.0]
policy = []
for s in range(len(STUDY)):
    qs = [q_value(STUDY, V, s, a, 0.9) for a in range(len(STUDY[s]))]
    print("state", s, "Q values:", qs)
    best_a = 0
    for a in range(1, len(qs)):
        if qs[a] > qs[best_a]:
            best_a = a
    policy.append(best_a)
print(policy)'''),
TIP("Compare Q values **within the same state only**. In state L you compare Q(L, Rest) with Q(L, Study), never with a Q of another state."),
EX("ex-pol-1", "greedy_policy(transitions, V, gamma)",
   "Return the list of best actions (lowest index on a tie). `q_value` is given.",
   QV + "\ndef greedy_policy(transitions, V, gamma):\n    pass\n",
   QV + "\ndef greedy_policy(transitions, V, gamma):\n    policy = []\n    for s in range(len(transitions)):\n        best_a = 0\n        best_q = None\n        for a in range(len(transitions[s])):\n            q = q_value(transitions, V, s, a, gamma)\n            if best_q is None or q > best_q:\n                best_a = a\n                best_q = q\n        policy.append(best_a)\n    return policy\n",
   ["greedy_policy(STUDY, [10.0, 9.0, 0.0], 0.9)", "greedy_policy(STUDY, [7.55, 13.775, 0.0], 0.9)",
    "greedy_policy(STUDY, [0.0, 0.0, 0.0], 0.9)", "greedy_policy(EX, [0.0, 0.0, 0.0], 0.9)"],
   ["For each state, run the `best_action` code from the Bellman lesson and append the result.", "`best_a = 0` and `best_q = None` must be reset **inside** the state loop."]),
)

lesson("p3-pe", PART, "Policy evaluation: value of a FIXED policy",
P("Policy evaluation answers: *if I always follow this policy, what is each state worth?* It is value iteration **without the max**: each state uses only the action `policy[s]`."),
P("V_{k+1}(s) = Q_k(s, policy[s])"),
P("Trace, STUDY, policy = [1, 0, 0] (Study, Revise), γ = 0.9:\n- V_1 = (−1, 9.5, 0)\n- V_2 = (−1 + 0.9·9.5, 10 + 0.5·(−1 + 0.9·9.5), 0) = (7.55, 13.775, 0)"),
C(QV + '''
policy = [1, 0, 0]
V = [0.0, 0.0, 0.0]
for k in range(2):
    new_V = [0.0] * 3
    for s in range(3):
        new_V[s] = q_value(STUDY, V, s, policy[s], 0.9)   # no max!
    V = new_V
    print(V)'''),
EX("ex-pe-1", "policy_evaluation(transitions, policy, gamma, k)",
   "Start from zeros, do `k` sweeps where each state uses only `policy[s]`, return V. `q_value` is given.",
   QV + "\ndef policy_evaluation(transitions, policy, gamma, k):\n    pass\n",
   QV + "\ndef policy_evaluation(transitions, policy, gamma, k):\n    n = len(transitions)\n    V = [0.0] * n\n    for _ in range(k):\n        new_V = [0.0] * n\n        for s in range(n):\n            new_V[s] = q_value(transitions, V, s, policy[s], gamma)\n        V = new_V\n    return V\n",
   ["policy_evaluation(STUDY, [1, 0, 0], 0.9, 1)", "policy_evaluation(STUDY, [1, 0, 0], 0.9, 2)",
    "policy_evaluation(STUDY, [0, 1, 0], 0.9, 2)", "policy_evaluation(STUDY, [0, 1, 0], 0.9, 300)", "policy_evaluation(EX, [1, 0, 0], 0.9, 3)"],
   ["Copy your `value_iteration`, delete the action loop and the max.", "`new_V[s] = q_value(transitions, V, s, policy[s], gamma)`"]),
EX("ex-pe-2", "policy_iteration(transitions, gamma)",
   "Challenge: start with policy all zeros. Repeat: evaluate it (use 500 sweeps of policy evaluation), then extract the greedy policy. Stop when the policy does not change and return `(policy, V)`. `q_value` is given.",
   QV + "\ndef policy_iteration(transitions, gamma):\n    pass\n",
   QV + '''
def policy_iteration(transitions, gamma):
    n = len(transitions)
    policy = [0] * n
    while True:
        V = [0.0] * n
        for _ in range(500):
            new_V = [0.0] * n
            for s in range(n):
                new_V[s] = q_value(transitions, V, s, policy[s], gamma)
            V = new_V
        new_policy = []
        for s in range(n):
            best_a, best_q = 0, None
            for a in range(len(transitions[s])):
                q = q_value(transitions, V, s, a, gamma)
                if best_q is None or q > best_q:
                    best_a, best_q = a, q
            new_policy.append(best_a)
        if new_policy == policy:
            return policy, V
        policy = new_policy
''',
   ["policy_iteration(STUDY, 0.9)[0]", "policy_iteration(STUDY, 0.9)[1]", "policy_iteration(EX, 0.9)[0]"],
   ["Write the two helpers first (`policy_evaluation` and `greedy_policy`) in the same box, then use them.", "Loop: `V = policy_evaluation(...)`, `new_policy = greedy_policy(...)`, `if new_policy == policy: return policy, V`, else `policy = new_policy`."]),
)
