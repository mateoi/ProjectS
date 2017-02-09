CC=gcc
CFLAGS= -std=gnu99 -Wall

all: linux_count_cycles tidy

linux_count_cycles: linux_cycle_calculator.o
	$(CC) $(CFLAGS) -o linux_count_cycles linux_cycle_calculator.o

linux_count_cycles.o: linux_cycle_calculator.c
	$(CC) $(CFLAGS) -c linux_cycle_calculator.c

clean:
	$(RM) linux_count_cycles *.o

tidy:
	$(RM) *.o

