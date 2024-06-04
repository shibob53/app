global_dict = {}

def post(key, value):
    global global_dict
    global_dict[key] = value
    return f"Added {key} with value {value} to the dictionary"

def get(key):
    global global_dict
    return global_dict.get(key, "Key not found in the dictionary")