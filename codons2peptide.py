'''
Codons2Peptide.py - A codon to peptide converter. 

This script recreates the biological translation of DNA into polypeptides. The 
DNA sequence can be in the form of a string or a file containing multiple 
strings. The output can either be printed into a specified file, or, by 
default, to the stdout.

Only built for Python 3, but no third-party modules are necessary. This script 
is also only runnable on the command line, and not as an import module. 

For any synthetic biologists, changes to the conversion table and 
allowed nucleotides can be done within the script:
    * Conversion table -> line 57
    * Legal nucleotides -> line 111

@author: Ivan Alexander Kristanto
'''

import sys 
import argparse
import os
import re


# Setting the Command-Line Arguments.
parser = argparse.ArgumentParser(
    description='Codons2Peptide - A DNA to peptide sequence converter.'
)
parser.add_argument(
    'input',
    metavar='<input-codon>',
    type=str,
    help='the codon sequence, as a STRING. Unless \'-f\' is specified.',
)
parser.add_argument(
   '-f',
   '--file',
   help='indicates input is a FILE containing codon sequence(s); one sequence per line.',
   action='store_true' 
)
parser.add_argument(
   '-o',
   '--output',
   help='specifies an output file; will overwrite any existing one.',
   action='store' 
)

# Parsing Arguments
args = parser.parse_args()
is_file: bool = not not args.file
outfile: str or None = args.output
    

# Conversion Table
conversion = {
    "ATA": "I", "ATC": "I", "ATT": "I", "ATG": "M",
    "ACA": "T", "ACC": "T", "ACG": "T", "ACT": "T",
    "AAC": "N", "AAT": "N", "AAA": "K", "AAG": "K",
    "AGC": "S", "AGT": "S", "AGA": "R", "AGG": "R",
    "CTA": "L", "CTC": "L", "CTG": "L", "CTT": "L",
    "CCA": "P", "CCC": "P", "CCG": "P", "CCT": "P",
    "CAC": "H", "CAT": "H", "CAA": "Q", "CAG": "Q",
    "CGA": "R", "CGC": "R", "CGG": "R", "CGT": "R",
    "GTA": "V", "GTC": "V", "GTG": "V", "GTT": "V",
    "GCA": "A", "GCC": "A", "GCG": "A", "GCT": "A",
    "GAC": "D", "GAT": "D", "GAA": "E", "GAG": "E",
    "GGA": "G", "GGC": "G", "GGG": "G", "GGT": "G",
    "TCA": "S", "TCC": "S", "TCG": "S", "TCT": "S",
    "TTC": "F", "TTT": "F", "TTA": "L", "TTG": "L",
    "TAC": "Y", "TAT": "Y", "TAA": "*", "TAG": "*",
    "TGC": "C", "TGT": "C", "TGA": "*", "TGG": "W"
}


# Defining Helper Functions 
def triplet2aa(codon: str) -> str:
    '''Converts a single codon into its corresponding amino acid.'''

    aa = conversion.get(codon, False)

    if not aa:
        print(f'Error: Conversion table is not complete. \'{codon}\' does not have an associated amino acid.')
    elif aa == '*':
        return ''

    return aa

def get_start() -> str:
    '''Obtains the start codon.'''

    for key, value in conversion.items():
        if 'M' == value:
            return key
    print('Error: The start codon is not defined.')
    sys.exit()

def process_output(peptides: str) -> None:
    '''Sends output to STDOUT or a file, depending on --output.'''

    if outfile:
        with open(outfile, 'w') as f:
            f.write(peptides)
            f.write('\n')
    else:
        print(peptides)


# One-time Regex Compilations.
re_dna = re.compile(r"[^ACTG]+");
re_start = re.compile(get_start());   


# Defining Main Functions 
def translation(dna: str) -> str: 
    '''Translates a DNA sequence into its corresponding polypeptide.

    Args:
        dna (str): the DNA sequence

    Returns:
        peptides (str): the poplypeptide
    '''

    dna: str = dna.upper()

    # Checks for non-nucleotide characters in DNA.
    if re_dna.search(dna):
        print('Error: Sequence must only contain A/T/C/G/a/t/c/g.')
        print(f'## Sequence: {dna}')
        sys.exit()

    # Checks for short DNA's.
    if len(dna) < 3:
        print('Error: DNA is too short. Must be at least 3 nucleotides long.')
        sys.exit()

    start_codon = re_start.search(dna)
    if not start_codon:
        return ''
        
    # Construct ORF and translate each codon.
    index_start_codon: int = start_codon.start()
    ORF: str = dna[index_start_codon:]
    peptide: str  = ''

    for trip in range(len(dna) // 3):
        i = trip * 3
        codon: str = ORF[i: i + 3]

        aa: str = triplet2aa(codon)

        if not aa:
            break

        peptide += aa

    process_output(peptide)

    return peptide

def file_translation(file_in: str) -> list:
    '''Translate a file containing DNA sequences into their polypeptides.

    Args:
        file_in (str): the location and name of the file containing the DNA sequences, delimited by newlines.

    Returns:
        peptides (list): the corresponding poplypeptides
    '''

    # Checking the arguments passed.
    if not os.path.isfile(args.input):
        print('Error: The input file specified does not exist.')
        sys.exit()

    with open(file_in, 'r') as f:
        codons_raw: list = f.read().splitlines()
        codons = list(filter(None, codons_raw)) 

    peptides = list(map(translation, codons))

    process_output('\n'.join(peptides))

    return peptides


def main():
    if is_file:
        file_translation(args.input)
    else:
        translation(args.input)


if __name__ == "__main__":
    main()
