#-*- coding:utf-8 -*-
import os
from subprocess import *

args = ['pylupdate4']
for parent,dirname,filename in os.walk("."):
	for f in filename:
		subfix = os.path.splitext(f)[1]
		if subfix == ".py" and f != "makeTS.py":
			args.append(f)
args.append('-ts')
args.append('qt_zh_Tids.ts')

print args
#把文件都指向了'qt_zh_Tids.ts'
Popen(args)
#运行完之后自动打开'qt_zh_Tids.ts'
Popen(['linguist','qt_zh_Tids.ts'])