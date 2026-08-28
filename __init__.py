import os
import subprocess

CPP_SUFFIX = (".cpp", ".cxx", ".cc", ".ipp", ".ixx")
C_SUFFIX = ".c"

def _try_run(args: str):
    try:
        subprocess.run(args)
    except subprocess.CalledProcessError:
        print("\033[31mCompilation error...\033[m")
    except OSError:
        print("\033[31mCannot run the command...\033[m")

def _search_dir(target: str, path="."):
    with os.scandir(path) as entry:
        for item in entry:
            if item.name == target and item.is_dir():
                return True
    return False

def _search_file(target: str, path="."):
    with os.scandir(path) as entry:
        for item in entry:
            if item.name == target and item.is_file():
                return True
    return False

def is_empty(string: str):
    return string == ""

class Builder():
    def __init__(self, compiler=""):
        self.__compiler = compiler
        self.__source_files = list()
        self.__executable_name = str()
        self.__flags = str()
    
    def compiler(self):
        return self.__compiler

    def set_compiler(self, name: str):
        self.__compiler = name

    def executable_name(self):
        return self.__executable_name

    def set_executable_name(self, name: str):
        self.__executable_name = name

    def source_files(self):
        return self.__source_files

    def get_sources(self, path: str):
        """
        Enter the path and search for valid source codes files, and
        returns a list of source code paths.
        """
        with os.scandir(path) as entry:
            for item in entry:
                fname = item.name
                if item.is_file() and fname.endswith(CPP_SUFFIX) or fname.endswith(C_SUFFIX):
                    self.__source_files.append(item.path)
                elif item.is_dir():
                    self.get_sources(item.path)
        return self.__source_files

    def flags(self):
        return self.__flags

    def set_flags(self, *args):
        """
        Set flags for the compiler
        """
        flags = ""
        for flag in args:
            flags += f"{flag} "
        self.__flags = flags

    def build_executable(self, builddir=".", executablename=""):
        """
        Build an executable to a given build path
        """
        if is_empty(self.__compiler):
            print("\033[31mCannot detect compiler... Compilation failed!\033[m")
            return
        if executablename == "":
            executablename = self.__executable_name
        sourcefiles = ""
        for file in self.__source_files:
            sourcefiles = sourcefiles + f"{file} "
        cmd = f"{self.__compiler} "
        if not is_empty(self.__flags):
            cmd += f"{self.__flags}"
        if not is_empty(sourcefiles):
            cmd += f"{sourcefiles}"
        if not is_empty(executablename):
            cmd += f"-o {builddir}/{executablename}"
        if builddir != ".":
            if not _search_dir(builddir):
                os.mkdir(builddir)
        print(cmd)
        # _try_run(cmd)
