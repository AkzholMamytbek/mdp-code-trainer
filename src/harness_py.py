import sys, json, io, math, traceback, contextlib

_SETUP = '''
EX = [
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
]
STUDY = [
    [[(1.0, 0, 1.0, False)],
     [(1.0, 1, -1.0, False)]],
    [[(0.5, 2, 20.0, True), (0.5, 1, -1.0, False)],
     [(1.0, 0, 0.0, False)]],
    [[(1.0, 2, 0.0, True)]],
]
'''

class _TooLong(Exception):
    pass

_LIMIT = 3_000_000

def _run_limited(fn):
    steps = [0]
    def tracer(frame, event, arg):
        if event == "line":
            steps[0] += 1
            if steps[0] > _LIMIT:
                raise _TooLong("Your code ran for too long. Is there an infinite loop (e.g. a while loop that never stops)?")
        return tracer
    sys.settrace(tracer)
    try:
        return fn()
    finally:
        sys.settrace(None)

def _close(a, b):
    if isinstance(b, bool) or isinstance(a, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if isinstance(a, float) and math.isnan(a):
            return False
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-6)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a.keys()) == set(b.keys()) and all(_close(a[k], b[k]) for k in b)
    if isinstance(a, set) and isinstance(b, set):
        return a == b
    return a == b

def _short(x, n=160):
    try:
        s = repr(x)
    except Exception:
        s = "<cannot show>"
    return s if len(s) <= n else s[:n] + " ..."

def _err_text(e, code):
    tb = traceback.extract_tb(e.__traceback__)
    line = None
    for fr in tb:
        if fr.filename == "<your code>":
            line = fr.lineno
    name = type(e).__name__
    msg = str(e)
    text = name + ": " + msg
    if line is not None:
        lines = code.split("\n")
        src = lines[line - 1].strip() if 0 < line <= len(lines) else ""
        text += "\n  at line " + str(line) + ":  " + src
    tip = ""
    if name == "NameError":
        tip = "A name is not defined. Check spelling, and that the function name in your def line is exactly the one asked for."
    elif name == "IndexError":
        tip = "An index is outside the list. Remember: indexes start at 0, and the last index is len(lst) - 1."
    elif name == "TypeError" and "NoneType" in msg:
        tip = "Something is None. A function that has no return statement gives back None."
    elif name == "TypeError" and "unpack" in msg:
        tip = "You are unpacking at the wrong level. Check which loop level gives you the 4-value tuples."
    elif name == "ValueError" and "unpack" in msg:
        tip = "The number of names on the left does not match the number of values. An outcome has exactly 4 values: prob, next_state, reward, terminal."
    elif name == "IndentationError":
        tip = "Indentation problem. Lines inside def / for / if must be indented by 4 more spaces than the line with the colon."
    elif name == "SyntaxError":
        tip = "Python could not read your code. Look for a missing colon ':' at the end of def / for / if lines, or unclosed brackets."
    elif name == "ZeroDivisionError":
        tip = "You divided by zero. Guard the division with an if."
    elif name == "_TooLong":
        text = msg
    return text, tip

def _check(code, tests_json):
    tests = json.loads(tests_json)
    out = io.StringIO()
    ns = {}
    exec(_SETUP, ns)
    res = {"compiled": True, "error": None, "tip": "", "results": [], "stdout": ""}
    try:
        compiled = compile(code, "<your code>", "exec")
    except SyntaxError as e:
        res["compiled"] = False
        line = e.lineno or 0
        lines = code.split("\n")
        src = lines[line - 1].strip() if 0 < line <= len(lines) else ""
        res["error"] = type(e).__name__ + ": " + str(e.msg) + "\n  at line " + str(line) + ":  " + src
        res["tip"] = _err_text(e, code)[1]
        return json.dumps(res)
    try:
        with contextlib.redirect_stdout(out):
            _run_limited(lambda: exec(compiled, ns))
    except BaseException as e:
        res["error"], res["tip"] = _err_text(e, code)
        res["stdout"] = out.getvalue()[-2000:]
        return json.dumps(res)
    stop = False
    for t in tests:
        if stop:
            res["results"].append({"expr": t["expr"], "expected": t["expected"], "got": "(skipped)", "pass": False, "note": "Skipped because an earlier test ran too long."})
            continue
        row = {"expr": t["expr"], "expected": t["expected"], "got": "", "pass": False, "note": ""}
        try:
            expected = eval(t["expected"], {})
            with contextlib.redirect_stdout(out):
                got = _run_limited(lambda: eval(t["expr"], ns))
            row["got"] = _short(got)
            row["pass"] = _close(got, expected)
            if not row["pass"]:
                if got is None and expected is not None:
                    row["note"] = "Your function returned None. Did you forget return (or is return inside an if that did not run)?"
                elif isinstance(expected, bool) and not isinstance(got, bool):
                    row["note"] = "Expected True or False."
                elif isinstance(expected, (list, tuple)) and isinstance(got, (list, tuple)) and len(got) != len(expected):
                    row["note"] = "Wrong length: expected " + str(len(expected)) + " items, got " + str(len(got)) + "."
        except BaseException as e:
            txt, tip = _err_text(e, code)
            row["got"] = txt.split("\n")[0]
            row["note"] = tip
            if isinstance(e, _TooLong):
                stop = True
        res["results"].append(row)
    res["stdout"] = out.getvalue()[-2000:]
    return json.dumps(res)

def _play(code):
    out = io.StringIO()
    ns = {}
    exec(_SETUP, ns)
    res = {"stdout": "", "error": None, "tip": ""}
    try:
        compiled = compile(code, "<your code>", "exec")
        with contextlib.redirect_stdout(out):
            _run_limited(lambda: exec(compiled, ns))
    except BaseException as e:
        res["error"], res["tip"] = _err_text(e, code)
    res["stdout"] = out.getvalue()[-5000:]
    return json.dumps(res)
