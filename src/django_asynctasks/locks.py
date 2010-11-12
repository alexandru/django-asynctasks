import os, re, shutil, sys
from django.db import connections

class AcquireLock:
    def __init__(self, lock_name):
        self.lock_name = lock_name

        locker_cls = FileLock
        connection = None

        for conn in connections.all():
            db_engine = conn.settings_dict['ENGINE']
            if db_engine == 'django.db.backends.mysql':
                locker_cls = MysqlLock
                connection = conn
                break

        self.locker = locker_cls(lock_name=self.lock_name, connection=connection)

    def __enter__(self):
        return self.locker.acquire()

    def __exit__(self, type, value, traceback):
        self.locker.release()


class MysqlLock:
    def __init__(self, lock_name, connection):
        self.lock_name = lock_name
        self.conn      = connection

    def acquire(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT GET_LOCK(%s, 0.5)", [self.lock_name])
        row = cursor.fetchone()
        return True if row and row[0] else False

    def release(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT RELEASE_LOCK(%s)", [self.lock_name])
        row = cursor.fetchone()
        return True if row[0] else False

    def __del__(self):
        self.release()


class FileLock:
    def __init__(self, lock_name, **kwargs):
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

