import bpy
	
bl_info = {
	"name": "Ordinary Mode Menu",
	"author": "obusto",
	"version": (0,1),
	"blender": (2,93,4),
	"description": "Activate the menu which sets the object interaction mode.",
	"location": "wm.call_menu, VIEW3D_MT_ordinary_mode_menu",
	"category": "3D View",
}

class MODE_OPT_hit_object(bpy.types.Operator):
	bl_idname = "mode.hit_object"
	bl_label = "Object Mode"
	bl_description = "Set the object interaction mode to Object"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='OBJECT')
		return {'FINISHED'}
	
class MODE_OPT_hit_edit(bpy.types.Operator):
	bl_idname = "mode.hit_edit"
	bl_label = "Edit Mode"
	bl_description = "Set the object interaction mode to Edit"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='EDIT')
		return {'FINISHED'}
	
class MODE_OPT_hit_pose(bpy.types.Operator):
	bl_idname = "mode.hit_pose"
	bl_label = "Pose Mode"
	bl_description = "Set the object interaction mode to Pose"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='POSE')
		return {'FINISHED'}
	
class MODE_OPT_hit_sculpt(bpy.types.Operator):
	bl_idname = "mode.hit_sculpt"
	bl_label = "Sculpt Mode"
	bl_description = "Set the object interaction mode to Sculpt"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='SCULPT')
		return {'FINISHED'}
	
class MODE_OPT_hit_vertex_paint(bpy.types.Operator):
	bl_idname = "mode.hit_vertex_paint"
	bl_label = "Vertex Paint"
	bl_description = "Set the object interaction mode to Vertex Paint"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='VERTEX_PAINT')
		return {'FINISHED'}
	
class MODE_OPT_hit_weight_paint(bpy.types.Operator):
	bl_idname = "mode.hit_weight_paint"
	bl_label = "Weight Paint"
	bl_description = "Set the object interaction mode to Weight Paint"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
		return {'FINISHED'}
	
class MODE_OPT_hit_texture_paint(bpy.types.Operator):
	bl_idname = "mode.hit_texture_paint"
	bl_label = "Texture Paint"
	bl_description = "Set the object interaction mode to Texture Paint"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='TEXTURE_PAINT')
		return {'FINISHED'}
	
class MODE_OPT_hit_edit_gpencil(bpy.types.Operator):
	bl_idname = "mode.hit_edit_gpencil"
	bl_label = "Edit Mode"
	bl_description = "Set the object interaction mode to Edit"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='EDIT_GPENCIL')
		return {'FINISHED'}
	
class MODE_OPT_hit_sculpt_gpencil(bpy.types.Operator):
	bl_idname = "mode.hit_sculpt_gpencil"
	bl_label = "Sculpt Mode"
	bl_description = "Set the object interaction mode to Sculpt"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='SCULPT_GPENCIL')
		return {'FINISHED'}
	
class MODE_OPT_hit_paint_gpencil(bpy.types.Operator):
	bl_idname = "mode.hit_paint_gpencil"
	bl_label = "Draw"
	bl_description = "Set the object interaction mode to Draw"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='PAINT_GPENCIL')
		return {'FINISHED'}
	
class MODE_OPT_hit_weight_gpencil(bpy.types.Operator):
	bl_idname = "mode.hit_weight_gpencil"
	bl_label = "Weight Paint"
	bl_description = "Set the object interaction mode to Weight Paint"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='WEIGHT_GPENCIL')
		return {'FINISHED'}
	
class MODE_OPT_hit_vertex_gpencil(bpy.types.Operator):
	bl_idname = "mode.hit_vertex_gpencil"
	bl_label = "Vertex Paint"
	bl_description = "Set the object interaction mode to Vertex Paint"
	
	def execute(self, context):
		bpy.ops.object.mode_set(mode='VERTEX_GPENCIL')
		return {'FINISHED'}

class OrdinaryModeMenu(bpy.types.Menu):
	bl_label = 'Mode'
	bl_idname = 'VIEW3D_MT_ordinary_mode_menu'

	def draw(self, context):
		layout = self.layout

		layout.operator(MODE_OPT_hit_object.bl_idname, icon='OBJECT_DATA')
		
		editable_types = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE']
		
		if bpy.context.view_layer.objects.active.type in editable_types:
			layout.operator(MODE_OPT_hit_edit.bl_idname, icon='EDITMODE_HLT')
		
		if bpy.context.view_layer.objects.active.type == 'MESH':
			layout.operator(MODE_OPT_hit_sculpt.bl_idname, icon='SCULPTMODE_HLT')
			layout.operator(MODE_OPT_hit_vertex_paint.bl_idname, icon='VPAINT_HLT')
			layout.operator(MODE_OPT_hit_weight_paint.bl_idname, icon='WPAINT_HLT')
			layout.operator(MODE_OPT_hit_texture_paint.bl_idname, icon='TPAINT_HLT')
		elif bpy.context.view_layer.objects.active.type == 'ARMATURE':
			layout.operator(MODE_OPT_hit_pose.bl_idname, icon='POSE_HLT')
		elif bpy.context.view_layer.objects.active.type == 'GPENCIL':
			layout.operator(MODE_OPT_hit_edit_gpencil.bl_idname, icon='EDITMODE_HLT')
			layout.operator(MODE_OPT_hit_sculpt_gpencil.bl_idname, icon='SCULPTMODE_HLT')
			layout.operator(MODE_OPT_hit_paint_gpencil.bl_idname, icon='GREASEPENCIL')
			layout.operator(MODE_OPT_hit_weight_gpencil.bl_idname, icon='WPAINT_HLT')
			layout.operator(MODE_OPT_hit_vertex_gpencil.bl_idname, icon='VPAINT_HLT')
		
classes = {
	MODE_OPT_hit_object, MODE_OPT_hit_edit, MODE_OPT_hit_sculpt, MODE_OPT_hit_pose,
	MODE_OPT_hit_vertex_paint, MODE_OPT_hit_weight_paint, MODE_OPT_hit_texture_paint,
	MODE_OPT_hit_edit_gpencil, MODE_OPT_hit_sculpt_gpencil, MODE_OPT_hit_paint_gpencil,
	MODE_OPT_hit_weight_gpencil, MODE_OPT_hit_vertex_gpencil,
	OrdinaryModeMenu
}
	
def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)
	
if __name__ == "__main__":
	register()