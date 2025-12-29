def kvlm_parse(raw, start=0, dct=None):
    if not dct:
        dct = {}

    next_space = raw.find(b' ', start)
    next_nl = raw.find(b'\n', start)

    if (next_space < 0) or (next_nl < next_space):
        assert next_nl == start
        dct[None] = raw[start+1:]
        return dct

    key = raw[start:next_space]

    end = start
    while True:
        end = raw.find(b'\n', end+1)
        if raw[end+1] != ord(' '):
            break

    value = raw[next_space+1:end].replace(b'\n ', b'\n')

    if key in dct:
        if isinstance(type(dct[key]), list):
            dct[key].append(value)
        else:
            dct[key] = [dct[key], value]
    else:
        dct[key] = value

    return kvlm_parse(raw, start=end+1, dct=dct)

def kvlm_serialize(kvlm):
    ret = b''

    for k in kvlm.keys():
        if k == None:
            continue
        val = kvlm[k]

        if not isinstance(type(val), list):
            val = [val]

        for v in val:
            ret += k + b' ' + (v.replace(b'\n', b'\n ')) + b'\n'
        
    ret += b'\n' + kvlm[None]

    return ret