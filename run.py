#!/usr/bin/python3
import os
import logging
import pathlib
import atexit
import shutil
import threading
import hydra
import docker
import wandb

client = docker.from_env()
log = logging.getLogger(__name__)

def next_path(path_pattern):
    """
    Finds the next free path in an sequentially named list of files

    e.g. path_pattern = 'file-%s.txt':

    file-1.txt
    file-2.txt
    file-3.txt

    Runs in log(n) time where n is the number of existing files in sequence
    """
    i = 1

    # First do an exponential search
    while os.path.exists(path_pattern % i):
        i = i * 2

    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i // 2, i)
    while a + 1 < b:
        c = (a + b) // 2 # interval midpoint
        a, b = (c, b) if os.path.exists(path_pattern % c) else (a, c)

    return path_pattern % b, b



class ExpConfig():
    def __init__(self, fuzzer, target, repeat_times = 30, output = "output", time_interval = 24 * 60 * 60):
        self.fuzzer = fuzzer
        self.target = target
        self.orig_path = hydra.utils.get_original_cwd()                     # orig_cwd
        self.relpath = os.path.relpath(os.getcwd(), self.orig_path)         # relpath of orig_cwd to cwd
        self.output_path = os.path.join(output, target.name, fuzzer.name)   # output_path related to cwd
        self.repeat_times = repeat_times
        self.prefix = os.path.join("/d/p", fuzzer.bin_dir)
        self.seeds = os.path.join("seeds/general_evaluation", target.seeds)
        try: 
            client.get(fuzzer.image)
        except:
            client.images.pull(fuzzer.image)
        try: 
            client.get("ucasqsl/unifuzz:cov")
        except:
            client.images.pull("ucasqsl/unifuzz:cov")
        self.containers = {"fuzzer": [], "cov": {}}
        self.time_interval = time_interval
        atexit.register(self.cleanup)

    def stop_fuzzer(self, container, name, output_path):
        container.stop()
        log.info("Container Stoped => {} {}".format(container.name, container.short_id))
        cov = self.containers['cov'][container]
        cov.wait()
        

    def run_afl_cov(self, output, name):
        container_name = name + "_afl_cov"
        cmd_temp = "./afl-cov -d {output} --live --coverage-cmd \
            \"/d/p/cov/{target} {fuzz_args}\" \
            --code-dir {code_dir} --name {name}"
            
        cmd = cmd_temp.format(
                output = output, 
                target = self.target.name, 
                fuzz_args = self.target.args.replace("@@", "AFL_FILE"),
                code_dir = self.target.source_dir,
                name = name
                )
        volumes = {self.orig_path: {"bind" : "/work", "mode": "rw"}}
                # str(pathlib.Path.home()): {"bind" : "/root", "mode": "ro"}}
        try: 
            old_container = client.containers.get(container_name)
            old_container.remove(force = True)
        except:
            pass
        container = client.containers.run(
            image = "ucasqsl/unifuzz:cov", 
            command = cmd,
            privileged = True,
            volumes = volumes,
            working_dir = "/work",
            detach = True,
            auto_remove = True,
            name = container_name,
        ) 
        netrc = os.path.join(str(pathlib.Path.home()), ".netrc")
        dst = os.path.join(self.orig_path, ".netrc")
        if not os.path.exists(dst):
            shutil.copyfile(netrc, dst)
        log.info("COV CMD => {}".format(cmd))
        log.info("Container Created => {} {}".format(container_name, container.short_id))
        return container

    def run_fuzzer(self):
        output_path, run_id = next_path(os.path.join(self.output_path, "%s"))
        pathlib.Path(output_path).mkdir(parents=True, exist_ok=True)
        if "additional_dirs" in self.fuzzer:
            dirs = self.fuzzer.additional_dirs.split(",")
            for d in dirs:
                dir_path = os.path.join(output_path, d)
                pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
        rel_output_path = os.path.join(self.relpath, output_path)
        log.info("Output Path => {}".format(output_path))
        cmd = self.fuzzer.cmd_temp.format(
            seeds = self.seeds, 
            output_path = rel_output_path, 
            prefix = self.prefix, 
            target = self.target.name,
            fuzz_args = self.target.args,
            **self.fuzzer)
        if "customized_placeholder" in self.fuzzer:
            cmd = cmd.replace("@@", self.fuzzer.customized_placeholder)
        log.info("CMD => {}".format(cmd))
        
        volumes = {self.orig_path: {"bind" : "/work", "mode": "rw"}}
        
        name = "unifuzz_{}_{}_{:d}".format(self.fuzzer.name, self.target.name, run_id)
        try: 
            old_container = client.containers.get(name)
            old_container.remove(force = True)
        except:
            pass
        afl_cov = self.run_afl_cov(rel_output_path, name)
        container = client.containers.run(
            image = self.fuzzer.image, 
            command = cmd,
            privileged = True,
            volumes = volumes,
            working_dir = "/work",
            detach = True,
            auto_remove = True,
            name = name,
            stop_signal ="SIGINT",
            user = os.getuid()
        )
        log.info("Container Created => {} {}".format(name, container.short_id))
        self.containers["fuzzer"].append(container)
        self.containers["cov"][container] = afl_cov
        return container, name, rel_output_path

    def run_experiment(self):
        for i in range(self.repeat_times):
            container, name, output_path = self.run_fuzzer()
            timethread=threading.Timer(self.time_interval, self.stop_fuzzer, [container, name, output_path])
            timethread.start()
    
    def cleanup(self):
        for container in self.containers["fuzzer"] + list(self.containers['cov'].values()):
            try:
                client.containers.get(container.id)
                container.stop()
            except:
                pass

@hydra.main(config_path="conf", config_name="config")
def main(cfg):
    if not os.path.exists(os.path.join(str(pathlib.Path.home()), ".netrc")):
        wandb.login()
    exp = hydra.utils.instantiate(cfg.exp)
    exp.run_experiment()

if __name__ == "__main__":
    main()