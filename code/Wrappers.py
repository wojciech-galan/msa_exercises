#! /usr/bin/python
# -*- coding: utf-8 -*-

import abc
import subprocess

from code.Parsers import parse_blaliscore_v2_output
from code.timer import timeit


class ToolWrapper(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    @timeit
    def run(self, infile: str, outfile: str, **kwargs):
        command = self.command.format(**{'infile': infile, 'outfile': outfile})
        subprocess.run(command, shell=True, stdout=subprocess.PIPE)


class ClustalWWrapper(ToolWrapper):
    command = 'clustalw -INFILE={infile} -OUTPUT=GCG -OUTFILE={outfile}'

    def __init__(self):
        super().__init__()

    def run(self, infile: str, outfile: str, **kwargs):
        super().run(infile, outfile, **kwargs)


class ClustalOWrapper(ToolWrapper):
    command = 'clustalo -i {infile} --outfmt=msf -o {outfile} --force'

    def __init__(self):
        super().__init__()

    def run(self, infile: str, outfile: str, **kwargs):
        super().run(infile, outfile, **kwargs)


class MuscleWrapper(ToolWrapper):
    command = 'muscle -in {infile} -msf -out {outfile} -QUIET'

    def __init__(self):
        super().__init__()

    def run(self, infile: str, outfile: str, **kwargs):
        super().run(infile, outfile, **kwargs)


class BaliScoreWrapper(object):
    command = 'bali_score {reference_alignment} {test_alignment} '

    def __init__(self):
        super().__init__()

    def run(self, reference_alignment: str, test_alignment: str):
        command = self.command.format(**{'reference_alignment': reference_alignment, 'test_alignment': test_alignment})
        output = subprocess.check_output(command, shell=True)
        return parse_blaliscore_v2_output(output)


if __name__ == '__main__':
    cw = MuscleWrapper()
    import os

    print(os.listdir('.'))
    cw.run('data/ref_1.2/BB12001.tfa', 'temp/test.out')
    bs = BaliScoreWrapper()
    print(bs.run('data/ref_1.2/BB12001.msf', 'temp/test.out'))
