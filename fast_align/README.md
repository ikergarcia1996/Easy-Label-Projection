# Fast Align: A Simple, Fast, and Effective Reparameterization of IBM Model 2.

This project contains python wrappers to easily generate word alignments using Fast Align.

* Paper: https://aclanthology.org/N13-1073.pdf
* Official GitHub: https://github.com/clab/fast_align

## Installation
See the official repository for installation instructions: https://github.com/clab/fast_align

In short, you can install FastAlign using the following commands:
```commandline
git cline https://github.com/clab/fast_align.git
cd fast_align
sudo apt-get install libgoogle-perftools-dev libsparsehash-dev
mkdir build
cd build
cmake ..
make
```

If the compilation ends successfully you should have the files "atools" and "fast_align" inside the build directory.
Please edit the line 24 in [generate_alignments.py](generate_alignments.py) file to point to the correct path of the "build" directory.

