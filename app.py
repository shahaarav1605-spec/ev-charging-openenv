# judges.comments: Hugging Face UI

import gradio as gr
from inference import run_inference


def run_simulation():
    results = run_inference()

    explanation = """
🚀 EV Charging Optimization Agent

✔ Dynamic pricing & power control
✔ Queue-aware decision making
✔ Overload handling
✔ Time-based optimization

Goal:
Maximize throughput while minimizing congestion
"""

    return results, explanation


with gr.Blocks() as demo:
    gr.Markdown("# ⚡ EV Charging Optimization Agent")
    gr.Markdown("Smart AI system for EV charging optimization")

    btn = gr.Button("🚀 Run Simulation")

    output = gr.JSON(label="📊 Results")
    explain = gr.Textbox(label="🧠 Explanation")

    btn.click(fn=run_simulation, outputs=[output, explain])

demo.launch()