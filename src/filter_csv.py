import pandas


from progress.bar import Bar

from src import global_parameters
from src import execution_log
from src import calculate_distances_osrm as calculate_distances

def filter_by_reaching(data, lat_column_name, lon_column_name, reaching_filter):
    """Remove points that can't reach another random point
    """
    if (not reaching_filter):
        return data


    execution_log.info_log("Filtering by reachability...")

    removed_set = pandas.DataFrame(columns=data.columns)

    bar = Bar("Applying filter:", max=len(data),suffix='%(percent)d%%')

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

        distance, time = calculate_distances.request_dist_and_time(
                                                    point_x, 
                                                    point_y
                                                )

        if ((distance is None) or (data is None)):
            removed_set = removed_set.append(row)

        bar.next()

    bar.finish()
    data = data.drop(removed_set.index)

    execution_log.info_log("Done.")

    return data

def filter_lat_limits(data, min_lat, max_lat, lat_column_name):
    """Remove points out of the latitude limits, if limits are given
    """

    if ((min_lat is None) and (max_lat is None)):
        return data

    if (max_lat is None):
        execution_log.info_log("Filtering by min latitude...")
        data = data.drop(data[data[lat_column_name] < min_lat].index)
        execution_log.info_log("Done.")
        
        return data

    if (min_lat is None):
        execution_log.info_log("Filtering by max latitude...")
        data = data.drop(data[data[lat_column_name] > max_lat].index)
        execution_log.info_log("Done.")

        return data

    execution_log.info_log("Filtering by min and max latitude...")
    data = data.drop(
        data[
            (data[lat_column_name] < min_lat) 
            | 
            (data[lat_column_name] > max_lat)
        ].index
    )
    execution_log.info_log("Done.")

    return data


def filter_lon_limits(data, min_lon, max_lon, lon_column_name):
    """Remove points out of the longitude limits, if limits are given
    """
    
    if ((min_lon is None) and (max_lon is None)):
        return data

    if (max_lon is None):
        execution_log.info_log("Filtering by min longitude...")
        data = data.drop(data[data[lon_column_name] < min_lon].index)
        execution_log.info_log("Done.")
        return data

    if (min_lon is None):
        execution_log.info_log("Filtering by max longitude...")
        data = data.drop(data[data[lon_column_name] > max_lon].index)
        execution_log.info_log("Done.")
        return data

    execution_log.info_log("Filtering by min and max longitude...")
    data = data.drop(
        data[
            (data[lon_column_name] < min_lon) 
            | 
            (data[lon_column_name] > max_lon)
        ].index
    )
    execution_log.info_log("Done.")

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

    execution_log.info_log("Removing lines without latitude or longitude...")
    
    # Remove rows with latidude or longitude with None values
    data = data.dropna(subset=[lat_column_name, lon_column_name])
    
    execution_log.info_log("Done.")

    execution_log.info_log(
                        "Removing lines with invalid latitude or longitude..."
                    )
    
    # Remove rows with invalid latitude
    data = data.drop(
        data[
            (data[lat_column_name] < -90) 
            | 
            (data[lat_column_name] > 90)
        ].index
    )

    # Remove rows with invalid longitude
    data = data.drop(
        data[
            (data[lon_column_name] < -180) 
            | 
            (data[lon_column_name] > 180)
        ].index
    )

    execution_log.info_log("Done.")


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
        execution_log.info_log("Removing lines without number...")
        data = data.dropna(subset=[number_column_name])
        execution_log.info_log("Done.")

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
        execution_log.info_log("Removing lines without street...")
        data = data.dropna(subset=[street_column_name])
        execution_log.info_log("Done.")

    return data



def filter_data(data):
    """Filter the input data
    """

    execution_log.info_log("Filtering data.")

    ### get values that will be used with their keys
    lat_column_name = global_parameters.lat_column_name()
    lon_column_name = global_parameters.lon_column_name()
    number_column_name = global_parameters.number_column_name()
    street_column_name = global_parameters.street_column_name()
    
    min_lat = global_parameters.min_lat()
    max_lat = global_parameters.max_lat()
    min_lon = global_parameters.min_lon()
    max_lon = global_parameters.max_lon()
    
    block_point_repetition = global_parameters.block_no_number()

    block_no_number = global_parameters.block_no_number()
    block_no_street = global_parameters.block_no_street()
    reaching_filter = global_parameters.reaching_filter()
    
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

    execution_log.info_log("Data filtered.")

    return data
