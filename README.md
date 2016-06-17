# AppImager

*Note: AppImager is a work in progress. All contributions and suggestions are much appreciated.*

AppImager is a CLI tool for creating and managing [AppImages](http://appimage.org/).

It has the ability to manage application dependences, setup an AppDir and package that AppDir into an AppImage.

## Why?

[AppImages](http://appimage.org/) are an amazing way to distribute apps on almost any Linux distribution, but the way these apps have to be packaged is a bit convoluted, requiring you to build your app on an old base system, and figure out which dependencies are *probably* part of the base system, and which should be packaged into your AppImage.

AppImager is designed to help with this. It creates a Docker container with an Arch Linux base system where you can download any version of a dependency you need for your app, and extract it into your AppDir.

We do this by using an AppImage.yml file to specify the dependencies required to compile the app, and the dependencies required to run it. AppImager then reads this YAML file, downloads and decompresses the dependencies into the AppDir, then compiles and packages your app into an AppImage.

The goal is to be able to add one AppImage.yml file alongside your source code, then use AppImager to build your app into an AppImage with no additional work required and no complicated scripts to be written.

Below is an example of an AppImage.yml file.

```yaml
name: AppImager
description: AppImager manages AppImage dependencies, assists in the creation of AppDir's and creates AppImages from source code

build: cmake . && make clean && make

base: 12.04

require:
    - fuse
    - zlib

require_build:
    - cmake
    - binutils
    - glibc
    - glib2
    - gcc
```

## AppImage.yml

AppImager works from an AppImage.yml file. This file tells AppImager numerous things about your app and the environment you want to compile it in.

### name

The name of your app.

### description

The description of your app.

### build

This is the command that is run to compile your app. Usually this will be the path to a bash script which compiles your app.

The command/script specified here will be called when running ```./appimager build```. It should compile your app into the ```build``` directory.

### base

The base Ubuntu version you want to target. To support a larger number of systems and distros then we recommend setting this to the oldest currently supported version of Ubuntu (12.04 at the time of writing).

We use Ubuntu as our base as it has multiple supported versions available, which gives you the flexibility of either supporting many systems, or using the latest libraries.

Although we use Ubuntu for our build environment, the compiled apps you create will work on almost any relatively recent Linux distribution.

### require

This is a list of dependencies that will be included in your AppImage. This should be a list of packages that are assumed to **not** be included on every system you want to target.

### require_build

This is a list of dependencies that are required to build/compile your app (e.g. gcc), but are not needed once your app is compiled and packaged.

## Building

### Dependencies

- cmake
- binutils
- docker
- fuse
- glibc
- glib2
- gcc
- zlib
- xorriso

### Building from source

```bash
sudo yum install cmake binutils docker fuse glibc-devel glib2-devel gcc zlib xorriso # Fedora 23
cmake .
make clean
make
```

## Usage

Once you have compiled the runtime binary, you can then start using AppImager. Most of the AppImager commands are based around your current working directory (we call this the environment). Your working directroy should be the directory which contains your AppImage.yml file.

### setup

The ```setup``` command creates a Docker container with a base Ubuntu installation to a version you specify in your AppImage.yml file and install the build dependencies. AppImager will then use this container to compile your app.

```bash
./appimager setup
```

### install

The ```install``` command reads the AppImage.yml file in the current working directory and downloads and extracts the dependencies into your build directory.

```bash
./appimager install
```

### build

The ```build``` command runs the build command/script specified in your AppImage.yml file.

```bash
./appimager build
```

### start

The ```start``` command starts the container for the current environment.

```bash
./appimager start
```

### stop

The ```stop``` command stops the container for the current environment.

```bash
./appimager stop
```

### status

The ```status``` command shows the current status of the container for this environment.

```bash
./appimager status
```

### package

The ```package``` command packages the AppDir (build directory) into an AppImage, ready for distribution.

```bash
./appimager package
```

### destroy

The ```destroy``` commnad stops and destroys/deletes the container for this environment.

```bash
./appimager destroy
```
