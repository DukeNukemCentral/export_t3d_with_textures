#==========================================================================
#
# Duke Nukem maps to Unreal DNF T3D Plug-in for blender
# by Snake Plissken and ZNukem
#
#==========================================================================
# This code is licensed under the MIT License.
# You can get a copy or revision of this license at
# https://opensource.org/licenses/MIT
# ==========================================================================



import bpy
from bpy.props import FloatProperty
from mathutils import Vector

bl_info = {
    "name": "DN Zero Hour To T3D Plugin",
    "blender": (2, 82, 0),  # Adjust this version to match your Blender version
    "category": "Object",
    "author": "Snake Plissken and ZNukem",
    "description": "Converts Duke Nukem Zero Hour asset or DN3D build imported maps to Unreal T3D format for DNF01/DNF2011.",
    "version": (1, 1, 1),
    "location": "View3D > Tool Shelf > T3D",
    "warning": "Still in beta. If you wish the help, contact Snake Plissken#5940 therealsnakeplissken on discord.",
    "support": "https://discord.com/channels/778619521527054357/1063837235675406366/1097867608906280992"
}


# Function to flip X-axis
def flip_x(vector):
    return Vector((-vector.x, vector.y, vector.z))

class ExportT3DWithTextures(bpy.types.Operator):
    bl_idname = "object.export_t3d_with_textures"
    bl_label = "Export T3D with Textures"
    bl_description = "Export T3D data with texture and material names and copy it to the clipboard"

    def execute(self, context):
        def format_vector(vector):
            return f'{vector.x:+013.6f},{vector.y:+013.6f},{vector.z:+013.6f}'

        obj = bpy.context.object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No active mesh object is selected")
            return {'CANCELLED'}

        scale = context.scene.t3d_export_settings.scale

        # Ensure we are in object mode.
        bpy.ops.object.mode_set(mode='OBJECT')

        # Triangulate the mesh
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris()
        bpy.ops.object.mode_set(mode='OBJECT')

        # Export geometry data
        t3d_data = "Begin Actor Class=Brush Name=LevelGeometry\n"
        t3d_data += "    CsgOper=CSG_Add\n"
        t3d_data += f"    Location=(X={obj.location.x * scale:.6f}, Y={obj.location.z * scale:.6f}, Z={-obj.location.y * scale:.6f})\n"
        t3d_data += "    Begin Brush Name=Model\n"
        t3d_data += "       Begin PolyList\n"

        uvs = obj.data.uv_layers.active.data if obj.data.uv_layers.active else []

        for face in obj.data.polygons:
            material = obj.material_slots[face.material_index].material if face.material_index >= 0 else None
            material_name = material.name if material else "None"

            vertices = [flip_x(obj.matrix_world @ obj.data.vertices[i].co) for i in face.vertices]
            origin = flip_x(obj.matrix_world @ face.center)
            normal = flip_x(obj.matrix_world.to_quaternion() @ face.normal)
            texture_u = flip_x(obj.matrix_world.to_quaternion() @ face.normal.cross(vertices[1] - vertices[0]).normalized())
            texture_v = normal.cross(texture_u)

            t3d_data += f"          Begin Polygon Texture={material_name} Flags=4194305\n"
            t3d_data += f"             Origin   {format_vector(origin)}\n"
            t3d_data += f"             Normal   {format_vector(normal)}\n"
            t3d_data += f"             TextureU {format_vector(texture_u)}\n"
            t3d_data += f"             TextureV {format_vector(texture_v)}\n"

            for vertex_index, vertex in enumerate(vertices):
                uv = uvs[face.loop_indices[vertex_index]].uv if uvs else (0.0, 0.0)
                t3d_data += f"             Vertex   {format_vector(vertex * scale)}   UV {uv[0] * scale:.6f},{uv[1] * scale:.6f}\n"

            t3d_data += "          End Polygon\n"

        t3d_data += "       End PolyList\n"
        t3d_data += "    End Brush\n"
        t3d_data += "End Actor"

        bpy.context.window_manager.clipboard = t3d_data

        self.report({'INFO'}, "T3D data with texture and material names copied to clipboard")
        print("T3D with materials and textures has been copied to the clipboard.")
        return {'FINISHED'}

