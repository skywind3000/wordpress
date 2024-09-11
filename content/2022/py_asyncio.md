---
uuid: 2618
title: 性能测试：asyncio vs gevent vs native epoll
status: publish
categories: 编程技术
tags: Python
slug: 
---
测试一下 python 的 asyncio 和 gevent 的性能，再和同等 C 程序对比一下，先安装依赖：

```bash
pip3 install hiredis gevent
```

如果是 Linux 的话，可以选择安装 uvloop 的包，可以测试加速 asyncio 的效果。

测试程序：`echo_bench_gevent.py`

```python
import sys
import gevent
import gevent.monkey
import hiredis

from gevent.server import StreamServer
gevent.monkey.patch_all()

d = {}

def process(req):
    # only support get/set
    cmd = req[0].lower()
    if cmd == b'set':
        d[req[1]] = req[2]
        return b"+OK\r\n"
    elif cmd == b'get':
        v = d.get(req[1])
        if v is None:
            return b'$-1\r\n'
        else:
            return b'$1\r\n1\r\n'
    else:
        print(cmd)
        raise NotImplementedError()
    return b''

def handle(sock, addr):
    reader = hiredis.Reader()
    while True:
        buf = sock.recv(4096)
        if not buf:
            return
        reader.feed(buf)
        while True:
            req = reader.gets()
            if not req:
                break
            sock.sendall(process(req))
    return 0

print('serving on 0.0.0.0:5000')
server = StreamServer(('0.0.0.0', 5000), handle)
server.serve_forever()
```

测试程序：`echo_bench_asyncio.py`

(点击 Read more 展开)

<!--more-->

```python
import asyncio
import hiredis

d = {}

def process(req):
    cmd = req[0].lower()
    if cmd == b'set':
        d[req[1]] = req[2]
        return b"+OK\r\n"
    elif cmd == b'get':
        v = d.get(req[1])
        if v is None:
            return b'$-1\r\n'
        else:
            return b'$1\r\n1\r\n'
    elif cmd == b'config':
        return b'-ERROR\r\n'
    else:
        return b'-ERROR\r\n'
    return b''

async def echo_server(reader, writer):
    hireader = hiredis.Reader()
    while True:
        s = await reader.read(4096)
        if not s:
            break
        hireader.feed(s)
        while True:
            req = hireader.gets()
            if not req:
                break
            res = process(req)
            writer.write(res)
            await writer.drain()
    return 0

async def main():
    server = await asyncio.start_server(echo_server, '0.0.0.0', 5001)
    print('serving on {}'.format(server.sockets[0].getsockname()))
    await server.serve_forever()
    return 0

asyncio.run(main())
```

测试程序：`echo_bench_asyncio_uvloop.py`

```python
import asyncio
import hiredis

d = {}

def process(req):
    cmd = req[0].lower()
    if cmd == b'set':
        d[req[1]] = req[2]
        return b"+OK\r\n"
    elif cmd == b'get':
        v = d.get(req[1])
        if v is None:
            return b'$-1\r\n'
        else:
            return b'$1\r\n1\r\n'
    elif cmd == b'config':
        return b'-ERROR\r\n'
    else:
        return b'-ERROR\r\n'
    return b''

async def echo_server(reader, writer):
    hireader = hiredis.Reader()
    while True:
        s = await reader.read(4096)
        if not s:
            break
        hireader.feed(s)
        while True:
            req = hireader.gets()
            if not req:
                break
            res = process(req)
            writer.write(res)
            await writer.drain()
    return 0

async def main():
    server = await asyncio.start_server(echo_server, '0.0.0.0', 5002)
    print('serving on {}'.format(server.sockets[0].getsockname()))
    await server.serve_forever()
    return 0

try:
    import uvloop
    uvloop.install()
    print('uvloop is enabled')
except ImportError:
    print('uvloop is not available')

asyncio.run(main())
```

启动程序：

```bash
python3 echo_bench_gevent.py          # listened on port 5000
python3 echo_bench_asyncio.py         # listened on port 5001
python3 echo_bench_asyncio_uvloop.py  # listened on port 5002
```

性能测试：

```bash
redis-benchmark -p 5000 -t get -n 100000 -r 100000000
redis-benchmark -p 5001 -t get -n 100000 -r 100000000
redis-benchmark -p 5002 -t get -n 100000 -r 100000000
```

测试结果：

| 程序             | Python 3.9                 | Python 3.11                |
| ---------------- | -------------------------- | -------------------------- |
| gevent           | 34281.80 requests / second | 32258.07 requests / second |
| asyncio          | 40144.52 requests / second | 51652.89 requests / second |
| asyncio + uvloop | 64102.57 requests / second | 66577.90 requests / second |

原生对比：

```bash
redis-benchmark -p 6379 -t get -n 100000 -r 100000000
```

输出

```
75244.55 requests per second
```


测试结论：

结论就是 3.11 下面，asyncio 比 gevent 快 50%，加上 uvloop 可以快一倍。纯用 asyncio 性能可以做到 redis 的 68%，而加上 uvloop 后可以做到 redis 的 88%，当然程序比较简单，没有复杂的数据处理，主要就是测评网络 I/O 性能。




