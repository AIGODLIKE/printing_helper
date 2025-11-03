import bpy


class PrintingHelperProperties(bpy.types.PropertyGroup):
    """插件属性组"""
    # 物理尺寸输入
    physical_width: bpy.props.FloatProperty(
        name="宽度",
        description="物理宽度",
        default=10.0,
        min=0.001,
        soft_max=1000.0
    )
    physical_height: bpy.props.FloatProperty(
        name="高度",
        description="物理高度",
        default=15.0,
        min=0.001,
        soft_max=1000.0
    )


def register():
    bpy.utils.register_class(PrintingHelperProperties)

    bpy.types.Scene.printing_helper = bpy.props.PointerProperty(type=PrintingHelperProperties)


def unregister():
    bpy.utils.unregister_class(PrintingHelperProperties)
    del bpy.types.Scene.printing_helper
