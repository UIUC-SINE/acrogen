#!/usr/bin/env python

# a custom string class where we can add a .base attribute
class String(str):
    base = None

def make_chunklist(base, str_list):
    """Annotate list of chunks to show they belong to same word"""
    chunklist = []
    for s in str_list:
        chunk = String(s)
        chunk.base = base
        chunklist.append(chunk)
    return chunklist

# --------- Chunks -----------
# list of units from which to build acronyms

vowel_chunks = (
    make_chunklist('obs.statistics', ['obs', 'os', 'ost']) + 
    make_chunklist('inference', ['i', 'in', 'inf']) + 
    make_chunklist('estimation', ['e', 'es', 'est'])
)

and_chunk = make_chunklist('and', ['a'])

consonant_chunks = (
    make_chunklist('detection', ['d', 'de', 'det']) +
    make_chunklist('comp.inference', ['cin']) +
    make_chunklist('comp.imaging', ['ci', 'cim']) +
    make_chunklist('remote.sensing', ['res', 'rs']) +
    make_chunklist('sig.processing', ['sip', 'sp', 'spr'])
)

# --------- Build acronyms ---------------

def build(word, used_chunks, result, length=4):
    """Build acronyms recursively,
    alternating between vowel and consonant chunks"""

    if word[-1][-1] in 'aeiou':
        chunks = consonant_chunks
    else:
        if len(word) == length - 2:
            chunks = vowel_chunks + and_chunk
        else:
            chunks = vowel_chunks
        # include 'and' only in second to last chunk
        # import ipdb
        # ipdb.set_trace()
        # if len(word) == length - 1:
        #     chunks += and_chunk

    for chunk in chunks:
        if chunk.base in used_chunks:
            continue

        new_word = word + [chunk]

        if len(new_word) == length:
            result.append((''.join(new_word), new_word))
        else:
            build(new_word, used_chunks + [chunk.base], result, length)

result = []
for chunk in vowel_chunks + consonant_chunks:
    build([chunk], [chunk.base], result)

# sort and print acronyms
for string, chunks in sorted(result):
    print('{:30}{}'.format(
        string,
        ' '.join([c.base for c in chunks])
    ))
    
