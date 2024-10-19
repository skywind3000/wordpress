---
uuid: 3002
title: 怎么样打包 pyqt 应用才是最佳方案？
status: publish
categories: 编程技术
tags: Python,GUI
slug: 
date: 2022-02-06 13:49
---
早先看一堆人说 PyQt 打包麻烦，部署困难的，打出来的包大（几十兆起步），而且启动贼慢，其实 Python+PyQt 打包非常容易，根本不需要用什么 PyInstaller，我手工打包出来的纯 Python 环境只有 5MB，加上 PyQt 也才 14MB。

很多人用 PyInstaller 喜欢加一个 -F 参数，打包成一个单文件：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p1.png)

这样的单文件看起来似乎很爽，其实他们不知道，这其实是一个自解压程序，每次运行时需要把自己解压到 temp 目录，然后再去用实际的方式运行一遍解压出来的东西：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p2.jpg)

Process Explorer 把雷达图标拖动到 pyqt_hello.exe 的窗口上，可以看到有两个 pyqt_hello.exe 的文件，外面那个是你打包出来的，里面那个才是真正的程序（虽然可执行都是一个），看看它下面依赖的 python310.dll 是在哪里？这不就是一个临时解压出来的目录么：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p3.jpg)

看到没？这就是你 PyInstaller 打包出来的 30MB 的程序，每次运行都要临时解压出 71MB 的文件，运行完又删除了，那么如果打包出来的可执行有 100MB，每次运行都要释放出 200-300 MB 的东西出来，所以为什么 PyInstaller 出来的单文件运行那么慢的原因除了每次要解压外，还有杀毒软件碰到新的二进制都要扫描一遍，你每次新增一堆 .dll , .pyd, .exe，每次都要扫描，不慢可能么？

其实 PyInstaller 如果不打包成单文件可执行（-F 参数），用起来问题不大，唯一不足有两个，首先是很多动态库其实我没用比如上面的 socket, ssl, QtQuick 等，但都被打包的时候打进去了，大小会偏大；其次是目录看起来很乱，上百个文件一个目录，找主程序都找不到。

#### 正确的打包姿势

当然是手工打包，现在 Python 3.5 以后，官方都会发布一个嵌入式 Python 包：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p4.jpg)

链接在这里：[Python Release Python 3.8.10](https://www.python.org/downloads/release/python-3810/)

（点击 more/continue 继续）

<!--more-->

现在不是都到 Python 3.10 了么，为什么选择 3.8 ? 因为 3.8 是最后一个支持 Win7 的版本，3.9 以后就不支持了。那么为什么选择 32 位？因为打包出来 32 位是最紧凑的，64 位会大很多，除非你要一次性在内存里 load 2GB 以上的数据，否则基本就选择 32 位的。

这个 32 位的包很小：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p5.jpg)

本身也只有 7MB，解压出来是一些必要的文件：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p6.jpg)

那么你在项目路径里建立一个新的 runtime 文件夹，把这些文件放进去，外层写个批处理，调用一下里面的 python.exe 基本就可以跑个命令行的程序了。当然这样看起来很原始，所以精细一点的话，为这个 embedded python 做一个壳，直接加载里面 python3.dll 或者 python38.dll 来运行程序。

#### 嵌入式 Python 加壳

上面说的加壳我写了个例子了，叫做 PyStand：

https://github.com/skywind3000/PyStand

到 Release 下载下来是这样：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p7.jpg)

选择第一个 PyStand-py38-pyqt5-lite 这个包，下载下来 14MB，解压后：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p8.jpg)

目录非常清爽，比 PyInstaller 非单文件那种上百个 dll 的目录干净多了，就几个文件：

runtime：之前官方包 embedded python 解压后的内容。

- site-packages：第三方依赖
- PyStand.exe：主程序入口。
- PyStand.int：脚本入口。

这个 PyStand.exe 就是可以直接运行的程序，双击：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p9.jpg)

运行成功，打包文件只有 14MB，就能跑一个完整 PyQt5 的项目了，比 PyInstaller 的 30MB 小不少，你就是解压开也才 40MB，比 70MB 的 PyInstaller 解压后大小精简很多。

主要代码就是写在 PyStand.int 里，这个 PyStand.exe 启动后会自动加载同名的 .int 文件：

