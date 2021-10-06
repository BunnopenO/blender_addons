bl_info = {
    "name": "Create Catenary",
    "author": "obusto",
    "version": (0,2),
    "blender": (2,93,4),
    "location": "Mesh>Specials>CreateCatenary",
    "category": "Mesh",
}

import bpy
from mathutils import Vector
from math import sinh, cosh, sqrt

def f_a(a, d, l, h):
    return 2 * a**2 * (cosh(d / a) - 1) - ((l - h) * (l + h))

def diff_f_a(a, d, l, h):
    return 4 * a * (cosh(d / a) - 1) - 2 * d * sinh(d / a)

def f_d(a, d, d_0, h):
    return a * (cosh((d - d_0) / a) - cosh(d_0 / a)) + h

def diff_f_d(a, d, d_0):
    return -sinh((d - d_0) / a) - sinh(d_0 / a)

def create_catenary(obj, cuts, slack, invert):
    bpy.context.object.update_from_editmode()
    
    edges = [e for e in obj.data.edges if e.select]
    
    if len(edges) == 1:
        bpy.ops.mesh.subdivide(number_cuts=cuts, smoothness=0)
        bpy.context.object.update_from_editmode()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        verts = [v for v in obj.data.vertices if v.select]
        
        #for v_index in edges[0].vertices:
        #    print(obj.data.vertices[v_index].co)
            
        #print(" -- ")
        
        # sort list
        verts.append(verts.pop(
            1 if (verts[2].co - verts[0].co).length < (verts[2].co - verts[1].co).length else 0))
        
        #for i in range(0, len(verts)):
        #    print(obj.data.vertices[verts[i].index].co)
            
        if(verts[0].co.z > verts[-1].co.z):
            verts.reverse()
            
        # geometry
        v_span = verts[-1].co - verts[0].co
        h_0 = verts[0].co.z
        h_1 = verts[-1].co.z
        chord = v_span.length
        v_span.z = 0
        
        if(v_span.length == 0):
            return
        
        # scale
        scale = 20 / v_span.length
        
        d = v_span.length * scale
        h = (h_1 - h_0) * scale
        
        slack_max = max(0.44 * (v_span.length / chord) - 0.01, 0)
        l = (chord + (8 * (chord * min(slack, slack_max))**2) / (3 * chord)) * scale
        
        #print("slack:" + str(slack) + " limited:" + str(slack_max))
        
        #print("h:" + str(h) + " d:" + str(d))
        #print("l:" + str(l) + " chord:" + str(chord))
        
        a = 10
        
        for i in range(0, 100):
            a_n = a - f_a(a, d, l, h) / diff_f_a(a, d, l, h)
            a = a_n
            
        d_m = d / 2
        
        for i in range(0, 100):
            d_m_n = d_m - f_d(a, d, d_m, h) / diff_f_d(a, d, d_m)
            d_m = d_m_n
            
        #print("a:" + str(a) + " d_m:" + str(d_m))
            
        for i in range(0, len(verts)):
            d_i = d * i / (len(verts) - 1) - d_m
            h_i = a * (cosh(d_i / a) - cosh(d_m / a)) / scale
            
            if not invert:
                verts[len(verts) - 1 - i].co.z = h_1 + h_i
            else:
                verts[i].co.z = h_0 - h_i
            
        bpy.ops.object.mode_set(mode='EDIT')

class CatenaryOperator(bpy.types.Operator):
    bl_idname = "mesh.catenary_operator"
    bl_label="Create Catenary"
    bl_options = {'REGISTER', 'UNDO'}
    
    cuts : bpy.props.IntProperty(name="Number of Cuts", default=7, min=1, max=100)
    slack : bpy.props.FloatProperty(name="Slack", default=0.03, min=0, max=1)
    invert : bpy.props.BoolProperty(name="Invert", default=False)
    
    def execute(self, context):
        obj = bpy.context.view_layer.objects.active

        if bpy.context.mode == "EDIT_MESH" :
            create_catenary(obj, self.cuts, self.slack, self.invert)
            
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(CatenaryOperator.bl_idname)
    
def register():
    bpy.utils.register_class(CatenaryOperator)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)

def unregister():
    bpy.utils.unregister_class(CatenaryOperator)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    
if __name__ == "__main__":
    register()