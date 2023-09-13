# it stores (file path name) and (datatype) of data stored in artifact folder
from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    feature_store_file_path: str
    train_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    report_file_path: str


@dataclass
class DataTransformationArtifact:
    transform_object_path: str
    transform_train_path: str
    transform_test_path: str
    target_encoder_path: str
