# COATL Artifact
## Contents
1) [Introduction](#introduction)
2) [Requirements](#requirements)
3) [Using the artifact](#using-the-artifact)
4) [Usage](#usage)

## Introduction
This Docker image contains everything necessary to replicate the results of the paper **Circuit Optimization Using Arithmetic Table Lookups**.
This includes:
* A fork of HEIR compiler, with our changes applied on top of it.
* A benchmark suite comprising of all the benchmarks described in the paper.
* Utility scripts to help write new benchmarks, run and compile them.
* Various scripts necessary to automate the process of compiling, running, and collecting data from the benchmarks.

## Requirements
### Software
* We used gcc-13 to compile HEIR, for best results please stick to it!
```
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/usr/libexec/gcc/x86_64-linux-gnu/13/lto-wrapper
OFFLOAD_TARGET_NAMES=nvptx-none:amdgcn-amdhsa
OFFLOAD_TARGET_DEFAULT=1
Target: x86_64-linux-gnu
Configured with: ../src/configure -v --with-pkgversion='Ubuntu 13.3.0-6ubuntu2~24.04' --with-bugurl=file:///usr/share/doc/gcc-13/README.Bugs --enable-languages=c,ada,c++,go,d,fortran,objc,obj-c++,m2 --prefix=/usr --with-gcc-major-version-only --program-suffix=-13 --program-prefix=x86_64-linux-gnu- --enable-shared --enable-linker-build-id --libexecdir=/usr/libexec --without-included-gettext --enable-threads=posix --libdir=/usr/lib --enable-nls --enable-bootstrap --enable-clocale=gnu --enable-libstdcxx-debug --enable-libstdcxx-time=yes --with-default-libstdcxx-abi=new --enable-libstdcxx-backtrace --enable-gnu-unique-object --disable-vtable-verify --enable-plugin --enable-default-pie --with-system-zlib --enable-libphobos-checking=release --with-target-system-zlib=auto --enable-objc-gc=auto --enable-multiarch --disable-werror --enable-cet --with-arch-32=i686 --with-abi=m64 --with-multilib-list=m32,m64,mx32 --enable-multilib --with-tune=generic --enable-offload-targets=nvptx-none=/build/gcc-13-fG75Ri/gcc-13-13.3.0/debian/tmp-nvptx/usr,amdgcn-amdhsa=/build/gcc-13-fG75Ri/gcc-13-13.3.0/debian/tmp-gcn/usr --enable-offload-defaulted --without-cuda-driver --enable-checking=release --build=x86_64-linux-gnu --host=x86_64-linux-gnu --target=x86_64-linux-gnu --with-build-config=bootstrap-lto-lean --enable-link-serialization=2
Thread model: posix
Supported LTO compression algorithms: zlib zstd
gcc version 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04)
```
### Hardware
amd64 ubuntu server with a good amount of threads (> 64) to build the heir compiler and run the benchmarks. Please not that the larger benchmarks will take indefinitely on smaller machines like say MacBook Pro or any laptop!

## Using the Artifact
The provided Dockerfile automatically builds and installs all dependencies of COATL.
To build and run the Docker image, run the following commands from the directory containing the Dockerfile:
```
docker buildx build --platform linux/amd64 -t artifact .
docker run --platform linux/amd64 -it artifact bash
```
Once the docker image has been built, you are able to run bash in it, run these following commands inside the docker container.

```
source setup.sh
bash run-evaluation.sh small
```

This will generate figures and tables used in the paper in the `result/` folder. The files are as follows:
1. `runtime-speedup-table1.csv`: This csv file has results generated for Table 1 in Section 6.1 in the paper. It has speedup data of benchmarks that were run.
2. `runtime-speedup-fig11.pdf`: This pdf file has a figure of speedup plot for the benchmarks run. This reproduces the Figure 11 in Section 6.1 in the paper.
3. `gatecount-table2.csv`: This csv file has results for the gatecount of the optimized vs unoptimized circuits. This reproduces Table 2 in Section 6.1.
4. `compiletime-stats-table3.csv`: This csv file has results for the compiletime statistics for COATL. This reproduces Table 3 in Section 6.2.

The docker image already builds the heir compiler, but if you want to say recompile it, please use the following commands.
```
source setup.sh
bazel build @heir//tools:heir-opt
bazel build @heir//tools:heir-translate
```

In addition to the compiler and the runtime, the image also conists of various scripts to automatically run the benchmarks from the paper and generate the associated figures.
These are:
* `run-evaluation.sh <option>`: Automatically invokes the build script on the benchmarks listed in the paper. There are several presets available, `small`, `medium`, `large`, `all`, representing the size of the circuits (and correspondingly the expected compile time). Please note that `large` and `all` benchmarks will take a very long time on desktop machines/laptops. Please use servers with high core counts to build it.
* `setup.sh`: This should be sourced (`source setup.sh`) before running any other scripts. This will source python virtual environment.
* `plot-speedup.py <path>`: This python script will create figure for speedup in `results/` folder. Provide the path to an input .csv file.
* `table-speedup.py <path>`: This python script will create tables as .csv for speedup in `results/` folder. Provide the path to the .csv file.
* `table-compiletime.py <path>`: This python script will create table as .csv for compiletime statistics in `results/` folder. Provide the path to the .csv file.

The benchmarks are divided into three levels based on the circuit complexity:
1. `small` has pir, mul8, add8 and psi8.
2. `medium` has mul16, add16 and add32.
3. `large` has mul32 and psi16.

### Demo
Lets start by building all the `small` benchmarks (pir, mul8, add8 and psi8)

```
source setup.sh
bash run-evaluation.sh small
```
This took about 30 mins to complete fully and generate the data. The run logs are dumped in the root folder as run-evaluation.log and the results in form of csv are dumped in benchmarks-small folder.

Now that this works with the results, you can test run `medium` and `large` benchmarks similarly. Please use a server with good multicore perf as these benchmarks take a very long time on desktop grade machines. After this is done, please run the `all` preset to run all the benchmarks described in the paper and generate the data for them.

This will generate figures and plots that reproduce the Evaluation (Section 6) in the paper as follows: `runtime-speedup-table1.csv`, `runtime-speedup-fig11.pdf`, `gatecount-table2.csv`, `compiletime-stats-table3.csv`

To view these, either attach to the running Docker container (e.g. using VS Code), or copy the files to your host machine:
`TODO: update command`
```
docker cp $(docker ps -q):/home/artifact/results/ .
```

## Usage
### Writing a COATL program
`TODO`

### Invoking the compiler
The heir compiler can be invoked by using the commands given below:
```
bazel run //tools:heir-opt -- --unroll-secret-loops '--yosys-optimizer=mode=LUT' --shrink-lut-constants --merge-luts --secret-distribute-generic --canonicalize --comb-to-cggi --cggi-canonicalize-luts --cse --cggi-to-openfhe <.mlir file path>
```

The options are described as follows:
1. `--unroll-secret-loops` since FHE can't work with loops, we need to unroll all loops completely. The loops wrapped in secret block are unrolled by this option.
2. `--yosys-optimizer=mode=LUT` set the yoysys optimizer mode to use LUTs.
3. `--shrink-lut-constants`, `--secret-distribute-generic`, `--canonicalize`, `--comb-to-cggi`, `--cggi-canonicalize-luts`, `--cse`, `--cggi-to-openfhe` generic options to canonicalize and optimize the generated code and then convert CGGI backend circuits to openFHE backend.
4. `--merge-luts` invokes the optimization implemented in the paper to merge LUTs.