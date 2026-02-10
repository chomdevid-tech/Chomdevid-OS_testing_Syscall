#include <windows.h>
#include <stdio.h>

#define BUFFER_SIZE 1024

int main() {
    HANDLE hSrc, hDest;
    DWORD bytesRead, bytesWritten;
    char buffer[BUFFER_SIZE];

    // Open source file
    hSrc = CreateFile(
        "result.txt",
        GENERIC_READ,
        0,
        NULL,
        OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL,
        NULL
    );

    if (hSrc == INVALID_HANDLE_VALUE) {
        printf("Error opening source file\n");
        return 1;
    }

    // Create destination file
    hDest = CreateFile(
        "copyresult.txt",
        GENERIC_WRITE,
        0,
        NULL,
        CREATE_ALWAYS,
        FILE_ATTRIBUTE_NORMAL,
        NULL
    );

    if (hDest == INVALID_HANDLE_VALUE) {
        printf("Error creating destination file\n");
        CloseHandle(hSrc);
        return 1;
    }

    // Copy loop
    while (ReadFile(hSrc, buffer, BUFFER_SIZE, &bytesRead, NULL) && bytesRead > 0) {
        WriteFile(hDest, buffer, bytesRead, &bytesWritten, NULL);
    }

    CloseHandle(hSrc);
    CloseHandle(hDest);

    printf("File copied successfully (Windows)\n");
    return 0;
}
