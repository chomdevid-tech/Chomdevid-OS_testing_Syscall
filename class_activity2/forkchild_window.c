#include <stdio.h>
#include <windows.h>

int main(void)
{
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    HANDLE hJob;
    JOBOBJECT_EXTENDED_LIMIT_INFORMATION jeli = {0};

    // Initialize structures
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    // Create a Job object
    hJob = CreateJobObject(NULL, NULL);
    if (hJob == NULL) {
        fprintf(stderr, "CreateJobObject failed\n");
        return -1;
    }

    // Set the job to kill all processes when the job handle is closed
    jeli.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
    if (!SetInformationJobObject(hJob, JobObjectExtendedLimitInformation,
                                 &jeli, sizeof(jeli))) {
        fprintf(stderr, "SetInformationJobObject failed\n");
        CloseHandle(hJob);
        return -1;
    }

    // Create child process (MSPaint)
    if (!CreateProcess(NULL,
        "C:\\Program Files\\WindowsApps\\Microsoft.Paint_11.2511.291.0_x64__8wekyb3d8bbwe\\PaintApp\\mspaint.exe",
        NULL, NULL, FALSE, 0, NULL, NULL,
        &si, &pi))
    {
        fprintf(stderr, "CreateProcess failed\n");
        CloseHandle(hJob);
        return -1;
    }

    // Assign the child process to the job
    if (!AssignProcessToJobObject(hJob, pi.hProcess)) {
        fprintf(stderr, "AssignProcessToJobObject failed\n");
        TerminateProcess(pi.hProcess, 0);
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        CloseHandle(hJob);
        return -1;
    }

    // Wait for child to complete (optional)
    WaitForSingleObject(pi.hProcess, INFINITE);
    printf("Child Complete\n");

    // Close handles
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    CloseHandle(hJob);

}
