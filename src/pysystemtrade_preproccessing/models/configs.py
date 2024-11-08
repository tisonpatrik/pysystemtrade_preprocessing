from pydantic import BaseModel, Field


class ConfigItem(BaseModel):
    name: str = Field(alias="Name")
    directory: str = Field(alias="Directory")
    columns: list[str] = Field(alias="Columns")
    raw_data: bool = Field(alias="RawData")
    daily_data: bool = Field(alias="DailyData")


class Config(BaseModel):
    items: list[ConfigItem]
