#!/usr/bin/env python3

__author__ = 'jtravis'

import sys

import itertools
import sys
from nasp2.matrix_DTO import parse_dto


def explain(matrix_parameters, sample_groups):
    from nasp2.analyze import sample_positions, analyze_position

    while True:
        try:
            print('\a')
            contig_name, _, position = input("Enter LocusID: ").partition('::')
            index = int(position) - 1
        except ValueError:
            print('LocusID is <contig name>::<position number> such as 500WT1::42')
            continue
        reference_contig = matrix_parameters.reference_fasta.get_contig(contig_name)
        dups_contig = matrix_parameters.reference_dups.get_contig(contig_name)
        print("Contig Objects:")
        print(reference_contig)
        print(dups_contig)
        for sample in sample_groups:
            print(sample[0].name)
            for analysis in sample:
                print('\t', analysis.get_contig(reference_contig.name))
        
        print("Scanning files...")
        for idx, row in enumerate(zip(reference_contig.positions, dups_contig.positions, sample_positions(reference_contig.name, sample_groups))):
            if index == idx:
                print('\a')
                #print('Positions:', "\n".join(str(row)), '\n')
                print('Position Analysis:')
                print(analyze_position(row[0], row[1], row[2]))
                break


def main():
    from nasp2.matrix_DTO import parse_dto
    print("Building contig indices...")
    matrix_parameters, sample_groups = parse_dto(sys.argv[1])
    print("Starting analysis...")

    if len(sys.argv) > 2 and sys.argv[2] == "explain":
        return explain(matrix_parameters, sample_groups)

    #for ref, dup in zip(matrix_parameters.reference_fasta.contigs, matrix_parameters.reference_dups.contigs):
    #    if ref.name == dup.name:
    #        print(ref.name, dup.name)
    #    else:
    #        print('\t', ref.name, dup.name)
        
    from nasp2.analyze import analyze_samples

    analyze_samples(matrix_parameters.reference_fasta, matrix_parameters.reference_dups, sample_groups)


if __name__ == '__main__':
    main()