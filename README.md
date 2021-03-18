# VRP Instance Generator

Generates VRP instances based on real data and open tools.

## Requirements

* Python 3

### Installing Python dependencies

Use the following command in the project home:

```
$ pip install -r requirements.txt
```

## Running locally

To calculate the route between two locations we recommend the Open [Source Routing Machine (OSRM)](https://github.com/Project-OSRM/). For faster calculations we suggest running it locally.

To do so, it is needed to install and configure [osrm-backend](https://github.com/Project-OSRM/osrm-backend). In this guide we summarize one of the osrm-backend installing options for Ubuntu (present in the original project quickstart guide).

### Installing osrm-backend

Clone the osrm-backend project:

```
$ git clone https://github.com/Project-OSRM/osrm-backend.git
```

The following instructions are from [osrm-backend/building-from-source](https://github.com/Project-OSRM/osrm-backend#building-from-source). Make sure to run the commands in OSRM directory.

* Install osrm dependencies:

    ```
    $ sudo apt install build-essential git cmake pkg-config libbz2-dev libxml2-dev libzip-dev libboost-all-dev lua5.2 liblua5.2-dev libtbb-dev
    ```

* Compile and install OSRM binaries:

    ```
    $ mkdir -p build
    $ cd build
    $ cmake ..
    $ cmake --build .
    $ sudo cmake --build . --target install
    ```

### Getting Maps


Before running OSRM it is needed to download the [OSM](www.openstreetmap.org) (OpenStreetMap) file of the region. [GEOFABRICK](https://download.geofabrik.de/) provides a large dataset of OSM files.

As example we will use the [Brazilian North Region](https://download.geofabrik.de/south-america/brazil.html) (norte.osm.pbf) map.

### Runing OSRM

OSRM provides state-of-art algorithms in routing context. In this tutorial we will explain how to use the Multi-Level Dijkstra algorithm. The following commands may require a too much memory, so it is recommended to set a STXXL program in a file named `.stxxl` in the osrm-backend main directory. This file will permit using memory swap. The content of the file should be as following:

```
disk=full_disk_filename,capacity,access_method
```

For example, it could be:

```
disk=/tmp/stxxl,10G,syscall
```

#### Preparing the MLD environment

It is needed to extract a graph based on the OSM data.

```
$ osrm-extract <path-to-the-.osm.pbf-file> -p <path-to-profile-file>
```

A profile file represent the behavior of a transport mode, for example a truck, a car or foot. As an example, we can run the command above with the downloaded Brazilian North Region and the profile for a car:

```
$ osrm-extract ./brazil/norte/norte-latest.osm.pbf -p profiles/car.lua
```

After extracting the graph must be partitioned into cells. Following the example:

```
$ osrm-partition ./brazil/norte/norte-latest.osrm
```

At last, the partitioned graph must be customized, which means routing weights for cells are calculated:

```
$ osrm-customize ./brazil/norte/norte-latest.osrm
```

#### Starting OSRM server

To start the server use the command:

```
$ osrm-routed --algorithm=MLD ./brazil/norte/norte-latest.osrm
```

To obtain the distance matrix it will be sent a `/table` request to the server. This request calculate the route from `sources` to `destinations`. This service has a limit of `100` locations and, to larger instances, it is needed to set a higher limit. To start the server with another limit, use the following command:
```
$ osrm-routed --algorithm=MLD <path-to-customized-osrm-file> --max-table-size <new-table-size>
```

# Running VRP Instance Generator

The instance generator has three mandatory arguments: an input instance name, the output instance name and the number of desired points in the generated instance. To run it, use the following command:

```
python3 instance_generator.py --instance-name <name-of-the-input-instace> --output-name <name-of-the-output-instance> --output-size <number-of-desired-points>
```

Besides the required inputs there are optional arguments which can be set using a configuration file. In the following sections we describe all the arguments in detail, incluinding the obrigatory

## Required Arguments

### Instance Name
    --instance-name INSTANCE_NAME

Path to the input instance. The instance must be a CSV file and needs to cointain at least the latitude and longitude of eache point. Points with invalid latitude or longitude will not be considered.

### Output Name
    --output-name OUTPUT_NAME

Path to the output instance. If the file does not exists it will be created. This output will be a CSV file containing the rows which were selected as part of the generated instnace.

### Output Size
    --output-size OUTPUT_SIZE

Desired number of elements for the generated instance. It will determine the number of clients of the generated instance

## Optional Arguments

### Latitude Column Name
    --lat-col LATITUDE_COLUMN_NAME

Name of the latitude column in the CSV input file. The default value for this argument is `"lat"`. This argument can have spaces between words (e.g. "latitude column name").

### Longitude Column Name
    --lon-col LONGITUDE_COLUMN_NAME

Name of the longitude column in the CSV input file. The default value for this argument is `"lon"`. This argument can have spaces between words (e.g. "longitude column name").

### Number Column Name
    --use-number-column NUMBER_COLUMN_NAME

If the input instance has complete address the number of the building can be used as a filter. The number column name is the building number column in the CSV file. This argument can have spaces between words (e.g. "number column name").

### Street Column Name
    --use-street-name STREET_COLUMN_NAME

If the input instance has complete address the street names can be used as filters. The street column name represents its column in the CSV file. This argument can have spaces between words (e.g. "street column name").

### Minimum Latitude
    --min-lat MIN_LAT

Limits the minimum possible latitude, avoiding the selection of clients with lower value for this attribute.

### Maximum Latitude
    --min-lat MAX_LAT

Limits the maximum possible latitude, avoiding the selection of clients with higher value for this attribute.

### Minimum Longitude
    --min-lat MIN_LON

Limits the minimum possible longitude, avoiding the selection of clients with lower value for this attribute.

### Maximum Longitude
    --min-lat MAX_LON

Limits the maximum possible longitude, avoiding the selection of clients with higher value for this attribute.

### Avoind Points Repetitions
    --block-point-repetition

Forbid two select two points with same values for latitude and longitude. This avoids, for example, selecting two apartaments of the same building. The default value for this argument is `False` and it is stored with the variable `BLOCK_POINT_REPETITION`.

### Avoind Blank Building Numbers
    --block-no-number

To use this feature it is needed the use of the argument `--use-number-column`. If set, the elements with no number in the column `NUMBER_COLUMN_NAME` will be removed. The default value for this argument is `False` and it is stored with the variable `BLOCK_NO_NUMBER`.

### Avoind Blank Street Names
    --block-no-street

To use this feature it is needed the use of the argument `--use-street-name`. If set, the elements with no street name in the column `NUMBER_COLUMN_NAME` will be removed. The default value for this argument is `False` and it is stored with the variable `BLOCK_NO_STREET`.

### Filter by reachability
    --use-reaching-filter

Remove points which are probably unreachable. For each element from the input it is selected another element and a route is calculated. If the route cannot be found, then the element is removed. It is possible that the second element is the one unreachable, but it is not worth to calculate many routes, since the input instance is intended to be too large. Also, note that the random element will be excluded once the algorithm try to calculate its route to another random element. The default value for this argument is `False` and it is stored with the variable `REACHING_FILTER`.


### Run the Matrices Calculations Remotelly
    --run-distances-remote

The distance and time matrices can be calculated remotelly (using [OSRM demo server](map.project-osrm.org/)) or locally. If this argument is set, the demo server will be used, otherwise the algorithm will requests distance from the `localhost` port `5000` (default port for OSRM backend). The value for this argument is stored with the variable `DISTANCES_LOCALLY` and its default is `True`.

### Using Configuration File
    --set-config-file SET_CONFIG_FILE

All the optionals arguments (excepting this one) can be setted in a configuration file. This argument asks for a `json` file containing values for the desired optional arguments. The file will have priority over the command line, but will not exclude it. For example, if `--min-lat` is set on the configuration file and in the command line, the value set in the file will be used. But if the `--min-lat` is set only in the second, the command line argument will be used. This is analogous for the configuration file. 

`config.json` file is an example file which contains all the optional variables set. The name of the variables are not read as case sensitive (`MIN_LAT` is the same as `min_lat`, for example).