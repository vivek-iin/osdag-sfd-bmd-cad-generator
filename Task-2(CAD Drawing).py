from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.gp import gp_Vec, gp_Trsf, gp_Pnt, gp_Ax2, gp_Dir
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Display.SimpleGui import init_display

# Function to create an I-Section
def create_I_section(length=3000):
    # Create top flange and position it correctly
    flange_top = BRepPrimAPI_MakeBox(300, 10, length).Shape()
    
    # Create bottom flange and position it correctly
    trsf_bottom = gp_Trsf()
    trsf_bottom.SetTranslation(gp_Vec(0, 200, 0))  # Position at the bottom with 190mm gap
    flange_bottom = BRepBuilderAPI_Transform(
        BRepPrimAPI_MakeBox(300, 10, length).Shape(),
        trsf_bottom
    ).Shape()
    
    # Create web - centered between flanges
    trsf_web = gp_Trsf()
    trsf_web.SetTranslation(gp_Vec(145, 10, 0))  # Center web horizontally
    web = BRepBuilderAPI_Transform(
        BRepPrimAPI_MakeBox(10, 190, length).Shape(),
        trsf_web
    ).Shape()
    
    # Fuse all components together instead of just creating a compound
    fused = BRepAlgoAPI_Fuse(flange_top, web).Shape()
    fused = BRepAlgoAPI_Fuse(fused, flange_bottom).Shape()
    
    return fused

# Function to create a laced column
def create_laced_column():
    # Create the first I-section
    I1 = create_I_section()
    
    # Create the second I-section with translation
    trsf = gp_Trsf()
    trsf.SetTranslation(gp_Vec(450, 0, 0))  
    I2 = BRepBuilderAPI_Transform(I1, trsf).Shape()
    
    # Create top batten plate
    top_batten = BRepPrimAPI_MakeBox(750, 210, 10).Shape()
    
    # Create bottom batten plate and position at the bottom
    trsf2 = gp_Trsf()
    trsf2.SetTranslation(gp_Vec(0, 0, 2990))  # Position just below the top
    bottom_batten = BRepBuilderAPI_Transform(top_batten, trsf2).Shape()
    
    # Create diagonal lacing members with proper orientation
    # First diagonal
    trsf_lace1 = gp_Trsf()
    trsf_lace1.SetTranslation(gp_Vec(150, 100, 500))
    lace1 = BRepBuilderAPI_Transform(
        BRepPrimAPI_MakeBox(450, 8, 10).Shape(),
        trsf_lace1
    ).Shape()
    
    # Second diagonal - positioned differently
    trsf_lace2 = gp_Trsf()
    trsf_lace2.SetTranslation(gp_Vec(150, 100, 1500))
    lace2 = BRepBuilderAPI_Transform(
        BRepPrimAPI_MakeBox(450, 8, 10).Shape(),
        trsf_lace2
    ).Shape()
    
    # Third diagonal - positioned differently
    trsf_lace3 = gp_Trsf()
    trsf_lace3.SetTranslation(gp_Vec(150, 100, 2500))
    lace3 = BRepBuilderAPI_Transform(
        BRepPrimAPI_MakeBox(450, 8, 10).Shape(),
        trsf_lace3
    ).Shape()
    
    # Build the compound
    builder = BRep_Builder()
    column = TopoDS_Compound()
    builder.MakeCompound(column)
    
    # Add all components to the compound
    for shape in [I1, I2, top_batten, bottom_batten, lace1, lace2, lace3]:
        builder.Add(column, shape)
    
    return column

# Generate Laced Column Model
laced_column = create_laced_column()

# Initialize display
display, start_display, add_menu, add_function_to_menu = init_display()

# Display the model
display.DisplayShape(laced_column, update=True)
display.FitAll()


# def export_to_step(shape, filename="laced_column_model.step"):
#     step_writer = STEPControl_Writer()
#     step_writer.Transfer(shape, STEPControl_AsIs)
#     status = step_writer.Write(filename)
#     if status == IFSelect_RetDone:
#         print(f"Model successfully saved to {filename}")
#     else:
#         print("Failed to save the model.")

# # Save the model
# export_to_step(laced_column)

start_display()

