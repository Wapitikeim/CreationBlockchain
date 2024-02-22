import bpy
import os
import sys
import io
import tempfile
from contextlib import contextmanager
import ctypes
from ctypes.util import find_library

class _FILE(ctypes.Structure):
    """opaque C FILE type"""

def c_fflush():
    try:
        libc = ctypes.cdll.LoadLibrary(find_library('ucrtbase'))
        libc.__acrt_iob_func.restype = ctypes.POINTER(_FILE)
        stdout = libc.__acrt_iob_func(1)
        libc.fflush(stdout)
        #stream.flush()
    except (AttributeError, ValueError, IOError):
        pass

@contextmanager
def redirect_c_stdout(binary_stream):
    __stack_tmp_file = tempfile.NamedTemporaryFile(mode='w+b', buffering=0, delete=False, dir=bpy.app.tempdir)
    stdout_file_descriptor = sys.stdout.fileno()
    original_stdout_file_descriptor_copy = os.dup(stdout_file_descriptor)
    try:
        # Flush the C-level buffer of stdout before redirecting.  This should make sure that only the desired data is captured.
        c_fflush()
        #  Move the file pointer to the start of the file
        __stack_tmp_file.seek(0)
        # Redirect stdout to your pipe.
        os.dup2(__stack_tmp_file.fileno(), stdout_file_descriptor)
        yield  # wait for input
    finally:
        # Flush the C-level buffer of stdout before returning things to normal.  This seems to be mainly needed on Windows because it looks like Windows changes the buffering policy to be fully buffered when redirecting stdout.
        c_fflush()
        # Redirect stdout back to the original file descriptor.
        os.dup2(original_stdout_file_descriptor_copy, stdout_file_descriptor)
        # Truncate file to the written amount of bytes
        __stack_tmp_file.truncate()
        #  Move the file pointer to the start of the file
        __stack_tmp_file.seek(0)
        # Write back to the input stream
        binary_stream.write(__stack_tmp_file.read())
        # Close the remaining open file descriptor.
        os.close(original_stdout_file_descriptor_copy)

def writeUndoStepsIntoFile():
    binary_stream = io.BytesIO()
    with redirect_c_stdout(binary_stream):
        bpy.context.window_manager.print_undo_steps()
    undo_steps_dump = binary_stream.getvalue().decode(sys.stdout.encoding)
    binary_stream.close()
    undo_steps = undo_steps_dump.split("\n")[1:-1]
    with open('INSERTPATH/scripts/undo_log.txt', 'w') as undoSteps:
        i = 0
        for step in undo_steps:
            undoSteps.write(step)
            undoSteps.write("\n")
            i+=1
    return i 

def everySecond():
    writeUndoStepsIntoFile()
    """ blender is just taking screenshots too slowly :/
    if(newCount != oldCount):
        oldCount = newCount
        bpy.ops.screen.screenshot(filepath="//C://Users//Wenz//Desktop//CreationBlockchain//out_put.png") """
    return 0.2

bpy.app.timers.register(everySecond, persistent=True)