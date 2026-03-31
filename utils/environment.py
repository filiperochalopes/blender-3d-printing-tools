import bpy


def _ranges_overlap(start_a, size_a, start_b, size_b):
    end_a = start_a + size_a
    end_b = start_b + size_b
    return min(end_a, end_b) > max(start_a, start_b)


def _get_area_center(area):
    return (
        area.x + int(area.width / 2),
        area.y + int(area.height / 2),
    )


def _find_area_to_join(screen, source_area):
    best_area = None
    best_score = -1

    for area in screen.areas:
        if area == source_area:
            continue

        shares_vertical_border = (
            (source_area.x + source_area.width == area.x or area.x + area.width == source_area.x)
            and _ranges_overlap(source_area.y, source_area.height, area.y, area.height)
        )
        shares_horizontal_border = (
            (source_area.y + source_area.height == area.y or area.y + area.height == source_area.y)
            and _ranges_overlap(source_area.x, source_area.width, area.x, area.width)
        )

        if not shares_vertical_border and not shares_horizontal_border:
            continue

        score = 2 if area.type == 'VIEW_3D' else 1
        if score > best_score:
            best_area = area
            best_score = score

    return best_area


def get_window_and_screen(context):
    window = getattr(context, "window", None)
    screen = getattr(context, "screen", None)

    if screen is None and window is not None:
        screen = window.screen

    if window is None:
        window = getattr(bpy.context, "window", None)

    if screen is None and window is not None:
        screen = window.screen

    if screen is None:
        screen = getattr(bpy.context, "screen", None)

    if window is None and screen is not None:
        window_manager = getattr(bpy.context, "window_manager", None)
        if window_manager is not None:
            for candidate_window in window_manager.windows:
                if candidate_window.screen == screen:
                    window = candidate_window
                    break

    return window, screen


def get_area_window_region(area):
    return next((region for region in area.regions if region.type == 'WINDOW'), None)


def get_largest_view_3d_area(screen):
    view_3d_areas = [area for area in screen.areas if area.type == 'VIEW_3D']
    if not view_3d_areas:
        return None

    return max(view_3d_areas, key=lambda area: area.width * area.height)


def configure_outliner_area(context, window, screen, area):
    region = get_area_window_region(area)
    override_args = {"window": window, "screen": screen, "area": area}
    if region is not None:
        override_args["region"] = region

    try:
        with context.temp_override(**override_args):
            bpy.ops.wm.context_set_enum(data_path="area.type", value='OUTLINER')
    except RuntimeError:
        area.type = 'OUTLINER'
    else:
        area.type = 'OUTLINER'

    try:
        area.ui_type = 'OUTLINER'
    except TypeError:
        pass

    for space in area.spaces:
        if space.type == 'OUTLINER':
            space.display_mode = 'VIEW_LAYER'
            break


def close_outliner_areas(context, keep_areas=None):
    window, screen = get_window_and_screen(context)
    if window is None or screen is None:
        return

    keep_area_pointers = {area.as_pointer() for area in (keep_areas or [])}
    outliner_areas = [
        area for area in screen.areas
        if area.type == 'OUTLINER' and area.as_pointer() not in keep_area_pointers
    ]
    outliner_areas.sort(key=lambda area: area.x, reverse=True)

    for area in outliner_areas:
        if len(screen.areas) <= 1:
            break

        region = get_area_window_region(area)

        try:
            override_args = {"window": window, "screen": screen, "area": area}
            if region:
                override_args["region"] = region

            with context.temp_override(**override_args):
                result = bpy.ops.screen.area_close()

            if 'FINISHED' in result:
                continue
        except RuntimeError:
            pass

        target_area = _find_area_to_join(screen, area)
        if not target_area:
            continue

        with context.temp_override(window=window, screen=screen, area=area):
            bpy.ops.screen.area_join(
                source_xy=_get_area_center(area),
                target_xy=_get_area_center(target_area),
            )


def ensure_outliner_area(context, window, screen):
    close_outliner_areas(context)

    source_area = get_largest_view_3d_area(screen)
    if source_area is None:
        return None

    region = get_area_window_region(source_area)
    override_args = {"window": window, "screen": screen, "area": source_area}
    if region is not None:
        override_args["region"] = region

    try:
        with context.temp_override(**override_args):
            result = bpy.ops.screen.area_split(direction='VERTICAL', factor=0.2)
    except RuntimeError:
        return None

    if 'FINISHED' not in result:
        return None

    all_areas = [area for area in screen.areas]
    if not all_areas:
        return None

    outliner_area = all_areas[-1]
    configure_outliner_area(context, window, screen, outliner_area)
    return outliner_area


def configure_environment(context):
    unit_settings = context.scene.unit_settings
    unit_settings.system = 'METRIC'
    unit_settings.scale_length = 0.001
    unit_settings.length_unit = 'MILLIMETERS'
    unit_settings.system_rotation = 'DEGREES'

    tool_settings = context.scene.tool_settings
    tool_settings.use_snap = True
    tool_settings.snap_elements_base = {'VERTEX'}

    window, screen = get_window_and_screen(context)
    if window is not None and screen is not None:
        ensure_outliner_area(context, window, screen)

    areas = [area for area in screen.areas if area.type == 'VIEW_3D'] if screen is not None else []

    for area in areas:
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'SOLID'
                space.shading.show_xray = True
                space.overlay.grid_scale = 0.001
                space.clip_start = 0.1
                space.clip_end = 10000

    if context.scene.camera:
        context.scene.camera.data.clip_start = 0.1
        context.scene.camera.data.clip_end = 10000

    for obj in list(context.scene.objects):
        if obj.type == 'LIGHT' or obj.type == 'CAMERA':
            bpy.data.objects.remove(obj, do_unlink=True)

    view_layer = getattr(context, "view_layer", None) or getattr(bpy.context, "view_layer", None)
    if view_layer is not None:
        view_layer.update()
