#!/usr/bin/env python3

import os
import sys
import argparse

def main():

    # parse command line
    parser = argparse.ArgumentParser()
    # First define all option groups
    group1 = parser.add_argument_group('Input files', 'Required input')
    group1.add_argument("-f", "--fastq", default="", type=str, dest="f",
                        help="input reads in fastq format")

    # exit so that log file is not written
    if len(sys.argv) == 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
        parser.print_help()
        sys.exit()

    import logging
    import logging.handlers

    logging.basicConfig(filename='minvar.log', level=logging.DEBUG,
                        format='%(levelname)s %(asctime)s %(filename)s: %(funcName)s() %(lineno)d: \t%(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    logging.info(' '.join(sys.argv))

    args = parser.parse_args()

    from minvar import prepare
    cns_file, prepared_bam = prepare.main(args.f)

    from minvar import callvar
    called_file = callvar.main(ref_file=cns_file, bamfile=prepared_bam,
                               caller='lofreq', recalibrate=False)

    from minvar import annotate
    annotate.main(vcf_file=called_file, ref_file=cns_file)

    from minvar import reportdrm
    reportdrm.main()

    from minvar import stats
    stats.coverage_stats(prepared_bam)

if __name__ == "__main__": #  and __package__ is None:
    main()
