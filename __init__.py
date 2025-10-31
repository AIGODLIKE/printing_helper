from . import register_module

bl_info = {
    "name": "Printing Helper",
    "description": "Printing Helper",
    "author": "小萌新",
    "version": (0, 1, 0),
    "blender": (4, 2, 0),
    "location": "",
    "support": "COMMUNITY",
    "category": "3D View",
}

ADDON_VERSION = ".".join([str(v) for v in bl_info["version"]])

import bpy
import bmesh
from bpy.types import Panel, Operator, PropertyGroup
from bpy.props import FloatProperty, IntProperty, EnumProperty, StringProperty


class PrintingHelperProperties(PropertyGroup):
    """插件属性组"""

    # 单位设置
    unit_mode: EnumProperty(
        name="计算模式",
        description="选择计算模式",
        items=[
            ('PHYSICAL', "物理尺寸 → 像素", "从物理尺寸计算像素"),
            ('PIXEL', "像素 → 物理尺寸", "从像素计算物理尺寸")
        ],
        default='PHYSICAL'
    )

    # 物理尺寸输入
    physical_width: FloatProperty(
        name="宽度",
        description="物理宽度",
        default=10.0,
        min=0.001,
        soft_max=1000.0
    )

    physical_height: FloatProperty(
        name="高度",
        description="物理高度",
        default=15.0,
        min=0.001,
        soft_max=1000.0
    )

    physical_unit: EnumProperty(
        name="物理单位",
        description="物理尺寸单位",
        items=[
            ('CM', "厘米", "厘米"),
            ('M', "米", "米"),
            ('INCH', "英寸", "英寸")
        ],
        default='CM'
    )

    # 像素尺寸输入
    pixel_width: IntProperty(
        name="宽度",
        description="像素宽度",
        default=1181,
        min=1,
        soft_max=10000
    )

    pixel_height: IntProperty(
        name="高度",
        description="像素高度",
        default=1772,
        min=1,
        soft_max=10000
    )

    # DPI设置
    dpi_value: IntProperty(
        name="DPI",
        description="像素密度 (每英寸点数)",
        default=300,
        min=72,
        max=1200
    )

    # 网格名称
    grid_name: StringProperty(
        name="网格名称",
        description="生成的网格平面名称",
        default="PrintingGrid"
    )


class PRINTINGHELPER_OT_calculate(Operator):
    """执行计算操作"""
    bl_idname = "printing_helper.calculate"
    bl_label = "计算"
    bl_description = "根据当前设置计算尺寸"

    def execute(self, context):
        props = context.scene.printing_helper

        if props.unit_mode == 'PHYSICAL':
            # 物理尺寸 → 像素
            if props.physical_unit == 'CM':
                # 厘米转英寸再乘DPI
                width_inch = props.physical_width / 2.54
                height_inch = props.physical_height / 2.54
            elif props.physical_unit == 'M':
                # 米转英寸再乘DPI
                width_inch = props.physical_width * 100 / 2.54
                height_inch = props.physical_height * 100 / 2.54
            else:  # 英寸
                width_inch = props.physical_width
                height_inch = props.physical_height

            props.pixel_width = int(width_inch * props.dpi_value)
            props.pixel_height = int(height_inch * props.dpi_value)

        else:  # PIXEL模式
            # 像素 → 物理尺寸
            width_inch = props.pixel_width / props.dpi_value
            height_inch = props.pixel_height / props.dpi_value

            if props.physical_unit == 'CM':
                props.physical_width = width_inch * 2.54
                props.physical_height = height_inch * 2.54
            elif props.physical_unit == 'M':
                props.physical_width = (width_inch * 2.54) / 100
                props.physical_height = (height_inch * 2.54) / 100
            else:  # 英寸
                props.physical_width = width_inch
                props.physical_height = height_inch

        self.report({'INFO'}, "计算完成!")
        return {'FINISHED'}


class PRINTINGHELPER_OT_create_grid(Operator):
    """创建物理尺寸网格平面"""
    bl_idname = "printing_helper.create_grid"
    bl_label = "创建网格平面"
    bl_description = "创建具有正确物理尺寸的网格平面"

    def execute(self, context):
        props = context.scene.printing_helper

        # 删除已存在的同名网格
        if props.grid_name in bpy.data.meshes:
            mesh_to_remove = bpy.data.meshes[props.grid_name]
            bpy.data.meshes.remove(mesh_to_remove)

        # 创建新网格
        bpy.ops.mesh.primitive_plane_add(size=1.0)
        plane = context.active_object
        plane.name = props.grid_name

        # 根据物理单位设置尺寸
        if props.physical_unit == 'CM':
            scale_factor = 0.01  # Blender中1单位=1米，所以厘米要除以100
        elif props.physical_unit == 'M':
            scale_factor = 1.0
        else:  # 英寸
            scale_factor = 0.0254  # 1英寸=0.0254米

        # 应用物理尺寸
        plane.scale.x = props.physical_width * scale_factor
        plane.scale.y = props.physical_height * scale_factor

        # 应用缩放变换
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


        self.report({'INFO'}, f"已创建网格平面: {props.grid_name}")
        return {'FINISHED'}


class PRINTINGHELPER_PT_main_panel(Panel):
    """主面板"""
    bl_label = "印刷助手"
    bl_idname = "PRINTINGHELPER_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Printing Helper"

    def draw(self, context):
        layout = self.layout
        props = context.scene.printing_helper

        # DPI设置
        box = layout.box()
        box.label(text="DPI设置")
        box.prop(props, "dpi_value")

        # 计算模式选择
        box = layout.box()
        box.label(text="计算模式")
        box.prop(props, "unit_mode", expand=True)

        if props.unit_mode == 'PHYSICAL':
            # 物理尺寸输入
            box = layout.box()
            box.label(text="物理尺寸")
            row = box.row()
            row.prop(props, "physical_unit", expand=True)

            col = box.column(align=True)
            col.prop(props, "physical_width")
            col.prop(props, "physical_height")

            # 计算结果
            box = layout.box()
            box.label(text="计算结果 - 像素尺寸")
            col = box.column(align=True)
            col.label(text=f"宽度: {props.pixel_width} 像素")
            col.label(text=f"高度: {props.pixel_height} 像素")

        else:  # PIXEL模式
            # 像素尺寸输入
            box = layout.box()
            box.label(text="像素尺寸")
            col = box.column(align=True)
            col.prop(props, "pixel_width")
            col.prop(props, "pixel_height")

            # 计算结果
            box = layout.box()
            box.label(text="计算结果 - 物理尺寸")
            row = box.row()
            row.prop(props, "physical_unit", expand=True)

            col = box.column(align=True)
            col.label(text=f"宽度: {props.physical_width:.2f} {self.get_unit_text(props.physical_unit)}")
            col.label(text=f"高度: {props.physical_height:.2f} {self.get_unit_text(props.physical_unit)}")

        # 操作按钮
        box = layout.box()
        box.operator("printing_helper.calculate", icon='FORCE_HARMONIC')
        box.operator("printing_helper.create_grid", icon='MESH_GRID')
        box.prop(props, "grid_name")

    def get_unit_text(self, unit):
        """获取单位文本"""
        if unit == 'CM':
            return "cm"
        elif unit == 'M':
            return "m"
        else:
            return "inch"


classes = (
    PrintingHelperProperties,
    PRINTINGHELPER_OT_calculate,
    PRINTINGHELPER_OT_create_grid,
    PRINTINGHELPER_PT_main_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.printing_helper = bpy.props.PointerProperty(type=PrintingHelperProperties)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.printing_helper
