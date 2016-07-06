# Usage:
# 1. Generate rigify.
# 2. Select generated armature.
# 3. Run script.
# Script generates 'FCP-' bones in armature layer[23].
# Simultaneously, other bones will be set as non deform bone.

# Don't make duplicated name bone (e.g. '.001') in metarig.
# Don't change specific bones' name. (upper_arm, forearm, hand, thigh, shin and foot)

# Warning! This script is under trial.

# Script copyright (C) Bunno pen O

import re
import bpy

def flip_bone(bone_name):
    bpy.ops.armature.select_all(action='DESELECT')
    bpy.ops.object.select_pattern(pattern=bone_name)
    roll = bpy.context.selected_bones[0].roll
    bpy.ops.transform.resize(value=(-1,-1,-1))
    bpy.context.selected_bones[0].roll = roll
    
# add bone constraints
def add_copy_location(bone, subtarget):
    anchor = bone.constraints.new(type='COPY_LOCATION')
    anchor.target = bpy.context.object;
    anchor.subtarget = subtarget
    
def add_copy_rotation(bone, subtarget, influence):
    twist = bone.constraints.new(type='COPY_ROTATION')
    twist.target = bpy.context.object;
    twist.subtarget = subtarget
    twist.influence = influence
    
def add_damped_track(bone, subtarget):
    track = bone.constraints.new(type='DAMPED_TRACK')
    track.target = bpy.context.object;
    track.subtarget = subtarget
    
def add_stretch_to(bone, subtarget):
    stretch = bone.constraints.new(type='STRETCH_TO')
    stretch.target = bpy.context.object;
    stretch.subtarget = subtarget
    stretch.volume = "NO_VOLUME"
    
def add_copy_transforms(bone, subtarget):
    copy = bone.constraints.new(type='COPY_TRANSFORMS')
    copy.target = bpy.context.object;
    copy.subtarget = subtarget;
    
def add_copy_rotation_invert(bone, subtarget, influence):
    twist = bone.constraints.new(type='COPY_ROTATION')
    twist.target = bpy.context.object;
    twist.subtarget = subtarget
    twist.influence = influence
    twist.target_space = "LOCAL"
    twist.owner_space = "LOCAL"
    twist.invert_x = True
    twist.invert_y = True

# __main__

re_org = re.compile('ORG-')
re_orgheel = re.compile('ORG-heel')
re_duplicated = re.compile('.001')
re_def = re.compile('DEF-')
re_02 = re.compile('.02')

amt = bpy.context.object.data
amt.layers[23] = True
amt.layers[29] = True
amt.layers[31] = True

bpy.ops.object.mode_set(mode='EDIT')

# deselect all
bpy.ops.armature.select_all(action='DESELECT')

for object in amt.edit_bones:
    object.use_deform = False

# duplicate
for object in amt.edit_bones:
    if re_org.match(object.name) and (not re_orgheel.match(object.name)):
        bpy.ops.object.select_pattern(pattern=object.name)
        
    # for twist bone
bpy.ops.object.select_pattern(pattern='DEF-upper_arm.01.L')
bpy.ops.object.select_pattern(pattern='DEF-forearm.02.L')
bpy.ops.object.select_pattern(pattern='DEF-upper_arm.01.R')
bpy.ops.object.select_pattern(pattern='DEF-forearm.02.R')
bpy.ops.object.select_pattern(pattern='DEF-thigh.01.L')
bpy.ops.object.select_pattern(pattern='DEF-shin.02.L')
bpy.ops.object.select_pattern(pattern='DEF-thigh.01.R')
bpy.ops.object.select_pattern(pattern='DEF-shin.02.R')

bpy.ops.armature.duplicate()

# change name, layer
for object in amt.edit_bones:
    if re_duplicated.search(object.name) and (re_org.match(object.name) or re_def.match(object.name)):
        object.layers[23] = True
        
        if re_org.match(object.name):
            object.layers[31] = False
            object.name = re_org.sub('FCP-', object.name)
            
        if re_def.match(object.name):
            object.layers[29] = False
            object.name = re_def.sub('FCP-twist_', object.name)
            
            if re_02.search(object.name):
                flip_bone(object.name) # flip .02 twist bones
            
        object.name = re_duplicated.sub('', object.name)
        
        object.use_deform = True
        
bpy.ops.object.mode_set(mode='OBJECT')

# delete disused constraints
bpy.ops.object.mode_set(mode='POSE')

amt = bpy.context.object.data

bpy.ops.pose.select_all(action='DESELECT')

amt.bones['FCP-thigh.L'].select = True
amt.bones['FCP-thigh.R'].select = True
amt.bones['FCP-shin.L'].select = True
amt.bones['FCP-shin.R'].select = True
amt.bones['FCP-foot.L'].select = True
amt.bones['FCP-foot.R'].select = True

amt.bones['FCP-upper_arm.L'].select = True
amt.bones['FCP-upper_arm.R'].select = True
amt.bones['FCP-forearm.L'].select = True
amt.bones['FCP-forearm.R'].select = True

amt.bones['FCP-twist_upper_arm.01.L'].select = True
amt.bones['FCP-twist_forearm.02.L'].select = True
amt.bones['FCP-twist_upper_arm.01.R'].select = True
amt.bones['FCP-twist_forearm.02.R'].select = True
amt.bones['FCP-twist_thigh.01.L'].select = True
amt.bones['FCP-twist_shin.02.L'].select = True
amt.bones['FCP-twist_thigh.01.R'].select = True
amt.bones['FCP-twist_shin.02.R'].select = True

