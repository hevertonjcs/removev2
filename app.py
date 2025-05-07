from flask import Flask, request, send_file
import cv2
import numpy as np
import os

app = Flask(__name__)

@app.route("/remover", methods=["POST"])
def remover_marca():
    if 'imagem' not in request.files:
        print("❌ Nenhuma imagem recebida no formulário")
        return {"erro": "nenhuma imagem enviada"}, 400

    file = request.files["imagem"]
    entrada = "entrada.jpg"
    saida = "saida.jpg"
    file.save(entrada)
    print("📥 Imagem recebida e salva:", entrada)

    # Leitura robusta da imagem com np.fromfile
    try:
        data = np.fromfile(entrada, dtype=np.uint8)
        imagem = cv2.imdecode(data, cv2.IMREAD_COLOR)
    except Exception as e:
        print("❌ Erro ao decodificar imagem:", e)
        return {"erro": "falha na leitura da imagem"}, 400

    if imagem is None:
        print("❌ OpenCV falhou ao decodificar a imagem")
        return {"erro": "imagem inválida"}, 400

    altura, largura = imagem.shape[:2]
    mascara = np.zeros(imagem.shape[:2], dtype=np.uint8)
    cv2.rectangle(mascara, (0, altura - 60), (200, altura), 255, -1)
    resultado = cv2.inpaint(imagem, mascara, 3, cv2.INPAINT_TELEA)
    cv2.imwrite(saida, resultado)

    print("✅ Imagem processada e enviada.")
    return send_file(saida, mimetype="image/jpeg")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
