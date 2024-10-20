from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os

# Define the FastAPI app
app = FastAPI()

# Input model for the prompt
class PromptInput(BaseModel):
    question: str

# Function to run inference using the command line
def run_inference(prompt: str):
    model_path = "models/Llama3-8B-1.58-100B-tokens/ggml-model-i2_s.gguf"
    command = [
        "python", "run_inference.py",
        "-m", model_path,
        "-p", prompt,
        "-n", "100",   # Number of tokens for output
        "-temp", "0" # Temperature (for deterministic output)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

@app.post("/answer")
async def get_answer(prompt_input: PromptInput):
    prompt = prompt_input.question + "\nAnswer:"
    # Run inference and capture the output
    output = run_inference(prompt)
    # Process the output to extract only the answer
    answer = output.strip().split("\n")[-1]
    # Remove "Answer:" if it exists in the answer string
    if answer.lower().startswith("answer:"):
        answer = answer[len("Answer:"):].strip()
    return {"answer": answer}

