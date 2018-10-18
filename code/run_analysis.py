#! /usr/bin/python
# -*- coding: utf-8 -*-
import glob
import os
import pickle
from code.Wrappers import ClustalOWrapper, ClustalWWrapper, MuscleWrapper, BaliScoreWrapper
from code.Parsers import NotProperNumberException


class SPTC(object):
    def __init__(self, sp, tc):
        super().__init__()
        self.sp = sp
        self.tc = tc

    def __str__(self):
        return 'SP: {:.3f}, TC:{:.3f}'.format(self.sp, self.tc)


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
        return Result(cow_results, cww_results, mw_results), times


if __name__ == '__main__':
    anal = Analysis()
    ref_sets = ('1.2', '10', '2')
    path_string = 'data/ref_%s/*.msf'
    for ref_set in ref_sets:
        pattern = path_string%ref_set
        res_dict = {}
        for path in glob.glob(pattern):
            base = path[:-3]
            print(base)
            try:
                res, times = anal.run(base + 'tfa', 'temp/blah', path)
                print(res)
                print(times)
                res_dict[base] = (res, times)
            except NotProperNumberException:
                continue
        with open(os.path.join('res', ref_set+'.dump'), 'wb') as f:
            pickle.dump(res_dict, f)