import textwrap
submission_header = textwrap.dedent("""\
#SBATCH --job-name=create_links
#SBATCH --output=log.%j
#SBATCH --time=5:00:00
#SBATCH --partition=sandyb
#SBATCH --account=pi-gnedin
##SBATCH --partition=kicp
##SBATCH --account=kicp
#SBATCH --nodes=1
#SBATCH --mail-type=ALL
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
""")
max_threads = 8

