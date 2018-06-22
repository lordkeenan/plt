#!/usr/local/bin/python3
import regex
import sys

try:
    input = open('INPUT.TXT','r')
    src = input.read()
    input.close
except FileNotFoundError:
    print("INPUT.TXT not found")
    sys.exit(42)
except:
    print("something's wrong with INPUT.TXT, check its content")
    sys.exit(42)

reservedids = ['absolute', 'and', 'array', 'asm', 'begin', 'break', 'case', 'const', 'constructor', 'continue', 'destructor', 'div', 'do', 'downto', 'else', 'end', 'file', 'for', 'function', 'goto', 'if', 'implementation', 'in', 'inherited', 'inline', 'interface', 'label', 'mod', 'nil', 'not', 'object', 'of', 'on', 'operator', 'or', 'packed', 'procedure', 'program', 'record', 'reintroduce', 'repeat', 'self', 'set', 'shl', 'shr', 'string', 'then', 'to', 'type', 'unit', 'until', 'uses', 'var', 'while', 'with', 'xor', 'abs', 'arctan', 'boolean', 'char', 'cos', 'dispose', 'eof', 'eoln', 'exp', 'false', 'input', 'integer', 'ln', 'maxint', 'new', 'odd', 'ord', 'output', 'pack', 'page', 'pred', 'read', 'readln', 'real', 'reset', 'rewrite', 'round', 'sin', 'sqr', 'sqrt', 'succ', 'text', 'true', 'trunc', 'write', 'writeln']

pattern = r"^\s*(?:var\s*(?:(?<=^\s*var\s+|;\s*)(?<variables>[_a-zA-Z]\w*)\s*(?:(?<=[_a-zA-Z]\w*\s*),\s*(?:(?<variables>[_a-zA-Z]\w*)\s*)?)*(?:(?<=[_a-zA-Z]\w*\s*):\s*(?:real(?:\s*;\s*)?|integer(?:\s*;\s*)?|boolean(?:\s*;\s*)?|char(?:\s*;\s*)?|(?:array(?:\s*\[\s*(?:(?:(?<lowindex>(?:\+\s*|-\s*)?\d+)\s*(?:\.\.\s*(?:(?<highindex>(?:\+\s*|-\s*)?\d+)\s*(?:(?:(?<=\.\.\s*(?:\+\s*|-\s*)?\d+\s*),\s*(?:(?<lowindex>(?:\+\s*|-\s*)?\d+)\s*(?:\.\.\s*(?:(?<highindex>(?:\+\s*|-\s*)?\d+)\s*)?)?)?)*\s*)?)?)?)|integer|real|boolean|char)?(?:(?<=(?:\.\.\s*(?:\+\s*|-\s*)?\d+\s*)|integer|real|boolean|char)\]\s*)?)?)(?:(?<=\]\s*)of\s+(?:array(?:\s*\[\s*(?:(?:(?<lowindex>(?:\+\s*|-\s*)?\d+)\s*(?:\.\.\s*(?:(?<highindex>(?:\+\s*|-\s*)?\d+)\s*(?:(?:(?<=\.\.\s*(?:\+\s*|-\s*)?\d+\s*),\s*(?:(?<lowindex>(?:\+\s*|-\s*)?\d+)\s*(?:\.\.\s*(?:(?<highindex>(?:\+\s*|-\s*)?\d+)\s*)?)?)?)*\s*)?)?)?)|integer|real|boolean|char)?(?:(?<=(?:\.\.\s*(?:\+\s*|-\s*)?\d+\s*)|integer|real|boolean|char)\]\s*)?)?))*(?:(?<=\]\s*)of\s+(?:(?:integer|real|boolean|char)\s*(?:;\s*)?)?)?|string(?=\s*;)(?:\s*;\s*)?|(?:string(?:\s*\[\s*(?:(?<strlen>\d+)\s*(?:\](?:\s*;\s*)?)?)?)?))?)?)*)?"

regexpat = regex.compile(pattern)
result = regexpat.match(src)
srclen = len(src)

if (result):
    matchlen = len(result.group(0))

    columnoffset = 1

    j = 0
    strlenindex = 0
    for i in result.captures('strlen'):
        if int(i) >= 256:
            strlenindex = result.starts('strlen')[j] + columnoffset
            break
        j += 1

    j = 0
    idsindex = 0
    for i in result.captures('variables'):
        if (i in reservedids):
            idsindex = result.starts('variables')[j] + columnoffset
            break
        j += 1

    j = 0
    dupindex = 0
    d = {}
    for i in result.captures('variables'):
        if (i in d):
            dupindex = result.starts('variables')[j] + columnoffset
            break
        else:
            d[i] = 0
        j += 1

    j = 0
    arraylhindex = 0
    for i in result.captures('highindex'):
        i = i.replace(' ', '').replace('\t', '').replace('\n', '')
        k = result.captures('lowindex')[j].replace(' ', '').replace('\t', '').replace('\n', '')
        if (int(i) < int(k)):
            arraylhindex = result.starts('lowindex')[j] + columnoffset
            break
        j += 1

    srcarray = src.split('\n')
    strcount = 0
    prevstrlen = [0]
    curstrlen = [0]
    for i in srcarray:
        curstrlen.insert(strcount, prevstrlen[strcount] + len(i))
        prevstrlen.insert(strcount+1, prevstrlen[strcount] + len(i) + 1)

        if ((strlenindex >= prevstrlen[strcount]) and (strlenindex <= curstrlen[strcount]) and (strlenindex != 0)):
            print("string type length must not exceed 255: line {} column {}".format(strcount+1, strlenindex-prevstrlen[strcount]))
            sys.exit(42)

        if ((idsindex >= prevstrlen[strcount]) and (idsindex <= curstrlen[strcount]) and (idsindex != 0)):
            print("reserved ID: line {} column {}".format(strcount+1, idsindex-prevstrlen[strcount]))
            sys.exit(42)

        if ((dupindex >= prevstrlen[strcount]) and (dupindex <= curstrlen[strcount]) and (dupindex != 0)):
            print("duplicate variable found: line {} column {}".format(strcount+1, dupindex-prevstrlen[strcount]))
            sys.exit(42)

        if ((arraylhindex >= prevstrlen[strcount]) and (arraylhindex <= curstrlen[strcount]) and (arraylhindex != 0)):
            print("upper bound of range is less than lower bound: line {} column {}".format(strcount+1, arraylhindex-prevstrlen[strcount]))
            sys.exit(42)

        if ((matchlen >= prevstrlen[strcount]) and (matchlen <= curstrlen[strcount]) and (matchlen != srclen)):
            print("syntax error: line {} column {}".format(strcount+1, result.end()-prevstrlen[strcount] + columnoffset))
            sys.exit(42)

        strcount += 1

    if (matchlen == srclen):
        print("OK")
else:
#    print("syntax error: line 1 column 1")
    sys.exit(42)
