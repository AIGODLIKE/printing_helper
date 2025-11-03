import bpy

modules = ["property", "panel", "preset"]

reg, un_reg = bpy.utils.register_submodule_factory(__package__, modules)


def register():
    reg()


def unregister():
    un_reg()
