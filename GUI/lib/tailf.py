from time import sleep

def tailf(f):
    fp = open(f, 'r')
    while True:
        line = fp.readline()
        if line:
            yield line
        else:
            sleep(0.3)
