# Building vg on HHPC
**BUILD INSTRUCTIONS INCOMPLETE**

In a directory where you want vg to be clone vg-Info (on HHPC login node for git):

`git clone --recursive https://github.com/gaddra/vg-Info`

In some working directory:

**GCC install**
```
wget http://mirrors.concertpass.com/gcc/releases/gcc-4.9.3/gcc-4.9.3.tar.gz
tar -zxf gcc-4.9.3.tar.gz && rm gcc-4.9.3.tar.gz
cd gcc-4.9.3
./contrib/download_prerequisites
mkdir gcc-build && cd gcc-build
../gcc-4.9.3/configure --prefix=$HOME/gcc-4.9.3
make && make install
(if you start a new session, paths might have to be set again)
export PATH=$HOME/gcc-4.9.3/bin:$PATH
export LD_LIBRARY_PATH=$HOME/gcc/lib64:$LD_LIBRARY_PATH
```
**get jansson**
```
wget http://www.digip.org/jansson/releases/jansson-2.7.tar.gz
tar -zxf jansson-2.7.tar.gz && rm jansson-2.7.tar.gz
cd jansson-2.7
./configure --prefix=$HOME/jansson-2.7
make && make install
```

# vg Usage
See 

https://docs.google.com/presentation/d/1bbl2zY4qWQ0yYBHhoVuXb79HdgajRotIUa_VEn3kTpI/edit#slide=id.g98a48eac1_0_16

for more information.

When using  vg in a new session, add vg and jansson to your path using `setvgpath` in the current shell with `. ./setvgpath`

**Constructing a graph**

Building the entire graph at once uses lots of memory, so it is more managable to build it in 500,000bp chunks. Create a directory to hold all of the subgraphs and run `./buildvg.sh`. The path to the ref fasta will probably need to be changed as well as start and stop positions. `COUNTER` is the start position, `$COUNTERB -le 52000000` is the end position. Note that the graph built is inclusive, `chr:a-b` will include positions a and b.

Building a small graph is done with `vg constrct -v VCF_FILE -r REF_FILE -R REGION > out.vg`

After the subgraphs are build they are joined with `vg concat`. It's probably easiest to form the command using excel.

`vg concat 16000001.vg 16500001.vg ...etc... > output.vg`

An associated graph with the same node numbering that does not have any variants and has just the reference can be made:

`vg mod -k NAME > output_ref.vg`

where `NAME` is the name of the reference fasta used to create the graph. In the below example, the top graph was joined to a copy of itself using `vg concat` to create the second graph. The reference was made from the second graph using `vg mod`.
![](https://raw.githubusercontent.com/gaddra/vg-Info/master/vgEx.png)

**Aligning to the graph**

To align a sequence to the graph use `vg align`.

`vg align -s GATAGAGACTAGAGAGATAGACA -j GRAPH.vg > alignment.json`

I used `simReads.py` to create a shell script to pull simulated reads and align them. This is slow however, ~1min per alignment. `matcher.py` finds the overlap in the nodes when aligning to the graph with variants and without variants. Note that this doesn't account for cases where the entire sequence lies in a variant path in the same area as the correct reference alignment, there must be atleast one common node for it to count as a match.

**Indexing the graph**

vg can index the graph. To create an index of 27mers that traverse no more than 7 edges (settings used in Erik Garrison's whole genome index) using a maximum of 16 threads:

`vg index -s -k 27 -t 16 -e 7 -p GRAPH.vg`

Aligning to the index should be done using the `vg map` command, but I'm yet to get that to work (alignment fails, I think it's not coming up with a score > 0. Use -D for debug printing).
