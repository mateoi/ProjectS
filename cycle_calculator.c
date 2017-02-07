#include <stdio.h>
#include <stdint.h>

#define ITERATIONS 10
int main() {
    uint64_t time0;
    uint64_t time1;
   
    uint64_t values[ITERATIONS];

    for (int i = 0; i < ITERATIONS; i++) {
        // Put some values in rbx, and rcx ready to multiply and call CPUID to synchronize CPU.
        asm("mov $0xAAAAAAAAAAAAAAAA, %rbx;"
            "mov $0xDEADBEEFEBBED007, %rcx;"
            "CPUID;"
            "CPUID;"
            "CPUID;");
        // read the timing register and put it in r8.
        asm("RDTSC;");
        asm("mov %%rax, %0;" : "=r"(time0));
        // Do a 64 bit multiplication -- the time this will take depends on the ALU load.
        asm("imul %rbx, %rcx;");
        // Check the clock again, put it somewhere safe, and synchronize the CPU.
        asm("RDTSC;");
        asm("mov %%rax, %0;" : "=r"(time1));
        asm("CPUID;"
            "CPUID;");
        
	values[i] = time1 - time0;
    }
    for (int i = 0; i < ITERATIONS; i++) {
        printf("%lu\n", values[i]);
    }
    return 0;

}
