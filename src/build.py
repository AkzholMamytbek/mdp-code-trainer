"""Validate every lesson and build ../index.html.

For each exercise the model solution is run against its tests to compute the
expected values, the solution must pass all tests, and the starter code must
not. Example code blocks are executed so the page can show their output.

Usage (from the repository root):  python3 src/build.py
"""
import contextlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import harness_py as H  # noqa: E402
import lessons_part1, lessons_part2, lessons_part3, lessons_part4, lessons_part5  # noqa: E402,F401
from dsl import LESSONS  # noqa: E402


def fresh_ns(code=""):
    ns = {}
    exec(H._SETUP, ns)
    if code:
        exec(code, ns)
    return ns


def main():
    problems, ids, n_ex = [], set(), 0
    for L in LESSONS:
        for b in L["blocks"]:
            if b["t"] == "code":
                ns, out = fresh_ns(), io.StringIO()
                try:
                    with contextlib.redirect_stdout(out):
                        exec(b["code"], ns)
                except Exception as e:  # pragma: no cover
                    problems.append(f"example error in {L['id']}: {e!r}")
                b["output"] = out.getvalue()
            elif b["t"] == "ex":
                n_ex += 1
                if b["id"] in ids:
                    problems.append("duplicate id " + b["id"])
                ids.add(b["id"])
                tests = []
                for expr in b["tests"]:
                    val = eval(expr, fresh_ns(b["solution"]))
                    tests.append({"expr": expr, "expected": repr(val)})
                b["tests"] = tests
                res = json.loads(H._check(b["solution"], json.dumps(tests)))
                if res["error"] or not all(r["pass"] for r in res["results"]):
                    problems.append(f"solution fails {b['id']}: {res}")
                res2 = json.loads(H._check(b["starter"], json.dumps(tests)))
                if not res2["error"] and all(r["pass"] for r in res2["results"]):
                    problems.append(f"starter passes {b['id']}")
    if problems:
        print("\n".join(problems))
        sys.exit(1)

    data = {"lessons": LESSONS, "setup": H._SETUP}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    template = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    out_path = os.path.join(HERE, "..", "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(template.replace("__DATA__", blob))
    print(f"OK: {len(LESSONS)} lessons, {n_ex} exercises -> index.html")


if __name__ == "__main__":
    main()
