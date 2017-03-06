from flask import Flask, render_template, jsonify, json, request
from pulp import *
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)


@app.route('/First', methods=['POST'])
def solution():
    try:
        valP1 = request.json['P1']  # Valor X1 Funcion Objetivo
        valP2 = request.json['P2']  # Valor X2 Funcion Objetivo

        valF1 = request.json['F1']  # Valor X1 Primer Restriccion
        valF2 = request.json['F2']  # Valor X2 Primer Restriccion
        valF3 = request.json['F3']  # Valor Igualdad Primer Restriccion
        valF4 = request.json['F4']  # Valor Simbolo Primer Restriccion

        valS1 = request.json['S1']  # Valor X1 Segunda Restriccion
        valS2 = request.json['S2']  # Valor X2 Segunda Restriccion
        valS3 = request.json['S3']  # Valor Igualdad Segunda Restriccion
        valS4 = request.json['S4']  # Valor Simbolo Segunda Restriccion

        valT1 = request.json['T1']  # Valor X1 Tercera Restriccion
        valT2 = request.json['T2']  # Valor X2 Tercera Restriccion
        valT3 = request.json['T3']  # Valor Igualdad Tercera Restriccion
        valT4 = request.json['T4']  # Valor Simbolo Tercera Restriccion

        # declarando las variables
        x1 = LpVariable("x1")
        x2 = LpVariable("x2")

        # definiendo el problema
        prob = LpProblem("problem", LpMaximize)

        # definiendo las restricciones
        if valF4 == "<=":
            prob += valF1 * x1 + valF2 * x2 <= valF3  # Primer Restriccion
        elif valF4 == ">=":
            prob += valF1 * x1 + valF2 * x2 >= valF3  # Primer Restriccion
        else:
            prob += valF1 * x1 + valF2 * x2 == valF3  # Primer Restriccion

        if valS4 == "<=":
            prob += valS1 * x1 + valS2 * x2 <= valS3  # Segunda Restriccion
        elif valS4 == ">=":
            prob += valS1 * x1 + valS2 * x2 >= valS3  # Segunda Restriccion
        else:
            prob += valS1 * x1 + valS2 * x2 == valS3  # Segunda Restriccion

        if valT4 == "<=":
            prob += valT1 * x1 + valT2 * x2 <= valT3  # Tercer Restriccion
        elif valT4 == ">=":
            prob += valT1 * x1 + valT2 * x2 >= valT3  # Tercer Restriccion
        else:
            prob += valT1 * x1 + valT2 * x2 == valT3  # Tercer Restriccion

        prob += x1 >= 0 # No
        prob += x2 >= 0 # Negatividad

        # definiendo la funcion objetivo a maximizar
        prob += valP1 * x1 + valP2 * x2

        # resolviendo el problema
        status = prob.solve(GLPK(msg=0))
        LpStatus[status]
        result = "x1: " + str(value(x1)) + " x2: " + str(value(x2))

        # Resolviendo la optimizacion graficamente.
        x_vals = np.linspace(0, 100, 10)  # 10 valores entre 0 y 800
        y1 = ((valF3 - valF1 * x_vals) / valF2)  # Primera Restriccion/ Equacion
        y2 = ((valS3 - valS1 * x_vals) / valS2)  # Segunda Restriccion/Equiacion
        y3 = ((valT3 - valT1 * x_vals) / valT2)  # Tercera Restriccion/Equacion

        plt.figure(figsize=(10, 8))

        if valF4 == "<=":
            plt.plot(x_vals, y1, label=r'$' + str(valF1) + 'x_1 + ' + str(valF2) + 'x_2 \leq ' + str(valF3) + '$')
        elif valF4 == ">=":
            plt.plot(x_vals, y1, label=r'$' + str(valF1) + 'x_1 + ' + str(valF2) + 'x_2 \geq ' + str(valF3) + '$')
        else:
            plt.plot(x_vals, y1, label=r'$' + str(valF1) + 'x_1 + ' + str(valF2) + 'x_2 = ' + str(valF3) + '$')

        if valS4 == "<=":
            plt.plot(x_vals, y2, label=r'$' + str(valS1) + 'x_1 + ' + str(valS2) + 'x_2 \leq ' + str(valS3) + '$')
        elif valF4 == ">=":
            plt.plot(x_vals, y2, label=r'$' + str(valS1) + 'x_1 + ' + str(valS2) + 'x_2 \geq ' + str(valS3) + '$')
        else:
            plt.plot(x_vals, y2, label=r'$' + str(valS1) + 'x_1 + ' + str(valS2) + 'x_2 = ' + str(valS3) + '$')

        if valT4 == "<=":
            plt.plot(x_vals, y3, label=r'$' + str(valT1) + 'x_1 + ' + str(valT2) + 'x_2 \leq ' + str(valT3) + '$')
        elif valF4 == ">=":
            plt.plot(x_vals, y3, label=r'$' + str(valT1) + 'x_1 + ' + str(valT2) + 'x_2 \geq ' + str(valT3) + '$')
        else:
            plt.plot(x_vals, y3, label=r'$' + str(valT1) + 'x_1 + ' + str(valT2) + 'x_2 = ' + str(valT3) + '$')

        plt.plot(value(x1), value(x2), 'b*', markersize=15)

        # Región factible
        y4 = np.minimum(y1, y2, y3)
        plt.fill_between(x_vals, 0, y4, alpha=0.15, color='b')
        plt.axis(ymin=0)
        plt.title('Optimización lineal')
        plt.legend()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue())
    except Exception as e:
        return str(e)
    return json.jsonify(result=result, image=plot_url.decode("utf-8"))


