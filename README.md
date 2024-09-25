# Toy ELF x86-64 crafting framework

This is a small set of functions which you can build on to create x86-64 ELF
executables from raw bytes.

## Quickstart

You will need to run this on a Linux/x86-64 system or in the dev container 
provided.

If you have your own Python set up you can replace `python3` with `python` or
whatever you prefer, I'll use `python3` here for ease of copy-paste on fresh
containers.

```shell
; uname -m # Check we're on the right architecture
x86_64

; python3 example_hello_world.py # This will write the binary to build/example
# No output is good

; chmod a+x build/hello-world # Set executable permissions

; ./build/hello-world
Hello, world!
```

If you see some kind of architecture or execution error, you're probably not

## Contents

* `.devcontainer/devcontainer.json`: which provides a [VS Code Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) for x86-64 Ubuntu Linux (particularly suitable for use on macOS).
* `elf.py`: small functions that will help you create ELF executables.
* `instructions.py`: functions that assist with encoding instructions into machine code.
* `example_hello_world.py`: a hello world example of using the framework.
* `example_quine.py`: an example of a (kind of) [Quine](https://en.wikipedia.org/wiki/Quine_(computing)) using ELF.

I suggest copying `example_hello_world.py` and working directly in that file. As
you create new instruction helpers you can add them to `instructions.py` or
similar to build a helpful library for yourself.

## Using the Dev Container

1. Install [Docker](http://docker.com)
2. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
3. Clone this repository.
4. Open it in VS Code.
5. Run "Dev Containers: Reopen in Container"
   1. Either by hitting Cmd/Ctrl+Shift+P and searching for it
   2. Or clicking the blue icon in the bottom left corner and select 'Reopen in container'
   
If you're new to Dev Containers you might appreciate [the Microsoft tutorial.](https://code.visualstudio.com/docs/devcontainers/tutorial)

If you want to use straight Docker, this will get you a container with the
current directory shared:

docker run -v $(pwd):/root/code -w /root/code --platform linux/amd64 -it python:3.12 bash

# Running the Quine

A [Quine](https://en.wikipedia.org/wiki/Quine_(computing)) is a program that,
given no input, outputs its own source code. 

Ours is a Quine that outputs its own executable. So it's not exactly a Quine.
However it's a good way to illustrate the ELF format.

To see it work:

```bash
; python3 example_quine.py # Generate the quine

; cd build                 # Go into the build dir
; chmod a+x quine          # Mark the quine executable
; ./quine > double         # Run the quine and output to a file

; sha1sum quine double     # Observe that they are the same file

; od -x quine              # Or check yourself with od
; od -x double
```
