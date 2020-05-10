"""
Python多进程demo
总结自https://www.liaoxuefeng.com/wiki/1016959663602400/1017628290184064
"""

import os
import time
import random
from multiprocessing import Process, Pool, Queue

# 子进程过程
def task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random()*3)
    end = time.time()
    print('Task %s done after %0.2f seconds.' % (name, end-start))

"""单个子进程"""
# if __name__ == "__main__":
#     print("Parent process %s" % os.getpid())
#     p = Process(target=task, args=('test',))
#     print("Child process will start.")
#     p.start()
#     p.join()
#     print('child process end.')

"""
总结：
1 定义子进程的过程函数
2 实例化Process对象，两个参数：target--子进程函数；args--序列，子进程参数
3 p.run()运行子进程
4 p.join()等待子进程运行结束
5 p.terminate()强行结束进程
"""

"""多个子进程"""
# if __name__ == "__main__":
#     print("Parent process %s" % os.getpid())
#     p = Pool(4)
#     for i in range(5):
#         p.apply_async(task, (i,))
#     print("Waiting for all subprocesses done...")
#     p.close()
#     p.join()
#     print('All subprocesses done.')

"""
总结
1 p = Pool(n) 实例化一个n个并行进程的进程池，默认是CPU的核数。
2 通过 p.apply_async(func, args) 添加进程。apply方法会阻塞，等待子进程返回，apply_async能并行
3 调用 p.close() 后不能再添加进程
4 p.join() 需要在 p.close() 之后调用，会在这里阻塞到进程池中所有的进程返回
"""

"""外部进程"""
import subprocess

# if __name__ == "__main__":
#     print("$ nslookup www.python.org")
#     r = subprocess.call(['nslookup', 'www.python.org'])
#     print("Exit code:", r)

#     print('$ nslookup')
#     p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
#     print('Exit code:', p.returncode)

"""
总结
r = subprocess.call(list) 就像命令行一样，直接调用命令，返回进程返回码。是阻塞的。
p = subprocess.Popen(list) 相当于命令行打开一个进程，重定向数据流。
Popen之后使用 p.communicate(str) 相当于打开cli程序之后继续输入内容
"""

"""进程间通信"""
def consumer(q:Queue):
    while True:
        v = q.get(True)
        print('Get %s from queue' % v)

def producer(q:Queue):
    for i in ['A','B','C','D']:
        q.put(i)
        print("Put %s to queue" % i)
        time.sleep(random.random())

if __name__ == "__main__":
    q = Queue(5)
    p = Process(target=producer, args=(q,))
    c = Process(target=consumer, args=(q,))
    p.start()
    c.start()
    p.join()
    c.terminate()

"""
总结
进程间通信通过Queue, Pipes等实现.
get和put方法均可以选择是否阻塞

Linux下multiprocessing封装fork调用
Windows下将父进程的所有python对象pickle后给子进程，所以如果Windows失败了，那就是有无法pickle的对象。
"""
