Linux-Management-Tools
======================

This tool can manage tens of thousands of Linux server.You can use it to execute a command, upload files, download files.


windows下运行的linux服务器批量管理工具（带UI界面）

产生背景：

	由于做服务器运维方面的工作，需要对近千台LINUX服务器进行统一的管理，如同时批量对LINUX服务器执行相关的指令、同时批量对LINUX服务器upload程序包、同时批量对LINUX服务器download程序包。当前世面上也存在一些常见且功能强大的工具，如puppet，dsh，parallel-ssh等，但不得不说，他们的功能太重量了，重量到不得不学习他们的命令以及复杂的用法，且对于刚入LINUX门道的“菜鸟”来说无UI界面纯命令操作也显得太“重”了。故基于当前行业的形式以及个人工作的需要，开发了此工具。

工具语言：

	此工具采用python2.7开发，结合其WxPython的强大的UI工具集-UI界面设计模块集，及paramiko的功能工具集-Linux服务器操作模块集的支持所开发。




如果你想了解更多，请访问我的博客：http://blog.csdn.net/ruberzhu/article/details/39648553