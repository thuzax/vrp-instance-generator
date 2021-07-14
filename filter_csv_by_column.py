import sys
import pandas

def read_input_file(input_name):
    """Read a CSV input file
    """

    chunks_data_frame = pandas.read_csv(input_name, chunksize=1000000)


    return chunks_data_frame


def filter_by_column_value(data_chunks, column_name, value):
    filtered_chunks = []

    text = ""

    for data_chunk in data_chunks:
        filtered_chunks.append(
            data_chunk[data_chunk[column_name].str.upper() == value.upper()]
        )
        text += "#"

        print(text)



    new_data = pandas.concat(filtered_chunks)

    return new_data


def write_output_file(data, output_name):
    data.to_csv(output_name, index=False)

if __name__=="__main__":
    if (len(sys.argv) < 5):
        text = ""
        text += "Input format:\n"
        text += "python3 filter_csv_by_column "
        text += "<csv-input> <csv-output> <column_name> <mantained-value>"
        print(text)

    
    input_name = sys.argv[1]
    output_name = sys.argv[2]
    column_name = sys.argv[3]
    column_value = sys.argv[4]

    print("INPUT FILE:", input_name)
    print("OUTPUT FILE:", output_name)
    print("FILTERED COLUMN:", column_name)
    print("MANTAINED VALUE:", column_value)


    data_chunks = read_input_file(input_name)
    new_data = filter_by_column_value(data_chunks, column_name, column_value)

    write_output_file(new_data, output_name)
