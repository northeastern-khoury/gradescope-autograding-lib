
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: %s <name>", argv[0]);
        return 1;
    }

    if (strncmp(argv[1], "Fail", 4) == 0) {
        printf("Nope!\n");
    } else {
        printf("Hello, %s!\n", argv[1]);
    }
    return 0;
}
