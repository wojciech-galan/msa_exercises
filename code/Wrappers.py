#! /usr/bin/python
# -*- coding: utf-8 -*-

import abc
import subprocess

from code.Parsers import parse_blaliscore_v2_output

class ToolWrapper(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def run(self, infile:str, outfile:str):
        command = self.command.format(**{'infile':infile, 'outfile':outfile})
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)

class ClustalWWrapper(ToolWrapper):
    command = 'clustalw -INFILE={infile} -OUTPUT=GCG -OUTFILE={outfile}'
    def __init__(self):
        super().__init__()

    def run(self, infile:str, outfile:str):
        super().run(infile, outfile)

class ClustalOWrapper(ToolWrapper):
    command = 'clustalo -i {infile} --outfmt=msf -o {outfile} --force'
    def __init__(self):
        super().__init__()

    def run(self, infile:str, outfile:str):
        super().run(infile, outfile)

class MuscleWrapper(ToolWrapper):
    command = 'muscle -in {infile} -msf -out {outfile} -QUIET'
    def __init__(self):
        super().__init__()

    def run(self, infile:str, outfile:str):
        super().run(infile, outfile)

class BaliScoreWrapper(object):
    command = 'bali_score_old {reference_alignment} {test_alignment} '
    def __init__(self):
        super().__init__()

    def run(self, reference_alignment:str, test_alignment:str):
        command = self.command.format(**{'reference_alignment':reference_alignment, 'test_alignment':test_alignment})
        output = subprocess.check_output(command, shell=True)
        return parse_blaliscore_v2_output(output)


if __name__ == '__main__':
    cw = MuscleWrapper()
    import os
    print(os.listdir('.'))
    cw.run('data/ref_1.2/BB12001.tfa', 'temp/test.out')
    bs = BaliScoreWrapper()
    print(bs.run('data/ref_1.2/BB12001.msf', 'temp/test.out'))