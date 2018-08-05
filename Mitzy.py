import tkinter as tk
from tkinter import *
from tkinter.messagebox import askquestion, showinfo
from tkinter.simpledialog import askstring


def createWebPartTemplate(title):
    f= open(title + ".ascx","w+")
    f.write("<%@ Control Language=\"C#\" AutoEventWireup=\"true\" Inherits=\"CMSWebParts_AFSI_" + title + "\"  CodeBehind=\"~/CMSWebParts/AFSI/" + title + ".ascx.cs\" %>\n")
    f.write("<asp:PlaceHolder runat=\"server\" id=\"plcWrapper\">\n")
    f.write("   <!-- Paste your html here! -->\n")
    f.write("</asp:PlaceHolder>\n")
    f.close()


def createWebPartCodeBehind(title, varList):
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


def createWebPartDesign(title):
    f= open(title + ".ascx.designer.cs","w+")
    f.write("public partial class CMSWebParts_AFSI_" + title + " {\n")
    f.write("   protected global::System.Web.UI.WebControls.PlaceHolder plcWrapper;\n")
    f.write("}")
    f.close()


class Mitzy(Frame):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.pack()
        varList = []
        varString = ""
        title = self.ask_for_webpart()
        addVar = True

        while addVar == True:
            str = self.ask_for_a_variable(varString)
            varList.append(str)
            if len(varList) == 1:
                varString = varString + str
            else:
                varString = varString + ", " + str

            addVar = self.ask_add_more(varString)

        createWebPartTemplate(title)
        createWebPartCodeBehind(title, varList)
        createWebPartDesign(title)
        showinfo('YAY!', 'Code has been farted!')

    def ask_for_webpart(self):
        str = askstring('Mitzy\'s Code Fart', 'Whats the title of your webpart?\n===================================')
        return str

    def ask_for_a_variable(self, varList):
        str = askstring('Mitzy\'s Code Fart', 'Do you want to add a variable [Variables added: ' + varList + ']')
        return str

    def ask_add_more(self, varList):
        str = askquestion('Mitzy\'s Code Fart', 'Do you want to add more?[Variables added: ' + varList + ']')
        if str == 'no':
            return False
        else:
            return True


if __name__ == '__main__':
    root = tk.Tk()
    Mitzy()