```python
import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
app = QApplication([])
win = QWidget()
win.setWindowTitle('PyStand')
layout = QVBoxLayout()
label = QLabel('Hello, World !!')
label.setAlignment(Qt.AlignCenter)
layout.addWidget(label)
btn = QPushButton(text = 'PUSH ME')
layout.addWidget(btn)
win.setLayout(layout)
win.resize(400, 300)
btn.clicked.connect(lambda : [
        print('exit'),
        sys.exit(0),
    ])
win.show()
app.exec_()
```

也就是说可执行叫做 PyStand.exe ，它会加载 PyStand.int；如果改名叫做 MyDemo.exe 它就会加载 MyDemo.int 里的代码。

那么其实大家可以直接使用了，把程序名字改成你想要的编写对应的 .int 即可，换图标的话，可以自己重新编译 PyStand 项目，或者直接 Resource Hacker 更换图标：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p10.jpg)

根本不需要配置 C/C++ 编译环境。

#### 安装依赖

我们需要一个对应版本号的 32 位的完整 python 3.8，然后新建个干净的虚拟环境：

```bash
\path\to\py38\python.exe  venv test
```

生成 test 目录里，大概目录是这样：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p11.jpg)

用 cmd.exe 进入 `Scripts` 目录，运行 `activate` 后，用 pip 安装你需要的包，然后到上面虚拟环境的 `Lib/site-packages` 里，把你需要的包找出来：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p12.jpg)

拷贝到 PyStand.exe 所在目录的 site-packages 里面即可使用，注意多余的，没有依赖的东西无需拷贝，比如上图的 pip 包。

#### 裁剪依赖

现在你已经把依赖的包拷贝到 PyStand 的 site-packages 里了，比如 PyQt5 这个包：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p13.jpg)

进去看一眼，把你不要的模块全部删除，什么 OpenGL，AxContainer，Multimedia，Position, Location, RemoteObject, DBus, QtQuick, QtWebEngine 之类的，不确定的可以删除了运行下你的程序测试下行不行，不行的又拷贝回来。

然后继续进入上图 Qt5 的目录里的 bin 目录：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p14.jpg)

这里有很多尺寸很大的模块，继续删除多余的，什么 QML，Test，Help，OpenGL ，GLES，Sensor, Bluetooth 之类的全部干掉，再到上层：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p15.jpg)

接着精简 plugins 目录里不要的东西，删除 qml/qsci, 然后到 translations 里把不要的语言删除掉，这么一圈下来，整个目录从原来的 134MB：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p16.jpg)

精简到 46.8 MB：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p17.jpg)

比你 PyInstaller 解压出来的 70MB 小了一大半，打包出来就是 14MB：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p18.jpg)

我已经帮你裁剪好了，你可以直接使用，还有好多可以根据你程序的需要进行裁剪，比如 openssl，sqlite 这些都非常大，总之还有很多压缩空间，按照你的程序需要还可以二次裁剪。

手工裁剪比无脑 PyInstaller 可靠的多，不但可以精细裁剪，每一步你都清晰的知道是怎么来的，出了问题你也知道该怎么回退。

#### 二进制压缩

还可以用 upx 压缩一些比较大的文件，但 runtime 下面的 python3.dll, python38.dll, vcruntime140.dll 不能压缩，而 PyQt5 里的 QtCore, QtWidgets, QtGUI 不能压缩，一边测试一边压缩，还可以进一步精简。

#### 代码组织

你有很多 py 代码，可以在 PyStand 下面新建一个 script 目录：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p19.jpg)

在里面放一个 main.py，实现一个 main 方法，然后改写 PyStand.int：

```python
import sys, os
os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.abspath('script'))
sys.path.append(os.path.abspath('script.egg'))
import main
main.main()
```

这个代码就是做了三件事情：矫正当前运行目录，设置 `sys.path`，然后导入 main 模块并执行 main 方法。注意后面 sys.path 里追加了一个 `script.egg`，意思是你调试好了，发布时把 script 目录里面的代码或者 pyc 压缩成要给 zip 文件，叫做 script.egg 放在 PyStand 那里删除 script 目录即可：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p20.jpg)

发布出来大概是这样，运行 PyStand.exe 成功的 import 到了 main.main() 函数：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p9.jpg)

