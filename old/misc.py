import bpy

context = bpy.context

# change to info
context.area.type = 'INFO'
bpy.ops.info.select_all()
bpy.ops.info.report_copy()
context.area.type = 'TEXT_EDITOR'
clipboard = bpy.context.window_manager.clipboard 

file = open("C:\Users\Wenz\Desktop\CreationBlockchain\scripts\info_log.txt", "w")
for line in clipboard:
    file.write(line)
file.close()