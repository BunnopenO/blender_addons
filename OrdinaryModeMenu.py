import bpy
	
bl_info = {
	"name": "Ordinary Mode Menu",
	"author": "obusto",
	"version": (0,1,2),
	"blender": (2,93,4),
	"description": "Activate the menu which sets the object interaction mode.",
	"location": "wm.call_menu, VIEW3D_MT_ordinary_mode_menu",
	"category": "3D View",
}

class OrdinaryModeMenu(bpy.types.Menu):
	bl_label = 'Mode'
	bl_idname = 'VIEW3D_MT_ordinary_mode_menu'

	def draw(self, context):
		layout = self.layout

		layout.operator("object.mode_set", text="Object Mode", icon='OBJECT_DATA').mode = 'OBJECT'
		
		editable_types = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE']
		
		if bpy.context.view_layer.objects.active.type in editable_types:
			layout.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT').mode = 'EDIT'
		
		if bpy.context.view_layer.objects.active.type == 'MESH':
			layout.operator("object.mode_set", text="Sculpt Mode", icon='SCULPTMODE_HLT').mode = 'SCULPT'
			layout.operator("object.mode_set", text="Vertex Paint", icon='VPAINT_HLT').mode = 'VERTEX_PAINT'
			layout.operator("object.mode_set", text="Weight Paint", icon='WPAINT_HLT').mode = 'WEIGHT_PAINT'
			layout.operator("object.mode_set", text="Texture Paint", icon='TPAINT_HLT').mode = 'TEXTURE_PAINT'
		elif bpy.context.view_layer.objects.active.type == 'ARMATURE':
			layout.operator("object.mode_set", text="Pose Mode", icon='POSE_HLT').mode = 'POSE'
		elif bpy.context.view_layer.objects.active.type == 'GPENCIL':
			layout.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT').mode = 'EDIT_GPENCIL'
			layout.operator("object.mode_set", text="Sculpt Mode", icon='SCULPTMODE_HLT').mode = 'SCULPT_GPENCIL'
			layout.operator("object.mode_set", text="Draw", icon='GREASEPENCIL').mode = 'PAINT_GPENCIL'
			layout.operator("object.mode_set", text="Weight Paint", icon='WPAINT_HLT').mode = 'WEIGHT_GPENCIL'
			layout.operator("object.mode_set", text="Vertex Paint", icon='VPAINT_HLT').mode = 'VERTEX_GPENCIL'
		
classes = {
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