import adsk.core
import adsk.fusion
import traceback
import math


ADDIN_ID = 'GuitarEngine'



class FretboardCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):

    def __init__(self):
        super().__init__()

    def notify(self, args):
        eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
        app = adsk.core.Application.get()
        ui = app.userInterface
        # Verify that a Fusion design is active.
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            ui.messageBox('A Fusion design must be active when invoking this command.')
            return()

        print(self._getUnits(design)


    def _getUnits(self, design):
        defaultUnits = design.unitsManager.defaultLengthUnits
        # Determine whether to use inches or millimeters as the intial default.
        if defaultUnits == 'in' or defaultUnits == 'ft':
            units = 'in'
        else:
            units = 'mm'

        # Define the default values and get the previous values from the attributes.
        if units == 'in':
            standard = 'English'
        else:
            standard = 'Metric'
            standardAttrib = design.attributes.itemByName(ADDIN_ID, 'standard')

        if standardAttrib:
            standard = standardAttrib.value

        if standard == 'English':
            units = 'in'
        else:
            units = 'mm'

        return units, standard



STARTUP_MESSAGE = """<b>Guitar Engine [Beta] (v2019.01.20)</b>\
has been added to the <i>SOLID</i> tab of the <i>DESIGN</i>\
 workspace.<br><br><div align="center"><b>This is a beta version.</div>"""


def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        # Create a command definition and add a button to the CREATE panel.
        addButtonDefinition = ui.commandDefinitions.addButtonDefinition
        cmdDef = addButtonDefinition(ADDIN_ID,
                                     'Guitar Engine [Beta] (v2019.01.20)',
                                     'Creates a fretboard component\n\n',
                                     'Resources/Icons')
        createPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        fretboardButton = createPanel.controls.addCommand(cmdDef)
        # Connect to the command created event.
        onCommandCreated = FretboardCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)

        # Make the button available in the panel.
        fretboardButton.isPromotedByDefault = True
        fretboardButton.isPromoted = True

        if context['IsApplicationStartup'] is False:
            ui.messageBox(STARTUP_MESSAGE)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        createPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        fretboardButton = createPanel.controls.itemById(ADDIN_ID)
        if fretboardButton:
            fretboardButton.deleteMe()

        cmdDef = ui.commandDefinitions.itemById(ADDIN_ID)
        if cmdDef:
            cmdDef.deleteMe()
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
