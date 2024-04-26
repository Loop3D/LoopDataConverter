from abc import ABC, abstractmethod
import beartype
import pandas
import geopandas
import os
import validators


class BaseFileReader(ABC):
    def __init__(self):
        self.file_reader_label = "FileReaderBaseClass"

    def type(self):
        return self.file_reader_label

    @beartype.beartype
    @abstractmethod
    def check_source_type(self, file_source: str):
        assert validators.url(file_source) or os.path.isfile(
            file_source
        ), "Invalid file source, must be a valid URL or file path"

    @beartype.beartype
    @abstractmethod
    def get_file(self, file_source: str, layer: str = None):
        pass

    @beartype.beartype
    @abstractmethod
    def save(self, file_path: str, file_extension: str = None):
        pass

    @abstractmethod
    def read(self):
        pass


class CSVFileReader(BaseFileReader):
    def __init__(self):
        self.file_reader_label = "CSVFileReader"
        self.file = None
        self.data = None

    def type(self):
        return self.file_reader_label

    @beartype.beartype
    def check_source_type(self, file_source: str):
        super().check_source_type(file_source)

    @beartype.beartype
    def get_file(self, file_source: str, layer: str = None):
        return pandas.read_csv(file_source)

    @beartype.beartype
    def save(self, file_path: str):
        self.data.to_csv(file_path)

    @beartype.beartype
    def read(self, file_source: str):
        self.check_source_type(file_source)
        self.file = self.get_file(file_source)
        self.data = pandas.DataFrame(self.file)


class GeoDataFileReader(BaseFileReader):
    def __init__(self):
        self.file_reader_label = "GeoDataFileReader"
        self.file = None
        self.data = None

    def type(self):
        return self.file_reader_label

    @beartype.beartype
    def check_source_type(self, file_source: str):
        super().check_source_type(file_source)

    @beartype.beartype
    def get_file(self, file_source: str, layer: str = None):
        file_extension = os.path.splitext(file_source)[1]

        if file_extension in [".shp", ".geojson"]:
            return geopandas.read_file(file_source)

        elif file_extension == ".gpkg":
            assert layer is not None, "Layer name must be provided for GeoPackage files"

            return geopandas.read_file(file_source, layer=layer)

        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    @beartype.beartype
    def save(self, file_path: str, file_extension: str = None):
        if file_extension == "geojson":
            self.data.to_file(file_path, driver="GeoJSON")

        elif file_extension == "gpkg":
            self.data.to_file(file_path, driver="GPKG")

        elif file_extension == "shp":
            self.data.to_file(file_path)

        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    @beartype.beartype
    def read(self, file_source: str):
        self.check_source_type(file_source)
        self.file = self.get_file(file_source)
        self.data = geopandas.GeoDataFrame(self.file)


class FileReader:
    def __init__(self, file_source, layer=None):
        self.layer = layer
        self.file_source = file_source
        self.reader = self.assign_reader()
        self.file_reader_label = self.reader.type()

    def get_extension(self):
        return os.path.splitext(self.file_source)[1]

    def assign_reader(self):
        file_extension = self.get_extension()

        if validators.url(self.file_source) or file_extension == ".csv":
            return CSVFileReader()

        elif file_extension in [".shp", ".geojson", ".gpkg"]:
            return GeoDataFileReader()

        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def read(self):
        self.reader.read(self.file_source, self.layer)

        return self.reader.data

    def save(self, file_path, file_extension=None):
        self.reader.save(file_path, file_extension)
