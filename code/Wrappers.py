#! /usr/bin/python
# -*- coding: utf-8 -*-

import abc
import subprocess

class MSAToolWrapper(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def run(self, infile:str, outfile:str):
        command = self.command.format(**{'infile':infile, 'outfile':outfile})
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)

class ClustalWWrapper(MSAToolWrapper):
    command = 'clustalw -INFILE={infile} -OUTPUT=msf -OUTFILE={outfile}'
    def __init__(self):
        super().__init__()

    def run(self, infile:str, outfile:str):
        super().run(infile, outfile)

class ClustalOWrapper(MSAToolWrapper):
    command = 'clustalo -infile={infile} -outfmt=msf -outfile={outfile}'
    def __init__(self):
        super().__init__()

    def run(self, infile:str, outfile:str):
        super().run(infile, outfile)


if __name__ == '__main__':
    cw = ClustalWWrapper()
    import os
    print(os.listdir('.'))
    cw.run('test', 'test.out')