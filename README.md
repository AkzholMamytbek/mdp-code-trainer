# MDP Code Trainer

An interactive, in-browser Python trainer for writing **Markov Decision Process (MDP)** and **Reinforcement Learning (RL)** code by hand. It is built for students preparing for coding tests where you must implement things like value iteration, policy evaluation or Q-learning yourself (CodeRunner-style questions).

It starts from Python basics and goes up step by step. Every lesson has a short explanation, examples, and small exercises that you write yourself and check instantly.

## How to use

1. Open `index.html` in any modern browser. Nothing to install: Python runs in the page.
2. Read a lesson, write code in the exercise box, press **Check** (or Ctrl / Cmd + Enter).
3. Stuck? Open **Hint 1**, then **Hint 2**. The **Solution** button asks twice so you try first.
4. Your progress and code are saved in your browser (localStorage).
5. The **Playground** button (bottom right) runs any code you like.

## What's inside

32 lessons, 86 exercises:

| Part | Topics |
|---|---|
| 1. Python warm-up | variables, functions and `return`, `if`, comparing floats, lists, `for` loops, `range`, `enumerate` and argmax, tuples and unpacking, nested lists and loops, sets, dictionaries |
| 2. Reading an MDP | the `transitions[s][a] = [(prob, next_state, reward, terminal), ...]` format, looping over outcomes / actions / the whole MDP, mock-test style questions |
| 3. Solving MDPs | Q-values, Bellman backup, batch sweeps, value iteration, policy extraction, policy evaluation, policy iteration |
| 4. Reinforcement learning | returns, Monte Carlo evaluation, TD(0), Q-learning, greedy and ε-greedy, model-based estimates of T and R |
| 5. Final challenge | 5 exam-style tasks without new theory |

Two example MDPs, `EX` and `STUDY`, are pre-loaded in every exercise and in the playground.

Each check shows every test with the expected and actual value, and explains common mistakes: a missing `return`, a missing `:`, wrong indentation, an index out of range, unpacking at the wrong loop level, or an infinite loop (stopped after a few seconds).

## How it works

- `index.html` is a single self-contained page. Python code runs in the browser with [Skulpt](https://skulpt.org), loaded from the jsDelivr CDN, so an internet connection is needed the first time.
- Lessons are written in Python in `src/lessons_part*.py` using a tiny DSL (`src/dsl.py`).
- `src/build.py` runs every model solution with real CPython to compute the expected test values, checks that each solution passes and each starter does not, runs the examples to capture their output, and writes `index.html`.

### Rebuild after editing lessons

```bash
python3 src/build.py
```

### Add an exercise

```python
EX("ex-my-id", "double(x)",
   "Write `double(x)` that returns x times 2.",
   "def double(x):\n    pass\n",          # starter code
   "def double(x):\n    return x * 2\n",  # model solution
   ["double(4)", "double(-1.5)"],        # test expressions (expected values are computed)
   ["Hint 1 text", "Hint 2 text"]),
```

## Disclaimer

This is an independent study aid, not official course material. The exercises are for practice; always follow your own course's rules for assessments.

## License

MIT
