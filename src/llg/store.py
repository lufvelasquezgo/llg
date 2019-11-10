import h5py


class StoreHDF:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.__dataset = h5py.File(self.filename, mode="w")
        return self

    def __exit__(self, a, b, c):
        self.__dataset.close()

    def populate(self, simulation_information):
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

        self.__states_dataset = self.__dataset.create_dataset(
            "states",
            (num_TH, num_iterations, num_sites, 3),
            dtype=float,
            chunks=True,
            compression="gzip",
        )

        self.__exchange_energy_dataset = self.__dataset.create_dataset(
            "exchange_energy",
            (num_TH, num_iterations),
            dtype=float,
            chunks=True,
            compression="gzip",
        )

        self.__anisotropy_energy_dataset = self.__dataset.create_dataset(
            "anisotropy_energy",
            (num_TH, num_iterations),
            dtype=float,
            chunks=True,
            compression="gzip",
        )

        self.__magnetic_energy_dataset = self.__dataset.create_dataset(
            "magnetic_energy",
            (num_TH, num_iterations),
            dtype=float,
            chunks=True,
            compression="gzip",
        )

        self.__total_energy_dataset = self.__dataset.create_dataset(
            "total_energy",
            (num_TH, num_iterations),
            dtype=float,
            chunks=True,
            compression="gzip",
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
