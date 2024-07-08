import pytest
import geopandas as gpd
from ..file_readers import GeoDataFileReader
import os
import tempfile

# Fixtures for sample file sources
@pytest.fixture
def shp_file_source():
    # Assuming a sample .shp file exists for testing
    return "sample_data/sample.shp"

@pytest.fixture
def geojson_file_source():
    # Assuming a sample .geojson file exists for testing
    return "sample_data/sample.geojson"

@pytest.fixture
def gpkg_file_source():
    # Assuming a sample .gpkg file exists for testing, with a layer name
    return "sample_data/sample.gpkg", "layer1"

@pytest.fixture
def invalid_file_source():
    return "sample_data/invalid.txt"

# Test Initialization
def test_initialization():
    reader = GeoDataFileReader()
    assert reader.file_reader_label == "GeoDataFileReader"

# Test Check Source Type
def test_check_source_type_valid(shp_file_source, geojson_file_source, gpkg_file_source):
    reader = GeoDataFileReader()
    # Assuming these calls do not raise an exception
    reader.check_source_type(shp_file_source[0])
    reader.check_source_type(geojson_file_source)
    reader.check_source_type(gpkg_file_source[0])

def test_check_source_type_invalid(invalid_file_source):
    reader = GeoDataFileReader()
    with pytest.raises(AssertionError):
        reader.check_source_type(invalid_file_source)

# Test Get File
@pytest.mark.parametrize("file_source", ["shp_file_source", "geojson_file_source", "gpkg_file_source"])
def test_get_file(file_source, request):
    reader = GeoDataFileReader()
    file_source = request.getfixturevalue(file_source)
    if isinstance(file_source, tuple):
        file, layer = file_source
        df = reader.get_file(file, layer)
    else:
        df = reader.get_file(file_source)
    assert isinstance(df, gpd.GeoDataFrame)

def test_get_file_unsupported(invalid_file_source):
    reader = GeoDataFileReader()
    with pytest.raises(ValueError):
        reader.get_file(invalid_file_source)

# Test Read Method
def test_read_method(shp_file_source):
    reader = GeoDataFileReader()
    reader.read(shp_file_source)
    assert isinstance(reader.data, gpd.GeoDataFrame)

# Test Save Method
def test_save_method(geojson_file_source):
    reader = GeoDataFileReader()
    reader.read(geojson_file_source)
    with tempfile.TemporaryDirectory() as tmpdirname:
        save_path = os.path.join(tmpdirname, "output.geojson")
        reader.save(save_path, "geojson")
        assert os.path.exists(save_path)

def test_save_method_unsupported(geojson_file_source):
    reader = GeoDataFileReader()
    reader.read(geojson_file_source)
    with pytest.raises(ValueError):
        reader.save("output.unsupported")