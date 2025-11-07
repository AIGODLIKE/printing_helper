import bpy

from .update import update_physical


class PrintingHelperProperties(bpy.types.PropertyGroup):
    args = {
        "min": 0.001,
        "precision": 2,
        "step": 0.1,
        "soft_max": 100000.0,
    }

    def update_x(self, context):
        update_physical("x")

    def update_y(self, context):
        update_physical("y")

    physical_x: bpy.props.FloatProperty(
        name="Width(CM)",
        description="Physical Width",
        update=update_x,
        default=29.1,
        **args
    )
    physical_y: bpy.props.FloatProperty(
        name="Height(CM)",
        description="Physical Height",
        update=update_y,
        default=21,
        **args
    )
    mode: bpy.props.EnumProperty(
        name="Resolution Sync Mode",
        description="How to handle DPI and physical pixels when modifying output resolution",
        items=[
            ("FIXED_DPI", "Fixed DPI", "Keep DPI fixed, modify physical dimensions"),
            ("FIXED_SIZE", "Fixed Size", "Keep the physical dimensions unchanged while modifying the DPI"),
        ],
        default="FIXED_SIZE",
    )

    @property
    def is_fixed_dpi(self) -> bool:
        return self.mode == "FIXED_DPI"

    @property
    def is_fixed_size(self) -> bool:
        return self.mode == "FIXED_SIZE"


def register():
    bpy.utils.register_class(PrintingHelperProperties)
    bpy.types.Scene.printing_helper = bpy.props.PointerProperty(type=PrintingHelperProperties)


def unregister():
    bpy.utils.unregister_class(PrintingHelperProperties)
    del bpy.types.Scene.printing_helper
