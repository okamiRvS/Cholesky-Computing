CC=g++
CFLAGS=-I. -O3 -march=native
DEPS = sparseMatrixMarket.h
OBJ = main.o sparseMatrixMarket.o 

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main.out: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)