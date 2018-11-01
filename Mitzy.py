from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Mitzy on Roids")
root.configure(bg="pink")
frames = []
properties = []

class Mitzy:
    """Mitzy creates a window that asks for title and property names and uses that to create a web part"""
    def __init__(self):
        frame = Frame(root)
        frame.pack(fill=None, expand=False)
        middle_frame = Frame(root)
        middle_frame.pack()
        app_title = Label(frame, text="------> Welcome to Mitzy's Web Part Creator! <------", bg="pink")
        app_title.pack(side=LEFT)
        wp_label = Label(middle_frame, text="Web Part Name: ", bg="pink")
        wp_label.pack(side=LEFT)
        wp_title_entry = Entry(middle_frame)
        wp_title_entry.pack(side=LEFT)

        location_selected = StringVar()
        location_selected.set("AFSI")
        wp_location_label = Label(middle_frame, text="Project Location: ", bg="pink")
        wp_location_label.pack(side=LEFT)
        AFSI_proj = Radiobutton(middle_frame, text="AFSI", value="AFSI", var=location_selected)
        Agency_proj = Radiobutton(middle_frame, text="AGENCY", value="Agency", var=location_selected)
        Amventure_proj = Radiobutton(middle_frame, text="AMVENTURE", value="Amventure", var=location_selected)
        AFSI_proj.pack(side=LEFT)
        Agency_proj.pack(side=LEFT)
        Amventure_proj.pack(side=LEFT)
        bottom_frame = Frame(root)
        bottom_frame.pack(side=BOTTOM)
        wp_add_prop = Button(bottom_frame, text="Add Property", command=self.add_property)
        wp_add_prop.pack(side=LEFT)
        create_web_part = Button(bottom_frame, text="Create Web Part!", command= lambda: self.end_program(wp_title_entry.get(), location_selected.get(), properties))
        create_web_part.pack(side=LEFT)

    @staticmethod
    def add_property():
        """Displays a text field to add a property"""
        global widgetNames
        global frameNames
        new_frame = Frame(root, borderwidth=2, relief="groove")
        frames.append(new_frame)
        new_frame.pack(side="top", fill="x")
        input_title_property = Label(new_frame, text="Property Name: ", bg="pink")
        input_title_property.pack(side="left")
        new_property = Entry(new_frame)
        new_property.pack(side="left")
        input_title_datatype = Label(new_frame, text="Datatype (string or int): ", bg="pink")
        input_title_datatype.pack(side=LEFT)
        data_type_selected = StringVar()
        data_type_string = Radiobutton(new_frame, text="STRING", value="string", var=data_type_selected)
        data_type_integer = Radiobutton(new_frame, text="INTEGER", value="int", var=data_type_selected)
        data_type_string.pack(side=LEFT)
        data_type_integer.pack(side=LEFT)
        properties.append((new_property, data_type_selected))


    @staticmethod
    def end_program(title, location, properties):
        """Uses the inserted values to create a user control codebehind"""
        if len(properties) == 0:
            messagebox.showinfo("Error", "You need to add a property before a web part can be created")
        else:
            create_web_part_template(title, location)
            create_web_part_code_behind(title, location, properties)
            create_web_part_design(title, location)
            messagebox.showinfo("POOF!", "The web part has been created!")



#  Creates The Actual Files
# ==========================
def create_web_part_template(title, location):
    code_behind_location = set_code_behind(location)

    f= open(title + ".ascx","w+")
    f.write("<%@ Control Language=\"C#\" AutoEventWireup=\"true\" Inherits=\"CMSWebParts_" + location + "_" + title + "\"  CodeBehind=\"" + code_behind_location + title + ".ascx.cs\" %>\n")
    f.write("<asp:PlaceHolder runat=\"server\" id=\"plcWrapper\">\n")
    f.write("   <!-- Paste your html here! -->\n")
    f.write("</asp:PlaceHolder>\n")
    f.close()


