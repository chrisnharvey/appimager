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
- xorriso

## Building

```bash
sudo yum install cmake binutils docker fuse glibc-devel glib2-devel gcc zlib xorriso # Fedora 23
cmake .
make clean
make
```
