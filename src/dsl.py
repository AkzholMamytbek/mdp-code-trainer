LESSONS = []

def lesson(id, part, title, *blocks):
    LESSONS.append(dict(id=id, part=part, title=title, blocks=list(blocks)))

def P(text):
    return {"t": "p", "text": text}

def C(code):
    return {"t": "code", "code": code}

def TIP(text):
    return {"t": "tip", "text": text}

def WARN(text):
    return {"t": "warn", "text": text}

def EX(id, title, task, starter, solution, tests, hints):
    return {"t": "ex", "id": id, "title": title, "task": task, "starter": starter,
            "solution": solution, "tests": tests, "hints": hints}
