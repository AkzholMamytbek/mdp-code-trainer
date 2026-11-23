from dsl import lesson, P, C, TIP, WARN, EX

PART = 4

lesson("p4-returns", PART, "Returns for every step (walking backwards)",
P("In RL we have **no transitions**, only experience: lists of rewards. The return from step t is G_t = r_t + γ·r_{t+1} + γ²·r_{t+2} + ..."),
P("Trick: G_t = r_t + γ · G_{t+1}. So start at the **end** and walk backwards, reusing the G you just computed."),
C('''rewards = [-1, -1, -1, 10]
gamma = 0.9
G = 0.0
for t in range(len(rewards) - 1, -1, -1):
    G = rewards[t] + gamma * G
    print("G_%d =" % t, G)'''),
EX("ex-ret-1", "returns_each_step(rewards, gamma)",
   "Return a list `out` where `out[t]` is the return G_t from step t.",
   "def returns_each_step(rewards, gamma):\n    pass\n",
   "def returns_each_step(rewards, gamma):\n    out = [0.0] * len(rewards)\n    G = 0.0\n    for t in range(len(rewards) - 1, -1, -1):\n        G = rewards[t] + gamma * G\n        out[t] = G\n    return out\n",
   ["returns_each_step([-1, -1, -1, 10], 0.9)", "returns_each_step([1, 2, 3], 0.5)", "returns_each_step([5], 0.9)", "returns_each_step([], 0.9)"],
   ["Make `out = [0.0] * len(rewards)` so you can fill it in by index.", "In the backwards loop: `G = rewards[t] + gamma * G` then `out[t] = G`."]),
)

lesson("p4-mc", PART, "Monte Carlo (direct evaluation)",
P("Monte Carlo: wait until the episode ends, compute the real return G for every visited state, and **average** over all visits."),
P("An episode here is a list of `(state, reward)`: the state, and the reward received when leaving it."),
C('''episodes = [
    [(0, -1), (1, -1), (2, 10)],
    [(0, -1), (0, -1), (2, 10)],
]
gamma = 1.0
total = [0.0, 0.0, 0.0]
count = [0, 0, 0]
for episode in episodes:
    G = 0.0
    for state, reward in reversed(episode):     # backwards, like before
        G = reward + gamma * G
        total[state] += G
        count[state] += 1
print("total:", total)
print("count:", count)
print("V(0) =", total[0] / count[0])'''),
P("State 0 was visited 3 times with returns 8, 9, 8, so V(0) = 25/3 = 8.33. This is **every-visit** Monte Carlo."),
TIP("`reversed(lst)` walks a list from the end without needing indexes."),
EX("ex-mc-1", "mc_every_visit(episodes, n_states, gamma)",
   "Return the list V where V[s] = average of all returns observed from state s (every visit). States never visited get `0.0`.",
   "def mc_every_visit(episodes, n_states, gamma):\n    pass\n",
   "def mc_every_visit(episodes, n_states, gamma):\n    total = [0.0] * n_states\n    count = [0] * n_states\n    for episode in episodes:\n        G = 0.0\n        for state, reward in reversed(episode):\n            G = reward + gamma * G\n            total[state] += G\n            count[state] += 1\n    V = []\n    for s in range(n_states):\n        if count[s] > 0:\n            V.append(total[s] / count[s])\n        else:\n            V.append(0.0)\n    return V\n",
   ["mc_every_visit([[(0, -1), (1, -1), (2, 10)], [(0, -1), (0, -1), (2, 10)]], 3, 1.0)",
    "mc_every_visit([[(0, -1), (1, -1), (2, 10)]], 4, 0.9)", "mc_every_visit([], 2, 0.9)"],
   ["The example above, inside a function, plus a final loop that divides.", "Guard the division: `if count[s] > 0: ... else: V.append(0.0)`."]),
)

