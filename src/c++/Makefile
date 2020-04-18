CC=g++
CFLAGS=-I.
DEPS = sparseMatrixMarket.h
OBJ = main.o sparseMatrixMarket.o 

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main.out: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)