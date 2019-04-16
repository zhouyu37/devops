#_*_coding:utf-8_*_
import os,sys,platform

if platform.system() == "Windows":
    BASE_DIR = '\\'.join(os.path.abspath(os.path.dirname(__file__)).split('\\')[:-1])
else:
    BASE_DIR = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[:-1])
sys.path.append(BASE_DIR)

from core import ClientStark

if __name__ == "__main__":
    ClientStark.ArgvHandler(sys.argv)