lesson("p4-td", PART, "TD learning: update after every step",
P("TD does not wait for the end. After one step `s → s'` with reward `r` it nudges V(s) towards a **target**:"),
P("- target = r + γ·V(s')   (or just r if s' ends the episode)\n- error = target − V(s)\n- V(s) ← V(s) + α · error"),
C('''V = [4.0, 6.0]
alpha, gamma = 0.5, 0.9
s, r, s2 = 0, -1, 1
target = r + gamma * V[s2]
error = target - V[s]
V[s] = V[s] + alpha * error
print("target", target, "error", error, "new V", V)'''),
TIP("Every learning update in this course has the same shape: **old + α × (target − old)**. Only the target changes."),
EX("ex-td-1", "td_target(r, gamma, v_next, terminal)",
   "Return the TD target: `r` if `terminal`, otherwise `r + gamma * v_next`.",
   "def td_target(r, gamma, v_next, terminal):\n    pass\n",
   "def td_target(r, gamma, v_next, terminal):\n    if terminal:\n        return r\n    return r + gamma * v_next\n",
   ["td_target(-1, 0.9, 6.0, False)", "td_target(5, 0.9, 6.0, True)", "td_target(0, 0.5, 10.0, False)"],
   ["Same idea as `future_value` in Part 1.", "`if terminal: return r` then `return r + gamma * v_next`."]),
EX("ex-td-2", "td_update(V, s, r, s2, alpha, gamma, terminal)",
   "Update `V[s]` **in place** with the TD rule and return the new `V[s]`.",
   "def td_update(V, s, r, s2, alpha, gamma, terminal):\n    pass\n",
   "def td_update(V, s, r, s2, alpha, gamma, terminal):\n    if terminal:\n        target = r\n    else:\n        target = r + gamma * V[s2]\n    V[s] = V[s] + alpha * (target - V[s])\n    return V[s]\n",
   ["td_update([4.0, 6.0], 0, -1, 1, 0.5, 0.9, False)", "td_update([4.0, 6.0], 0, 5, 1, 0.5, 0.9, True)",
    "(lambda V: (td_update(V, 0, -1, 1, 0.5, 0.9, False), V))([4.0, 6.0])", "td_update([0.0, 5.0, 0.0], 0, 2, 1, 0.1, 0.9, False)"],
   ["Compute `target` first, then change `V[s]`.", "`V[s] = V[s] + alpha * (target - V[s])` then `return V[s]`. (Test 3 checks that V itself was changed.)"]),
EX("ex-td-3", "td_episode(V, steps, alpha, gamma)",
   "`steps` is a list of `(s, r, s2, terminal)`. Apply the TD update for each step **in order** and return V.",
   "def td_episode(V, steps, alpha, gamma):\n    pass\n",
   "def td_episode(V, steps, alpha, gamma):\n    for s, r, s2, terminal in steps:\n        if terminal:\n            target = r\n        else:\n            target = r + gamma * V[s2]\n        V[s] = V[s] + alpha * (target - V[s])\n    return V\n",
   ["td_episode([0.0, 0.0, 0.0], [(0, -1, 1, False), (1, 10, 2, True)], 0.5, 0.9)",
    "td_episode([0.0, 0.0, 0.0], [(0, -1, 1, False), (1, 10, 2, True), (0, -1, 1, False), (1, 10, 2, True)], 0.5, 0.9)"],
   ["Loop over steps and unpack 4 names: `for s, r, s2, terminal in steps:`.", "Inside: the body of `td_update`. Order matters: later steps see earlier updates."]),
)

