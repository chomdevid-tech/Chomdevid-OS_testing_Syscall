#include <windows.h>
int main() {
    const char *message = "Hello, Windows API!\n";
    DWORD bytesWritten;
    // Write to the console (STD_OUTPUT_HANDLE is stdout)
    WriteFile(GetStdHandle(STD_OUTPUT_HANDLE), message, strlen(message), &bytesWritten, NULL);
    return 0;

}
