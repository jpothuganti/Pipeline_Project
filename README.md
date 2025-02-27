# Pipeline_Project
Pipeline project for comp 383

To run the code run the wrapper.py file in the same directory as the fastq files

Dependencies Needed to run the following pipeline:

Libraries:
biopython (pip install biopython)

Command line tools:

NCBI Datasets

SRA Toolkit

Bowtie2

SAMtools

SPAdes

Blast+


Step 1:

First run the following commands

- wget https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos5/sra-pub-zq-14/SRR005/660/SRR5660030.sralite.1

- wget https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos5/sra-pub-zq-14/SRR005/660/SRR5660033.sralite.1

The links come from the NCBI database under data access from the SRR numbers

Use the commands

- fastq-dump --split-files --outdir ./ SRR5660030.sralite.1

- fastq-dump --split-files --outdir ./ SRR5660033.sralite.1

Store those locally as they are too big to be pushed to git

Then run the commands

- head -n 40000 /home/2025/jpothuganti/Pipeline_Files/SRR5660030.sralite.1_1.fastq > SRR5660030_1.fastq

- head -n 40000 /home/2025/jpothuganti/Pipeline_Files/SRR5660030.sralite.1_2.fastq > SRR5660030_2.fastq

- head -n 40000 /home/2025/jpothuganti/Pipeline_Files/SRR5660033.sralite.1_1.fastq > SRR5660033_1.fastq

- head -n 40000 /home/2025/jpothuganti/Pipeline_Files/SRR5660033.sralite.1_2.fastq > SRR5660033_2.fastq

- git add SRR5660030_1.fastq

- git add SRR5660030_2.fastq

- git add SRR5660033_1.fastq

- git add SRR5660033_2.fastq

- git commit -m "update"

- git push

Now the first 10,000 reads are stored in git.

