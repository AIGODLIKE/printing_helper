import bpy

owner = object()
__is_updatable__ = False


def update_lock(func, ):
    """缓存更新锁"""

    def wap(*args, **kwargs):
        global __is_updatable__
        if __is_updatable__:
            __is_updatable__ = False
            func_return = func(*args, **kwargs)
            __is_updatable__ = True
            return func_return
        return None

    return wap


def update_ppm_factor():
    print("update_ppm_factor")


def update_resolution_x():
    print("update_resolution_x")
    ph = bpy.context.scene.render.resolution_x


def update_resolution_y():
    print("update_resolution_y")


bpy.msgbus.subscribe_rna(
    key=(bpy.types.RenderSettings, "ppm_factor"),
    owner=owner,
    args=(),
    notify=update_ppm_factor,
)
bpy.msgbus.subscribe_rna(
    key=(bpy.types.RenderSettings, "resolution_x"),
    owner=owner,
    args=(),
    notify=update_resolution_x,
)
bpy.msgbus.subscribe_rna(
    key=(bpy.types.RenderSettings, "resolution_y"),
    owner=owner,
    args=(),
    notify=update_resolution_y,
)


def register():
    update_resolution_x()
    update_resolution_y()
    ...


def unregister():
    bpy.msgbus.clear_by_owner(owner)