@app.route('/Second', methods=['POST'])
def solution2():
    try:
        valP1 = request.json['P1']  # Valor X1 Funcion Objetivo
        valP2 = request.json['P2']  # Valor X2 Funcion Objetivo

        valF1 = request.json['F1']  # Valor X1 Primer Restriccion
        valF2 = request.json['F2']  # Valor X2 Primer Restriccion
        valF3 = request.json['F3']  # Valor Igualdad Primer Restriccion
        valF4 = request.json['F4']  # Valor Simbolo Primer Restriccion

        valS1 = request.json['S1']  # Valor X1 Segunda Restriccion
        valS2 = request.json['S2']  # Valor X2 Segunda Restriccion
        valS3 = request.json['S3']  # Valor Igualdad Segunda Restriccion
        valS4 = request.json['S4']  # Valor Simbolo Segunda Restriccion

        # declarando las variables
        x1 = LpVariable("x1")
        x2 = LpVariable("x2")

        # definiendo el problema
        prob = LpProblem("problem", LpMaximize)

        # definiendo las restricciones
        if valF4 == "<=":
            prob += valF1 * x1 + valF2 * x2 <= valF3  # Primer Restriccion
        elif valF4 == ">=":
            prob += valF1 * x1 + valF2 * x2 >= valF3  # Primer Restriccion
        else:
            prob += valF1 * x1 + valF2 * x2 == valF3  # Primer Restriccion

        if valS4 == "<=":
            prob += valS1 * x1 + valS2 * x2 <= valS3  # Segunda Restriccion
        elif valS4 == ">=":
            prob += valS1 * x1 + valS2 * x2 >= valS3  # Segunda Restriccion
        else:
            prob += valS1 * x1 + valS2 * x2 == valS3  # Segunda Restriccion


        prob += x1 >= 0 # No
        prob += x2 >= 0 # Negatividad

        # definiendo la funcion objetivo a maximizar
        prob += valP1 * x1 + valP2 * x2

        # resolviendo el problema
        status = prob.solve(GLPK(msg=0))
        LpStatus[status]
        result = "x1: " + str(value(x1)) + " x2: " + str(value(x2))

        # Resolviendo la optimizacion graficamente.
        x_vals = np.linspace(0, 100, 10)  # 10 valores entre 0 y 800
        y1 = ((valF3 - valF1 * x_vals) / valF2)  # Primera Restriccion
        y2 = ((valS3 - valS1 * x_vals) / valS2)  # 2x1 + x2 = 1000

        plt.figure(figsize=(10, 8))

        if valF4 == "<=":
            plt.plot(x_vals, y1, label=r'$' + str(valF1) + 'x_1 + ' + str(valF2) + 'x_2 \leq ' + str(valF3) + '$')
        elif valF4 == ">=":
            plt.plot(x_vals, y1, label=r'$' + str(valF1) + 'x_1 + ' + str(valF2) + 'x_2 \geq ' + str(valF3) + '$')
        else:
            plt.plot(x_vals, y1, label=r'$' + str(valF1) + 'x_1 + ' + str(valF2) + 'x_2 = ' + str(valF3) + '$')

        if valS4 == "<=":
            plt.plot(x_vals, y2, label=r'$' + str(valS1) + 'x_1 + ' + str(valS2) + 'x_2 \leq ' + str(valS3) + '$')
        elif valF4 == ">=":
            plt.plot(x_vals, y2, label=r'$' + str(valS1) + 'x_1 + ' + str(valS2) + 'x_2 \geq ' + str(valS3) + '$')
        else:
            plt.plot(x_vals, y2, label=r'$' + str(valS1) + 'x_1 + ' + str(valS2) + 'x_2 = ' + str(valS3) + '$')

        plt.plot(value(x1), value(x2), 'b*', markersize=15)

        # Región factible
        y3 = np.minimum(y1, y2)
        plt.fill_between(x_vals, 0, y3, alpha=0.15, color='b')
        plt.axis(ymin=0)
        plt.title('Optimización lineal')
        plt.legend()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue())
    except Exception as e:
        return str(e)
    return json.jsonify(result=result, image=plot_url.decode("utf-8"))


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
