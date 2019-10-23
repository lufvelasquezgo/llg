import h5py


class StoreHDF:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.__dataset = h5py.File(self.filename, mode="w")
        return self

    def __exit__(self, a, b, c):
        self.__dataset.close()

    def store_attributes(self, system_information):
        self.__dataset.attrs["num_sites"] = system_information["num_sites"]
        self.__dataset.attrs["seed"] = system_information["seed"]
        self.__dataset.attrs["units"] = system_information["parameters"]["units"]
        self.__dataset.attrs["damping"] = system_information["parameters"]["damping"]
        self.__dataset.attrs["gyromagnetic"] = system_information["parameters"][
            "gyromagnetic"
        ]
        self.__dataset.attrs["deltat"] = system_information["parameters"]["deltat"]
        self.__dataset.attrs["kb"] = system_information["parameters"]["kb"]
        self.__dataset.attrs["num_TH"] = len(system_information["temperature"])

    def store_types(self, types):
        types_dataset = self.__dataset.create_dataset(
            "types", (len(types),), dtype=h5py.string_dtype()
        )
        types_dataset[:] = types

    def store_positions(self, positions):
        self.__dataset["positions"] = positions

    def store_initial_state(self, initial_state):
        self.__dataset["initial_state"] = initial_state

    def store_temperature(self, temperature):
        self.__dataset["temperature"] = temperature

    def store_field(self, field):
        self.__dataset["field"] = field

    def create_states(self, num_TH, num_iterations, num_sites):
        self.__states_dataset = self.__dataset.create_dataset(
            "states",
            (num_TH, num_iterations, num_sites, 3),
            dtype=float,
            chunks=True,
            compression="gzip",
        )

    def store_state(self, state, i, j):
        self.__states_dataset[i, j, :] = state
