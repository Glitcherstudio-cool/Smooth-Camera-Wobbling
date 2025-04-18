bl_info = {
    "name": "Smooth Camera Wobble",
    "blender": (2, 80, 0),
    "category": "3D View",
    "author": "Your Name",
    "description": "Applies a smooth camera wobble effect.",
    "version": (1, 0, 0),
}

import bpy
import math


class SmoothCameraWobbleOperator(bpy.types.Operator):
    """Applies a smooth camera wobble effect"""
    bl_idname = "animation.smooth_camera_wobble"
    bl_label = "Apply Smooth Camera Wobble"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        camera = scene.camera

        if not camera:
            self.report({'ERROR'}, "No active camera found in the scene.")
            return {'CANCELLED'}

        for frame in range(scene.frame_range):
            bpy.context.scene.frame_set(frame)

            strength = scene.wobble_strength
            speed = scene.wobble_speed

            x_wobble = strength * math.sin(speed * frame * 0.1)
            y_wobble = strength * math.cos(speed * frame * 0.1)
            z_wobble = strength * math.sin(speed * frame * 0.1)

            camera.location.x += x_wobble
            camera.location.y += y_wobble
            camera.location.z += z_wobble

            camera.rotation_euler.x += strength * math.sin(speed * frame * 0.1)
            camera.rotation_euler.y += strength * math.cos(speed * frame * 0.1)
            camera.rotation_euler.z += strength * math.sin(speed * frame * 0.1)

            camera.keyframe_insert(data_path="location", index=-1)
            camera.keyframe_insert(data_path="rotation_euler", index=-1)

            for fcurve in camera.animation_data.action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'SINE'

        self.report({'INFO'}, "Smooth camera wobble applied.")
        return {'FINISHED'}


class SmoothCameraWobblePanel(bpy.types.Panel):
    """Panel in the Sidebar (right 'N' panel) under Camera Shake tab"""
    bl_label = "Smooth Camera Wobble"
    bl_idname = "VIEW3D_PT_smooth_camera_wobble"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'  # <--- This puts it in the right-side panel!
    bl_category = 'Camera Shake'  # This becomes the tab name

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "wobble_strength")
        layout.prop(scene, "wobble_speed")
        layout.prop(scene, "frame_range")
        layout.operator("animation.smooth_camera_wobble")


def register():
    bpy.utils.register_class(SmoothCameraWobbleOperator)
    bpy.utils.register_class(SmoothCameraWobblePanel)

    bpy.types.Scene.wobble_strength = bpy.props.FloatProperty(
        name="Wobble Strength",
        description="How strong the wobble effect is",
        default=0.09,
        min=0.0,
        max=1.0
    )
    bpy.types.Scene.wobble_speed = bpy.props.FloatProperty(
        name="Wobble Speed",
        description="How fast the wobble oscillates",
        default=1.0,
        min=0.1,
        max=10.0
    )
    bpy.types.Scene.frame_range = bpy.props.IntProperty(
        name="Frame Range",
        description="Number of frames to apply the wobble effect to",
        default=250,
        min=1,
        max=1000
    )


def unregister():
    bpy.utils.unregister_class(SmoothCameraWobbleOperator)
    bpy.utils.unregister_class(SmoothCameraWobblePanel)

    del bpy.types.Scene.wobble_strength
    del bpy.types.Scene.wobble_speed
    del bpy.types.Scene.frame_range


if __name__ == "__main__":
    register()
