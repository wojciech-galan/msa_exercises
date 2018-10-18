#! /usr/bin/python
# -*- coding: utf-8 -*-
import glob
from code.Wrappers import ClustalOWrapper, ClustalWWrapper, MuscleWrapper, BaliScoreWrapper
from code.Parsers import NotProperNumberException


class SPTC(object):
    def __init__(self, sp, tc):
        super().__init__()
        self.sp = sp
        self.tc = tc

    def __str__(self):
        return 'SP: {}, TC:{}'.format(self.sp, self.tc)


class Result(object):
    def __init__(self, clustal_omega_data: SPTC, clustal_w_data: SPTC, muscle_data: SPTC):
        super().__init__()
        self.co = clustal_omega_data
        self.cw = clustal_w_data
        self.mu = muscle_data

    def __str__(self):
        return 'ClustalOmega: {}, ClustalW: {}, Muscle: {}'.format(self.co, self.cw, self.mu)


class Analysis(object):
    def __init__(self):
        super().__init__()
        self.cow = ClustalOWrapper()
        self.cww = ClustalWWrapper()
        self.mw = MuscleWrapper()
        self.bsw = BaliScoreWrapper()

    def run(self, seqs_to_be_aligned_path: str, test_alignment_path: str, reference_alignment_path: str):
        times = {}
        self.cow.run(seqs_to_be_aligned_path, test_alignment_path, log_time=times, log_name='cl_omega')
        cow_results = SPTC(*self.bsw.run(reference_alignment_path, test_alignment_path))
        self.cww.run(seqs_to_be_aligned_path, test_alignment_path, log_time=times, log_name='cl_w')
        cww_results = SPTC(*self.bsw.run(reference_alignment_path, test_alignment_path))
        self.mw.run(seqs_to_be_aligned_path, test_alignment_path, log_time=times, log_name='muscle')
        mw_results = SPTC(*self.bsw.run(reference_alignment_path, test_alignment_path))
        print(times)
        return Result(cow_results, cww_results, mw_results)


if __name__ == '__main__':
    anal = Analysis()
    for path in glob.glob('data/ref_10/*.msf'):
        base = path[:-3]
        print(base)
        try:
            print(anal.run(base + 'tfa', 'temp/blah10', path))
        except NotProperNumberException:
            continue
