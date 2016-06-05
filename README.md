# AppImager

AppImager is a CLI tool for creating and managing [AppImages](http://appimage.org/).

It has the ability to manage application dependences, setup an AppDir and package that AppDir into an AppImage.

## Why?

[AppImages](http://appimage.org/) are an amazing way to distribute apps on almost any Linux distribution, but the way these apps have to be packaged is a bit convoluted, requiring you to build your app on an old base system, and figure out which dependencies are *probably* part of the base system, and which should be packaged into your AppImage.

AppImager is designed to help with this. It creates a Docker container with an Arch Linux base system where you can download any version of a dependency you need for your app, and extract it into your AppDir.

We do this by using an AppImage.yaml file to specify the dependencies required to compile the app, and the dependencies required to run it. AppImager then reads this YAML file, downloads and decompresses the dependencies into the AppDir, then compiles and packages your app into an AppImage.

The goal is to be able to add one AppImage.yml file to your source code, then use AppImager to build your app into an AppImage with no additional work required and no complicated scripts to be written.

Below is an example of an AppImage.yml file.

```yaml
name: AppImager
description: AppImager manages AppImage dependencies, assists in the creation of AppDir's and creates AppImages from source code.

build: cmake . && make clean && make

require:
    fuse: 2.9.6-1
    zlib: 1.2.8-4

require_build:
    cmake: 3.5.2-2
    binutils: 2.26-4
    glibc: 2.23-4
    glib2: 2.48.1-1
    gcc: 6.1.1-1
```

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

### Building

```bash
sudo yum install cmake binutils docker fuse glibc-devel glib2-devel gcc zlib xorriso # Fedora 23
cmake .
make clean
make
```
