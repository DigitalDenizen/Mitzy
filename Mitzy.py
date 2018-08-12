from tkinter import *


class Mitzy:
    """Mitzy creates a window that asks for title and property names and uses that to create a web part"""
    def __init__(self, master):
        frame = Frame(master)
        frame.pack(fill=None, expand=False)
        middle_frame = Frame(master)
        middle_frame.pack()
        app_title = Label(frame, text="Welcome to Mitzy's Web Part Creator!", bg="bisque")
        app_title.pack(side=LEFT)
        wp_label = Label(middle_frame, text="Web Part Name: ", bg="bisque")
        wp_label.pack(side=LEFT)
        wp_title_entry = Entry(middle_frame, text="What is the name of your Web Part?: ")
        wp_title_entry.pack(side=LEFT)
        bottom_frame = Frame(master)
        bottom_frame.pack(side=BOTTOM)
        wp_add_prop = Button(bottom_frame, text="Add Property", command=self.add_property(master))
        wp_add_prop.pack(side=LEFT)

    @staticmethod
    def add_property(master):
        """Displays a text field to add a property"""
        new_frame = Frame(master)
        new_frame.pack()
        button_title = Label(new_frame, text="Web Part Name: ")

        new_button = Entry


#  Creates The Actual Files
# ==========================
def create_web_part_template(title):
    f= open(title + ".ascx","w+")
    f.write("<%@ Control Language=\"C#\" AutoEventWireup=\"true\" Inherits=\"CMSWebParts_AFSI_" + title + "\"  CodeBehind=\"~/CMSWebParts/AFSI/" + title + ".ascx.cs\" %>\n")
    f.write("<asp:PlaceHolder runat=\"server\" id=\"plcWrapper\">\n")
    f.write("   <!-- Paste your html here! -->\n")
    f.write("</asp:PlaceHolder>\n")
    f.close()


def create_web_part_code_behind(title, varList):
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
    f.write("public partial class CMSWebParts_AFSI_" + title + " : CMSAbstractWebPart\n")
    f.write("{\n")
    f.write("    #region \"Properties\"\n")
    f.write("\n")
    for i in range(0, len(varList)):
        f.write("    protected string m" + varList[i] + "\n")

    f.write("\n\n")

    for i in range(0,len(varList)):
        f.write("    public string " + varList[i] + "\n")
        f.write("    {\n")
        f.write("       get\n")
        f.write("       {\n")
        f.write("           return ValidationHelper.GetString(this.GetValue(\""+ varList[i] +"\"), m" + varList[i] + ");\n")
        f.write("       }\n")
        f.write("       set\n")
        f.write("       {\n")
        f.write("           this.SetValue(\"" + varList[i] + "\", value);\n")
        f.write("           m" + varList[i] + " = value\n")
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


def create_web_part_design(title):
    f= open(title + ".ascx.designer.cs","w+")
    f.write("public partial class CMSWebParts_AFSI_" + title + " {\n")
    f.write("   protected global::System.Web.UI.WebControls.PlaceHolder plcWrapper;\n")
    f.write("}")
    f.close()


# =============================
#  End of File Creation Region

root = Tk()
root.title("Mitzy")
root.configure(bg="bisque")
root.geometry("300x150")
m = Mitzy(root)
root.mainloop()
