#!/usr/bin/python3
from config import *
for target in FUZZ_ARGS:
    with open("conf/target/{}.yaml".format(target), "w") as f:
        f.write("name: {}\n".format(target))
        for i in FUZZ_ARGS[target]:
            f.write("{}: \"{}\"\n".format(i, FUZZ_ARGS[target][i]))

for fuzzer in FUZZER:
    with open("conf/fuzzer/{}.yaml".format(fuzzer), "w") as f:
        f.write("name: {}\n".format(fuzzer))
        for i in FUZZER[fuzzer]:
            f.write("{}: \"{}\"\n".format(i, FUZZER[fuzzer][i]))