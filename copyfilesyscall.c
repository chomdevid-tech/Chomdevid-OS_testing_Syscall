// copyfilesyscall.c
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>

int main() {
    int src_fd, dest_fd;
    char buffer[1024];
    ssize_t bytesRead;

    // Open source file
    src_fd = open("result.txt", O_RDONLY);
    if (src_fd < 0) {
        perror("Error opening result.txt");
        return 1;
    }

    // Open destination file
    dest_fd = open("copyresult.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (dest_fd < 0) {
        perror("Error opening copyresult.txt");
        close(src_fd);
        return 1;
    }

    // Copy content
    while ((bytesRead = read(src_fd, buffer, sizeof(buffer))) > 0) {
        write(dest_fd, buffer, bytesRead);
    }

    // Close files
    close(src_fd);
    close(dest_fd);

    printf("File copied successfully using system calls.\n");
    return 0;
}
