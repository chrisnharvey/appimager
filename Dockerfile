FROM base/devel
RUN pacman -Syu --noconfirm
RUN pacman -S --noconfirm xorriso