def create_web_part_code_behind(title, location, properties):
    f= open(title + ".ascx.cs","w+")
    f.write("using System;\n")
    f.write("using System.Data;\n")
    f.write("using System.Collections;\n")
    f.write("using System.Web;\n")
    f.write("using System.Web.UI;\n")
    f.write("using System.Web.UI.WebControls;\n")
    f.write("\n")
    f.write("using CMS.PortalEngine.Web.UI;\n")
    f.write("using CMS.Helpers;\n")
    f.write("\n")
    f.write("public partial class CMSWebParts_" + location + "_" + title + " : CMSAbstractWebPart\n")
    f.write("{\n")
    f.write("    #region \"Properties\"\n")
    f.write("\n")
    for property in properties:
        f.write("    protected " + property[1].get() + " m" + property[0].get() + ";\n")

    f.write("\n\n")

    for property in properties:
        f.write("    public " + property[1].get() +" " + property[0].get() + "\n")
        f.write("    {\n")
        f.write("       get\n")
        f.write("       {\n")
        if property[1].get() == "string":
            f.write("           return ValidationHelper.GetString(this.GetValue(\""+ property[0].get() +"\"), m" + property[0].get() + ");\n")
        elif property[1].get() == "int":
            f.write("           return ValidationHelper.GetInteger(this.GetValue(\""+ property[0].get() +"\"), m" + property[0].get() + ");\n")
        f.write("       }\n")
        f.write("       set\n")
        f.write("       {\n")
        f.write("           this.SetValue(\"" + property[0].get() + "\", value);\n")
        f.write("           m" + property[0].get() + " = value;\n")
        f.write("       }\n")
        f.write("    }\n")
        f.write("\n")

    f.write("\n")
    f.write("    #endregion\n")
    f.write("\n")
    f.write("    #region \"Methods\"\n")
    f.write("\n")
    f.write("    /// <summary>\n")
    f.write("    /// Content loaded event handler.\n")
    f.write("    /// </summary>\n")
    f.write("    public override void OnContentLoaded()\n")
    f.write("    {\n")
    f.write("        base.OnContentLoaded();\n")
    f.write("        SetupControl();\n")
    f.write("    }\n")
    f.write("\n")
    f.write("    /// <summary>\n")
    f.write("    /// Initializes the control properties.\n")
    f.write("    /// </summary>\n")
    f.write("    protected void SetupControl()\n")
    f.write("    {\n")
    f.write("        if (this.StopProcessing)\n")
    f.write("        {\n")
    f.write("            // Do not process\n")
    f.write("        }\n")
    f.write("        else\n")
    f.write("        {\n")
    f.write("            plcWrapper.DataBind();\n")
    f.write("        }\n")
    f.write("    }\n")
    f.write("\n")
    f.write("    /// <summary>\n")
    f.write("    /// Reloads the control data.\n")
    f.write("    /// </summary>\n")
    f.write("    public override void ReloadData()\n")
    f.write("    {\n")
    f.write("        base.ReloadData();\n")
    f.write("\n")
    f.write("        SetupControl();\n")
    f.write("    }\n")
    f.write("\n")
    f.write("    #endregion\n")
    f.write("}\n")
    f.close()


def create_web_part_design(title, location):
    f= open(title + ".ascx.designer.cs","w+")
    f.write("public partial class CMSWebParts_" + location + "_" + title + " {\n")
    f.write("   protected global::System.Web.UI.WebControls.PlaceHolder plcWrapper;\n")
    f.write("}")
    f.close()


def set_code_behind(location):
    code_behind_location = ""
    if location == "AFSI":
        code_behind_location = "~/CMSWebParts/AFSI/"
    elif location == "Agency":
        code_behind_location = "~/CMSWebParts/Agency/"
    elif location == "Amventure":
        code_behind_location = "~/CMSWebParts/Amventure/"
    return code_behind_location


# =============================
#  End of File Creation Region

if __name__ == '__main__':
    """Run code as a python command"""
    m = Mitzy()
    root.mainloop()
