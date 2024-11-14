from pathlib import Path

import pandas as pd


def create_instrumentconfigs(path: Path) -> pd.DataFrame:
    columns = ["symbol", "description", "pointsize", "currency", "asset_class", "per_block", "percentage", "per_trade", "region"]
    df = pd.read_csv(path, parse_dates=True)
    df.columns = columns
    return df


def create_rollconfig(path: Path) -> pd.DataFrame:
    columns = ["symbol", "hold_roll_cycle", "roll_offset_days", "carry_offset", "priced_roll_cycle", "expiry_offset"]
    df = pd.read_csv(path, parse_dates=True)
    df.columns = columns
    return df


def create_spreadcosts(path: Path) -> pd.DataFrame:
    columns = ["symbol", "spread_cost"]
    df = pd.read_csv(path, parse_dates=True)
    df.columns = columns
    return df
