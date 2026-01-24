_state = {}

def get(uid, key=None):
    if key:
        return _state.get(uid, {}).get(key)
    return _state.get(uid, {})

def set(uid, key, value):
    _state.setdefault(uid, {})[key] = value

def clear(uid):
    _state.pop(uid, None)

MAX_RECENT = 9

def push_recent(uid, key, value):
    user = _state.setdefault(uid, {})
    recents = user.setdefault(key, [])

    if value in recents:
        recents.remove(value)

    recents.insert(0, value)
    del recents[MAX_RECENT:]