#import libraries
import os
from Bio import SeqIO

#create output directory
directory = 'PipelineProject_Jay_Pothuganti'
os.system(f'mkdir -p {directory}')
os.chdir(directory)

#download the dataset from ncbi and unzip the data
os.system('datasets download virus genome accession NC_006273.2')
os.system('unzip ncbi_dataset.zip')

''' These commands are used to get the fastq files that are in github
#move this chunk to a seperate directory -large files wont be pushed to git
#download the datasets and split them into forward and backward reads
os.system('prefetch SRR5660030')
os.system('prefetch SRR5660033')
os.system('fastq-dump --split-files SRR5660030/SRR5660030.sra')
os.system('fastq-dump --split-files SRR5660033/SRR5660033.sra')

#create the sample test data
#os.system('head -n 40000 WholeFiles/SRR5660030_1.fastq > SRR5660030_1.fastq')
#os.system('head -n 40000 WholeFiles/SRR5660030_2.fastq > SRR5660030_2.fastq')
#os.system('head -n 40000 WholeFiles/SRR5660033_1.fastq > SRR5660033_1.fastq')
#os.system('head -n 40000 WholeFiles/SRR5660033_2.fastq > SRR5660033_2.fastq')
'''

#create a directory
os.system('mkdir bowtie2')
#use bowtie2 to create an index
os.system('bowtie2-build ncbi_dataset/data/genomic.fna bowtie2/NC_006273.2')

#create a sam file from the paired fastq files
os.system('bowtie2 -x bowtie2/NC_006273.2 -1 FastqFiles/SRR5660030_1.fastq -2 FastqFiles/SRR5660030_2.fastq -S SRR5660030.sam')
os.system('bowtie2 -x bowtie2/NC_006273.2 -1 FastqFiles/SRR5660033_1.fastq -2 FastqFiles/SRR5660033_2.fastq -S SRR5660033.sam')
#compress the sam files to bam files and only keep the reads that map to the index
os.system('samtools view -b -F 4 SRR5660030.sam > SRR5660030_mapped.bam')
os.system('samtools view -b -F 4 SRR5660033.sam > SRR5660033_mapped.bam')
#use the bam files to create filtered fastqs and ignore reads that arent in both forward and reverse to use for spades
os.system('samtools fastq -f 3 -1 SRR5660030_mapped_1.fastq -2 SRR5660030_mapped_2.fastq SRR5660030_mapped.bam')
os.system('samtools fastq -f 3 -1 SRR5660033_mapped_1.fastq -2 SRR5660033_mapped_2.fastq SRR5660033_mapped.bam')
#line count of original data (divide by 4 for number of reads)
before2 = os.system('wc -l SRR5660030_1.fastq')
before6 = os.system('wc -l SRR5660033_1.fastq')
#line count of filtered data (divide by 4 for number of reads)
after2 = os.system('wc -l SRR5660030_mapped_1.fastq')
after6 = os.system('wc -l SRR5660033_mapped_1.fastq')

#run spades based on the forward and backwards reads that map
os.system('spades.py --pe1-1 SRR5660030_mapped_1.fastq --pe1-2 SRR5660030_mapped_2.fastq --pe2-1 SRR5660033_mapped_1.fastq --pe2-2 SRR5660033_mapped_2.fastq -k 99 -o spades')

#initialize variables
contigs = 0
bps = 0
#open contigs file from spades
with open('spades/contigs.fasta', 'r') as f:
    #itterate through the file
    for line in f:
        line = line.strip()
        #only look at header files
        if line.startswith('>'):
            #length is given in the header so a list can be indexed to retrieve the value
            info = line.split('_')
            length = int(info[3])
            #only look at contigs longer than 1000 bp
            if length > 1000:
                #add 1 number of contigs and length to total base pairs
                contigs += 1
                bps += length
with open('PipelineProject.log', 'w') as log:
    log.write(f'Donor 1 (2dpi) had {before2}] read pairs before Bowtie2 filtering and {after2} readpairs after.\n')
    log.write(f'Donor 1 (6dpi) had {before6}] read pairs before Bowtie2 filtering and {after6} readpairs after.\n')
    log.write(f'There are {contigs} contigs > 1000 bp in the assembly.\n')
    log.write(f'There are {bps} bp in the assembly.\n')

#read the longes contig from spades
with open('spades/contigs.fasta', 'r') as handle:
    longest_contig = max(SeqIO.parse(handle, 'fasta'), key=lambda record: len(record.seq))
print(longest_contig)
#create a fasta file with just the longest contig
with open('longest_contig.fasta', 'w') as f:
    SeqIO.write(longest_contig, f, 'fasta')

#download the betaherpesvirinae subfamily from ncbi and unzip it
os.system('datasets download virus genome taxon Betaherpesvirinae --filename betaherpesvirinae.zip')
os.system('unzip betaherpesvirinae.zip -d betaherpesvirinae')
#create a local nucleotide database from the fasta from ncbi
os.system('makeblastdb -in betaherpesvirinae/ncbi_dataset/data/genomic.fna -out betaherpesvirinae/betaherpesvirinae_db -title betaherpesvirinae_db -dbtype nucl')
#input the longest contig found from spades into a blast search from the local database'''
os.system('blastn -query longest_contig.fasta -db betaherpesvirinae/betaherpesvirinae_db -out blast_results.tsv -outfmt "6 sacc pident length qstart qend sstart send bitscore evalue stitle" -max_target_seqs 10 -max_hsps 1 >> PipelineProject.log')
os.system('cat blast_results.tsv >> PipelineProject.log')
