from . import register_module

bl_info = {
    "name": "Printing Helper",
    "description": "Set the resolution required for printing more simply",
    "author": "ACGGIT Community(小萌新)",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "location": "",
    "support": "COMMUNITY",
    "category": "Render",
}

ADDON_VERSION = ".".join([str(v) for v in bl_info["version"]])


def register():
    register_module.register()


def unregister():
    register_module.unregister()