lesson("p4-ql", PART, "Q-learning",
P("Q-learning learns Q(s, a) directly, so we can pick actions without knowing T and R. `Q` is a list of lists: `Q[s][a]`."),
P("- target = r + γ · **max** Q[s'] (best action in the next state)   or just r if terminal\n- Q[s][a] ← Q[s][a] + α · (target − Q[s][a])"),
C('''Q = [[2.0, 0.0],
     [5.0, 1.0]]
alpha, gamma = 0.25, 0.8
s, a, r, s2 = 0, 0, 3, 1
target = r + gamma * max(Q[s2])     # max over the actions of s2
Q[s][a] = Q[s][a] + alpha * (target - Q[s][a])
print("target", target, "-> Q[0][0] =", Q[0][0])'''),
TIP("The `max` is why Q-learning is called **off-policy**: it learns about the best action even if the agent actually took a random one."),
EX("ex-ql-1", "q_learning_update(Q, s, a, r, s2, alpha, gamma, terminal)",
   "Update `Q[s][a]` in place and return the new value.",
   "def q_learning_update(Q, s, a, r, s2, alpha, gamma, terminal):\n    pass\n",
   "def q_learning_update(Q, s, a, r, s2, alpha, gamma, terminal):\n    if terminal:\n        target = r\n    else:\n        target = r + gamma * max(Q[s2])\n    Q[s][a] = Q[s][a] + alpha * (target - Q[s][a])\n    return Q[s][a]\n",
   ["q_learning_update([[2.0, 0.0], [5.0, 1.0]], 0, 0, 3, 1, 0.25, 0.8, False)",
    "q_learning_update([[1.0, 2.0], [4.0, 3.0]], 0, 1, 1, 1, 0.5, 0.9, False)",
    "q_learning_update([[3.0]], 0, 0, 5, 0, 0.6, 0.8, True)",
    "(lambda Q: (q_learning_update(Q, 0, 0, -2, 1, 0.6, 0.8, False), Q))([[0.0, 0.0], [0.0, 0.0]])"],
   ["Copy `td_update` and change two things: `Q[s][a]` instead of `V[s]`, and `max(Q[s2])` instead of `V[s2]`.", "`target = r + gamma * max(Q[s2])` (or `r` if terminal)."]),
EX("ex-ql-2", "q_learning_episode(Q, steps, alpha, gamma)",
   "`steps` is a list of `(s, a, r, s2, terminal)`. Apply the Q-learning update for each, in order, and return Q.",
   "def q_learning_episode(Q, steps, alpha, gamma):\n    pass\n",
   "def q_learning_episode(Q, steps, alpha, gamma):\n    for s, a, r, s2, terminal in steps:\n        if terminal:\n            target = r\n        else:\n            target = r + gamma * max(Q[s2])\n        Q[s][a] = Q[s][a] + alpha * (target - Q[s][a])\n    return Q\n",
   ["q_learning_episode([[0.0, 0.0], [0.0, 0.0], [0.0]], [(0, 1, -1, 1, False), (1, 0, 10, 2, True)], 0.5, 0.9)",
    "q_learning_episode([[0.0, 0.0], [0.0, 0.0], [0.0]], [(0, 1, -1, 1, False), (1, 0, 10, 2, True), (0, 1, -1, 1, False), (1, 0, 10, 2, True)], 0.5, 0.9)"],
   ["Five names when unpacking: `for s, a, r, s2, terminal in steps:`.", "Inside: the body of `q_learning_update`."]),
)

lesson("p4-eps", PART, "Choosing actions: greedy and ε-greedy",
P("**Greedy** = take the action with the biggest Q (argmax, lowest index on ties). **ε-greedy** = with probability ε take a random action (explore), otherwise greedy (exploit)."),
C('''import random

def greedy_action(Q, s):
    best_a = 0
    for a in range(1, len(Q[s])):
        if Q[s][a] > Q[s][best_a]:
            best_a = a
    return best_a

def epsilon_greedy(Q, s, epsilon):
    if random.random() < epsilon:            # random number in [0, 1)
        return random.randrange(len(Q[s]))   # explore
    return greedy_action(Q, s)               # exploit

Q = [[1.0, 5.0, 2.0]]
print(greedy_action(Q, 0))
print(epsilon_greedy(Q, 0, 0.0))    # epsilon 0 = always greedy'''),
P("MCQ favourite: the probability of choosing the greedy action is **1 − ε + ε/|A|**, because a random pick can also land on the greedy action. Example: ε = 0.2, 4 actions → 0.8 + 0.05 = 0.85."),
EX("ex-eps-1", "greedy_action(Q, s)",
   "Return the index of the largest `Q[s][a]` (lowest index on ties).",
   "def greedy_action(Q, s):\n    pass\n",
   "def greedy_action(Q, s):\n    best_a = 0\n    for a in range(1, len(Q[s])):\n        if Q[s][a] > Q[s][best_a]:\n            best_a = a\n    return best_a\n",
   ["greedy_action([[1.0, 5.0, 2.0]], 0)", "greedy_action([[1, 3, 3, 2]], 0)", "greedy_action([[0.0], [-1.0, -1.0]], 1)", "greedy_action([[-4.0, -2.0, -9.0]], 0)"],
   ["This is `index_of_max` from Part 1, on the list `Q[s]`.", "Start `best_a = 0`, compare with `>`."]),
EX("ex-eps-2", "prob_greedy(epsilon, n_actions)",
   "Return the probability that ε-greedy picks the greedy action: `1 - epsilon + epsilon / n_actions`.",
   "def prob_greedy(epsilon, n_actions):\n    pass\n",
   "def prob_greedy(epsilon, n_actions):\n    return 1 - epsilon + epsilon / n_actions\n",
   ["prob_greedy(0.2, 4)", "prob_greedy(0.0, 3)", "prob_greedy(1.0, 2)", "prob_greedy(0.1, 10)"],
   ["One line.", "`return 1 - epsilon + epsilon / n_actions`"]),
)

