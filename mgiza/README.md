# mGiza: Multi-threaded GIZA++

This project contains python wrappers to easily generate word alignments using MGIZA.

* Paper: https://doi.org/10.1162/089120103321337421
* Official GitHub: https://github.com/moses-smt/mgiza

## Installation
Compiling mgiza might be little tricky (seriously, unless you have a specific reason to use mgiza, just use SimAlign or AWESOME, they are better and easier to install).
Here is a great guide by ho xuan binh that I followed to compile mgiza: https://hovinh.github.io/blog/2016-04-29-install-mgiza-ubuntu/

If the link is down here is a snapshop: https://web.archive.org/web/20201130085657/https://hovinh.github.io/blog/2016-04-29-install-mgiza-ubuntu/


If the compilation ends successfully you should edit the mgizapp path in line 19 in [generate_alignments.py](generate_alignments.py) file to point to the correct path of the "mgiza" directory.

You should also modify the mgizapp path in line 91 in [model_utils.py](model_utils.py) file to point to the correct path of the "mgiza" directory.

You need the aatols from fast_align to merge the formard and backward alignments. So please, follow the steps in fast_align/README.md to compile fast_align and then
edit line 92 in [model_utils.py](model_utils.py) file to point to the correct path of the "aatols" file.
