import os, re, shutil, sys

class FileLock:
    def __init__(self, lock_name):
        dirpath = os.path.join(_get_home_dir(), '.django_async.locks')
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)

        self.filename = os.path.abspath(
            os.path.normpath(
                os.path.join(dirpath, re.sub(r'\W+', '-', lock_name))))

        self.fd = None
        self.pid = os.getpid()

    def acquire(self):
        try:
            self.fd = os.open(self.filename, os.O_CREAT|os.O_EXCL|os.O_RDWR)
            # Only needed to let readers know who's locked the file
            os.write(self.fd, "%d" % self.pid)
            return 1    # return ints so this can be used in older Pythons
        except OSError:
            self.fd = None
            return 0

    def release(self):
        if not self.fd:
            return 0
        try:
            os.close(self.fd)
            os.remove(self.filename)
            return 1
        except OSError:
            return 0

    def __del__(self):
        self.release()


def _get_home_dir():
    try:
        from win32com.shell import shellcon, shell            
        homedir = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0) 
    except: # quick semi-nasty fallback for non-windows/win32com case
        homedir = os.path.expanduser("~")    
    return homedir


def main():
    lock = FileLock("lock.file")
    while 1:
        if lock.acquire():
            raw_input("acquired lock. Press ENTER to release:")
            lock.release()
            raw_input("released lock. Press ENTER to retry:")
        else:
            raw_input("Unable to acquire lock. Press ENTER to retry:")

if __name__ == "__main__":
    main()

