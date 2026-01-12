# state.py

state = {}

def set(uid, k, v): state.setdefault(uid,{})[k]=v
def get(uid, k): return state.get(uid,{}).get(k)
def clear(uid): state[uid]={}