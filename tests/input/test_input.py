import pytest
from LoopDataConverter.input.input_data import InputData, OutputData
from LoopDataConverter.datatypes import Datatype

# Test Initialization
def test_input_data_initialization():
	input_data = InputData()
	assert input_data.geology is None
	assert input_data.structure is None
	assert input_data.fault is None
	assert input_data.fold is None

def test_output_data_initialization():
	output_data = OutputData()
	assert output_data.geology is None
	assert output_data.structure is None
	assert output_data.fault is None
	assert output_data.fold is None

# Test __getitem__ Method
@pytest.mark.parametrize("datatype, value", [
	(Datatype.GEOLOGY, "geology_value"),
	(Datatype.STRUCTURE, "structure_value"),
	(Datatype.FAULT, "fault_value"),
	(Datatype.FOLD, "fold_value"),
])
def test_input_data_getitem(datatype, value):
	input_data = InputData(**{datatype: value})
	assert input_data[datatype] == value

@pytest.mark.parametrize("datatype, value", [
	(Datatype.GEOLOGY, "geology_value"),
	(Datatype.STRUCTURE, "structure_value"),
	(Datatype.FAULT, "fault_value"),
	(Datatype.FOLD, "fold_value"),
])
def test_output_data_getitem(datatype, value):
	output_data = OutputData(**{datatype: value})
	assert output_data[datatype] == value

# Test Attribute Assignment
def test_input_data_attribute_assignment():
	input_data = InputData()
	input_data.geology = "new_geology"
	input_data.structure = "new_structure"
	input_data.fault = "new_fault"
	input_data.fold = "new_fold"
	assert input_data.geology == "new_geology"
	assert input_data.structure == "new_structure"
	assert input_data.fault == "new_fault"
	assert input_data.fold == "new_fold"

def test_output_data_attribute_assignment():
	output_data = OutputData()
	output_data.geology = "new_geology"
	output_data.structure = "new_structure"
	output_data.fault = "new_fault"
	output_data.fold = "new_fold"
	assert output_data.geology == "new_geology"
	assert output_data.structure == "new_structure"
	assert output_data.fault == "new_fault"
	assert output_data.fold == "new_fold"

# Test Inheritance
def test_output_data_inheritance():
	output_data = OutputData(geology="geology_inherited", structure="structure_inherited", fault="fault_inherited", fold="fold_inherited")
	assert output_data[Datatype.GEOLOGY] == "geology_inherited"
	assert output_data[Datatype.STRUCTURE] == "structure_inherited"
	assert output_data[Datatype.FAULT] == "fault_inherited"
	assert output_data[Datatype.FOLD] == "fold_inherited"