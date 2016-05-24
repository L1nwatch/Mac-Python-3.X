#include <stdio.h>
#include <LIMITS.H>

void main(void) {
	unsigned int a = ULONG_MAX;
	char c = -1;

	if (c == a) {
		printf("-1 == 4, 294, 967, 295\n");
	}
}