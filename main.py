import datetime
import time
import hashlib

def timeline(path):
    logfile = open(path, 'a')
    logfile.write('-' * 50 + '\n')

    def decorator(old_function):

        def new_function(*args, **kwargs):
            nonlocal logfile
            logfile.write('Func name "' + old_function.__name__ + '"\n')
            logfile.write('Func args ' + str(args) + '\n')
            logfile.write('Func kwargs ' + str(kwargs) + '\n')
            start = datetime.datetime.now()
            something = old_function(*args, **kwargs)
            end = datetime.datetime.now()
            logfile.write('Timeline ' + str(end - start) + '\n')
            return something

        return new_function

    return decorator


@timeline('log.txt')
def foo(b, c):
    a = b * c
    b = a * c
    c = a * b
    time.sleep(1)
    return a * b * c


@timeline('log.txt')
def gen(path):
    with open(path, "r") as data:
        end = sum(1 for line in data)
        data.seek(0)
        for i in range(0, end):
            if i > end:
                raise StopIteration
            hash = hashlib.md5(data.read(i).encode())
            yield hash.hexdigest()


if __name__ == '__main__':
    foo(20, 2)
    foo(10, 15)
    foo(15, 99999999)
    for i in gen('countries.txt'):
        print(i)