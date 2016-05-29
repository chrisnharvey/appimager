# AppImager

AppImager is a CLI tool for creating and managing [AppImages](http://appimage.org/).

It has the ability to manage application dependences, setup an AppDir and package that AppDir into an AppImage.

## Dependencies

- cmake
- binutils
- docker
- fuse
- glibc
- glib2
- gcc
- zlib

## Building

```bash
cmake .
make clean
make
```
