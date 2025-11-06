import bpy

from .update import update_lock
from .utils import cm_to_pixels_decimal


@update_lock
def update_physical(direction="x"):
    from .update import last_update
    print("update_physical", direction)
    scene = bpy.context.scene
    ph = scene.printing_helper
    render = scene.render

    rk = f"resolution_{direction.lower()}"
    pk = f"physical_{direction.lower()}"

    new_pixels = int(cm_to_pixels_decimal(getattr(ph, pk), render.ppm_factor))
    setattr(render, rk, new_pixels)
    k = f"update_resolution_{direction.lower()}"
    if k not in last_update:
        last_update.append(k)


class PrintingHelperProperties(bpy.types.PropertyGroup):
    """插件属性组"""
    args = {
        "min": 0.001,
        "precision": 2,
        "step": 0.1,
        "soft_max": 100000.0,
        "default": 10,
    }

    def update_x(self, context):
        print("update_physica_x")
        update_physical("x")

    def update_y(self, context):
        print("update_physica_y")
        update_physical("y")

    # 物理尺寸输入
    physical_x: bpy.props.FloatProperty(
        name="Width(CM)",
        description="Physical Width",
        update=update_x,
        **args
    )
    physical_y: bpy.props.FloatProperty(
        name="Height(CM)",
        description="Physical Height",
        update=update_y,
        **args
    )
    mode: bpy.props.EnumProperty(
        name="Resolution Sync Mode",
        items=[
            ("FIXED_DPI", "Fixed DPI", ""),
            ("FIXED_SIZE", "Fixed Size", ""),
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
