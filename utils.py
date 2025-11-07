from decimal import Decimal, ROUND_HALF_UP

import bmesh
import bpy


def calculate_dpi_decimal(pixels, cm):
    """
    通过物理尺寸(厘米)及像素数量求DPI（使用Decimal模块确保精度）
    Calculate DPI using physical dimensions (in centimeters) and pixel count (using the Decimal module to ensure precision)
    参数:
        pixels (int/float/Decimal): 像素数量
        cm (int/float/Decimal): 厘米值
    返回:
        Decimal: DPI值(每英寸的点数)，保留2位小数
    """
    # 转换为Decimal类型确保精度
    pixels_dec = Decimal(str(pixels))
    cm_dec = Decimal(str(cm))
    inch_per_cm = Decimal('2.54')  # 1英寸=2.54厘米

    # 计算英寸数：厘米 / 2.54
    inches = cm_dec / inch_per_cm

    # 计算DPI：像素 / 英寸
    dpi = pixels_dec / inches

    # 四舍五入保留2位小数
    return dpi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def pixels_to_cm_decimal(pixels, dpi):
    """
    通过像素点及DPI求物理单位(厘米)（使用Decimal模块确保精度）
    Calculate physical units (centimeters) from pixels and DPI (using the Decimal module to ensure precision)
    参数:
        pixels (int/float/Decimal): 像素数量
        dpi (int/float/Decimal): 每英寸的点数
    返回:
        Decimal: 厘米值，保留2位小数
    """
    pixels_dec = Decimal(str(pixels))
    dpi_dec = Decimal(str(dpi))
    inch_per_cm = Decimal('2.54')

    inches = pixels_dec / dpi_dec
    cm = inches * inch_per_cm

    return cm.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def cm_to_pixels_decimal(cm, dpi):
    """
    通过DPI及物理单位(厘米)求像素点（使用Decimal模块确保精度）
    Calculate pixels using DPI and physical units (centimeters) (use the Decimal module to ensure precision)
    参数:
        cm (int/float/Decimal): 厘米值
        dpi (int/float/Decimal): 每英寸的点数
    返回:
        Decimal: 像素数量，保留0位小数（整数像素）
    """
    cm_dec = Decimal(str(cm))
    dpi_dec = Decimal(str(dpi))
    inch_per_cm = Decimal('2.54')

    inches = cm_dec / inch_per_cm
    pixels = inches * dpi_dec

    return pixels.quantize(Decimal('1'), rounding=ROUND_HALF_UP).to_integral_value()


def create_plane_by_bmesh(width_cm=15, height_cm=10, name="Rectangle_Plane"):
    """
    使用BMesh创建矩形面片（可指定宽度和高度）

    参数:
        width_cm: 宽度（厘米）
        height_cm: 高度（厘米）
        name: 对象名称
    """
    # 单位转换
    width_m = width_cm / 100
    height_m = height_cm / 100

    # 创建BMesh实例
    bm = bmesh.new()

    # 添加平面几何体
    bmesh.ops.create_grid(
        bm,
        x_segments=1,
        y_segments=1,
        size=0.5  # 初始大小，后面会缩放
    )

    # 缩放至指定尺寸
    bmesh.ops.scale(
        bm,
        vec=(width_m, height_m, 1),
        verts=bm.verts
    )

    # 创建网格和对象
    mesh = bpy.data.meshes.new(name + "_Mesh")
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    print(f"创建了 {width_cm}cm × {height_cm}cm 的矩形面片")
    return obj
