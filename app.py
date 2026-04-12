# judges.comments: Hugging Face demo interface

import gradio as gr
from inference import run_inference


def run_simulation():
    results = run_inference()

    explanation = """
    🚀 EV Charging Optimization Agent

    Strategy:
    - Dynamic pricing + power allocation
    - Queue-aware optimization
    - Load balancing under high demand
    - Time-based (solar window) optimization

    Goal:
    Maximize throughput while minimizing wait time & overload
    """

    return results, explanation


with gr.Blocks() as demo:
    gr.Markdown("# ⚡ EV Charging Optimization Agent")
    gr.Markdown("AI-based decision system for smart EV charging.")

    btn = gr.Button("🚀 Run Simulation")

    output = gr.JSON(label="📊 Results")
    explain = gr.Textbox(label="🧠 Explanation")

    btn.click(fn=run_simulation, outputs=[output, explain])

demo.launch()