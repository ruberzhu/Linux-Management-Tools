__author__ = 'zhuhongbao'
# -*- coding: GBK  -*-
'''批量执行命令'''
import wx
import sys
import paramiko
import datetime
import os
import string
import traceback
import threading
import time
import ServersFrame
# import SshKey
reload(sys)
sys.setdefaultencoding('utf-8')
class StatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self,parent,-1)
        self.SetFieldsCount(2)
        self.SetStatusWidths([-2,-1])
        self.count=0
        self.gauge=wx.Gauge(self,-1,100,pos=(2,2),size=(265,20),style = wx.GA_HORIZONTAL)
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
    def setValue(self,value):
        self.gauge.SetValue(value)
class MainWindow(wx.Frame):
    '''定义一个窗口类'''
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000, 750),pos=wx.DefaultPosition,style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        now = datetime.datetime.now()
        self.now_time = now.strftime("%Y-%m-%d %H:%M:%S")
        date = now.strftime("%Y-%m-%d")
        ServersFrame.setupAllShow(self)
        self.bindRadio()
        self.bindCheck()
        self.bindBtnRun()
        self.bindBtnClear()
        self.bindBtnView()
        self.bindBtnKeyView()
        statusbar=self.CreateStatusBar(number=2)
        statusbar.SetStatusText("时间：%s"%(date),0)
        self.Show(True)
    def setuptime(self):
        self.Bind(wx.EVT_TIMER, self.OnTimeout,self.timer)
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
    def OnTimeout(self):
        print self.now_time
    def bindRadio(self):
        for eachRadio in [self.radio1, self.radio2, self.radio3]:
            self.Bind(wx.EVT_RADIOBUTTON, self.onRadio, eachRadio)
    def bindCheck(self):
        self.Bind(wx.EVT_CHECKBOX,self.onCheck,self.check1)
    def bindBtnRun(self):
            self.Bind(wx.EVT_BUTTON,self.onBtnRun,self.btn_run)
    def bindBtnClear(self):
        self.Bind(wx.EVT_BUTTON,self.onBtnClear,self.btn_clear)
    def bindBtnView(self):
        self.Bind(wx.EVT_BUTTON,self.onBtnView,self.btn_view)
    def bindBtnKeyView(self):
        self.Bind(wx.EVT_BUTTON,self.onBtnKeyView,self.btn_keyview)
    def onRadio(self,event):
        radioSelected=event.GetEventObject()
        self.radio1=radioSelected.GetLabel()
        if cmp(self.radio1,("执行命令".decode('gbk')))==0:
            self.txt_local.Enable(False)
            self.txt_remote.Enable(False)
            self.btn_view.Enable(False)
            self.txt_keypwd.Enable(False)
            self.txt_keyfile.Enable(False)
            self.btn_keyview.Enable(False)
            self.txt_cmd.Enable(True)
            # self.txt_cmd.SetBackgroundColour('#B0C4DE')
            if self.check1.GetValue():
                # self.txt_key.Enable(True)
                self.txt_keypwd.Enable(True)
                self.txt_keyfile.Enable(True)
                self.btn_keyview.Enable(True)
            else:
                # self.txt_key.Enable(False)
                self.txt_keypwd.Enable(False)
                self.txt_keyfile.Enable(False)
                self.btn_keyview.Enable(False)
        if cmp(self.radio1,("上传文件".decode('gbk')))==0:
            self.txt_local.Enable(True)
            self.txt_remote.Enable(True)
            self.btn_view.Enable(True)
            self.txt_cmd.Enable(False)
            self.txt_keypwd.Enable(False)
            self.txt_keyfile.Enable(False)
            self.btn_keyview.Enable(False)
            if self.check1.GetValue():
                # self.txt_key.Enable(True)
                self.txt_keypwd.Enable(True)
                self.txt_keyfile.Enable(True)
                self.btn_keyview.Enable(True)
            else:
                # self.txt_key.Enable(False)
                self.txt_keypwd.Enable(False)
                self.txt_keyfile.Enable(False)
                self.btn_keyview.Enable(False)
        if cmp(self.radio1,("下载文件".decode('gbk')))==0:
            self.txt_local.Enable(True)
            self.txt_remote.Enable(True)
            self.btn_view.Enable(True)
            self.txt_cmd.Enable(False)
            self.txt_keypwd.Enable(False)
            self.txt_keyfile.Enable(False)
            self.btn_keyview.Enable(False)
            if self.check1.GetValue():
                # self.txt_key.Enable(True)
                self.txt_keypwd.Enable(True)
                self.txt_keyfile.Enable(True)
                self.btn_keyview.Enable(True)
            else:
                # self.txt_key.Enable(False)
                self.txt_keypwd.Enable(False)
                self.txt_keyfile.Enable(False)
                self.btn_keyview.Enable(False)
    def onCheck(self,event):
        checkBox=event.GetEventObject()
        if checkBox.GetValue():
            # self.txt_key.Enable(True)
            self.txt_keypwd.Enable(True)
            self.txt_keyfile.Enable(True)
            self.btn_keyview.Enable(True)
        else:
            # self.txt_key.Enable(False)
            self.txt_keypwd.Enable(False)
            self.txt_keyfile.Enable(False)
            self.btn_keyview.Enable(False)
    def onBtnClear(self,event):
        self.txt_log.Clear()
    def onBtnView(self,event):
        # self.dialog=wx.FileDialog(self,message="Choose a file",defaultDir="",defaultFile="", wildcard="*.*", style=wx.OPEN)
        dir_dialog=wx.DirDialog(self,message=wx.DirSelectorPromptStr,defaultPath="",style=wx.DD_NEW_DIR_BUTTON,pos=wx.DefaultPosition)
        if dir_dialog.ShowModal()==wx.ID_OK:
            self.txt_local.SetValue(dir_dialog.GetPath())
            dir_dialog.Destroy()
    def onBtnKeyView(self,event):
        file_dialog=wx.FileDialog(self,message="选择Key文件",defaultDir="",defaultFile="", wildcard="*.*", style=wx.OPEN)
        # dir_dialog=wx.DirDialog(self,message=wx.DirSelectorPromptStr,defaultPath="",style=wx.DD_NEW_DIR_BUTTON,pos=wx.DefaultPosition)
        if file_dialog.ShowModal()==wx.ID_OK:
            self.txt_keyfile.SetValue(file_dialog.GetPath())
            print file_dialog.GetPath()
            file_dialog.Destroy()
    def onBtnRun(self,event):
        self.btn_run.Enable(False)
        self.cfail=[]
        self.cdone=[]
        self.count=0
        fileName='ssh_info.log'
        mode='w+'         #通过追加写日志文件
        file=open(fileName,mode)
        if cmp(self.radio1,("执行命令".decode('gbk')))==0:
            if self.check1.GetValue():
                self.setupCmdKey(file)
            else:
                self.setupCmd(file)
        if cmp(self.radio1,("上传文件".decode('gbk')))==0:
            if self.check1.GetValue():
                self.setupUploadKey(file)
            else:
                self.setupUpload(file)
        if cmp(self.radio1,("下载文件".decode('gbk')))==0:
            if self.check1.GetValue():
                self.setupDownloadKey(file)
            else:
                self.setupDownload(file)
    def setupCmd(self,file):
        self.cmds=[]
        value_info=self.txt_info.GetValue()
        line_info=self.txt_info.GetNumberOfLines()
        self.portstr=self.txt_port.GetValue()
        self.timeout=2
        self.username='root'
        if value_info=='':
            self.setupLog(args_log="IP及密码信息为空！！！")
        else:
            line_cmd=self.txt_cmd.GetNumberOfLines()
            value_cmd=self.txt_cmd.GetValue()
            if value_cmd=='':
                self.setupLog(args_log="命令信息为空!!!")
            else:
                if self.portstr=='':
                    self.setupLog(args_log="端口信息为空!!!")
                else:
                    self.port=int(self.portstr)
                    try:
                        for j in range(0,line_cmd,1):
                            line_cmds=self.txt_cmd.GetLineText(j).strip()
                            #获取命令
                            self.cmds.append(line_cmds)
                        self.setupLog(args_log="[Command:] %s"%(string.join(self.cmds)))
                    except Exception , e:
                        self.setupLog(args_log='**************************************************************')
                        self.setupLog(args_log="请检查命令信息是否正确！！！")
                    try:
                        threads=[]
                        self.setupLog(args_log='****ALL START CMD****')
                        file.write("****ALL START CMD****\n")
                        while self.txt_info.GetLineText(line_info-1)=='':
                            line_info-=1
                        else:
                            self.count=line_info
                            for i in range(0,line_info,1):
                                line=self.txt_info.GetLineText(i).split()
                                self.ips = line[0].strip()
                                self.pwds = line[1].strip()
                                thread=CmdThread(ip=self.ips,username=self.username,passwd=self.pwds,port=self.port,cmd=self.cmds,timeout=self.timeout,window=self,file=file)
                                thread.start()
                                # t=threading.Thread(target=self.ssh2,args=(self.ips,self.username,self.pwds,self.port,self.cmds,self.timeout,file))
                                # t.start()
                            # for i in range(0,line_info,1):
                            #     mutex.acquire()
                            #     threads[i].start()
                            #     mutex.release()
                            self.setupLog(args_log='服务器总数为[%d]台，开始执行……'%(self.count))
                    except Exception , e:
                        self.setupLog(args_log='**************************************************************')
                        self.setupLog(args_log="请检查IP及密码信息是否正确！！！")
                        self.setupLog(args_log="[error][ip]"+self.now_time+" "+str(e))
                        self.btn_run.Enable(True)
    def setupUpload(self,file):
        value_info=self.txt_info.GetValue()
        line_info=self.txt_info.GetNumberOfLines()
        self.portstr=self.txt_port.GetValue()
        self.username='root'
        if value_info=='':
            self.setupLog(args_log="IP及密码信息为空！！！")
            return
        else:
            self.local_dir=self.txt_local.GetValue()
            self.remote_dir=self.txt_remote.GetValue()
            if self.local_dir=="":
                self.setupLog(args_log="本地目录不能为空!!!")
            else:
                if self.remote_dir=="":
                    self.setupLog(args_log="远程目录不能为空!!!")
                else:
                    if self.portstr=='':
                        self.setupLog(args_log="端口信息为空!!!")
                    else:
                        self.port=int(self.portstr)
                        threads=[]
                        try:
                            self.setupLog(args_log='****ALL START UPLOAD****')
                            file.write("****ALL START UPLOAD****\n")
                            while self.txt_info.GetLineText(line_info-1)=='':
                                line_info-=1
                            else:
                                self.count=line_info
                                for i in range(0,line_info,1):
                                    line=self.txt_info.GetLineText(i).split()
                                    self.ips = line[0].strip()
                                    self.pwds = line[1].strip()
                                    uploadThread=UploadThread(ip=self.ips,username='root',port=self.port,passwd=self.pwds,local_dir=self.local_dir,remote_dir=self.remote_dir,window=self,file=file)
                                    uploadThread.start()
                                #     t=threading.Thread(target=self.upload,args=(self.ips,self.username,self.port,self.pwds,self.local_dir,self.remote_dir,file))
                                #     threads.append(t)
                                # for i in range(0,line_info,1):
                                #     mutex.acquire()
                                #     threads[i].start()
                                #     mutex.release()
                                self.setupLog(args_log='服务器总数为[%d]台，开始执行……'%(self.count))
                        except Exception , e:
                            self.setupLog(args_log='**************************************************************')
                            self.setupLog(args_log="请检查ip及密码信息是否正确!!!")
                            self.setupLog(args_log="[error][ip]"+self.now_time+" "+str(e))
                            self.btn_run.Enable(True)
    def setupDownload(self,file):
        value_info=self.txt_info.GetValue()
        line_info=self.txt_info.GetNumberOfLines()
        self.portstr=self.txt_port.GetValue()
        self.username='root'
        if value_info=='':
            self.setupLog(args_log="IP及密码信息为空！！！")
            return
        else:
            # try:
            self.local_dir=self.txt_local.GetValue()
            self.remote_dir=self.txt_remote.GetValue()
            if self.local_dir=="":
                self.setupLog(args_log="本地目录不能为空!!!")
            else:
                if self.remote_dir=="":
                    self.setupLog(args_log="远程目录不能为空!!!")
                else:
                    if self.portstr=='':
                        self.setupLog(args_log="端口信息为空!!!")
                    else:
                        threads=[]
                        self.port=int(self.portstr)
                        try:
                            self.setupLog(args_log='****ALL START DOWNLOAD****')
                            file.write("****ALL START DOWNLOAD****\n")
                            while self.txt_info.GetLineText(line_info-1)=='':
                                line_info-=1
                            else:
                                self.count=line_info
                                for i in range(0,line_info,1):
                                    line=self.txt_info.GetLineText(i).split()
                                    self.ips = line[0].strip()
                                    self.pwds = line[1].strip()
                                    print self.ips,self.pwds
                                    print
                                    downloadThread=DownloadThread(ip=self.ips,username=self.username,port=self.port,passwd=self.pwds,local_dir=self.local_dir,remote_dir=self.remote_dir,window=self,file=file)
                                    downloadThread.start()
                                #     t=threading.Thread(target=self.download,args=(self.ips,self.username,self.port,self.pwds,self.local_dir,self.remote_dir,file))
                                #     threads.append(t)
                                # for i in range(0,line_info,1):
                                #     mutex.acquire()
                                #     threads[i].start()
                                #     mutex.release()
                                self.setupLog(args_log='服务器总数为[%d]台，开始执行……'%(self.count))
                        except Exception , e:
                            self.setupLog(args_log='**************************************************************')
                            self.setupLog(args_log="请检查ip及密码信息是否正确!!!")
                            self.setupLog(args_log="[error][ip]"+self.now_time+" "+str(e))
                            self.btn_run.Enable(True)
    def setupCmdKey(self,file):
        self.cmds=[]
        value_info=self.txt_info.GetValue()
        line_info=self.txt_info.GetNumberOfLines()
        self.portstr=self.txt_port.GetValue()
        self.keyfile=self.txt_keyfile.GetValue()
        self.keypwd=self.txt_keypwd.GetValue()
        self.timeout=2
        self.username='root'
        if value_info=='':
            self.setupLog(args_log="IP及密码信息为空！！！")
        else:
            line_cmd=self.txt_cmd.GetNumberOfLines()
            value_cmd=self.txt_cmd.GetValue()
            if value_cmd=='':
                self.setupLog(args_log="命令信息为空!!!")
            else:
                if self.portstr=='':
                    self.setupLog(args_log="端口信息为空!!!")
                else:
                    self.port=int(self.portstr)
                    if self.keyfile=='':
                        self.setupLog(args_log="Key文件信息为空!!!")
                    else:
                        if self.keypwd=='':
                            self.setupLog(args_log="Key密码信息为空!!!")
                        else:
                            try:
                                for j in range(0,line_cmd,1):
                                    line_cmds=self.txt_cmd.GetLineText(j).strip()
                                    #获取命令
                                    self.cmds.append(line_cmds)
                                self.setupLog(args_log="[Command:] %s"%(string.join(self.cmds)))
                            except Exception , e:
                                self.setupLog(args_log='**************************************************************')
                                self.setupLog(args_log="请检查命令信息是否正确！！！")
                            try:
                                self.setupLog(args_log='****ALL START CMD****')
                                file.write("****ALL START CMD****\n")
                                threads=[]
                                while self.txt_info.GetLineText(line_info-1)=='':
                                    line_info-=1
                                else:
                                    self.count=line_info
                                    for i in range(0,line_info,1):
                                        line=self.txt_info.GetLineText(i).split()
                                        self.ips = line[0].strip()
                                        # t=threading.Thread(target=self.ssh2Key,args=(self.ips,self.username,self.port,self.cmds,self.timeout,self.keyfile,self.keypwd,file))
                                        # threads.append(t)
                                        thread=CmdKeyThread(ip=self.ips,username=self.username,port=self.port,cmd=self.cmds,timeout=self.timeout
                                            ,window=self,keypwd=self.keypwd,keyfile=self.keyfile,file=file)
                                        thread.start()
                                    # for i in range(0,line_info,1):
                                    #     mutex.acquire()
                                    #     threads[i].start()
                                    #     mutex.release()
                                    self.setupLog(args_log='服务器总数为[%d]台，开始执行……'%(self.count))
                            except Exception , e:
                                self.setupLog(args_log='**************************************************************')
                                self.setupLog(args_log="请检查IP及密码信息是否正确！！！")
                                self.setupLog(args_log="[error][ip]"+self.now_time+" "+str(e))
                                self.btn_run.Enable(True)
    def setupUploadKey(self,file):
        value_info=self.txt_info.GetValue()
        line_info=self.txt_info.GetNumberOfLines()
        self.portstr=self.txt_port.GetValue()
        self.keyfile=self.txt_keyfile.GetValue()
        self.keypwd=self.txt_keypwd.GetValue()
        self.username='root'
        if value_info=='':
            self.setupLog(args_log="IP及密码信息为空！！！")
            return
        else:
            self.local_dir=self.txt_local.GetValue()
            self.remote_dir=self.txt_remote.GetValue()
            if self.local_dir=="":
                self.setupLog(args_log="本地目录不能为空!!!")
            else:
                if self.remote_dir=="":
                    self.setupLog(args_log="远程目录不能为空!!!")
                else:
                    if self.portstr=='':
                        self.setupLog(args_log="端口信息为空!!!")
                    else:
                        self.port=int(self.portstr)
                        if self.keyfile=='':
                            self.setupLog(args_log="Key文件信息为空!!!")
                        else:
                            if self.keypwd=='':
                                self.setupLog(args_log="Key密码信息为空!!!")
                            else:
                                try:
                                    threads=[]
                                    self.setupLog(args_log='****ALL START UPLOAD****')
                                    file.write("****ALL START UPLOAD****\n")
                                    while self.txt_info.GetLineText(line_info-1)=='':
                                        line_info-=1
                                    else:
                                        self.count=line_info
                                        for i in range(0,line_info,1):
                                            line=self.txt_info.GetLineText(i).split()
                                            self.ips = line[0].strip()
                                            uploadKeyThread=UploadKeyThread(ip=self.ips,username='root',port=self.port,local_dir=self.local_dir ,remote_dir=self.remote_dir,window=self,keypwd=self.keypwd,keyfile=self.keyfile,file=file)
                                            uploadKeyThread.start()
                                        #     t=threading.Thread(target=self.uploadKey,args=(self.ips,self.username,self.port,self.local_dir,self.remote_dir,self.keyfile,self.keypwd,file))
                                        #     threads.append(t)
                                        # for i in range(0,line_info,1):
                                        #     mutex.acquire()
                                        #     threads[i].start()
                                        #     mutex.release()
                                        self.setupLog(args_log='服务器总数为[%d]台，开始执行……'%(self.count))
                                except Exception , e:
                                    self.setupLog(args_log='**************************************************************')
                                    self.setupLog(args_log="请检查ip及密码信息是否正确!!!")
                                    self.setupLog(args_log="[error][ip]"+self.now_time+" "+str(e))
                                    self.btn_run.Enable(True)
    def setupDownloadKey(self,file):
        value_info=self.txt_info.GetValue()
        line_info=self.txt_info.GetNumberOfLines()
        self.portstr=self.txt_port.GetValue()
        self.keyfile=self.txt_keyfile.GetValue()
        self.keypwd=self.txt_keypwd.GetValue()
        self.username='root'
        if value_info=='':
            self.setupLog(args_log="IP及密码信息为空！！！")
            return
        else:
            # try:
            self.local_dir=self.txt_local.GetValue()
            self.remote_dir=self.txt_remote.GetValue()
            if self.local_dir=="":
                self.setupLog(args_log="本地目录不能为空!!!")
            else:
                if self.remote_dir=="":
                    self.setupLog(args_log="远程目录不能为空!!!")
                else:
                    if self.portstr=='':
                        self.setupLog(args_log="端口信息为空!!!")
                    else:
                        self.port=int(self.portstr)
                        if self.keyfile=='':
                            self.setupLog(args_log="Key文件信息为空!!!")
                        else:
                            if self.keypwd=='':
                                self.setupLog(args_log="Key密码信息为空!!!")
                            else:
                                try:
                                    threads=[]
                                    self.setupLog(args_log='****ALL START DOWNLOAD****')
                                    file.write("****ALL START DOWNLOAD****\n")
                                    while self.txt_info.GetLineText(line_info-1)=='':
                                        line_info-=1
                                    else:
                                        self.count=line_info
                                        for i in range(0,line_info,1):
                                            line=self.txt_info.GetLineText(i).split()
                                            self.ips = line[0].strip()
                                            donwnloadKeyThread=DownloadKeyThread(ip=self.ips,username='root',port=self.port,local_dir=self.local_dir ,remote_dir=self.remote_dir,window=self,keypwd=self.keypwd,keyfile=self.keyfile,file=file)
                                            donwnloadKeyThread.start()
                                        #     t=threading.Thread(target=self.downloadKey,args=(self.ips,self.username,self.port,self.local_dir,self.remote_dir,self.keyfile,self.keypwd,file))
                                        #     threads.append(t)
                                        # for i in range(0,line_info,1):
                                        #     mutex.acquire()
                                        #     threads[i].start()
                                        #     mutex.release()
                                        self.setupLog(args_log='服务器总数为[%d]台，开始执行……'%(self.count))
                                except Exception , e:
                                    self.setupLog(args_log='**************************************************************')
                                    self.setupLog(args_log="请检查ip信息是否正确!!!")
                                    self.setupLog(args_log="[error][ip]"+self.now_time+" "+str(e))
                                    self.btn_run.Enable(True)
    def setupLog(self,args_log):
        # mutex.acquire()
        self.txt_log.AppendText(args_log+"\n")
        # mutex.release()
    def onAbout(self, evt):
        '''点击about的事件响应'''
        dlg = wx.MessageDialog(self, 'This app is a simple text editor', 'About my app', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    def onExit(self, evt):
        '''点击退出'''
        self.Close(True)
    def ssh2(self,ip,username,passwd,port,cmd,timeout,file):
        try:
           # paramiko.util.log_to_file('paramiko.log')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ip,port=port,username=username,password=passwd,timeout=timeout)
            # transport=ssh.get_transport()
            # channel=transport.open_session()
            # channel.settimeout(timeout)
            for m in cmd:
                # print m,
                stdin,stdout,stderr = ssh.exec_command(m,timeout=timeout)
                #stdin.write("Y")   #简单交互，输入 ‘Y’
                # out = stdout.readlines()
                # errorout=stderr.readlines()
                # out = unicode(stdout.read(),"gbk")
                # errorout=unicode(stderr.read(),"gbk")
                out=stdout.read()
                errorout=stderr.read()
                # print out,
                # if type(out).__name__!="unicode":
                #     str=unicode(out,"utf-8")
                #     print str
                # print out,
                if cmp(out,"")>0:
                    # print out
                    file.write("[succeed][cmd][%s]%s\n%s\n\n"%(ip,self.now_time,out))
                else:
                    file.write("[error][cmd][%s]%s****Cause by :%s\n\n"%(ip,self.now_time,errorout))
            ssh.close()
            self.cdone.append(ip)
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
            self.setupLog(args_log='ip:[%s]'%(ip))
        except Exception,e :
            self.cfail.append(ip)
            file.write("[error][cmd]%s\t%s\tError\t****Cause by :%s****end\n\n"%(ip,self.now_time,e))
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
            self.setupLog(args_log='ip:[%s] ***fail***'%(ip))
            print "[error][cmd][%s]\t%s\tError\t****Cause by :%s****end\n\n"%(ip,self.now_time,e)
            self.btn_run.Enable(True)
        finally:
            if self.count==(len(self.cdone)+len(self.cfail)):
                print "****ALL END CMD****\n"
                file.write("****ALL END CMD****\n")
                self.setupLog(args_log='****ALL END CMD****')
                self.btn_run.Enable(True)
                file.close()
    def download(self,ip, username, port,passwd, local_dir, remote_dir,file):
        try:
            print ip, username, port,passwd, local_dir, remote_dir,file
            paramiko.util.log_to_file('paramiko_download.log')
            t = paramiko.Transport((ip,port))
            t.connect(username=username,password=passwd)
            sftp = paramiko.SFTPClient.from_transport(t)
            files = sftp.listdir(remote_dir)
            for f in files:
                file.write("[succeed][download][%s] %s \n"%(ip,self.now_time))
                # self.setupLog(args_log='--------------------------------------------------------------')
                # self.setupLog(args_log="[succeed][download]"+self.now_time)
                file.write('Start to download file  from %s  %s \n' % (ip, datetime.datetime.now()))
                # self.setupLog(args_log='Start to download file  from %s  %s ' % (ip, datetime.datetime.now()))
                file.write('Downloading file:%s \n'%(os.path.join(remote_dir, f)))
                # self.setupLog(args_log='Downloading file:'+os.path.join(remote_dir, f))
                # self.setupLog(args_log='To dir:'+os.path.join(local_dir, f))
                file.write('To dir:%s \n'%(os.path.join(local_dir, f)))
                sftp.get(os.path.join(remote_dir, f), os.path.join(local_dir, f))#下载
                file.write('Download file success %s \n\n' % datetime.datetime.now())
                # self.setupLog(args_log='Download file success %s ' % datetime.datetime.now())
                # self.setupLog(args_log='--------------------------------------------------------------')
            t.close()
            self.cdone.append(ip)
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
        except Exception,e:
            self.cfail.append(ip)
            # self.setupLog(args_log='**************************************************************')
            # self.setupLog(args_log="[error][download]"+ip+" "+self.now_time+" "+str(e))
            print "[error][download]"+ip+" "+self.now_time+" "+str(e)
            file.write("[error][download]%s %s %s \n"%(ip,self.now_time,str(e)))
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
            self.btn_run.Enable(True)
        finally:
            if self.count==(len(self.cdone)+len(self.cfail)):
                print "****ALL END DOWNLOAD****\n"
                file.write("****ALL END DOWNLOAD****\n")
                self.setupLog(args_log='****ALL END DOWNLOAD****')
                self.btn_run.Enable(True)
                file.close()
    def upload(self,ip, username,port, passwd, local_dir, remote_dir,file):
        try:
            print ip, username,port, passwd, local_dir, remote_dir,file
            paramiko.util.log_to_file('paramiko_upload.log')
            t = paramiko.Transport((ip, port))
            t.connect(username=username, password=passwd)
            sftp = paramiko.SFTPClient.from_transport(t)
            #files = sftp.listdir(remote_dir)
            files = os.listdir(local_dir)
            for f in files:
                file.write("[succeed][upload][%s] %s \n"%(ip,self.now_time))
                # self.setupLog(args_log='--------------------------------------------------------------')
                file.write('Start to upload file  from %s  %s \n' % (ip, datetime.datetime.now()))
                # self.setupLog(args_log='Start to upload file  to %s  %s ' % (ip, datetime.datetime.now()))
                # self.setupLog(args_log='Uploading file:'+os.path.join(local_dir, f))
                file.write('Uploading file:%s \n'%(os.path.join(local_dir, f)))
                # self.setupLog(args_log='To dir:'+ os.path.join(remote_dir, f))
                file.write('To dir:%s \n'%(os.path.join(remote_dir, f)))
                sftp.put(os.path.join(local_dir, f), os.path.join(remote_dir, f))#上传
                file.write('Upload file success %s \n\n' % datetime.datetime.now())
                # self.setupLog(args_log='Upload file success %s ' % datetime.datetime.now())
                # self.setupLog(args_log='--------------------------------------------------------------')
            t.close()
            self.cdone.append(ip)
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
        except Exception,e:
            self.cfail.append(ip)
            # self.setupLog(args_log='**************************************************************')
            # self.setupLog(args_log="[error][upload]"+ip+" "+self.now_time+" "+str(e))
            print "[error][upload]"+ip+" "+self.now_time+" "+str(e)
            file.write("[error][upload]%s %s %s \n"%(ip,self.now_time,str(e)))
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
            self.btn_run.Enable(True)
        finally:
            if self.count==(len(self.cdone)+len(self.cfail)):
                print "****ALL END UPLOAD****\n"
                file.write("****ALL END UPLOAD****\n")
                self.setupLog(args_log='****ALL END UPLOAD****')
                self.btn_run.Enable(True)
                file.close()
    def ssh2Key(self,ip,username,port,cmd,timeout,keyfile,keypwd,file):
        try:
            paramiko.util.log_to_file('paramiko_cmd_key.log')
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            mykey=paramiko.DSSKey.from_private_key_file(filename=keyfile,password=keypwd)
            ssh.connect(hostname=ip,port=port,username=username , pkey=mykey,timeout=timeout)
            for m in cmd:
                stdin,stdout,stderr = ssh.exec_command(m,timeout=timeout)
                #stdin.write("Y")   #简单交互，输入 ‘Y’
                out=stdout.read()
                errorout=stderr.read()
                # print out
                # print errorout
                if cmp(out,"")>0:
                    file.write("[succeed][cmd][%s]%s\n%s\n\n"%(ip,self.now_time,out))
                    self.setupLog(args_log="[succeed][cmd][%s]%s\n%s"%(ip,self.now_time,out))
                else:
                    file.write("[error][cmd][%s]%s****Cause by :%s\n\n"%(ip,self.now_time,errorout))
                    self.setupLog(args_log="[error][cmd][%s]%s****Cause by :%s\n\n"%(ip,self.now_time,errorout))
            ssh.close()
            self.cdone.append(ip)
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
            self.setupLog(args_log='ip:[%s]'%(ip))
            self.btn_run.Enable(True)
        except Exception,e :
            self.cfail.append(ip)
            file.write("[error][cmd]%s\t%s\tError\t****Cause by :%s****end\n\n"%(ip,self.now_time,e))
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
            self.setupLog(args_log='ip:[%s] ***fail***'%(ip))
            print "[error][cmd][%s]\t%s\tError\t****Cause by :%s****end\n\n"%(ip,self.now_time,e)
        finally:
            if self.count==(len(self.cdone)+len(self.cfail)):
                print "****ALL END CMD****\n"
                file.write("****ALL END CMD****\n")
                self.setupLog(args_log='****ALL END CMD****')
                self.btn_run.Enable(True)
                file.close()
    def downloadKey(self,ip, username, port,local_dir, remote_dir,keyfile,keypwd,file):
        try:
            paramiko.util.log_to_file('paramiko_download_key.log')
            t = paramiko.Transport((ip,port))
            mykey=paramiko.DSSKey.from_private_key_file(filename=keyfile,password=keypwd)
            t.connect(username = username, pkey=mykey)
            sftp = paramiko.SFTPClient.from_transport(t)
            files = sftp.listdir(remote_dir)
            for f in files:
                file.write("[succeed][download][%s] %s \n"%(ip,self.now_time))
                # self.setupLog(args_log='--------------------------------------------------------------')
                # self.setupLog(args_log="[succeed][download]"+self.now_time)
                file.write('Start to download file  from %s  %s \n' % (ip, datetime.datetime.now()))
                # self.setupLog(args_log='Start to download file  from %s  %s ' % (ip, datetime.datetime.now()))
                file.write('Downloading file:%s \n'%(os.path.join(remote_dir, f)))
                # self.setupLog(args_log='Downloading file:'+os.path.join(remote_dir, f))
                # self.setupLog(args_log='To dir:'+os.path.join(local_dir, f))
                file.write('To dir:%s \n'%(os.path.join(local_dir, f)))
                sftp.get(os.path.join(remote_dir, f), os.path.join(local_dir, f))#下载
                file.write('Download file success %s \n\n' % datetime.datetime.now())
                # self.setupLog(args_log='Download file success %s ' % datetime.datetime.now())
                # self.setupLog(args_log='--------------------------------------------------------------')
            t.close()
            self.cdone.append(ip)
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
        except Exception,e:
            self.cfail.append(ip)
            # self.setupLog(args_log='**************************************************************')
            # self.setupLog(args_log="[error][download]"+ip+" "+self.now_time+" "+str(e))
            print "[error][download]"+ip+" "+self.now_time+" "+str(e)
            file.write("[error][download]%s %s %s \n"%(ip,self.now_time,str(e)))
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
            self.btn_run.Enable(True)
        finally:
            if self.count==(len(self.cdone)+len(self.cfail)):
                print "****ALL END DOWNLOAD****\n"
                file.write("****ALL END DOWNLOAD****\n")
                self.setupLog(args_log='****ALL END DOWNLOAD****')
                self.btn_run.Enable(True)
                file.close()
    def uploadKey(self,ip, username,port, local_dir, remote_dir,keyfile,keypwd,file):
        try:
            paramiko.util.log_to_file('paramiko_upload_key.log')
            t = paramiko.Transport((ip, port))
            mykey=paramiko.DSSKey.from_private_key_file(filename=keyfile,password=keypwd)
            t.connect(username = username, pkey=mykey)
            sftp = paramiko.SFTPClient.from_transport(t)
            #files = sftp.listdir(remote_dir)
            files = os.listdir(local_dir)
            for f in files:
                file.write("[succeed][upload][%s] %s \n"%(ip,self.now_time))
                # self.setupLog(args_log='--------------------------------------------------------------')
                file.write('Start to upload file  from %s  %s \n' % (ip, datetime.datetime.now()))
                # self.setupLog(args_log='Start to upload file  to %s  %s ' % (ip, datetime.datetime.now()))
                # self.setupLog(args_log='Uploading file:'+os.path.join(local_dir, f))
                file.write('Uploading file:%s \n'%(os.path.join(local_dir, f)))
                # self.setupLog(args_log='To dir:'+ os.path.join(remote_dir, f))
                file.write('To dir:%s \n'%(os.path.join(remote_dir, f)))
                sftp.put(os.path.join(local_dir, f), os.path.join(remote_dir, f))#上传
                file.write('Upload file success %s \n\n' % datetime.datetime.now())
                # self.setupLog(args_log='Upload file success %s ' % datetime.datetime.now())
                # self.setupLog(args_log='--------------------------------------------------------------')
            t.close()
            self.cdone.append(ip)
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
        except Exception,e:
            self.cfail.append(ip)
            # self.setupLog(args_log='**************************************************************')
            # self.setupLog(args_log="[error][upload]"+ip+" "+self.now_time+" "+str(e))
            print "[error][upload]"+ip+" "+self.now_time+" "+str(e)
            file.write("[error][upload]%s %s %s \n"%(ip,self.now_time,str(e)))
            self.setupLog(args_log='服务器总数为[%d]台，正在操作第[%d]台，执行未通过[%d]台'%(self.count,len(self.cdone)+len(self.cfail),len(self.cfail)))
            self.btn_run.Enable(True)
        finally:
            if self.count==(len(self.cdone)+len(self.cfail)):
                print "****ALL END UPLOAD****\n"
                file.write("****ALL END UPLOAD****\n")
                self.setupLog(args_log='****ALL END UPLOAD****')
                self.btn_run.Enable(True)
                file.close()
class CmdThread(threading.Thread):
    def __init__(self,ip,username,passwd,port,cmd,window,timeout,file):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username=username
        self.port=port
        self.passwd=passwd
        self.cmd=cmd
        self.timeout=timeout
        self.window = window
        # self.timeToQuit = threading.Event()
        self.file=file
    def run(self):
        mutex.acquire()
        self.window.ssh2(self.ip,self.username,self.passwd,self.port,self.cmd,self.timeout,self.file)
        mutex.release()
class UploadThread(threading.Thread):
    def __init__(self,ip,username,port,passwd,local_dir,remote_dir, window,file):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username=username
        self.passwd=passwd
        self.local_dir=local_dir
        self.remote_dir=remote_dir
        self.window = window
        self.port=port
        self.file=file
    def run(self):
        mutex.acquire()
        self.window.upload(self.ip,self.username,self.port,self.passwd,self.local_dir,self.remote_dir,self.file)
        mutex.release()
class DownloadThread(threading.Thread):
    def __init__(self,ip,username,port,passwd,local_dir,remote_dir, window,file):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username=username
        self.passwd=passwd
        self.local_dir=local_dir
        self.remote_dir=remote_dir
        self.window = window
        self.port=port
        # self.timeToQuit = threading.Event()
        self.file=file
    def run(self):
        mutex.acquire()
        self.window.download(self.ip,self.username,self.port,self.passwd,self.local_dir,self.remote_dir,self.file)
        mutex.release()
class CmdThread(threading.Thread):
    def __init__(self,ip,username,passwd,port,cmd,window,timeout,file):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username=username
        self.port=port
        self.passwd=passwd
        self.cmd=cmd
        self.timeout=timeout
        self.window = window
        self.file=file
    def run(self):
        mutex.acquire()
        self.window.ssh2(self.ip,self.username,self.passwd,self.port,self.cmd,self.timeout,self.file)
        mutex.release()
class CmdKeyThread(threading.Thread):
    def __init__(self,ip,username,port,cmd,window,timeout,keyfile,keypwd,file):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username=username
        self.port=port
        self.keyfile=keyfile
        self.keypwd=keypwd
        self.cmd=cmd
        self.timeout=timeout
        self.window = window
        # self.timeToQuit = threading.Event()
        self.file=file
    def run(self):
        mutex.acquire()
        # print "%s %s %d %s %d %s %s %s"%(self.ip,self.username,self.port,self.cmd,self.timeout,self.keyfile,self.keypwd,self.file)
        self.window.ssh2Key(self.ip,self.username,self.port,self.cmd,self.timeout,self.keyfile,self.keypwd,self.file)
        #def ssh2Key(self,ip,username,port,cmd,timeout,keyfile,keypwd,file):
        mutex.release()
class UploadKeyThread(threading.Thread):
    def __init__(self,ip,username,port,local_dir,remote_dir, window,keyfile,keypwd,file):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username=username
        self.keyfile=keyfile
        self.keypwd=keypwd
        self.local_dir=local_dir
        self.remote_dir=remote_dir
        self.window = window
        self.port=port
        # self.timeToQuit = threading.Event()
        self.file=file
    def run(self):
        mutex.acquire()
        self.window.uploadKey(self.ip,self.username,self.port,self.local_dir,self.remote_dir,self.keyfile,self.keypwd,self.file)
        mutex.release()
class DownloadKeyThread(threading.Thread):
    def __init__(self,ip,username,port,local_dir,remote_dir, window,keyfile,keypwd,file):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username=username
        self.keyfile=keyfile
        self.keypwd=keypwd
        self.local_dir=local_dir
        self.remote_dir=remote_dir
        self.window = window
        self.port=port
        # self.timeToQuit = threading.Event()
        self.file=file
    def run(self):
        mutex.acquire()
        self.window.downloadKey(self.ip,self.username,self.port,self.local_dir,self.remote_dir,self.keyfile,self.keypwd,self.file)
        mutex.release()
mutex = threading.RLock()
app = wx.App(redirect=False)
frame = MainWindow(None, 'LINUX服务器批量管理工具v1.1')
app.MainLoop() #循环监听事件
