#!/usr/bin/env python

import pandas as pd
import json
import os
import sys


def help():
    print("Uso: python excel2json.py <archivo_excel> <directorio_salida> [creditos de electivas necesarios (24)]")


def get_plan23(df: pd.DataFrame) -> dict[
    str: list[dict[
        str: list[str],
        str: int
    ]]
]:
    plan23 = {}

    for _index, fila in df.iterrows():
        nombre = fila["Nombre"]
        if nombre not in plan23:
            plan23[nombre] = []

        if not pd.isna(fila["Equivalencia por materias"]):
            plan23[nombre] += [{
                "materias": list(map(
                    lambda x: x.strip(),
                    fila["Equivalencia por materias"].split("&")
                )),
                "creditos": int(fila["Diferencia de creditos"])
            }]
        else:
            plan23[nombre] += [{
                "materias": [],
                "creditos": int(fila["Diferencia de creditos"])
            }]

        if not pd.isna(fila["Equivalencia por creditos"]):
            plan23[nombre][-1]["creditosNecesarios"] = int(
                fila["Equivalencia por creditos"]
            )

    return plan23


def save_plan23(
    salida: str,
    plan23: dict[
        str: list[dict[
            str: list[str],
            str: int
        ]]
    ],
    creditos_electivas: int
):
    plan = []

    for materia, equivalencias in plan23.items():
        plan += [{"nombre": materia, "equivalencias": equivalencias}]

    file = open(f"{salida}/plan_nuevo.json", "w", encoding = "utf-8")
    json.dump(
        {"materias": plan, "creditosElectivas": creditos_electivas},
        file,
        ensure_ascii = False
    )
    file.close()


def parsear_materia_vieja(fila: pd.Series) -> dict[
    str: str,
    str: int,
    str: int
]:
    return {
        "nombre": fila["Nombre"],
        "creditos": fila["Creditos"],
        "creditosExtra": fila["Creditos extra"]
    }


def save_plan_viejo(
    salida: str,
    df_obligatorias: pd.DataFrame,
    df_electivas: pd.DataFrame,
    df_orientaciones: pd.DataFrame
):
    plan_viejo = {"obligatorias": [], "orientaciones": [], "electivas": []}

    for _index, fila in df_obligatorias.iterrows():
        plan_viejo["obligatorias"].append(parsear_materia_vieja(fila))

    for index, fila in df_electivas.iterrows():
        plan_viejo["electivas"].append(parsear_materia_vieja(fila))

    for orientacion, df in df_orientaciones.items():
        plan_viejo["orientaciones"] += [{
            "nombre": orientacion,
            "materias": []
        }]
        for _index, fila in df.iterrows():
            plan_viejo["orientaciones"][-1]["materias"].append(
                parsear_materia_vieja(fila)
            )

    file = open(f"{salida}/plan_viejo.json", "w", encoding = "utf-8")
    json.dump(plan_viejo, file, ensure_ascii = False)
    file.close()


def main(entrada: str, salida: str, creditos_electivas: int):
    excel = pd.read_excel(entrada, sheet_name = None)

    try:
        df_plan23 = excel["Plan23"]
        df_obligatorias = excel["Obligatorias"]
        df_electivas = excel["Electivas"]
        df_orientaciones = {}

        for hoja, df in excel.items():
            if not hoja.startswith("Orientacion"):
                continue

            df_orientaciones[hoja[len("Orientacion - "):]] = df
    except Exception as e:
        print("Hubo un error al leer el excel")
        print(e)
        exit(-3)

    plan23 = get_plan23(df_plan23)

    save_plan23(salida, plan23, creditos_electivas)
    save_plan_viejo(salida, df_obligatorias, df_electivas, df_orientaciones)


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        help()
        exit(-1)

    if not os.path.exists(sys.argv[1]):
        print("El archivo de entrada no existe")
        exit(-2)

    os.makedirs(sys.argv[2], exist_ok = True)

    try:
        creditos_electivas = 24
        if len(sys.argv) == 4:
            creditos_electivas = int(sys.argv[3])
    except ValueError:
        print("El tercer argumento debe ser un número entero")
        exit(-2)

    main(sys.argv[1], sys.argv[2].rstrip("/"), creditos_electivas)