class UpdateMaterialNames(bpy.types.Operator):
    bl_idname = "object.update_material_names"
    bl_label = "Update Material Names"
    bl_description = "Update material names based on the specified format"

    def execute(self, context):
        for material in bpy.data.materials:
            if material.name.startswith("picnum"):
                new_name = material.name.replace("picnum", "").split("_")[0]
                material.name = new_name
        return {'FINISHED'}

class UpdateDN3DObjectMaterialNames(bpy.types.Operator):
    bl_idname = "object.update_dn3d_object_material_names"
    bl_label = "Update DN3D object material names to XXXX_XXX format"

    def execute(self, context):
        for material in bpy.data.materials:
            if material.name.startswith("picnum"):
                parts = material.name.replace("picnum", "").split("_")
                if len(parts) > 1:
                    new_name = f"{parts[1].split('-')[0]}-{parts[1].split('-')[1]}"
                    material.name = new_name
        return {'FINISHED'}

class CopyTextureNames(bpy.types.Operator):
    bl_idname = "object.copy_texture_names"
    bl_label = "Copy Texture Names"
    bl_description = "Copy the names of all textures in use by materials on the selected object to the clipboard"

    def execute(self, context):
        obj = bpy.context.object
        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No active mesh object is selected")
            return {'CANCELLED'}
            
        texture_names = set()
        
        for mat_slot in obj.material_slots:
            material = mat_slot.material
            if material and material.node_tree:
                for node in material.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        texture_names.add(node.image.name)
        
        if texture_names:
            bpy.context.window_manager.clipboard = "\n".join(texture_names)
            self.report({'INFO'}, "Texture names copied to clipboard")
        else:
            self.report({'INFO'}, "No textures found on the selected object")
            
        return {'FINISHED'}

class T3DExportSettings(bpy.types.PropertyGroup):
    scale: FloatProperty(
        name="Scale",
        description="Scale for T3D export",
        default=10.0,
        min=0.01,
        max=100.0
    )

class T3DExporterPanel(bpy.types.Panel):
    bl_label = "T3D Exporter"
    bl_idname = "OBJECT_PT_t3d_exporter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "T3D"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene.t3d_export_settings, "scale", text="Export Scale")
        layout.operator(ExportT3DWithTextures.bl_idname, text="Send as T3D to clipboard")
        layout.operator(UpdateMaterialNames.bl_idname, text="Update Material Names")
        layout.operator(UpdateDN3DObjectMaterialNames.bl_idname, text="Update DN3D object material names")
        layout.operator(CopyTextureNames.bl_idname, text="Copy Texture Names")

def menu_func(self, context):
    self.layout.operator(ExportT3DWithTextures.bl_idname)
    self.layout.operator(UpdateMaterialNames.bl_idname)
    self.layout.operator(UpdateDN3DObjectMaterialNames.bl_idname)
    self.layout.operator(CopyTextureNames.bl_idname)

def register():
    bpy.utils.register_class(ExportT3DWithTextures)
    bpy.utils.register_class(UpdateMaterialNames)
    bpy.utils.register_class(UpdateDN3DObjectMaterialNames)
    bpy.utils.register_class(CopyTextureNames)
    bpy.utils.register_class(T3DExportSettings)
    bpy.utils.register_class(T3DExporterPanel)
    bpy.types.Scene.t3d_export_settings = bpy.props.PointerProperty(type=T3DExportSettings)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(ExportT3DWithTextures)
    bpy.utils.unregister_class(UpdateMaterialNames)
    bpy.utils.unregister_class(UpdateDN3DObjectMaterialNames)
    bpy.utils.unregister_class(CopyTextureNames)
    bpy.utils.unregister_class(T3DExportSettings)
    bpy.utils.unregister_class(T3DExporterPanel)
    del bpy.types.Scene.t3d_export_settings
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
