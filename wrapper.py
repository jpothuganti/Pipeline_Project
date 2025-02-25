#Import libraries
import os

#Create directory and move into it
directory = 'PipelineProject_Jay_Pothuganti'
os.system(f"mkdir -p {directory}")
os.chdir(directory)




import subprocess
from pathlib import Path

def create_bowtie2_index_and_map(fastq_dir, output_dir="“PipelineProject_Jay_Pothuganti", output_sam="output.sam"):
    """
    Downloads the HCMV genome (NCBI accession NC_006273.2), creates a Bowtie2 index,
    and maps FASTQ files in the specified directory to the index.
    
    :param fastq_dir: Directory containing FASTQ files
    :param output_dir: Directory to store the index files
    :param output_sam: Output SAM file for read alignment
    """
    accession = "NC_006273.2"
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Define file paths
    fasta_file = os.path.join(output_dir, f"{accession}.fasta")
    index_prefix = os.path.join(output_dir, accession)
    
    # Download reference genome from NCBI
    subprocess.run(
        f"esearch -db nucleotide -query {accession} | efetch -format fasta > {fasta_file}",
        shell=True, check=True
    )
    print(f"Downloaded {accession} to {fasta_file}")
    
    # Build Bowtie2 index
    subprocess.run(["bowtie2-build", fasta_file, index_prefix], check=True)
    print(f"Bowtie2 index created with prefix {index_prefix}")
    
    # Find FASTQ files
    fastq_files = sorted(Path(fastq_dir).glob("*.fastq"))
    if not fastq_files:
        print("No FASTQ files found in the directory.")
        return
    
    # Construct Bowtie2 command
    fastq_inputs = [str(f) for f in fastq_files]
    bowtie2_cmd = ["bowtie2", "-x", index_prefix, "-U", ",".join(fastq_inputs), "-S", output_sam]
    
    # Run Bowtie2 mapping
    subprocess.run(bowtie2_cmd, check=True)
    print(f"Mapping completed. Results saved in {output_sam}")