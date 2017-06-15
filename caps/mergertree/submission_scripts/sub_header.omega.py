import textwrap
submission_header = textwrap.dedent("""\
#PBS -q astro_prod
#PBS -l nodes=8:ppn=8,mem=280gb
#PBS -l walltime=96:00:00
#PBS -j oe
#PBS -o outputs/$PBS_JOBNAME.$PBS_JOBID
##PBS -M YOUR_EMAIL_ADDRESS
##PBS -m e
#PBS -V
""")
max_threads = 16
