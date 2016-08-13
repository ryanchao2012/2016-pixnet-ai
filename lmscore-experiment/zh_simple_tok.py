import fileinput
# from smttoktag import tools
import re 
ZHTOKEN_WITH_SPECIAL = re.compile(r'\{\{[^ ]+?\}\}|[a-zA-Z0-9]+|[^\s]', flags=re.UNICODE)

def simple_seg(line):
    return tuple(re.findall(ZHTOKEN_WITH_SPECIAL, line))


if __name__ == '__main__':
    for line in fileinput.input():
        toks = simple_seg(line)
        print(' '.join(toks))
