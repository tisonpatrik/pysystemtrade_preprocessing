import os

import pandas as pd

from src.csv_utils.csv_generator import generate_csv_file

file_name = "tradable_instruments.csv"


def generate_tradable_instruments_csv(dir_path: str):
    print("Generation of tradable_instruments.csv")
    full_path = os.path.join(dir_path, file_name)
    df = pd.DataFrame(symbols, columns=["symbol"])
    generate_csv_file(df, full_path)


def get_tradable_instruments():
    return symbols


symbols = [
    "AEX",
    "ALUMINIUM",
    "AUD",
    "AUDJPY",
    "BB3M",
    "BBCOMM",
    "BITCOIN",
    "BOBL",
    "BONO",
    "BOVESPA",
    "BRE",
    "BRENT-LAST",
    "BTP",
    "BTP3",
    "BUND",
    "BUTTER",
    "BUXL",
    "CAC",
    "CAD",
    "CH10",
    "CHEESE",
    "CHF",
    "CHFJPY",
    "CLP",
    "CNH",
    "COPPER-micro",
    "CORN",
    "COTTON",
    "CRUDE_W",
    "CZK",
    "DAX",
    "DJSTX-SMALL",
    "DOW",
    "EPRA-EUROPE",
    "ETHANOL",
    "ETHEREUM",
    "EU-AUTO",
    "EU-BANKS",
    "EU-BASIC",
    "EU-CHEM",
    "EU-CONSTRUCTION",
    "EU-DIV30",
    "EU-DJ-TELECOM",
    "EU-DJ-UTIL",
    "EU-FOOD",
    "EU-HEALTH",
    "EU-HOUSE",
    "EU-INSURE",
    "EU-MEDIA",
    "EU-MID",
    "EU-OIL",
    "EU-REALESTATE",
    "EU-RETAIL",
    "EU-TECH",
    "EU-TRAVEL",
    "EURAUD",
    "EURCAD",
    "EURCHF",
    "EURIBOR",
    "EURO600",
    "EUROSTX",
    "EUROSTX-LARGE",
    "EUROSTX-SMALL",
    "EUROSTX200-LARGE",
    "EUR_micro",
    "FED",
    "FEEDCOW",
    "FTSECHINAA",
    "FTSECHINAH",
    "FTSEINDO",
    "FTSETAIWAN",
    "FTSEVIET",
    "GAS-LAST",
    "GAS-PEN",
    "GASOILINE",
    "GAS_US_mini",
    "GBP",
    "GBPCHF",
    "GBPEUR",
    "GBPJPY",
    "GICS",
    "GOLD_micro",
    "HEATOIL",
    "HOUSE-US",
    "INR",
    "IRON",
    "IRS",
    "JGB-SGX-mini",
    "JP-REALESTATE",
    "JPY",
    "KOSDAQ",
    "KOSPI_mini",
    "KR10",
    "KR3",
    "KRWUSD_mini",
    "LEANHOG",
    "LIVECOW",
    "LUMBER-new",
    "MILK",
    "MILKDRY",
    "MILKWET",
    "MSCIASIA",
    "MSCISING",
    "MSCIWORLD",
    "MUMMY",
    "MXP",
    "NASDAQ_micro",
    "NIFTY",
    "NIKKEI",
    "NIKKEI400",
    "NOK",
    "NZD",
    "OAT",
    "OATIES",
    "OMX",
    "PALLAD",
    "PLAT",
    "PLN",
    "R1000",
    "REDWHEAT",
    "RICE",
    "RUBBER",
    "RUR",
    "RUSSELL",
    "SEK",
    "SGD",
    "SGX",
    "SHATZ",
    "SILVER",
    "SMI",
    "SMI-MID",
    "SOFR",
    "SOYBEAN_mini",
    "SOYMEAL",
    "SOYOIL",
    "SP400",
    "SP500_micro",
    "STEEL",
    "SWISSLEAD",
    "TOPIX",
    "TWD",
    "US-DISCRETE",
    "US-ENERGY",
    "US-FINANCE",
    "US-HEALTH",
    "US-INDUSTRY",
    "US-MATERIAL",
    "US-PROPERTY",
    "US-REALESTATE",
    "US-STAPLES",
    "US-TECH",
    "US-UTILS",
    "US10",
    "US10U",
    "US2",
    "US20",
    "US3",
    "US30",
    "US5",
    "USIRS10",
    "USIRS2ERIS",
    "USIRS5",
    "USIRS5ERIS",
    "V2X",
    "VIX",
    "VNKI",
    "WHEAT",
    "WHEY",
    "YENEUR",
    "ZAR",
]
