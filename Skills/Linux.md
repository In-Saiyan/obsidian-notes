# **Linux Commands**

## **Table of Contents**
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

## **1. File Structure Commands**

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
## **2. File and Directory Management**

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
We can `chmod` on u, g, o, a and add permissions with `+` and remove permissions with `-` for r, w, x, s

for example if we want to give read permission to everyone, no write permission to others and execute permission only to user
`rwxrw-r--`
`chmod a-rwx,a+r,ug+w,u+x filename/directory` or `chmod 764`
### **chown**
- Changes file ownership.
- Examples
  - `chown -R root: foldername` - 
### **chgrp**
- Changes group ownership.

---

## **3. Process Management**

### **ps**
- Displays running processes.
- Examples:
  - `ps -aux` - Shows all processes.
### **kill**
- Terminates a process using its PID.
- Example:
  - `kill 1234` - Kill process with PID 1234.
### **fg**
- Brings a process to the foreground.
### **bg**
- Resumes a background process.

---
## **4. System Information and Utilities**

### **whoami**
- Prints the username of the current user.
### **su**
- Switches to another user account.
### **sudo**
- Executes commands with elevated privileges.

### **uname**
- Displays system information.
  - `uname -a` - Show all system details.
### **df**
- Displays disk usage.
  - `df -h` - Human-readable format.
### **ifconfig**
- Displays network interface configurations.

---
## **5. Search and File Operations**

### **grep**
- Searches for patterns in files.
  - Example: `grep "pattern" file.txt`.
### **find**
- Finds files in the filesystem.
  - Example: `find /path -name "file.txt"`.
### **locate**
- Searches using a prebuilt database.
### **man**
- Displays the manual page for a command.

---

## **6. Viewing and Editing Files**

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

## **7. Archiving and Compression**

### **zip**
- Compresses files into a ZIP archive.
  - Example: `zip -r archive.zip dir/`.
### **unzip**
- Extracts files from a ZIP archive.
### **tar**
- Archives files.
  - Example: `tar -cvf archive.tar dir/`.

---
## **8. Networking and Downloads**

### **wget**
- Downloads files from the web.
  - Example: `wget URL`.

---

## **9. Miscellaneous**

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