import multiprocessing as mp

def __input(cbk):
    return cbk(input())

def get_input(cbk):
    p = mp.Process(target=__input, args=[cbk])
    p.start()
    return p.terminate

if __name__ == "__main__":
    import time
    do_ipt = True
    while True:
        if do_ipt:
            do_ipt = False
            def l(i):
                global do_ipt
                do_ipt = True
                print(i)
            get_input(l)
        time.sleep(1)
        print("hi")