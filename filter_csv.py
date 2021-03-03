import pandas
import random
import time

import global_parameters
import calculate_distances

def filter_by_reaching(data, lat_column_name, lon_column_name, reaching_filter):

    if (not reaching_filter):
        return data


    removed_set = pandas.DataFrame(columns=data.columns)


    for ind, row in data.iterrows():
        random_ind = data.sample(n=1).index
        while(ind == random_ind):
            random_ind = data.sample(n=1).index

        random_row = data.loc[random_ind].iloc[0]

        point_x = (
            float(row[lat_column_name]), 
            float(row[lon_column_name])
        )

        point_y = (
            float(random_row[lat_column_name]), 
            float(random_row[lon_column_name])
        )

        reaching_data = calculate_distances.request_osrm_dist(point_x, point_y)
        # time.sleep(random.randint(0, 1))

        if (reaching_data["code"].upper() != "OK"):
            removed_set = removed_set.append(row)

    print(data)
    print(removed_set)

    data = data.drop(removed_set.index)

    print(data)

    return data

def filter_lat_limits(data, min_lat, max_lat, lat_column_name):
    """Remove points out of the latitude limits, if limits are given
    """

    if ((min_lat is None) and (max_lat is None)):
        return data
    
    if (max_lat is None):
        data = data.drop(data[data[lat_column_name] < min_lat].index)
        return data

    if (min_lat is None):
        data = data.drop(data[data[lat_column_name] > max_lat].index)
        return data

    data = data.drop(
        data[
            (data[lat_column_name] < min_lat) 
            | 
            (data[lat_column_name] > max_lat)
        ].index
    )
    
    return data


def filter_lon_limits(data, min_lon, max_lon, lon_column_name):
    """Remove points out of the longitude limits, if limits are given
    """
    
    if ((min_lon is None) and (max_lon is None)):
        return data

    if (max_lon is None):
        data = data.drop(data[data[lon_column_name] < min_lon].index)
        return data

    if (min_lon is None):
        data = data.drop(data[data[lon_column_name] > max_lon].index)
        return data

    data = data.drop(
        data[
            (data[lon_column_name] < min_lon) 
            | 
            (data[lon_column_name] > max_lon)
        ].index
    )
    
    return data


def filter_by_lat_and_lon(
    data, 
    min_lat, 
    max_lat, 
    min_lon, 
    max_lon, 
    lat_column_name, 
    lon_column_name,
    block_point_repetition
):
    """
    Remove points based on latitude and longitude
    """

    # Remove rows with latidude or longitude with None values
    data = data.dropna(subset=[lat_column_name, lon_column_name])


    # Remove reapeated points if --block-point-repetition flag was specified
    if (block_point_repetition):
        data = data.drop_duplicates(
                        subset=[lat_column_name, lon_column_name], 
                        keep="first"
                    )

    # Remove points out of the latitude limits, if limits are given
    data = filter_lat_limits(data, min_lat, max_lat, lat_column_name)

    # Remove points out of the longitude limits, if limits are given
    data = filter_lon_limits(data, min_lon, max_lon, lon_column_name)

    return data


def filter_by_number(
    data, 
    number_column_name, 
    block_no_number, 
):
    """
    Remove points nased on the address number
    """
    
    # Remove rows without number
    if (block_no_number):
        data = data.dropna(subset=[number_column_name])

    return data


def filter_by_street(
    data, 
    street_column_name, 
    block_no_street, 
):
    """
    Remove points nased on the address number
    """
    
    # Remove rows without number
    if (block_no_street):
        data = data.dropna(subset=[street_column_name])

    return data



def filter_data(data):
    """Filter the input data
    """

    parameter_names = global_parameters.get_global_parameters_names()
    
    ### get parameters keys
    par_input_instance = parameter_names[0]

    par_lat_column_name = parameter_names[1]
    par_lon_column_name = parameter_names[2]
    par_number_column_name = parameter_names[3]
    par_street_column_name = parameter_names[4]

    par_min_lat = parameter_names[5]
    par_max_lat = parameter_names[6]
    par_min_lon = parameter_names[7]
    par_max_lon = parameter_names[8]

    par_block_point_repetition = parameter_names[9]
    par_block_no_number = parameter_names[10]
    par_block_no_street = parameter_names[11]
    par_reaching_filter = parameter_names[12]


    ### get values that will be used with their keys
    lat_column_name = global_parameters.get_parameter(par_lat_column_name)
    lon_column_name = global_parameters.get_parameter(par_lon_column_name)
    number_column_name = global_parameters.get_parameter(par_number_column_name)
    street_column_name = global_parameters.get_parameter(
                                                par_street_column_name
                                            )
    
    min_lat = global_parameters.get_parameter(par_min_lat)
    max_lat = global_parameters.get_parameter(par_max_lat)
    min_lon = global_parameters.get_parameter(par_min_lon)
    max_lon = global_parameters.get_parameter(par_max_lon)
    
    block_point_repetition = global_parameters.get_parameter(
                                                    par_number_column_name
                                                )

    block_no_number = global_parameters.get_parameter(par_block_no_number)
    block_no_street = global_parameters.get_parameter(par_block_no_street)
    reaching_filter = global_parameters.get_parameter(par_reaching_filter)
    
    ### filter data
    data = filter_by_lat_and_lon(
            data, 
            min_lat, 
            max_lat, 
            min_lon, 
            max_lon, 
            lat_column_name, 
            lon_column_name,
            block_point_repetition
        )

    data = filter_by_number(
                data, 
                number_column_name, 
                block_no_number
            )

    data = filter_by_street(
            data, 
            street_column_name, 
            block_no_street
        )

    filter_by_reaching(data, lat_column_name, lon_column_name, reaching_filter)

    return data
