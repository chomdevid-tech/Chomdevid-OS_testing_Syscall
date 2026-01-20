#include <unistd.h>

int main() {
    char msg[] = "Hello from Linux system call!\n";
    write(1, msg, sizeof(msg) - 1);  // 1 = stdout
    return 0;
}