lesson("p4-model", PART, "Model-based RL: estimate T from samples",
P("Model-based RL counts what happened and turns counts into probabilities:"),
P("T(s, a, s') ≈ count(s, a, s') / count(s, a)"),
C('''samples = [(0, 1, 5, 1), (0, 1, 5, 1), (0, 1, -1, 0)]   # (s, a, r, s2)
count_sa = {}
count_sas = {}
for s, a, r, s2 in samples:
    count_sa[(s, a)] = count_sa.get((s, a), 0) + 1
    count_sas[(s, a, s2)] = count_sas.get((s, a, s2), 0) + 1
print(count_sa)
print(count_sas)
for (s, a, s2) in count_sas:
    print((s, a, s2), "->", count_sas[(s, a, s2)] / count_sa[(s, a)])'''),
EX("ex-mb-1", "estimate_T(samples)",
   "`samples` is a list of `(s, a, r, s2)`. Return a dict mapping `(s, a, s2)` → estimated probability.",
   "def estimate_T(samples):\n    pass\n",
   "def estimate_T(samples):\n    count_sa = {}\n    count_sas = {}\n    for s, a, r, s2 in samples:\n        count_sa[(s, a)] = count_sa.get((s, a), 0) + 1\n        count_sas[(s, a, s2)] = count_sas.get((s, a, s2), 0) + 1\n    T = {}\n    for (s, a, s2) in count_sas:\n        T[(s, a, s2)] = count_sas[(s, a, s2)] / count_sa[(s, a)]\n    return T\n",
   ["estimate_T([(0, 1, 5, 1), (0, 1, 5, 1), (0, 1, -1, 0)])", "estimate_T([(0, 1, 5, 1), (1, 0, 2, 2), (1, 0, 4, 2)])", "estimate_T([])"],
   ["Two dicts of counts, then a loop that divides.", "Use `.get(key, 0) + 1` with tuple keys `(s, a)` and `(s, a, s2)`."]),
EX("ex-mb-2", "estimate_R(samples)",
   "Return a dict mapping `(s, a, s2)` → **average** reward seen for that transition.",
   "def estimate_R(samples):\n    pass\n",
   "def estimate_R(samples):\n    sums = {}\n    counts = {}\n    for s, a, r, s2 in samples:\n        key = (s, a, s2)\n        sums[key] = sums.get(key, 0.0) + r\n        counts[key] = counts.get(key, 0) + 1\n    R = {}\n    for key in sums:\n        R[key] = sums[key] / counts[key]\n    return R\n",
   ["estimate_R([(0, 1, 5, 1), (0, 1, 3, 1), (0, 1, -1, 0)])", "estimate_R([(1, 0, 2, 2), (1, 0, 4, 2)])"],
   ["This is `average_by_key` from Part 1, with the key `(s, a, s2)`.", "`key = (s, a, s2)`; keep sums and counts; divide at the end."]),
)
