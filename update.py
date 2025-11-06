import bpy

from .utils import pixels_to_cm_decimal, cm_to_pixels_decimal, calculate_dpi_decimal

owner = object()
__is_updatable__ = True
last_update = []  # 另外一个锁


def update_lock(func, ):
    def wap(*args, **kwargs):
        global __is_updatable__
        if __is_updatable__:
            __is_updatable__ = False
            try:
                func_return = func(*args, **kwargs)
                __is_updatable__ = True
                return func_return
            finally:
                __is_updatable__ = True
        return None
    return wap


@update_lock
def update_ppm_factor():
    print("update_ppm_factor")
    scene = bpy.context.scene
    ph = scene.printing_helper
    render = scene.render
    render.resolution_x = int(cm_to_pixels_decimal(ph.physical_x, render.ppm_factor))
    render.resolution_y = int(cm_to_pixels_decimal(ph.physical_y, render.ppm_factor))
    global last_update

    last_update.append("update_resolution_x")
    last_update.append("update_resolution_y")
    print("update_ppm_factor end")


@update_lock
def update_resolution(direction="x", fixed_dpi=None, fixed_size=None):
    scene = bpy.context.scene
    ph = scene.printing_helper
    render = scene.render

    rk = f"resolution_{direction.lower()}"
    pk = f"physical_{direction.lower()}"
    value = getattr(render, rk, 114)
    if ph.is_fixed_dpi or fixed_dpi:  # 固定DPI,设置物理尺寸
        new_cm = pixels_to_cm_decimal(value, render.ppm_factor)
        setattr(ph, pk, new_cm)
        print("pixels_to_cm_decimal", new_cm, direction)
    elif ph.is_fixed_size or fixed_size:  # 固定物理尺寸,设置DPI
        new_dpi = calculate_dpi_decimal(value, getattr(ph, pk))
        render.ppm_factor = new_dpi
        print("calculate_dpi_decimal", new_dpi, direction)


def update_resolution_x():
    global __is_updatable__, last_update
    if "update_resolution_x" in last_update:
        last_update.remove("update_resolution_x")
    elif __is_updatable__:
        print("update_resolution_x")
        update_resolution("x")


def update_resolution_y():
    global __is_updatable__
    if "update_resolution_y" in last_update:
        last_update.remove("update_resolution_y")
    elif __is_updatable__:
        print("update_resolution_y")
        update_resolution("y")


bpy.msgbus.subscribe_rna(
    key=(bpy.types.RenderSettings, "ppm_factor"),
    owner=owner,
    args=(),
    notify=lambda: update_ppm_factor(),
)
bpy.msgbus.subscribe_rna(
    key=(bpy.types.RenderSettings, "resolution_x"),
    owner=owner,
    args=(),
    notify=lambda: update_resolution_x(),
)
bpy.msgbus.subscribe_rna(
    key=(bpy.types.RenderSettings, "resolution_y"),
    owner=owner,
    args=(),
    notify=lambda: update_resolution_y(),
)


def init_register():
    update_resolution_x()
    update_resolution_y()


def register():
    bpy.app.timers.register(init_register, first_interval=0.1, persistent=True)


def unregister():
    bpy.msgbus.clear_by_owner(owner)
