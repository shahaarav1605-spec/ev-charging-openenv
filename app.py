# ============================================================
# 🚀 EV Charging Optimization Agent - Hugging Face Demo
# judges.comments: Gradio UI for evaluation
# ============================================================

import gradio as gr
from inference import main

def run_simulation():
    try:
        results = main()
        return results
    except Exception as e:
        return {"error": str(e)}

def explain():
    return """The agent:
- Evaluates multiple actions at each step
- Selects optimal pricing and power strategy
- Balances utilization and queue
- Uses time-based optimization (solar window)
- Applies overload penalties for stability
"""

with gr.Blocks() as demo:
    gr.Markdown("# ⚡ EV Charging Optimization Agent")
    gr.Markdown("Interactive demo for evaluating the agent.")

    run_btn = gr.Button("🚀 Run Simulation")
    output = gr.JSON(label="📊 Results")

    run_btn.click(fn=run_simulation, outputs=output)

    gr.Markdown("## 🧠 Explainability")
    explain_btn = gr.Button("Show How It Works")
    explain_output = gr.Textbox()

    explain_btn.click(fn=explain, outputs=explain_output)

demo.launch()