all:
	arm-poky-linux-gnueabi-gcc -Wall -Wextra -O -ansi -pedantic -shared -fPIC malloc_and_mlock.c -o malloc_and_mlock.so 
clean:
	rm malloc_and_mlock.so