主目录下面就三个文件，打包放到其他机器上解压就运行，不喜欢 PyStand.exe 这个名字可以随便改，同时修改 PyStand.int 的名字即可：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p21.jpg)

比如这样，运行 PyQt-Demo.exe 它会根据自身的名字，正确的找到 PyQt-Demo.int 文件并执行。

#### 基础加密

要求不高的话，上面你将 script 目录内的 .py 文件打包成 script.egg，直接就可以发布了，至少不会满目录的 .py 文件。要求高一点的话，把 .py 先转换成 .pyc 再压缩成 script.egg，然后把关键几个模块用 cython 之类的工具转换成 .pyd 即可。

上面基础加密基本够用了，个人开发者可以就此止步，如果你是一个团队，要发布面向百万以上用户产品级的东西，追求比 PyInstaller 更安全的加密方式可以继续往下。

#### 高级加密

接下来技巧我在 Python 2 时代都做过，你可以视精力酌情添加：

第一层：pyc 加密，自己写一个 importer，放到 PyStand.int 里初始化，作用是加载自定义的 .pz 文件，而 .pz 文件是根据 .pyo 文件加密得到，你的 importer 负责解密并加载这些字节码，把这个 importer 添加到 sys.path_hooks 里面，这样 python 就能 import .pz 文件了，再写个批处理，把项目文件全部编译转换成 .pz 压缩成 script.egg。

第二层：zip 文件加密码，参考 python 自带的 zipimporter 实现一个 zipimporter2，支持 zip 文件加密码，只要在 sys.path.append('script.egg@12345') 类似这样的路径，就可以按给定密码 import zip 内的东西，当然密码可以写的不那么明显，还可以支持 7zip 导入。

第三层：将 .dll/.pyd 封装近 python38.zip 或者 script.egg 内，这里你会用到 py2exe 的两个子模块：MemoryModule：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p22.jpg)

地址：https://github.com/py2exe/py2exe/tree/master/source

可以用来从内存加载 dll/pyd，然后还有一个 zipdllimporter 的脚本，可以从内存/zip 文件直接加载 pyd/dll，这样你的所有的 pyd/dll 都可以塞到 .zip/.egg 文件里了，根本不用暴露。

第四层：源代码重新编译 Python，将很多东西直接编译进去，比如上面说的各种 importer 实现，memory importer，加密 zip 文件之类的，并且支持加密的 PyStand.int。

第五层：修改字节码，找到 python 源代码的 include/opcode.h：
![](https://skywind3000.github.io/images/blog/2022/pyqt/p23.jpg)

自己魔改一遍，基本反编译的程序都蒙圈了，再到 Include/internal/pycore_ast.h 下面修改一些结构体的内部顺序，这样只要对方没有你的头文件，想从进程内存级别 intercept 进来获取字节码或者 ast 的都会非常麻烦。

第六层：静态编译，把所有第三方库和 python 自己静态编译成一个 exe 或者 dll，没有任何依赖，不暴露任何 dll 接口，集成上面说过的所有功能。由于你全部依赖都静态编译了，所以可以给 PyObject 里加两个无关的成员，调整一下已有成员顺序，别人就是进程截取 PyObject 的指针，由于没有头文件，内部结构不知道，所以它也没有任何办法。

第七层：你的可执行每次启动会检测可执行文件末尾，是否有添加的内容，如果有，把他视为一个加密的压缩包，在内存里解密并 import 对应模块，这样你上面的单个程序就可以和具体逻辑相分离，有了新的逻辑代码，压缩加密后添加在唯一可执行尾部即可。

。。。。。

还有很多类似的方法，这里仅仅抛砖引玉，没有绝对的安全，就是看你愿意投入多少人力，可以做到哪一层，个人的话，上面基础加密足够了，公司团队的话，安排人搞个一两个月，基本也就搞定了。

#### 错误调试

这个 PyStand.exe 是窗口程序，那么出错了怎么看 exception 呢？可以打开一个 cmd.exe，用 cmd.exe 启动 PyStand，就能看到错误了，你自己也可以记录下日志，catch 一下内部的 exception。

更多阅读：
[为什么很多Python开发者写GUI不用Tkinter，而要选择PyQt和wxPython或其他？](/blog/archives/3039)

