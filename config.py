FUZZER = {
    "afl-aflasan":{
        "bin_dir": "aflasan",
        "image": "unifuzz/unibench:afl",
        "memory_limit": "none",
        "time_limit": "500+",
        "cmd_temp": "afl-fuzz -i {seeds} -o {output_path} -m {memory_limit} -t {time_limit} {prefix}/{target} {fuzz_args}"
    },
    "afl-justafl":{
        "bin_dir": "justafl",
        "image": "unifuzz/unibench:afl",
        "memory_limit": "2G",
        "time_limit": "100+",
        "cmd_temp": "afl-fuzz -i {seeds} -o {output_path} -m {memory_limit} -t {time_limit} {prefix}/{target} {fuzz_args}"
    },
    "aflpp-aflasan":{
        "bin_dir": "aflasan",
        "image": "unifuzz/unibench:afl",
        "memory_limit": "none",
        "time_limit": "500+",
        "cmd_temp": "afl-fuzz -i {seeds} -o {output_path} -m {memory_limit} -t {time_limit} {prefix}/{target} {fuzz_args}"
    },
    "aflpp-justafl":{
        "bin_dir": "justafl",
        "image": "unifuzz/unibench:afl",
        "memory_limit": "2G",
        "time_limit": "100+",
        "cmd_temp": "afl-fuzz -i {seeds} -o {output_path} -m {memory_limit} -t {time_limit} {prefix}/{target} {fuzz_args}"
    },
    "aflfast":{
        "bin_dir": "justafl",
        "image": "unifuzz/unibench:aflfast",
        "power_schedule": "fast", # available options: {fast, coe, explore, quad, lin, exploit}
        "cmd_temp": "afl-fuzz -p {power_schedule} -i {seeds} -o {output_path} -- {prefix}/{target} {fuzz_args}"
    },
    # "angora":{
    #     "bin_dir": "angora",
    #     "image": "unifuzz/unibench:angora",
    #     "cmd_temp": "/angora/angora_fuzzer --input {seeds} --output {output_path}/output \
    #         -t {prefix}/taint/{target} -- \
    #         {prefix}/fast/{target} {fuzz_args}"
    # },
    # "honggfuzz": {
    #     "bin_dir": "honggfuzz",
    #     "image": "unifuzz/unibench:honggfuzz",
    #     "thread": "1",
    #     "customized_placeholder": "___FILE___",
    #     "additional_dirs": "queue",
    #     "cmd_temp": "/honggfuzz/honggfuzz -f {seeds} -W {output_path}/output \
    #         --covdir_all {output_path}/queue --threads 1 -- \
    #         {prefix}/{target} {fuzz_args}"
    # },
    "mopt":{
        "bin_dir": "justafl",
        "image": "unifuzz/unibench:mopt",
        "pacemaker_time": "1",
        "cmd_temp": "afl-fuzz -L {pacemaker_time} -i {seeds} -o {output_path} -- {prefix}/{target} {fuzz_args}"
    },
}
FUZZ_ARGS = {'exiv2': {'args': '@@', 'seeds': 'seeds/general_evaluation/jpg', 'source_dir': '/unibench/exiv2-0.26'},
        'tiffsplit': {'args': '@@', 'seeds': 'seeds/general_evaluation/tiff', 'source_dir': '/unibench/libtiff-3.9.7'},
        'mp3gain': {'args': '@@', 'seeds': 'seeds/general_evaluation/mp3', 'source_dir': '/unibench/mp3gain-1.5.2'},
        'wav2swf': {'args': '-o /dev/null @@', 'seeds': 'seeds/general_evaluation/wav', 'source_dir': '/unibench/swftools-0.9.2'},
        'pdftotext': {'args': '@@ /dev/null', 'seeds': 'seeds/general_evaluation/pdf', 'source_dir': '/unibench/xpdf-4.00'},
        'infotocap': {'args': '-o /dev/null @@', 'seeds': 'seeds/general_evaluation/text', 'source_dir': '/unibench/ncurses-6.1'},
        'mp42aac': {'args': '@@ /dev/null', 'seeds': 'seeds/general_evaluation/mp4','source_dir': '/unibench/Bento4-1.5.1-628'},
        'flvmeta': {'args': '@@', 'seeds': 'seeds/general_evaluation/flv', 'source_dir': '/unibench/flvmeta-1.2.1'},
        'objdump': {'args': '-S @@', 'seeds': 'seeds/general_evaluation/obj', 'source_dir': '/unibench/binutils-2.28'},
        # 'uniq': {'args': '@@', 'seeds': 'uniq'},
        # 'base64': {'args': '-d @@', 'seeds': 'base64'},
        # 'md5sum': {'args': '-c @@', 'seeds': 'md5sum'},
        # 'who': {'args': '@@', 'seeds': 'who'},
        'tcpdump': {'args': '-e -vv -nr @@', 'seeds': 'seeds/general_evaluation/tcpdump100', 'source_dir': '/unibench/tcpdump-4.8.1'},
        'ffmpeg': {'args': '-y -i @@ -c:v mpeg4 -c:a copy -f mp4 /dev/null',
                   'seeds': 'seeds/general_evaluation/ffmpeg100', 'source_dir': '/unibench/ffmpeg-4.0.1'},
        'gdk-pixbuf-pixdata': {'args': '@@ /dev/null', 'seeds': 'seeds/general_evaluation/pixbuf', 'source_dir': '/unibench/gdk-pixbuf-2.31.1'},
        'cflow': {'args': '@@', 'seeds': 'seeds/general_evaluation/cflow', 'source_dir': '/unibench/cflow-1.6'},
        'nm-new': {'args': '-A -a -l -S -s --special-syms --synthetic --with-symbol-versions -D @@',
                   'seeds': 'seeds/general_evaluation/nm', 'source_dir': '/unibench/binutils-5279478'},
        'sqlite3': {'args': ' < @@', 'seeds': 'seeds/general_evaluation/sql', 'source_dir': '/unibench/SQLite-3.8.9'},
        'lame': {'args': '@@ /dev/null', 'seeds': 'seeds/general_evaluation/lame3.99.5', 'source_dir': '/unibench/lame-3.99.5'},
        'jhead': {'args': '@@', 'seeds': 'seeds/general_evaluation/jhead', 'source_dir': '/unibench/jhead-3.00'},
        'imginfo': {'args': '-f @@', 'seeds': 'seeds/general_evaluation/imginfo', 'source_dir': '/unibench/jasper-2.0.12'},
        # 'pngimage': {'args': '@@', 'seeds': 'pngimage'},
        'jq': {'args': '. @@', 'seeds': 'seeds/general_evaluation/json', 'source_dir': '/unibench/jq-1.5'},
        'mujs': {'args': '@@', 'seeds': 'seeds/general_evaluation/mujs', 'source_dir': '/unibench/mujs-1.0.2'}}
