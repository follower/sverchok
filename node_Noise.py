from node_s import *
from util import *

import operator
import mathutils.noise as noise
import inspect


# noise nodes
# from http://www.blender.org/documentation/blender_python_api_2_70_release/mathutils.noise.html

def avail_noise(self,context):
    n_t=[(t[0],t[0].title(),t[0].title(),'',t[1]) for t in inspect.getmembers(noise.types) if isinstance(t[1],int)]
    n_t.sort(key=operator.itemgetter(0),reverse=True)
    return n_t
    
class SvNoiseNode(Node, SverchCustomTreeNode):
    '''Basic Noise node'''
    bl_idname = 'SvNoiseNode'
    bl_label = 'Noise'
    bl_icon = 'OUTLINER_OB_EMPTY'
    
    def changeMode(self,context):
        if self.out_mode == 'SCALAR':
            if not 'Noise S' in self.outputs:
                self.outputs.remove(self.outputs[0])
                self.outputs.new('StringsSocket','Noise S','Noise S')
                return
        if self.out_mode == 'VECTOR':
            if not 'Noise V' in self.outputs:
                self.outputs.remove(self.outputs[0])
                self.outputs.new('VerticesSocket', 'Noise V', 'Noise V')
                return
        
    out_modes = [
            ('SCALAR','Scalar','Scalar output','',1),
            ('VECTOR','Vector','Vector output','',2)]
         
    out_mode = EnumProperty(
            items=out_modes,
            default='VECTOR',
            description='Output type',
            update=changeMode)
            
    
    noise_type = EnumProperty(  
        items=avail_noise,
        description="Noise type",
        update=updateNode)
    
    noise_dict = {}
    noise_f = {'SCALAR':noise.noise,'VECTOR':noise.noise_vector}
                
    def init(self, context):
        self.inputs.new('VerticesSocket', 'Vertices', 'Vertices')
        self.outputs.new('VerticesSocket', 'Noise V', 'Noise V')
                
    def draw_buttons(self, context, layout):
        layout.prop(self,'out_mode',expand=True)
        layout.prop(self,'noise_type',text="Type")
        
    def update(self):
    
        if not self.noise_dict:
            self.noise_dict = {t[0]:t[1] for t in  inspect.getmembers(noise.types) if isinstance(t[1],int)}
        
        if self.outputs and not self.outputs[0].links:
            return
            
        if 'Vertices' in self.inputs and self.inputs['Vertices'].links:
            
            verts = Vector_generate(SvGetSocketAnyType(self,self.inputs['Vertices']))
            out = []
            n_t = self.noise_dict[self.noise_type]
            n_f = self.noise_f[self.out_mode]
                
            for obj in verts: 
                out.append([n_f(v,n_t) for v in obj])
                
            if 'Noise V' in self.outputs and self.outputs['Noise V'].links:
                SvSetSocketAnyType(self, 'Noise V',Vector_degenerate(out))
     
            if 'Noise S' in self.outputs and self.outputs['Noise S'].links:
                SvSetSocketAnyType(self, 'Noise S',out)
            return
            
        SvSetSocketAnyType(self, self.outputs[0].name,[[]])

    def update_socket(self, context):
        self.update()

def register():
    bpy.utils.register_class(SvNoiseNode)   
    
def unregister():
    bpy.utils.unregister_class(SvNoiseNode)

if __name__ == "__main__":
    register()







