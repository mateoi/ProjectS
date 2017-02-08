CC=gcc
CFLAGS= -std=gnu99 -Wall

all: count_cycles tidy

count_cycles: cycle_calculator.o
	$(CC) $(CFLAGS) -o count_cycles cycle_calculator.o

count_cycles.o: cycle_calculator.c
	$(CC) $(CFLAGS) -c cycle_calculator.c

clean:
	$(RM) count_cycles *.o

tidy:
	$(RM) *.o

