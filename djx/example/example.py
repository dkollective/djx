import time


def start(value):
    time.sleep(5)
    return value


def mod(_dependencies, *, function, bias, activation, weight):
    time.sleep(5)
    _func = {
        'prod': lambda a, b: a*b,
        'add': lambda a, b: a+b
    }
    act = _func[activation['function']]
    return act(_dependencies['result'], weight) + bias


def final(_dependencies):
    time.sleep(5)
    return sum(dep['result'] for dep in _dependencies)


def reference():
    value = 10
    value = [value + 1, value + 2, value * 3]
    value = [v + b for b in [0, 10, 20] for v in value]
    value = [v * 10 for v in value]
    return sum(value)
