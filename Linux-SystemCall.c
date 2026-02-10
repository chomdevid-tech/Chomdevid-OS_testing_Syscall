#include <unistd.h>
int main() {
    const char *message = "Hello, System Call!\n";
    write(1, message, 19); // File descriptor 1 is stdout
    return 0;
}