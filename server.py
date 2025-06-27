from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import render_template
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.keras.layers import Input, Embedding, Dense, LayerNormalization, Dropout
import pickle
import config.settings as config 
# Flask uygulaması oluşturuyoruz
app = Flask(__name__,template_folder='src')
CORS(app)  
@app.route('/')
def index():
    return render_template('main.html')
class TransformerBlock(tf.keras.layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = tf.keras.Sequential(
            [Dense(ff_dim, activation="relu"), Dense(embed_dim)]
        )
        self.layernorm1 = LayerNormalization(epsilon=1e-6)
        self.layernorm2 = LayerNormalization(epsilon=1e-6)
        self.dropout1 = Dropout(rate)
        self.dropout2 = Dropout(rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)


# Modelleri yükleyelim
model_1 = load_model(config.MODEL_PATH_1, custom_objects={"TransformerBlock": TransformerBlock})
model_2 = load_model(config.MODEL_PATH_2)

# Tokenizer'ı tekrar yükleyin, ya da eğitim sırasında kaydedilen bir tokenizer kullanabilirsiniz
with open(config.TOKENIZER_PATH, 'rb') as file:
    tokenizer = pickle.load(file)
maxlen = 100  # Modelin beklediği maxlen

@app.route('/check_xss', methods=['POST'])
def check_xss():
    data = request.get_json()  # Gelen JSON verisini alıyoruz
    user_input = data['input']
    print(f"Received input: {user_input}")
    # Kullanıcıdan gelen veriyi sayılara dönüştürme
    input_seq = tokenizer.texts_to_sequences([user_input])
    input_seq_padded = pad_sequences(input_seq, maxlen=maxlen, padding='post')

    # Model ile tahmin yapıyoruz
    output_1 = model_1.predict(input_seq_padded)
    output_2 = model_2.predict(input_seq_padded)

    # Çıktıyı değerlendiriyoruz, örneğin 0.5 eşik kullanarak
    result_1 = "XSS Vulnerability Found" if output_1 > 0.5 else "No XSS Vulnerability"
    result_2 = "XSS Vulnerability Found" if output_2 > 0.5 else "No XSS Vulnerability"

    # Sonuçları JSON formatında döndürüyoruz
    return jsonify({
        'result': f"Model 1: {result_1}, Model 2: {result_2}"
    })

if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
