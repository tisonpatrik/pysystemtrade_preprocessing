from pathlib import Path

from pydantic import BaseModel, Field


class DataFile(BaseModel):
    name: str
    local_path: Path


class Directory(BaseModel):
    name: str
    raw_data: list[DataFile] = []

    def add_file(self, data_file: DataFile):
        self.raw_data.append(data_file)


class ConfigItem(BaseModel):
    name: str = Field(alias="Name")
    directory: str = Field(alias="Directory")
    columns: list[str] = Field(alias="Columns")
