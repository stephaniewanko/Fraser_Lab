#Brandi

cd /Users/stephaniewankowicz/Dropbox/Fraser_Rotation/qfit_refine_stru/

viewport 900,500
bg_color white
set mesh_width, 0.4
set stick_radius, 0.15

load 1gyx_qFit.pdb
load 1gyx_qFit.mtz, 2FOFC
map_double 2FOFC
load 1gyx_qFit.mtz, FOFC
map_double FOFC

remove hydro
show sticks, resi 150 and chain A
color green, alt A
color yellow, alt B
color orange, alt C
color deepteal, alt D
color raspberry, alt E

util.cnc

#isomesh 2fofc_15, 2FOFC, 1.5, resi 150 and chain A, carve=1.5
#color marine, 2fofc_15
#show mesh, 2fofc_15

#isomesh 2fofc_03, 2FOFC, 0.3, resi 150 and chain A, carve=1.5
#color lightblue, 2fofc_03
#show mesh, 2fofc_03

#isomesh fofc_pos, FOFC, 3.0, resi 150 and chain A, carve=1.5
#color forest, fofc_pos

#isomesh fofc_neg, FOFC, -3.0, resi 150 and chain A, carve=1.5
#color red, fofc_neg
#show mesh, fofc_neg

hide lines
hide nonbonded
orient resi 150

ray 2400
png test_multi.png
