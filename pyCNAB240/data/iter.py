

fields_line = [0, 2, 3]

HEADER_DE_ARQUIVO = {'HEADER_DE_ARQUIVO': fields_line}

HEADER_DE_LOTE = {'HEADER_DE_LOTE': fields_line}

SEGMENTS = {'SEGMENTS': 3*[{'P': 2*fields_line},
                         {'Q': 2*fields_line},
                         {'R': 2*fields_line}]
            }

TRAILER_DE_ARQUIVO = {'TRAILER_DE_ARQUIVO': fields_line}

TRAILER_DE_LOTE = {'TRAILER_DE_LOTE': fields_line}

d = {**HEADER_DE_ARQUIVO, **HEADER_DE_LOTE, **SEGMENTS, **TRAILER_DE_ARQUIVO, **TRAILER_DE_LOTE}

def itera(d):
    for key in d:
        if key == 'SEGMENTS':
            for segment in d['SEGMENTS']:
                for key_2 in segment:
                    yield segment[key_2]
        else:
            yield d[key]

# for e in itera(d):
#     print(e)


def apply_in_segments(dictionary, function, *args, **kwargs):
    for i, segment in enumerate(dictionary['SEGMENTS']):
        for key in segment:
            dictionary['SEGMENTS'][i] = function(segment[key], *args, **kwargs)

    return dictionary

def iter_in_segments(dictionary):
    for i, segment in enumerate(dictionary['SEGMENTS']):
        for key in segment:
            yield dictionary['SEGMENTS'][i]


def f(l):
    return [e**2 for e in l]

def count(l):
    if l[0] == 0:
        return 1
    else:
        return



list(iter_in_segments(d))