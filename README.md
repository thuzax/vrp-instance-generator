# VRP Instance Generator

Generates VRP instances based on real data and open tools.

## Requirements

* Python 3

## Installing Python dependencies

Use the following command in the project home:

```
pip install -r requirements.txt
```

## OSRM Option

As an option, the distance and time matrices calculation can be made with the [Open Source Routing Machine (OSRM)](https://github.com/Project-OSRM/). For faster calculations we suggest running it locally. To do so, it is needed to install and configure [osrm-backend](https://github.com/Project-OSRM/osrm-backend). In this guide we summarize one of the osrm-backend installing options for Ubuntu (present in the original project quickstart guide).

More about the implementation of distance and time matrices calculation can be found at [Distance and Time Calculation](documentation/distance_and_times.md)

### Installing osrm-backend

Clone the osrm-backend project:

```
git clone https://github.com/Project-OSRM/osrm-backend.git
```

The following instructions are from [osrm-backend/building-from-source](https://github.com/Project-OSRM/osrm-backend#building-from-source). Make sure to run the commands in OSRM directory.

* Install OSRM dependencies:

    ```
    sudo apt install build-essential git cmake pkg-config libbz2-dev libxml2-dev libzip-dev libboost-all-dev lua5.2 liblua5.2-dev libtbb-dev
    ```

* Compile and install OSRM binaries:

    ```
    mkdir -p build
    ```
    ```
    cd build
    ```
    ```
    cmake ..
    ```
    ```
    cmake --build .
    ```
    ```
    sudo cmake --build . --target install
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
osrm-extract <path-to-the-.osm.pbf-file> -p <path-to-profile-file>
```

A profile file represent the behavior of a transport mode, for example a truck, a car or foot. As an example, we can run the command above with the downloaded Brazilian North Region and the profile for a car:

```
osrm-extract ./brazil/norte/norte-latest.osm.pbf -p profiles/car.lua
```

After extracting the graph must be partitioned into cells. Following the example:

```
osrm-partition ./brazil/norte/norte-latest.osrm
```

At last, the partitioned graph must be customized, which means routing weights for cells are calculated:

```
osrm-customize ./brazil/norte/norte-latest.osrm
```

#### Starting OSRM server

To start the server use the command:

```
osrm-routed --algorithm=MLD ./brazil/norte/norte-latest.osrm
```

To obtain the distance matrix it will be sent a `/table` request to the server. This request calculate the route from `sources` to `destinations`. This service has a limit of `100` locations and, to larger instances, it is needed to set a higher limit. To start the server with another limit, use the following command:
```
osrm-routed --algorithm=MLD <path-to-customized-osrm-file> --max-table-size <new-table-size>
```


## Generating Instances

To run this program use the following command:

```
python3 generic_generator.py --set-config-file <configuration-file.json> --set-seed <seed-value>
```

The parameter ``--set-config-file`` is required and recevies a ``json`` file with the parameters needed to run the program. More about the configuration file can be found at [Configuration File Documentation](documentation/configuration_file.md).

The second parameter ``--set-seed`` is a optional parameter which set the program random seed, allowing reproduction of the generations.

As an example, you can use the ``configuration.json`` file with seed 0 to run the program:

```
python3 python3 generic_generator.py --set-config-file configuration.json --set-seed 0
```



## Authors

[Arthur Henrique Sousa Cruz](https://github.com/thuzax/)

[Mayron César de Oliveira Moreira](https://github.com/mayronmoreira)

[Miguel Rodrigues](https://github.com/ElMigu17)

[Franklina Maria Bragion de Toledo](https://sites.icmc.usp.br/fran/wiki/pmwiki.php)