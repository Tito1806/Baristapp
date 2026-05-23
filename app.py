from cs50 import SQL
from flask import Flask, render_template, request, redirect, jsonify
from openai import OpenAI
import os
import sqlite3

app = Flask(__name__)

db = SQL("sqlite:///recetas.db")

# Ruta de Inicio
@app.route("/")
def index():
    return render_template("index.html")

# Ruta a métodos
@app.route("/metodos")
def metodos():
    return render_template("metodos.html")

# Ruta para hacer Recetas
@app.route("/recetas", methods=["GET", "POST"])
def recetas():
    if request.method == "POST":
        # Obtener datos del formulario
        nombre = request.form.get("nombre")
        g_cafe = request.form.get("cafe")
        temp = request.form.get("temp")
        ratio = request.form.get("ratio")
        infusion = request.form.get("infusion")
        comentarios = request.form.get("comentarios")

        # Guardar en la base de datos
        db.execute(
            "INSERT INTO recetas (nombre, g_cafe, temp, ratio, infusion, comentarios) VALUES (?, ?, ?, ?, ?, ?)",
            nombre, g_cafe, temp, ratio, infusion, comentarios
        )

    # Leer todas las recetas para mostrarlas
    recetas_guardadas = db.execute(
        "SELECT * FROM recetas ORDER BY created_at DESC"
    )

    # Retornar la plantilla con las recetas
    return render_template("recetas.html", recetas=recetas_guardadas)

# Ruta a Mejorar Receta

@app.route("/mejorar_receta", methods=["POST"])
def mejorar_receta():
    data = request.get_json()  # recibe JSON enviado desde JS

    receta_str = (
        f"Nombre de receta: {data['nombre']}. "
        f"Café: {data['g_cafe']} g. "
        f"Agua: {int(data['g_cafe']) * int(data['ratio'])} g "
        f"a {data['temp']} ºC. "
        f"Ratio: 1:{data['ratio']}. "
        f"Infusión: {data['infusion']} min. "
        f"Comentarios: {data.get('comentario_ia','')}"
    )

    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        #api oculta 
        api_key=os.getenv("HF_API_KEY")
    )

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V4-Pro:novita",
        messages=[
            {
                "role": "system",
                "content": "Responde como un barista experto dando consejos a no profesionales aficionadas del cafe  tomando en cuenta los parametros de la receta para una prensa francesa y recomienda como mejorarla alterando unicamente uno o dos de los parametros dados. Responde de manera breve,máximo 90 palabras."
            },
            {
                "role": "user",
                "content": receta_str
            }
        ],
    )

    consejo = completion.choices[0].message.content

    return jsonify({"consejo": consejo})


# Ruta a tips
@app.route("/tips")
def tips():
    return render_template("tips.html")

# Ruta para eliminar recetas
@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):

    db.execute("DELETE FROM recetas WHERE id = ?", id)
    return redirect("/recetas")



