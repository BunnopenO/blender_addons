import bpy
import bmesh
import mathutils
import math
	
bl_info = {
	"name": "Snap and Align Menu",
	"author": "obusto",
	"version": (0,1),
	"blender": (2,93,4),
	"description": "Replacing for the snap menu",
	"location": "wm.call_menu, VIEW3D_MT_snap_align_menu",
	"category": "3D View",
}

class OBJECT_OPT_align_selection_to_cursor(bpy.types.Operator):
	bl_idname = "object.align_selection_to_cursor"
	bl_label = "Selection to Cursor Orientation"
	bl_description = "Align Selected Objects Orientation to Cursor"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		if len(bpy.context.selected_objects) > 0 and bpy.context.mode == "OBJECT" :
			for selection in bpy.context.selected_objects:
				selection.rotation_euler = bpy.context.scene.cursor.rotation_euler

		return {'FINISHED'}

def rotate_cursor(rotation_euler):
	mode = bpy.context.scene.cursor.rotation_mode
	bpy.ops.wm.context_set_enum(data_path="scene.cursor.rotation_mode", value="XYZ")

	bpy.context.scene.cursor.rotation_euler = rotation_euler

	bpy.ops.wm.context_set_enum(data_path="scene.cursor.rotation_mode", value=mode)

class VIEW3D_OPT_align_cursor_to_world(bpy.types.Operator):
	bl_idname = "view3d.align_cursor_to_world"
	bl_label = "Cursor to World Orientation"
	bl_description = "Align 3D Cursor Orientation to World"
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = bpy.context.view_layer.objects.active

		if obj:
			rotate_cursor(mathutils.Euler((0.0,0.0,0.0), 'XYZ'))

		return {'FINISHED'}

class VIEW3D_OPT_align_cursor_to_local(bpy.types.Operator):
	bl_idname = "view3d.align_cursor_to_local"
	bl_label = "Cursor to Local Orientation"
	bl_description = "Align 3D Cursor Orientation to Local."
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = bpy.context.view_layer.objects.active

		if obj:
			rotate_cursor(obj.rotation_euler)

		return {'FINISHED'}

class VIEW3D_OPT_align_cursor_to_normal(bpy.types.Operator):
	bl_idname = "view3d.align_cursor_to_normal"
	bl_label = "Cursor to Face Normal"
	bl_description = "Align 3D Cursor Orientation to Face Normal."
	bl_options = {'REGISTER', 'UNDO'}
	
	def execute(self, context):
		obj = bpy.context.edit_object

		if obj:
			bm = bmesh.from_edit_mesh(obj.data)
			selected_faces = [face for face in bm.faces if face.select]
			if len(selected_faces) > 0:
				normal = mathutils.Vector((0.0, 0.0, 0.0))
				for face in selected_faces:
					normal += face.normal

				tangent = mathutils.Vector((0.0, 0.0, 0.0))
				for face in selected_faces:
					tangent += face.calc_tangent_edge_pair()

				print(obj.rotation_euler)

				normal.rotate(obj.rotation_euler)
				tangent.rotate(obj.rotation_euler)

				cross = normal.cross(tangent)
				tangent = -normal.cross(cross)

				normal.normalize()
				tangent.normalize()
				cross.normalize()

				#print("normal : " + str(normal))
				#print("tangent : " + str(tangent))
				#print("cross : " + str(cross))

				mat = mathutils.Matrix().to_3x3()

				mat[0][0] = tangent.x
				mat[0][1] = cross.x
				mat[0][2] = normal.x

				mat[1][0] = tangent.y
				mat[1][1] = cross.y
				mat[1][2] = normal.y

				mat[2][0] = tangent.z
				mat[2][1] = cross.z
				mat[2][2] = normal.z

				euler = mathutils.Euler((0.0, 0.0, math.radians(90.0)), 'XYZ')
				euler.rotate(mat.to_euler())
				
				#print(math.degrees(euler.x))
				#print(math.degrees(euler.y))
				#print(math.degrees(euler.z))

				rotate_cursor(euler)

		return {'FINISHED'}

class SnapAlignMenu(bpy.types.Menu):
	bl_label = 'Snap & Align'
	bl_idname = 'VIEW3D_MT_snap_align_menu'

	def draw(self, context):
		layout = self.layout

		layout.operator("view3d.snap_selected_to_cursor", text="Selection to Cursor").use_offset = False
		layout.operator("view3d.snap_selected_to_cursor", text="Selection to Cursor (Keep Offset)").use_offset = True

		layout.separator()

		row = layout.row(align=True)
		row.operator(OBJECT_OPT_align_selection_to_cursor.bl_idname)

		if bpy.context.mode != "OBJECT":
			row.enabled = False

		layout.separator()

		layout.operator("view3d.snap_cursor_to_selected", text="Cursor to Selected")

		props = layout.operator("wm.context_set_value", text="Cursor to World Origin")
		props.data_path = "scene.cursor.location"
		props.value = "(0.0,0.0,0.0)"

		layout.separator()
		
		#props = layout.operator("wm.context_set_value", text="Cursor to World Orientation", icon='ORIENTATION_GLOBAL')
		#props.data_path = "scene.cursor.rotation_euler"
		#props.value = "(0.0,0.0,0.0)"

		layout.operator(VIEW3D_OPT_align_cursor_to_world.bl_idname, icon='ORIENTATION_GLOBAL')

		layout.operator(VIEW3D_OPT_align_cursor_to_local.bl_idname, icon='ORIENTATION_LOCAL')

		row = layout.row(align=True)
		row.operator(VIEW3D_OPT_align_cursor_to_normal.bl_idname, icon='NORMALS_FACE')

		if bpy.context.mode != "EDIT_MESH" :
			row.enabled = False
		
classes = {
	OBJECT_OPT_align_selection_to_cursor,
	VIEW3D_OPT_align_cursor_to_world, VIEW3D_OPT_align_cursor_to_local, VIEW3D_OPT_align_cursor_to_normal,
	SnapAlignMenu
}
	
def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)
	
if __name__ == "__main__":
	register()