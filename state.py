_state = {}

def get(uid, key=None):
    if key:
        return _state.get(uid, {}).get(key)
    return _state.get(uid, {})

def set(uid, key, value):
    _state.setdefault(uid, {})[key] = value

def clear(uid):
    _state.pop(uid, None)