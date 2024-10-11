---
uuid: 2991
title: Python 的 asyncio 网络性能比 C 写的 Redis 还好？
status: publish
categories: 网络编程
tags: Python
slug: 
date: 2024-10-10 23:15
---
先前我做过一个 asyncio/gevent 的性能比较《[性能测试：asyncio vs gevent vs native epoll](https://skywind.me/blog/archives/2618)》，今天修改了一下 asyncio 的测试程序的消息解析部分，改用 Protocol，发现它甚至比 redis 还快了：

安装依赖：

```bash
pip install hiredis uvloop
```

编辑 echosvr.py 文件：

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

class RedisServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.hireader = hiredis.Reader()

    def data_received(self, data):
        self.hireader.feed(data)
        while True:
            req = self.hireader.gets()
            if not req:
                break
            res = process(req)
            self.transport.write(res)

async def main():
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: RedisServerProtocol(), '0.0.0.0', 5003)
    print('serving on {}'.format(server.sockets[0].getsockname()))
    async with server:
        await server.serve_forever()

try:
    import uvloop
    uvloop.install()
except ImportError:
    print('uvloop is not available')

asyncio.run(main())
```

启动：

```bash
python echosvr.py
```

测试：

```bash
redis-benchmark -p 5003 -t get -n 100000 -r 100000000
...
95238.10 requests per second
```

同一台机器上测试 redis：

```bash
redis-benchmark -p 6379 -t get -n 100000 -r 100000000
...
91407.68 requests per second
```

同一台机器上，Python 版本的服务可以跑到 95k requests/s 而 redis 只能跑到 91k requests/s，前者比后明显快了 5%。

那么 asyncio 比 C 写的 redis 性能还好么？其实不是，因为 redis 做了更多事情，比如为了更高并发，它把读写线程从主线程分离出去了，而这个 Python 代码只有一个高度紧凑的主线程；其次 redis 功能复杂，结构也相应有更多层次的抽线，一条消息从接收到处理需要经过多个模块，这是业务复杂度上到一定层次必然的。

目前市面上不少新项目号称比久经考验的老项目更快，其中部分也就是和这个 python 测试程序类似，老项目考虑的东西它们都不考虑，就是浅浅一层，用最简单的测试跑一下，好像是比老项目快那么一点了，但是复杂度但凡稍微上去一点，只需要它实现老项目一半不到的功能，那点薄薄的优势立马荡然无存，马上跑的比老项目还慢。


