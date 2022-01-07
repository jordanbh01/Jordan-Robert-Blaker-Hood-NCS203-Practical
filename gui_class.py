"""Jordan Robert Blaker-Hood NCS-203 Practical . This python file contains the abstract class Gui which is subclassed
by ServerGui and Client Gui. """
# Imports
from abc import abstractmethod, ABC


# This creates the abstract class Gui with the attributes to be inherited by ServerGui and ClientGui
class Gui(ABC):
    icon = 'icon.ico'
    sticky = 'NSEW'
    style = 'AccentButton'
    padding = 5
    app_size = "520x550"
    title = 'Application'
    theme = 'proxttk-dark'
    connection_label_foreground = 'red'
    application_frame = None

    # This creates the abstract function app which is overridden in ServerGui and ClientGui
    @abstractmethod
    def app(self):
        pass
