FROM unifuzz/unibench:coverage

RUN apt update&& apt install -y gcovr lcov

ENV CC=gcc CXX=g++

RUN pip2 install --upgrade wandb