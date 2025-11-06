import bpy


class SwitchXY(bpy.types.Operator):
    bl_idname = "render.switch_xy"
    bl_label = "Switch XY"

    def execute(self, context):
        scene = context.scene
        ph = scene.printing_helper
        ph.physical_x, ph.physical_y = ph.physical_y, ph.physical_x
        return {"FINISHED"}


def register():
    bpy.utils.register_class(SwitchXY)


def unregister():
    bpy.utils.unregister_class(SwitchXY)
