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
    uint64_t time0, time1;

    for (int i = 0; i < number_of_iterations; i++) {
        // Put some values in rbx, and rcx ready to multiply and call CPUID to synchronize CPU.
        asm("mov $0xAAAAAAAAAAAAAAAA, %rbx;"
            "mov $0xDEADBEEFEBBED007, %rcx;"
            "CPUID;"
            "CPUID;"
            "CPUID;");
        // read the timing register and put it in r8.
        asm("RDTSC;");
        asm("mov %%rax, %0;" : "=r" (time0));
        // Do a 64 bit multiplication -- the time this will take depends on the ALU load.
        asm("imul %rbx, %rcx;");
        // Check the clock again, put it somewhere safe, and synchronize the CPU.
        asm("RDTSC;");
        asm("mov %%rax, %0;" : "=r" (time1));
        asm("CPUID;"
            "CPUID;");
        
        array[i] = time1 - time0;
    }
}

int main(int argc, char** argv) {
    int iterations = ITERATIONS;
    if (argc >= 2) {
        iterations = atoi(argv[1]);
    }
    uint64_t values[iterations];
    calculate_time(iterations, values);
    for (int i = 0; i < iterations; i++) {
        printf("%lu\n", values[i]);
    }
    return 0;
}

