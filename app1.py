import gradio as gr
import pickle
import numpy as np

# -------------------------
# Load trained model
# -------------------------
with open("disease_model.pkl", "rb") as f:
    model = pickle.load(f)


# -------------------------
# Prediction Function with styled output
# -------------------------
def predict_disease(age, bp, chol):
    features = np.array([[age, bp, chol]])
    pred = model.predict(features)[0]
    
    if pred == 1:
        return """<div style="padding:15px; border-radius:10px; 
                   background:#F8D7DA; color:#721C24; 
                   font-weight:bold; text-align:center;">
                   ❌ Disease Detected – Please consult a doctor!
                  </div>"""
    else:
        return """<div style="padding:15px; border-radius:10px; 
                   background:#D4EDDA; color:#155724; 
                   font-weight:bold; text-align:center;">
                   ✅ No Disease – Patient is Healthy
                  </div>"""


# -------------------------
# Login Function
# -------------------------
def login(username, password):
    if username == "admin" and password == "1234":
        return gr.update(visible=False), gr.update(visible=True), "✅ Login successful! Welcome 🎉"
    else:
        return gr.update(visible=True), gr.update(visible=False), "❌ Invalid credentials. Try again."


# -------------------------
# Gradio Blocks UI
# -------------------------
with gr.Blocks(
    css="""
    body {
        background: linear-gradient(120deg, #89f7fe, #66a6ff);
        font-family: 'Poppins', sans-serif;
    }
    .card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin: 20px auto;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.15);
        max-width: 500px;
        transition: transform 0.2s ease-in-out;
    }
    .card:hover {
        transform: scale(1.02);
    }
    h1, h2, h3 {
        text-align: center;
        color: #2C3E50;
    }
    button {
        background: linear-gradient(45deg, #6dd5ed, #2193b0) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
    }
    """
) as demo:
    # -------------------------
    # Login Screen
    # -------------------------
    with gr.Group(visible=True) as login_screen:
        gr.Markdown("<h1>🩺 Disease Detection System</h1>")
        gr.Markdown("### 🔑 Please log in to continue")
        
        with gr.Column(elem_classes="card"):
            username = gr.Textbox(label="👤 Username", placeholder="Enter username")
            password = gr.Textbox(label="🔒 Password", placeholder="Enter password", type="password")
            login_btn = gr.Button("🔓 Login")
            login_msg = gr.Markdown("")

    # -------------------------
    # Dashboard (after login)
    # -------------------------
    with gr.Group(visible=False) as dashboard_screen:
        gr.Markdown("<h2>👨‍⚕️ Patient Risk Prediction</h2>")
        
        with gr.Column(elem_classes="card"):
            gr.Markdown("### 📋 Enter Patient Details")
            age = gr.Number(label="Age (Years)")
            bp = gr.Number(label="Blood Pressure (mmHg)")
            chol = gr.Number(label="Cholesterol (mg/dL)")
            predict_btn = gr.Button("🔮 Predict Disease")
            predict_out = gr.HTML()
            
            predict_btn.click(
                fn=predict_disease,
                inputs=[age, bp, chol],
                outputs=predict_out
            )

    # -------------------------
    # Switch screens after login
    # -------------------------
    def handle_login(u, p):
        return login(u, p)

    login_btn.click(
        fn=handle_login,
        inputs=[username, password],
        outputs=[login_screen, dashboard_screen, login_msg]
    )

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    demo.launch()
