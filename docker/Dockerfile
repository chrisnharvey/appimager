FROM base/archlinux:latest
MAINTAINER Max Schaefer <max@excloo.com>
ADD etc /etc
CMD /bin/bash
RUN rm -rf /etc/pacman.d/gnupg && \
	pacman-key --init && \
	pacman-key --populate archlinux && \
	pacman -Sy --noconfirm archlinux-keyring && \
	pacman -Syy && \
	pacman -S --noconfirm pacman && \
	pacman-db-upgrade && \
	pacman -Suu --noconfirm && \
	pacman -S --asdeps --noconfirm $(pacman -Qq) && \
	pacman -S --asexplicit --noconfirm $(cat /etc/pacman.list) && \
	pacman -Rcns --noconfirm $(pacman -Qdqt) && \
	pacman -Scc && \
	pacman -Sy --needed --noconfirm base-devel && \
	find /etc/ -type f -name '*.pac*' -exec rm {} \; && \
	rm -rf /var/cache/pacman/pkg/* && \
	pacman -S --noconfirm xorriso
