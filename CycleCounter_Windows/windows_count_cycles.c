#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define ITERATIONS 10

/*
* Calculates the clock cycles taken to perform a 64-bit multiplication
* for the given number of times, and stores the results in the given array,
* which must be of (at least) the required size.
*/
void calculate_time(int number_of_iterations, uint64_t* array) {
	uint32_t time0, time1;

	for (int i = 0; i < number_of_iterations; i++) {
		__asm {
            // Put some values in rbx, and rcx ready to multiply and call CPUID to synchronize CPU.
			mov ebx, 0xAAAAAAAA;
			mov ecx, 0XDEADBEEF;
			CPUID;
			CPUID;
			CPUID;
	    	// read the timing register and put it in r8.
			RDTSC;
			mov time0, eax;
		    // Do a 32 bit multiplication -- the time this will take depends on the ALU load.
            imul ebx, ecx;
	    	// Check the clock again, put it somewhere safe, and synchronize the CPU.
			RDTSC;
			mov time1, eax;
			CPUID;
			CPUID;
		}

		array[i] = time1 - time0;
	}
}

int main(int argc, char** argv) {
    int iterations = ITERATIONS;
	if (argc >= 2) {
		iterations = atoi(argv[1]);
	}
	uint64_t* values = (uint64_t*) malloc(iterations * sizeof(uint64_t));
	calculate_time(iterations, values);
	for (int i = 0; i < iterations; i++) {
		printf("%lu\n", values[i]);
	}
	return 0;
}

