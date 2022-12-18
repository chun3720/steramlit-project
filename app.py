import streamlit as st
import numpy as np
import pandas as pd
import re

file = st.file_uploader(label="select file ")


class Supercap_mpt:
    def __init__(self, file):
        self.file_path = file
        self.method = ""

        with open(self.file_path, "r") as f:
            lines = f.readlines()
            self.method = method_dict[lines[3]]
            # header = lines[1][18:20]
            h = re.findall(
                "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", lines[1]
            )

        self.header = int(h[0])
        self.df = pd.read_csv(
            self.file_path, skiprows=self.header - 1, sep="\t", header=0
        )

        check = self.df["cycle number"].value_counts().to_dict()
        _check = sorted(list(check.keys()))
        if len(check) != 1:
            key = _check[-2]
            filt = self.df[self.df["cycle number"] == key]
            self.df = filt.reset_index(drop=True)

        num = self.df["cycle number"].loc[0]
        to_delete = f"_{int(num)}"

        if self.name[-2:] == to_delete:
            self.name = self.name[:-2]

        if self.method == "GCD":
            self.df.drop(
                columns=[
                    "mode",
                    "ox/red",
                    "error",
                    "Ns changes",
                    "counter inc.",
                    "P/W",
                ],
                inplace=True,
            )
            self.appl_current = self.df["control/mA"].loc[0]
            self.appl_unit = self.df.columns[2].split("/")[1]
            self.cap_result = 0
            self.cap_unit = "F"
            self.origin = self.df["time/s"].loc[0]
            self.df["time/s"] -= self.origin

            if self.appl_unit == "mA":
                self.Is = self.appl_current / 1000

            elif self.appl_unit == "uA":
                self.Is = self.appl_current / 1000000

            self.max = self.df["<Ewe>/V"].idxmax()
            self.df_charge = self.df.loc[: self.max]
            self.df_discharge = self.df.loc[self.max + 1 :]

            if self.name.endswith("_CstC"):
                self.name = self.name[:-8]

        elif self.method == "CV":
            self.df.drop(
                columns=["mode", "ox/red", "error", "counter inc.", "P/W"], inplace=True
            )
            t1, v1 = self.df[["time/s", "control/V"]].loc[1]
            t2, v2 = self.df[["time/s", "control/V"]].loc[2]

            self.scan_rate = round((v2 - v1) / (t2 - t1), 2)
            if self.name.endswith("_CV"):
                self.name = self.name[:-6]


def predict():

    # df = pd.read_csv(file, delimiter="\s+")
    # st.success(f"{df.columns}")
    df = pd.read_csv(file)
    # soln = Supercap_mpt(file)
    _, x, y = df.columns
    st.line_chart(df, x= x, y = y)


st.button("Predict", on_click=predict)
