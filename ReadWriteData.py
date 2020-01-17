import argparse
import os

import pandas as pd

input_type = ''
order = ''


# Method to validate the input file
def validate_input_file(input_file):
    # prefix = ''
    global order
    global input_type
    first_job_index = ''
    last_job_index = ''
    extension = ''
    valid = True
    # Split the file name and verify each substring
    new_input_file = input_file.split(".")

    if len(new_input_file) < 1:
        valid = False

    prefix = new_input_file[0][-1]

    # Alpha or Beta
    input_type = new_input_file[1]
    if (input_type == "Alpha" or input_type == "Beta" or input_type == "best") and valid:
        if input_type != "best":
            order = new_input_file[2]
            if order != "1" and order != "2" and order != "3" and order != "4":
                valid = False

            # JobIndex is only there depending on the length of the list
            if len(new_input_file) == 5 and valid:
                valid = False

            if len(new_input_file) == 6 and valid:
                first_job_index = new_input_file[3]
                last_job_index = new_input_file[4]

        extension = new_input_file[-1]

        if (extension != "csv") and valid:
            valid = False

    # print("prefix: {} ".format(prefix))
    # print("input_type: {} ".format(input_type))
    # print("order: {} ".format(order))
    # print("first_job_index: {} ".format(first_job_index))
    # print("last_job_index: {} ".format(last_job_index))
    # print("extension: {} ".format(extension))
    # print("valid: {} ".format(valid))

    return valid


# Method to create the Node DataFrame
def create_node_df(df, int_order):
    # A DataFrame with the interaction node (concat of all the names of the gene) and SNPs
    node_df = pd.DataFrame(columns=["Node"])

    # Loop through each row
    # Get the cell values of each column of each row and concat the values
    # Add the values to the new DataFrame
    for index, row in df.iterrows():
        for i in range(int_order):
            # Get the single SNPs at the specific position
            cell_value = df.iat[index, i + 1]
            # Add a cell value to the new DataFrame
            node_df = node_df.append(pd.DataFrame([cell_value], columns=["Node"]), ignore_index=True)
            if (i + 1) >= 2:
                new_cell_value = ''
                if (i + 1) == 2:
                    snp_a_cell_value = df.iat[index, i]
                    new_cell_value = str(snp_a_cell_value) + str(cell_value)

                elif (i + 1) == 3:
                    snp_b_cell_value = df.iat[index, i]
                    snp_a_cell_value = df.iat[index, i - 1]
                    new_cell_value = str(snp_a_cell_value) + str(snp_b_cell_value) + str(cell_value)

                elif (i + 1) == 4:
                    snp_c_cell_value = df.iat[index, i]
                    snp_b_cell_value = df.iat[index, i - 1]
                    snp_a_cell_value = df.iat[index, i - 2]
                    new_cell_value = str(snp_a_cell_value) + str(snp_b_cell_value) + str(snp_c_cell_value) + str(
                        cell_value)

                    # Add a cell value to the new DataFrame
                node_df = node_df.append(pd.DataFrame([new_cell_value], columns=["Node"]), ignore_index=True)

    # print(node_df)
    return node_df


# Method to create the edge DataFrame
def create_edge_df(df, int_order):
    # A DataFrame with all the nodes: individual SNP -> interaction node
    edge_df = pd.DataFrame(columns=["Edge", "Node"])

    # TODO Check if there is an existing file i.e check existing DataFrame
    for index, row in df.iterrows():
        for i in range(int_order):
            # Get the cell value
            edge_value = df.iat[index, i + 1]

            # If order is one
            # TODO Check if the SNP is from Alpha and Beta
            # TODO Check if there are any duplicates i.e same SNPs but different ordering            # Add the single SNP as a Node to the new DataFrame
            if int_order == 1:
                # Add the edge_value as the Node as there are no interactions with the edge
                edge_df = edge_df.append(pd.DataFrame([edge_value], columns=["Node"]), ignore_index=True)
            # If order is greater than 1
            if int_order >= 2:
                node = ''
                # Create the node which is a concatenation of all the SNPs
                if int_order == 2:
                    snp_a_cell_value = df.at[index, "SNP_A"]
                    snp_b_cell_value = df.at[index, "SNP_B"]
                    node = str(snp_a_cell_value) + str(snp_b_cell_value)

                elif int_order == 3:
                    snp_a_cell_value = df.at[index, "SNP_A"]
                    snp_b_cell_value = df.at[index, "SNP_B"]
                    snp_c_cell_value = df.at[index, "SNP_C"]
                    node = str(snp_a_cell_value) + str(snp_b_cell_value) + str(snp_c_cell_value)

                elif int_order == 4:
                    snp_a_cell_value = df.at[index, "SNP_A"]
                    snp_b_cell_value = df.at[index, "SNP_B"]
                    snp_c_cell_value = df.at[index, "SNP_C"]
                    snp_d_cell_value = df.at[index, "SNP_D"]
                    node = str(snp_a_cell_value) + str(snp_b_cell_value) + str(snp_c_cell_value) + str(snp_d_cell_value)

                # Add the new edge-node pair to the DataFrame
                edge_df = edge_df.append(pd.DataFrame([[edge_value, node]], columns=["Edge", "Node"]),
                                         ignore_index=True)

    print(edge_df)
    return edge_df


# Method to write data in the correct format to csv files
def write_data(node_df, edge_df):
    data_written = True

    return data_written


# Method to read in data and write data from and to a csv file
def read_write_data(input_file):
    data_done = True

    file_path = os.path.join('../sampleData/', input_file)
    df = pd.read_csv(file_path)
    int_order = int(order)

    if df.empty:
        data_done = False
    else:
        print(df)
        # Get the node_df in order to write to csv
        node_df = create_node_df(df, int_order)

        # Get the edge_df in order to write to csv
        edge_df = create_edge_df(df, int_order)

        # TODO Append to the existing output csv files
        data_written = write_data(node_df, edge_df)

        if not data_written:
            data_done = False
    return data_done


def main():
    # Read in the arguments and check for validity
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "-bfile", required=True, help="Argument in the form of: -i <input_file.csv>")
    args = vars(parser.parse_args())
    input_file = args["i"]
    valid = validate_input_file(input_file)
    if valid:
        print("The input file, {}, has been successfully validated.".format(input_file))
        data_done = read_write_data(input_file)
        if data_done:
            print(
                "The input file, {}, has been successfully loaded and the output file has been created successfully.".format(
                    input_file))
        else:
            print("Error has occurred in Read and/or Write of the file.")
    else:
        print("Error found in input file format.")


if __name__ == "__main__":
    main()
