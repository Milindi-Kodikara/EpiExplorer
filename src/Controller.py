# Controller class to join the View and the Model
from ReadWriteData import ReadWriteData
from CytoscapeIntegration import CytoscapeIntegration
from FormGUI import FormGUI


class Controller:
    def __init__(self):
        self.input_file = ''
        self.annotation_file = ''

    # Method to call forth the GUI
    def perform_form_functionality(self):
        controller = Controller()
        form = FormGUI(controller)
        form.form()

    # Method to call Model functionality from View
    # Takes the arguments: GUI filtering requirements, whether graph should be updated or if it's the first time,
    # if the network type is Interaction or Edge
    def perform_core_functionality(self, core_details, update, interaction_or_edge):
        global integration
        files_loaded = False
        if not update:
            # Validate input file
            input_files = core_details.iat[0, 0]
            input_files = input_files.split()
            number_of_input_files = len(input_files)
            print('Loading in ', number_of_input_files, ' input files.')

            files_loaded = True
            read_write_data = ReadWriteData(input_files, core_details.iat[0, 1].split(), core_details.iat[0, 2])
            # Get the node_df, edge_df and if the functions were successful
            read_write_done = read_write_data.get_dataframes(interaction_or_edge)
            if read_write_done[2]:
                print(
                    'The input files, {}, have been successfully loaded '
                    'and the output file has been created successfully.'.format(
                        input_files))
                print('Sending data to Cytoscape . . .')
                # Send the DataFrames in order to create the json file and create the network
                if integration is None or not update:
                    integration = CytoscapeIntegration(read_write_done[0], read_write_done[1],
                                                       interaction_or_edge)
                # Call function and determine if cytoscape worked
                cytoscape_successful = integration.cytoscape_successful(update, core_details)

                if cytoscape_successful:
                    print('Successful creation of network!')
                else:
                    print('Network creation unsuccessful, please make sure that Cytoscape is running in '
                          'the '
                          'background.')
            else:
                print('Error has occurred in Read and/or Write of the file.')
        elif update:
            print('Updating the network')
            cytoscape_successful = integration.cytoscape_successful(update, core_details)
            if cytoscape_successful:
                print('Successful creation of network!')
            else:
                print('Network creation unsuccessful, please make sure your update requests are correct')

        print('____________________DONE ~>.<~___________________')
        return files_loaded


integration = None
