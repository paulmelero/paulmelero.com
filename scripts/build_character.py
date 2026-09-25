"""
Build a faceted low-poly waist-up character of Paul for Three.js.

Run headless:
    /Applications/Blender.app/Contents/MacOS/Blender --background --python scripts/build_character.py

Outputs:
    public/models/paul.glb       (runtime asset for Three.js)
    public/models/paul.blend     (editable source)
    /tmp/opencode/previews/*.png (front / 3q / side / face checks)
"""

import math
import os
import random

import bmesh
import bpy
from mathutils import Vector

random.seed(7)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "public", "models")
PREVIEW_DIR = "/tmp/opencode/previews"

HEAD_Z = 0.60
SHOULDER_Z = 0.44
WAIST_Z = 0.0


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hexcol(h, alpha=1.0):
    h = h.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    return (srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b), alpha)


def make_mat(name, color_hex, roughness=0.7, metallic=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = hexcol(color_hex, alpha)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        m.blend_method = "BLEND"
    m.diffuse_color = hexcol(color_hex, alpha)
    return m


def set_active(obj):
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def shade_flat(obj):
    set_active(obj)
    bpy.ops.object.shade_flat()


def assign_mat(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def ellipse_ring(z, rx, ry, cx=0.0, cy=0.0, n=12, rot=0.0):
    return [
        (
            cx + rx * math.cos(2 * math.pi * i / n + rot),
            cy + ry * math.sin(2 * math.pi * i / n + rot),
            z,
        )
        for i in range(n)
    ]


def rect_ring(z, cx, cy, hx, hy):
    return [
        (cx - hx, cy - hy, z),
        (cx + hx, cy - hy, z),
        (cx + hx, cy + hy, z),
        (cx - hx, cy + hy, z),
    ]


def loft(name, rings, cap_bottom=True, cap_top=True):
    bm = bmesh.new()
    layers = [[bm.verts.new(p) for p in ring] for ring in rings]
    for a, b in zip(layers, layers[1:]):
        n = len(a)
        for i in range(n):
            bm.faces.new([a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]])
    if cap_bottom:
        bm.faces.new(list(reversed(layers[0])))
    if cap_top:
        bm.faces.new(layers[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    return obj


def primitive(name, op, mat=None, **kw):
    op(**kw)
    obj = bpy.context.active_object
    obj.name = name
    if mat:
        assign_mat(obj, mat)
    shade_flat(obj)
    return obj


def duplicate(obj, name):
    new = obj.copy()
    new.data = obj.data.copy()
    new.name = name
    bpy.context.collection.objects.link(new)
    return new


def mesh_center(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    c = Vector((0, 0, 0))
    for v in bm.verts:
        c += v.co
    c /= len(bm.verts)
    bm.free()
    return c


# --------------------------------------------------------------------------- #
# head
# --------------------------------------------------------------------------- #
def build_head(mat_skin):
    rings = [
        ellipse_ring(-0.105, 0.020, 0.030, cy=0.052, n=16),
        ellipse_ring(-0.090, 0.038, 0.046, cy=0.044, n=16),
        ellipse_ring(-0.070, 0.055, 0.060, cy=0.030, n=16),
        ellipse_ring(-0.050, 0.068, 0.068, cy=0.018, n=16),
        ellipse_ring(-0.030, 0.076, 0.073, cy=0.010, n=16),
        ellipse_ring(-0.010, 0.081, 0.076, cy=0.004, n=16),
        ellipse_ring(0.010, 0.083, 0.078, cy=0.000, n=16),
        ellipse_ring(0.030, 0.082, 0.077, cy=-0.002, n=16),
        ellipse_ring(0.050, 0.078, 0.074, cy=-0.004, n=16),
        ellipse_ring(0.070, 0.070, 0.068, cy=-0.006, n=16),
        ellipse_ring(0.090, 0.056, 0.056, cy=-0.008, n=16),
        ellipse_ring(0.108, 0.034, 0.036, cy=-0.010, n=16),
    ]
    head = loft("Head", rings)
    for v in head.data.vertices:
        if 0.018 < v.co.z < 0.048 and v.co.y > 0.045:
            v.co.y += 0.005 * (1 - abs(v.co.z - 0.033) / 0.015)
    assign_mat(head, mat_skin)
    shade_flat(head)
    return head


def build_ears(mat_skin):
    ears = []
    for sx in (-1, 1):
        e = primitive(
            f"Ear_{'R' if sx > 0 else 'L'}",
            bpy.ops.mesh.primitive_uv_sphere_add,
            mat_skin,
            segments=8,
            ring_count=6,
            radius=0.020,
            location=(sx * 0.076, -0.004, 0.000),
        )
        e.scale = (0.45, 0.85, 1.15)
        bpy.ops.object.transform_apply(scale=True)
        ears.append(e)
    return ears


def build_nose(mat_skin):
    rings = [
        rect_ring(0.030, 0.0, 0.070, 0.006, 0.005),
        rect_ring(0.012, 0.0, 0.080, 0.0075, 0.006),
        rect_ring(-0.006, 0.0, 0.089, 0.010, 0.008),
        rect_ring(-0.020, 0.0, 0.089, 0.013, 0.009),
        rect_ring(-0.028, 0.0, 0.079, 0.012, 0.008),
    ]
    nose = loft("Nose", rings)
    assign_mat(nose, mat_skin)
    shade_flat(nose)
    return nose


def shell_from_head(head, name, mat, keep, scale, thickness, spike=0.0):
    obj = duplicate(head, name)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    center = mesh_center(obj)
    for v in bm.verts:
        v.co = center + (v.co - center) * scale
    drop = [f for f in bm.faces if not keep(f.calc_center_median())]
    bmesh.ops.delete(bm, geom=drop, context="FACES")
    bm.to_mesh(obj.data)
    bm.free()

    if spike > 0:
        for v in obj.data.vertices:
            up = max(0.0, (v.co.z - center.z) / 0.12)
            v.co += Vector(
                (
                    random.uniform(-1, 1) * spike * up,
                    random.uniform(-1, 1) * spike * up,
                    random.uniform(0, 1) * spike * 1.5 * up,
                )
            )

    sol = obj.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = thickness
    sol.offset = 0.0
    set_active(obj)
    bpy.ops.object.modifier_apply(modifier=sol.name)

    assign_mat(obj, mat)
    shade_flat(obj)
    return obj


def build_hair(head, mat_hair):
    def keep(c):
        face = c.y > 0.015 and c.z < 0.062 and abs(c.x) < 0.085
        side_low = abs(c.x) > 0.072 and c.z < -0.010
        nape = c.z < -0.055
        return not (face or side_low or nape)

    return shell_from_head(
        head, "Hair", mat_hair, keep, scale=1.020, thickness=0.009, spike=0.007
    )


def build_beard(head, mat_hair):
    def keep(c):
        jaw = -0.100 < c.z < -0.015 and c.y > -0.020
        cheek = abs(c.x) > 0.055 and -0.100 < c.z < 0.025 and c.y > -0.010
        return jaw or cheek

    return shell_from_head(
        head, "Beard", mat_hair, keep, scale=1.012, thickness=0.007, spike=0.002
    )


def build_eyes(mat_white, mat_iris):
    eyes = []
    for sx in (-1, 1):
        eyes.append(
            primitive(
                f"Eye_{'R' if sx > 0 else 'L'}",
                bpy.ops.mesh.primitive_uv_sphere_add,
                mat_white,
                segments=10,
                ring_count=8,
                radius=0.0095,
                location=(sx * 0.031, 0.070, 0.010),
            )
        )
        eyes.append(
            primitive(
                f"Iris_{'R' if sx > 0 else 'L'}",
                bpy.ops.mesh.primitive_uv_sphere_add,
                mat_iris,
                segments=8,
                ring_count=6,
                radius=0.0055,
                location=(sx * 0.031, 0.078, 0.009),
            )
        )
    return eyes


def build_brows(mat_hair):
    brows = []
    for sx in (-1, 1):
        b = primitive(
            f"Brow_{'R' if sx > 0 else 'L'}",
            bpy.ops.mesh.primitive_cube_add,
            mat_hair,
            size=1.0,
            location=(sx * 0.030, 0.080, 0.029),
        )
        b.scale = (0.021, 0.008, 0.0045)
        b.rotation_euler = (0, sx * math.radians(8), 0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        brows.append(b)
    return brows


def build_glasses(mat_frame):
    parts = []
    for sx in (-1, 1):
        frame = primitive(
            f"Lens_{'R' if sx > 0 else 'L'}",
            bpy.ops.mesh.primitive_torus_add,
            mat_frame,
            major_segments=18,
            minor_segments=5,
            major_radius=0.020,
            minor_radius=0.0035,
            location=(sx * 0.032, 0.086, 0.010),
        )
        frame.scale = (1.42, 1.0, 0.82)
        frame.rotation_euler = (math.radians(90), 0, 0)
        bpy.ops.object.transform_apply(rotation=True, scale=True)
        parts.append(frame)

        temple = primitive(
            f"Temple_{'R' if sx > 0 else 'L'}",
            bpy.ops.mesh.primitive_cube_add,
            mat_frame,
            size=1.0,
            location=(sx * 0.066, 0.045, 0.016),
        )
        temple.scale = (0.0032, 0.048, 0.0042)
        bpy.ops.object.transform_apply(scale=True)
        parts.append(temple)

    bridge = primitive(
        "Bridge",
        bpy.ops.mesh.primitive_cube_add,
        mat_frame,
        size=1.0,
        location=(0.0, 0.090, 0.020),
    )
    bridge.scale = (0.010, 0.004, 0.0035)
    bpy.ops.object.transform_apply(scale=True)
    parts.append(bridge)
    return parts


# --------------------------------------------------------------------------- #
# body
# --------------------------------------------------------------------------- #
def build_body_volume():
    verts = [
        (0.0, 0.006, 0.02),  # 0 waist
        (0.0, 0.006, 0.16),  # 1 belly
        (0.0, 0.000, 0.30),  # 2 chest
        (0.0, 0.000, 0.40),  # 3 upper chest
        (0.0, 0.000, 0.45),  # 4 neck base
        (0.13, 0.000, 0.42),  # 5 shoulder L
        (0.185, 0.012, 0.20),  # 6 elbow L
        (0.195, 0.015, 0.02),  # 7 wrist L
        (-0.13, 0.000, 0.42),  # 8 shoulder R
        (-0.185, 0.012, 0.20),  # 9 elbow R
        (-0.195, 0.015, 0.02),  # 10 wrist R
    ]
    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (3, 5),
        (5, 6),
        (6, 7),
        (3, 8),
        (8, 9),
        (9, 10),
    ]
    radii = {
        0: 0.112,
        1: 0.118,
        2: 0.116,
        3: 0.110,
        4: 0.082,
        5: 0.068,
        6: 0.056,
        7: 0.048,
        8: 0.068,
        9: 0.056,
        10: 0.048,
    }

    me = bpy.data.meshes.new("BodyVolume")
    me.from_pydata(verts, edges, [])
    me.update()
    obj = bpy.data.objects.new("BodyVolume", me)
    bpy.context.collection.objects.link(obj)
    set_active(obj)

    obj.modifiers.new("Skin", "SKIN")
    sv = obj.data.skin_vertices[0].data
    for i, r in radii.items():
        sv[i].radius = (r, r)
    sv[0].use_root = True
    bpy.ops.object.modifier_apply(modifier="Skin")

    sub = obj.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = 1
    bpy.ops.object.modifier_apply(modifier="Subsurf")

    smooth = obj.modifiers.new("Smooth", "SMOOTH")
    smooth.factor = 0.5
    smooth.iterations = 2
    bpy.ops.object.modifier_apply(modifier="Smooth")

    dec = obj.modifiers.new("Decimate", "DECIMATE")
    dec.decimate_type = "COLLAPSE"
    dec.ratio = 0.55
    bpy.ops.object.modifier_apply(modifier="Decimate")
    shade_flat(obj)
    return obj


def build_clothing(body, mat_shirt, mat_light, mat_dark):
    center = mesh_center(body)

    shirt = duplicate(body, "TShirt")
    for v in shirt.data.vertices:
        v.co = center + (v.co - center) * 0.985
    assign_mat(shirt, mat_shirt)

    jacket = duplicate(body, "Jacket")
    for v in jacket.data.vertices:
        v.co = center + (v.co - center) * 1.022
    assign_mat(jacket, mat_light)

    bm = bmesh.new()
    bm.from_mesh(jacket.data)
    drop = []
    for f in bm.faces:
        c = f.calc_center_median()
        if c.y > 0.03 and abs(c.x) < 0.045 and c.z < 0.415:
            drop.append(f)
    bmesh.ops.delete(bm, geom=drop, context="FACES")
    bm.to_mesh(jacket.data)
    bm.free()

    sol = jacket.modifiers.new("Solidify", "SOLIDIFY")
    sol.thickness = 0.012
    sol.offset = 0.0
    set_active(jacket)
    bpy.ops.object.modifier_apply(modifier=sol.name)

    jacket.data.materials.append(mat_dark)
    for poly in jacket.data.polygons:
        if poly.center.z > 0.40:
            poly.material_index = 1

    shade_flat(shirt)
    shade_flat(jacket)
    bpy.data.objects.remove(body, do_unlink=True)
    return shirt, jacket


def build_neck(mat_skin):
    rings = [
        ellipse_ring(0.43, 0.070, 0.062, cy=0.004, n=12),
        ellipse_ring(0.48, 0.058, 0.054, cy=0.008, n=12),
        ellipse_ring(0.53, 0.052, 0.050, cy=0.012, n=12),
    ]
    neck = loft("Neck", rings, cap_bottom=False, cap_top=False)
    assign_mat(neck, mat_skin)
    shade_flat(neck)
    return neck


# --------------------------------------------------------------------------- #
# scene / export / preview
# --------------------------------------------------------------------------- #
def parent_all(objs):
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    root = bpy.context.active_object
    root.name = "Paul"
    for o in objs:
        o.parent = root
    return root


def setup_render():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 600
    scene.render.resolution_y = 800

    world = bpy.data.worlds.new("W")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.55, 0.57, 0.60, 1)
    bg.inputs[1].default_value = 0.9
    scene.world = world

    bpy.ops.object.light_add(type="AREA", location=(1.4, 1.8, 1.8))
    key = bpy.context.active_object
    key.data.energy = 320
    key.data.size = 2.0
    key.rotation_euler = (math.radians(50), 0, math.radians(145))

    bpy.ops.object.light_add(type="AREA", location=(-1.8, 1.2, 1.0))
    fill = bpy.context.active_object
    fill.data.energy = 130
    fill.data.size = 2.5
    fill.rotation_euler = (math.radians(70), 0, math.radians(-120))

    bpy.ops.object.light_add(type="AREA", location=(0, -1.8, 1.6))
    rim = bpy.context.active_object
    rim.data.energy = 200
    rim.data.size = 2.0
    rim.rotation_euler = (math.radians(110), 0, 0)

    bpy.ops.object.camera_add(location=(0, 2.2, 0.5))
    cam = bpy.context.active_object
    cam.data.lens = 80
    scene.camera = cam
    return cam


def look_at(cam, target):
    d = Vector(target) - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()


def render_views(cam):
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    body = (0.0, 0.0, 0.38)
    face = (0.0, 0.0, HEAD_Z + 0.01)
    views = {
        "front": ((0.0, 2.2, 0.5), body, 80),
        "three_quarter": ((1.55, 1.55, 0.58), body, 80),
        "side": ((2.2, 0.0, 0.5), body, 80),
        "face": ((0.0, 0.70, HEAD_Z + 0.03), face, 90),
    }
    for name, (loc, target, lens) in views.items():
        cam.location = loc
        cam.data.lens = lens
        look_at(cam, target)
        bpy.context.scene.render.filepath = os.path.join(PREVIEW_DIR, f"{name}.png")
        bpy.ops.render.render(write_still=True)

    for n in ("Hair", "Beard"):
        o = bpy.data.objects.get(n)
        if o:
            o.hide_render = True
    cam.location, target, lens = views["face"]
    cam.data.lens = lens
    look_at(cam, target)
    bpy.context.scene.render.filepath = os.path.join(PREVIEW_DIR, "face_bare.png")
    bpy.ops.render.render(write_still=True)
    for n in ("Hair", "Beard"):
        o = bpy.data.objects.get(n)
        if o:
            o.hide_render = False


def export(objs):
    os.makedirs(OUT_DIR, exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.export_scene.gltf(
        filepath=os.path.join(OUT_DIR, "paul.glb"),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
    )
    bpy.context.preferences.filepaths.save_version = 0
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "paul.blend"))


def verify_glb():
    path = os.path.join(OUT_DIR, "paul.glb")
    reset_scene()
    bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    tris = 0
    for o in meshes:
        o.data.calc_loop_triangles()
        tris += len(o.data.loop_triangles)
    print(
        f"VERIFY: {len(meshes)} meshes, {tris} triangles, "
        f"{len(bpy.data.materials)} materials, "
        f"{os.path.getsize(path) / 1024:.0f} KB"
    )
    cam = setup_render()
    cam.location = (1.55, 1.55, 0.58)
    cam.data.lens = 80
    look_at(cam, (0.0, 0.0, 0.38))
    bpy.context.scene.render.filepath = os.path.join(PREVIEW_DIR, "glb_check.png")
    bpy.ops.render.render(write_still=True)


def main():
    reset_scene()

    m_skin = make_mat("Skin", "#d9a884", roughness=0.75)
    m_hair = make_mat("Hair", "#2a221d", roughness=0.85)
    m_shirt = make_mat("Shirt", "#f4f2ec", roughness=0.85)
    m_light = make_mat("JacketLight", "#b7b0a2", roughness=0.8)
    m_dark = make_mat("JacketDark", "#2f3135", roughness=0.8)
    m_frame = make_mat("GlassesFrame", "#17161a", roughness=0.35)
    m_white = make_mat("EyeWhite", "#f2f2f0", roughness=0.3)
    m_iris = make_mat("Iris", "#3a2a20", roughness=0.25)

    head = build_head(m_skin)
    ears = build_ears(m_skin)
    nose = build_nose(m_skin)
    hair = build_hair(head, m_hair)
    beard = build_beard(head, m_hair)
    eyes = build_eyes(m_white, m_iris)
    brows = build_brows(m_hair)
    glasses = build_glasses(m_frame)

    head_parts = [head, *ears, nose, hair, beard, *eyes, *brows, *glasses]
    for o in head_parts:
        o.location.z += HEAD_Z

    neck = build_neck(m_skin)
    body = build_body_volume()
    shirt, jacket = build_clothing(body, m_shirt, m_light, m_dark)

    all_objs = [*head_parts, neck, shirt, jacket]
    root = parent_all(all_objs)

    export([*all_objs, root])

    cam = setup_render()
    render_views(cam)
    verify_glb()
    print("DONE: character built, exported and previewed")


if __name__ == "__main__":
    main()
