from burp import IBurpExtender, ITab, IContextMenuFactory, IHttpListener
from javax.swing import JPanel, JButton, JTextArea, JScrollPane, JMenuItem, JFileChooser, JOptionPane
from java.awt import BorderLayout
from java.util import List, ArrayList
import java.awt.event.ActionListener
import java.awt.event.ActionEvent
import os

class BurpExtender(IBurpExtender, ITab, IContextMenuFactory, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        self._callbacks.setExtensionName("Param Extractor")
        
        # Create UI
        self.panel = JPanel(BorderLayout())
        self.text_area = JTextArea()
        scroll_pane = JScrollPane(self.text_area)
        
        # Buttons
        self.scan_button = JButton("Scan", actionPerformed=self.fetch_params)
        self.clear_button = JButton("Clear", actionPerformed=self.clear_output)
        self.export_button = JButton("Export to File", actionPerformed=self.export_to_file)
        
        # Add UI elements
        self.panel.add(scroll_pane, BorderLayout.CENTER)
        button_panel = JPanel()
        button_panel.add(self.scan_button)
        button_panel.add(self.clear_button)
        button_panel.add(self.export_button)
        self.panel.add(button_panel, BorderLayout.SOUTH)
        
        # Register UI
        self._callbacks.addSuiteTab(self)
        self._callbacks.registerContextMenuFactory(self)
        self._callbacks.registerHttpListener(self)

    def getTabCaption(self):
        return "Param Extractor"

    def getUiComponent(self):
        return self.panel

    def createMenuItems(self, invocation):
        menu_list = ArrayList()
        menu_item = JMenuItem("Copy to file", actionPerformed=lambda x: self.export_to_file(None))
        menu_list.add(menu_item)
        return menu_list

    def fetch_params(self, event):
        """Extract URLs with parameters from Burp history"""
        try:
            self.text_area.setText("")
            history = self._callbacks.getProxyHistory()
            extracted_params = set()

            for entry in history:
                request_info = self._helpers.analyzeRequest(entry)
                url = request_info.getUrl().toString()
                
                # Capture GET, POST, and JSON parameters
                params = request_info.getParameters()
                param_strings = ["{}=FUZZ".format(p.getName()) for p in params if p.getType() in (p.PARAM_URL, p.PARAM_BODY, p.PARAM_JSON)]

                if param_strings:
                    full_url = "{}?{}".format(url, "&".join(param_strings))
                    extracted_params.add(full_url)

            self.text_area.setText("\n".join(extracted_params))
        except Exception as e:
            JOptionPane.showMessageDialog(self.panel, "Error fetching parameters: {}".format(str(e)), "Error", JOptionPane.ERROR_MESSAGE)

    def clear_output(self, event):
        """Clear the text area"""
        self.text_area.setText("")
    
    def export_to_file(self, event):
        """Export extracted URLs to a text file"""
        try:
            file_chooser = JFileChooser()
            if file_chooser.showSaveDialog(self.panel) == JFileChooser.APPROVE_OPTION:
                file_path = file_chooser.getSelectedFile().getAbsolutePath()
                if not file_path.endswith(".txt"):
                    file_path += ".txt"
                
                with open(file_path, "w") as f:
                    f.write(self.text_area.getText())
        except Exception as e:
            JOptionPane.showMessageDialog(self.panel, "Error saving file: {}".format(str(e)), "Error", JOptionPane.ERROR_MESSAGE)
