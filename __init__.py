from . import register_module

bl_info = {
    "name": "Printing Helper",
    "description": "Printing Helper",
    "author": "小萌新",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "location": "",
    "support": "COMMUNITY",
    "category": "3D View",
}

ADDON_VERSION = ".".join([str(v) for v in bl_info["version"]])


def register():
    register_module.register()


def unregister():
    register_module.unregister()
