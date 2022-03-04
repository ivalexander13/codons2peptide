# Codons2Peptide
By Ivan Alexander Kristanto; for an Inscripta Technical Screening.

This script recreates the biological translation of DNA into polypeptides. The 
DNA sequence can be in the form of a string or a file containing multiple 
strings. The output can either be printed into a specified file, or, by 
default, to the stdout.

Only built for Python 3, but no third-party modules are necessary. This script 
is also only runnable on the command line, and not as an import module. 

For any synthetic biologists, changes to the conversion table and 
allowed nucleotides can be done within the script:

- Conversion table -> `line 57`
- Legal nucleotides -> `line 111`


## Usage
Run the codons2peptide.py script in the command line:
```
python codons2peptide.py [-h] [-f] [-o OUTPUT] <input-codon>
```

Where:

- **input-codon**: the codon sequence, as a STRING. Unless '-f' is specified.
- **-h, --help**: show a help message.
- **-f, --file**: indicates input is a FILE containing codon sequence(s); one sequence per line.
- **-o OUTPUT, --output OUTPUT**: specifies an output file; will overwrite any existing one.

## Example Usage
Run this where the main script is located:
```
python codons2peptide.py -f ./data/codons.txt -o ./data/out.txt
```