for bone in bpy.context.selected_pose_bones:
    disused_constraints = [ c for c in bone.constraints ]

    for c in disused_constraints:
        bone.constraints.remove(c)

# add constraints
    
bpy.ops.pose.select_all(action='DESELECT') # uppder arm L
amt.bones['FCP-upper_arm.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_location(bone, "ORG-upper_arm.L")
    add_copy_rotation(bone, "DEF-upper_arm.02.L", 1.0)
    add_damped_track(bone, "elbow_hose.L")
    add_stretch_to(bone, "elbow_hose.L")
    
bpy.ops.pose.select_all(action='DESELECT')
amt.bones['FCP-twist_upper_arm.01.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_transforms(bone, "DEF-upper_arm.01.L")
    
bpy.ops.pose.select_all(action='DESELECT') # forearm L
amt.bones['FCP-forearm.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_rotation(bone, "DEF-forearm.01.L", 1.0)
    add_damped_track(bone, "DEF-hand.L")
    add_stretch_to(bone, "DEF-hand.L")
    
bpy.ops.pose.select_all(action='DESELECT')
amt.bones['FCP-twist_forearm.02.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_location(bone, "forearm_hose_end.L")
    add_copy_rotation_invert(bone, "DEF-forearm.02.L", 1.0)
    add_damped_track(bone, "forearm_hose.L")
    add_stretch_to(bone, "forearm_hose.L")
    
bpy.ops.pose.select_all(action='DESELECT') # hand L
amt.bones['FCP-hand.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_transforms(bone, "DEF-hand.L")
    
bpy.ops.pose.select_all(action='DESELECT') # thigh L
amt.bones['FCP-thigh.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_location(bone, "ORG-thigh.L")
    add_copy_rotation(bone, "DEF-thigh.02.L", 1.0)
    add_damped_track(bone, "knee_hose.L")
    add_stretch_to(bone, "knee_hose.L")
    
bpy.ops.pose.select_all(action='DESELECT')
amt.bones['FCP-twist_thigh.01.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_transforms(bone, "DEF-thigh.01.L")
    
bpy.ops.pose.select_all(action='DESELECT') # shin L
amt.bones['FCP-shin.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_rotation(bone, "DEF-shin.01.L", 1.0)
    add_damped_track(bone, "DEF-foot.L")
    add_stretch_to(bone, "DEF-foot.L")
    
bpy.ops.pose.select_all(action='DESELECT')
amt.bones['FCP-twist_shin.02.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_location(bone, "shin_hose_end.L")
    add_copy_rotation_invert(bone, "DEF-shin.02.L", 1.0)
    add_damped_track(bone, "shin_hose.L")
    add_stretch_to(bone, "shin_hose.L")
    
bpy.ops.pose.select_all(action='DESELECT') # foot L
amt.bones['FCP-foot.L'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_transforms(bone, "DEF-foot.L")

# mirror bones
    
bpy.ops.pose.select_all(action='DESELECT') # uppder arm R
amt.bones['FCP-upper_arm.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_location(bone, "ORG-upper_arm.R")
    add_copy_rotation(bone, "DEF-upper_arm.02.R", 1.0)
    add_damped_track(bone, "elbow_hose.R")
    add_stretch_to(bone, "elbow_hose.R")
    
bpy.ops.pose.select_all(action='DESELECT')
amt.bones['FCP-twist_upper_arm.01.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_transforms(bone, "DEF-upper_arm.01.R")
    
bpy.ops.pose.select_all(action='DESELECT') # forearm R
amt.bones['FCP-forearm.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_rotation(bone, "DEF-forearm.01.R", 1.0)
    add_damped_track(bone, "DEF-hand.R")
    add_stretch_to(bone, "DEF-hand.R")
    
bpy.ops.pose.select_all(action='DESELECT')
amt.bones['FCP-twist_forearm.02.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_location(bone, "forearm_hose_end.R")
    add_copy_rotation_invert(bone, "DEF-forearm.02.R", 1.0)
    add_damped_track(bone, "forearm_hose.R")
    add_stretch_to(bone, "forearm_hose.R")
    
bpy.ops.pose.select_all(action='DESELECT') # hand R
amt.bones['FCP-hand.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_transforms(bone, "DEF-hand.R")
    
bpy.ops.pose.select_all(action='DESELECT') # thigh R
amt.bones['FCP-thigh.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_location(bone, "ORG-thigh.R")
    add_copy_rotation(bone, "DEF-thigh.02.R", 1.0)
    add_damped_track(bone, "knee_hose.R")
    add_stretch_to(bone, "knee_hose.R")
    
bpy.ops.pose.select_all(action='DESELECT')
amt.bones['FCP-twist_thigh.01.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_transforms(bone, "DEF-thigh.01.R")
    
bpy.ops.pose.select_all(action='DESELECT') # shin R
amt.bones['FCP-shin.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_rotation(bone, "DEF-shin.01.R", 1.0)
    add_damped_track(bone, "DEF-foot.R")
    add_stretch_to(bone, "DEF-foot.R")
    
bpy.ops.pose.select_all(action='DESELECT')
amt.bones['FCP-twist_shin.02.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_location(bone, "shin_hose_end.R")
    add_copy_rotation_invert(bone, "DEF-shin.02.R", 1.0)
    add_damped_track(bone, "shin_hose.R")
    add_stretch_to(bone, "shin_hose.R")
    
bpy.ops.pose.select_all(action='DESELECT') # foot R
amt.bones['FCP-foot.R'].select = True

for bone in bpy.context.selected_pose_bones:
    add_copy_transforms(bone, "DEF-foot.R")
    
# mirror end