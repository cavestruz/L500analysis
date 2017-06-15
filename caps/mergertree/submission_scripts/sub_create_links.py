#!/usr/bin/env python
import textwrap
import  sub_header 
def generate_submission_script(indir, aelist, fraction_most_bound ):
    num_epochs = len(aelist)
    if num_epochs <2:
        return
    output = open("temp.sub", "w")
    print >>output, textwrap.dedent("#!/usr/bin/perl")
    print >>output, sub_header.submission_header
    print >>output, "$HC_dir = \""+indir+"\";"
    print >>output, "@epochs = ();"
    print >>output, "$fraction = "+str(fraction_most_bound)+";"
    print >>output, "$max_threads = "+str(sub_header.max_threads)+";"
    for ae in aelist:
        print >>output, "push(@epochs,\""+ae+"\");"
    print >>output, "$num_epochs = @epochs;"
    print >>output, textwrap.dedent("""\
for ($i=0;$i<$num_epochs-1;$i++){
    my $pid = fork();

    if ( $pid ) {
            $children++;

            if ( $children >= $max_threads ) {
                    wait();
                    $children--;
            }
    } else {
        $j = $i+1;
        $input = "./create_links.py ". $HC_dir ." ". $epochs[$i] . " " . $epochs[$j] . " " . $fraction;
        print $input."\n";
        system($input);
        exit(0);
    }
}

while ( $children > 0 ) {
    wait();
    $children--;
}
    """)
    output.close()
    
#################
from choose_files import which_input_todo
from subprocess import call
from header import HC_dir, fraction_most_bound, forward

indir = HC_dir
infileprefix = "halo_catalog_a"
infilesuffix = ".dat"
outdir = HC_dir+"/../mergertrees/links/"
outdir = None
outfileprefix = "link_"
outfilesuffix = ".pkl"
pattern = '[0-1].[0-9][0-9][0-9][0-9]'
if forward: # sort so lowest a is first 
    reverse = False
else: # sort so higher a is first (find progenitors)
    reverse = True
#################
(halofile, aelist) = which_input_todo(pattern, indir, infileprefix, infilesuffix, reverse=reverse, outdir=outdir, outfileprefix=outfileprefix, outfilesuffix=outfilesuffix)
if len(aelist) <2:
    print "not enough epochs to link"
generate_submission_script(indir, aelist, fraction_most_bound )
print "qsub temp.sub" 
call(["qsub", "temp.sub"])
#os.system("qsub temp.sub")


