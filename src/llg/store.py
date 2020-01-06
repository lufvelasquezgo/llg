import h5py


class StoreHDF:
    """This is a class for store the information in a hdf file, as a result of the ``Simulate`` class. 

    :param filename: This is the file with the information of the simulation.
    :type filename: file
    :param compress: This is an option to compress the file in which the logical size of a file is reduced. It allows faster transmission over a network. It serialize the entire file.
    :type compress: bool
    """

    def __init__(self, filename, compress=False):
        """The constructor for StoreHDF class.
        """
        self.filename = filename
        self.compress = compress

    def __enter__(self):
        # make a database connection and return it
        self.__dataset = h5py.File(self.filename, mode="w")
        return self

    def __exit__(self, a, b, c):
        # make sure the dbconnection gets closed
        self.__dataset.close()

    def populate(self, simulation_information):
        """It is a function responsible of set the information of the simulation file and the results of the system evolve. It receives the ``simulation_information``, and it contains the information of the simulation file and the results of the system evolve
        """
        num_sites = simulation_information["num_sites"]
        num_TH = simulation_information["num_TH"]
        num_iterations = simulation_information["num_iterations"]

        # create attributes
        self.__dataset.attrs["num_sites"] = num_sites
        self.__dataset.attrs["num_iterations"] = num_iterations
        self.__dataset.attrs["seed"] = simulation_information["seed"]
        self.__dataset.attrs["units"] = simulation_information["parameters"]["units"]
        self.__dataset.attrs["damping"] = simulation_information["parameters"][
            "damping"
        ]
        self.__dataset.attrs["gyromagnetic"] = simulation_information["parameters"][
            "gyromagnetic"
        ]
        self.__dataset.attrs["deltat"] = simulation_information["parameters"]["deltat"]
        self.__dataset.attrs["kb"] = simulation_information["parameters"]["kb"]
        self.__dataset.attrs["num_TH"] = len(simulation_information["temperature"])

        # create types
        types_dataset = self.__dataset.create_dataset(
            "types", (num_sites,), dtype=h5py.string_dtype()
        )
        types_dataset[:] = simulation_information["types"]

        self.__dataset["positions"] = simulation_information["positions"]
        self.__dataset["initial_state"] = simulation_information["initial_state"]
        self.__dataset["temperature"] = simulation_information["temperature"]
        self.__dataset["field"] = simulation_information["field"]

        compression_options = (
            {"chunks": True, "compression": "gzip"} if self.compress else {}
        )

        self.__states_dataset = self.__dataset.create_dataset(
            "states",
            (num_TH, num_iterations, num_sites, 3),
            dtype=float,
            **compression_options,
        )

        self.__exchange_energy_dataset = self.__dataset.create_dataset(
            "exchange_energy",
            (num_TH, num_iterations),
            dtype=float,
            **compression_options,
        )

        self.__anisotropy_energy_dataset = self.__dataset.create_dataset(
            "anisotropy_energy",
            (num_TH, num_iterations),
            dtype=float,
            **compression_options,
        )

        self.__magnetic_energy_dataset = self.__dataset.create_dataset(
            "magnetic_energy",
            (num_TH, num_iterations),
            dtype=float,
            **compression_options,
        )

        self.__total_energy_dataset = self.__dataset.create_dataset(
            "total_energy", (num_TH, num_iterations), dtype=float, **compression_options
        )

    def store_state(self, state, i, j):
        self.__states_dataset[i, j, :] = state

    def store_exchange_energy(self, exchange_energy, i, j):
        self.__exchange_energy_dataset[i, j] = exchange_energy

    def store_anisotropy_energy(self, anisotropy_energy, i, j):
        self.__anisotropy_energy_dataset[i, j] = anisotropy_energy

    def store_magnetic_energy(self, magnetic_energy, i, j):
        self.__magnetic_energy_dataset[i, j] = magnetic_energy

    def store_total_energy(self, total_energy, i, j):
        self.__total_energy_dataset[i, j] = total_energy
