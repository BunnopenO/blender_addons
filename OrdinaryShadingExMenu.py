import bpy
	
bl_info = {
	"name": "Ordinary Shading Ex Menu",
	"author": "obusto",
	"version": (0,1),
	"blender": (2,93,4),
	"description": "Activate the menu which changes the shading mode",
	"location": "wm.call_menu, VIEW3D_MT_ordinary_shading_ex",
	"category": "3D View",
}

class OrdinaryShadingExMenu(bpy.types.Menu):
	bl_label = 'Shading'
	bl_idname = 'VIEW3D_MT_ordinary_shading_ex'

	def draw(self, context):
		layout = self.layout

		props = layout.operator("wm.context_set_enum", text="Solid", icon='SHADING_SOLID')
		props.data_path = "space_data.shading.type"
		props.value = "SOLID"

		props = layout.operator("wm.context_set_enum", text="Wireframe", icon='SHADING_WIRE')
		props.data_path = "space_data.shading.type"
		props.value = "WIREFRAME"

		props = layout.operator("wm.context_set_enum", text="Material Preview", icon='MATERIAL')
		props.data_path = "space_data.shading.type"
		props.value = "MATERIAL"

		props = layout.operator("wm.context_set_enum", text="Rendered", icon='SHADING_RENDERED')
		props.data_path = "space_data.shading.type"
		props.value = "RENDERED"

		layout.separator()

		props = layout.operator("wm.context_set_boolean", text="Toggle Overlay", icon='OVERLAY')
		props.data_path = "space_data.overlay.show_overlays"
		props.value = not bpy.context.space_data.overlay.show_overlays

		props = layout.operator("wm.context_set_boolean", text="Toggle X-Ray", icon='XRAY')
		props.data_path = "space_data.shading.show_xray"
		props.value = not bpy.context.space_data.shading.show_xray
		
classes = {
	OrdinaryShadingExMenu
}
	
def register():
	for cls in classes:
		bpy.utils.register_class(cls)
	
def unregister():
	for cls in classes:
		bpy.utils.unregister_class(cls)
	
if __name__ == "__main__":
	register()