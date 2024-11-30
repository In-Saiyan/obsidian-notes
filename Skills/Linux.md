# <span style="color:rgb(0, 176, 80)">Linux Commands</span>

## Table of Contents
1. [File Structure Commands](#file-structure-commands)
   - [cd](#cd)
   - [ls](#ls)
   - [clear](#clear)
   - [pwd](#pwd)
   - [touch](#touch)
   - [rm](#rm)
   - [mkdir](#mkdir)
   - [rmdir](#rmdir)
   -  [cp](#cp)
   - [mv](#mv)
1. [File and Directory Management](#file-and-directory-management)
   - [chmod](#chmod)
   - [chown](#chown)
   - [chgrp](#chgrp)
3. [Process Management](#process-management)
   - [ps](#ps)
   - [kill](#kill)
   - [fg](#fg)
   - [bg](#bg)
4. [System Information and Utilities](#system-information-and-utilities)
   - [whoami](#whoami)
   - [su](#su)
   - [sudo](#sudo)
   - [uname](#uname)
   - [df](#df)
   - [ifconfig](#ifconfig)
5. [Search and File Operations](#search-and-file-operations)
   - [grep](#grep)
   - [find](#find)
   - [locate](#locate)
   - [man](#man)
6. [Viewing and Editing Files](#viewing-and-editing-files)
   - [cat](#cat)
   - [tac](#tac)
   - [head](#head)
   - [tail](#tail)
   - [sort](#sort)
   - [diff](#diff)
   - [cmp](#cmp)
   - [comm](#comm)
7. [Archiving and Compression](#archiving-and-compression)
   - [zip](#zip)
   - [unzip](#unzip)
   - [tar](#tar)
8. [Networking and Downloads](#networking-and-downloads)
   - [wget](#wget)
9. [Miscellaneous](#miscellaneous)
   - [cal](#cal)
   - [wc](#wc)
   - [echo](#echo)
   - [expr](#expr)
   - [read](#read)

---

## <span style="color:rgb(0, 112, 192)">1. File Structure Commands</span>

### **cd**
- Changes the working directory.
- Examples:
  - `cd folder` - Navigate to a folder.
  - `cd ..` - Move one directory up.
  - `cd /path/to/folder` - Change to an absolute path.
### **ls**
- Lists the contents of the directory.
- Options:
  - `ls -a` - Show hidden files.
  - `ls -l` - Show detailed list.
  - `ls -R` - Recursively list all files in subdirectories.
  - `ls -lh` - Show detailed list in human readable format(changes sizes to KB, MB etc).
  - `ls -t` - Shows all directories and files sorted last time changed 
  - `ls -S` - Shows all directories and files sorted by file size
  - `ls -s` - Print the allocated size of each file, in blocks
  - `ls -r` Prints in reverse order
  - `ls -U` Prints in unsorted order
  - `ls -d */` Prints all the subdirectories
  - `ls -F` prints everything with their format specifier - directories + /, symbolic links + @ , executables + \*
### **clear**
- Clears the terminal screen.
  - `clear -x` - Retains scrollable history.
### **pwd**
- Displays the current working directory.
### **touch**
- Creates or updates files.
- Examples:
  - `touch filename` - Create a new file.
  - `touch -c` - Don't Create a new file if it does not exists.
  - `touch -a filename` - Update access time.
  - `touch -m filename` - Update modification time.
  - `touch -r file1 file2` - Copy the access and modification time of file2 to file1.
  - `touch YYYYMMDDHHmm.ss -t filename` - Add the modification and access time manually
### **rm**
- Removes files or directories.
- Options:
  - `rm -f file` - Forcefully remove a file.
  - `rm -i` - Remove files interatively, ask before every deletion
  - `rm -r dir` - Recursively remove a directory.
  - `rm --no-preserve-root` - Allows us to remove root directory
  - `rm -d` - removes empty directories
  - `rm -v` - (verbose) notifies "what got removed" on each step
### **mkdir**
- Creates new directories.
- Options:
  - `mkdir -p dir` - Create parent directories if needed.
  - `mkdir -v` - (verbose) notifies after making directories
### **rmdir**
- Removes empty directories.
- Options:
  - `rmdir -p dir` - Remove parent directories if empty.
  - `rmdir -v` - (verbose) notifies after deleting directories

### **cp**
- Copies files and directories.
- Examples:
  - `cp file1 file2` - Copy the contents of file1 into a new file named file2.
  - `cp -r dir1 dir2` - Copy directory recursively.
### **mv**
- Moves or renames files and directories.
- Examples:
  - `mv source destination` 

---
## <span style="color:rgb(0, 112, 192)">2. File and Directory Management</span>

### **chmod**
- Modifies file permissions.
- Examples:
  - `chmod 777 file` - Full permissions for everyone.

bits are in group of three user, group, others
and bits are rwx with value either 0 or 1
first bit represents if it is a directory or not, the following 9 bits show the permissions for these three group for these 3 access types

for example
`drw-r-----`
shows that user has read and write permissions, group has read permissions and others do not have any permission
We can `chmod` on u, g, o, a and add permissions with `+` and remove permissions with `-`  or just assign permission with `=` for r, w, x, s

for example if we want to give read permission to everyone, no write permission to others and execute permission only to user
`rwxrw-r--`
`chmod a-rwx,a+r,ug+w,u+x filename/directory` or `chmod 764`
    Owner (u): The user who owns the file.
    Group (g): The group associated with the file.
    Others (o): All other users on the system.
    All (a) : (owner, group, and others) 
    Read (r): Permission to view the contents of a file.
    Write (w): Permission to modify or delete the contents of a file.
    Execute (x): Permission to run a file as a program or script. 
    Sudo(s): Need sudo to run the executable/script
### **chown**
- Changes file ownership.
- Examples
  - `sudo chown -R root: foldername` - Makes root the owner of the folder
  - `sudo chown root: filename` - Makes root the owner of the file
  - `sudo chown username: filename` - Makes user the owner of the file
  - `sudo chown -R username: foldername` - Makes user the owner of the folder
  - `sudo chown -R username:group foldername` - If there are multiple users we can specify the username from the group
### **chgrp**
- Changes group ownership.

---

## <span style="color:rgb(0, 112, 192)">3. Process Management</span>

### **ps**
- Displays running processes.
- Examples:
  - `ps -e` - Shows processes for all users.
  - `ps -f` - Shows all details including Parent Process ID
  - `ps -u username` - Shows processes for user provided
  - `ps aux` - Shows all processes with Memory and CPU usage.
  - `pdf -ef` - Shows all processes for all users with their parent process ID
### **kill**
- Terminates a process using its PID.
- Example:
  - `kill 1234` - Kill process with PID 1234.
Signals are numeric or named values that dictate the action taken on the process.

| Signal Name | Signal Number | Description                                 |
| ----------- | ------------- | ------------------------------------------- |
| `SIGHUP`    | 1             | Reloads the configuration of the process.   |
| `SIGINT`    | 2             | Interrupts the process (similar to Ctrl+C). |
| `SIGKILL`   | 9             | Forcefully terminates the process.          |
| `SIGTERM`   | 15            | Gracefully terminates the process.          |
| `SIGSTOP`   | 19            | Stops (pauses) the process.                 |
| `SIGCONT`   | 18            | Resumes a stopped process.                  |

The `SIGKILL` and `SIGTERM` signals are most commonly used for terminating processes.
- **Gracefully terminate a process**:
```bash
kill -9 1234
```
this forcefully kills the process with id = 1234 because signal number 9 is forceful termination.
### **fg**
- Brings a process to the foreground.
### **bg**
- Resumes a background process.

---
## <span style="color:rgb(0, 112, 192)">4. System Information and Utilities</span>

### **whoami**
- Prints the username of the current user.
### **su**
- Switches to another user account.
- `su` - Switches to root
- `su user` - Switches to user
### **sudo**
- Executes commands with elevated privileges.
- `sudo command ...flags ...args`

### **uname**
- Displays system information.
  - `uname` - Operating system
  - `uname -r` - Shows kernel version
  - `uname -a` - Show all system details.
### **df**
- Displays disk usage.
  - `df -h` - Human-readable format.
  - `df -T` - Shows the file systems.
  - `df -t ext4` - Shows the partitions of the type mentioned in this case, ext4
### **ifconfig**
- Displays network interface configurations.
- Displays the following information - 
   Interface Name: The name of the network interface (e.g., eth0, wlan0, lo).
   IP Address: The IPv4 address assigned to the interface.
   Broadcast Address: The address used to send packets to all network devices.
   Netmask: The subnet mask that defines the network’s size.
   MAC Address: The hardware (MAC) address of the interface.
   MTU (Maximum Transmission Unit): The largest size of data packets that can be transmitted.
   RX and TX: Information about data packets received (RX) and transmitted (TX), including errors, dropped packets, and byte counts.

---
## <span style="color:rgb(0, 112, 192)">5. Search and File Operations</span>

### **grep**
- Searches for patterns in files.
  - Example: `grep "pattern" file.txt`.
  - `grep -r "pattern" path/to/directory` - finds all the patterns in every file inside the given directory
  - 
### **find**
- Finds files in the filesystem.
  - Example: `find /path -name "file.txt"`.
### **locate**
- Searches using a prebuilt database.
### **man**
- Displays the manual page for a command.

---

## <span style="color:rgb(0, 112, 192)">6. Viewing and Editing Files</span>

### **cat**
- Concatenates and displays file content.
  - Options:
    - `cat -n` - Show line numbers.
### **tac**
- Displays file content in reverse order.
### **head**
- Displays the first lines of a file.
  - Example: `head -n 5 file.txt`.
### **tail**
- Displays the last lines of a file.
  - Example: `tail -n 5 file.txt`.
### **sort**
- Sorts file content.
  - Example: `sort -r file.txt` - Reverse order.
### **diff**
- Compares two files line by line.
### **cmp**
- Compares two files byte by byte.
### **comm**
- Compares sorted files line by line.

---

## <span style="color:rgb(0, 112, 192)">7. Archiving and Compression</span>

### **zip**
- Compresses files into a ZIP archive.
  - Example: `zip -r archive.zip dir/`.
### **unzip**
- Extracts files from a ZIP archive.
### **tar**
- Archives files.
  - Example: `tar -cvf archive.tar dir/`.

---
## <span style="color:rgb(0, 112, 192)">8. Networking and Downloads</span>

### **wget**
- Downloads files from the web.
  - Example: `wget URL`.

---

## <span style="color:rgb(0, 112, 192)">9. Miscellaneous</span>

### **cal**
- Displays a calendar.
  - Example: `cal 2024`.
### **wc**
- Counts lines, words, and characters in files.
### **echo**
- Displays text to the terminal.
### **expr**
- Evaluates expressions.
### **read**
- Reads user input.

---