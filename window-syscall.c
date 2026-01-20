// windows-syscall.c
#include <windows.h>

int main() {
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    char msg[] = "Hello from Windows system call!\n";
    DWORD written;

    WriteFile(hOut, msg, sizeof(msg) - 1, &written, NULL);
    return 0;
}
