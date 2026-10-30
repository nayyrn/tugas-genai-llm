import os
import json
import gradio as gr

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import AsyncGroq


# =========================
# ENVIRONMENT & GROQ
# =========================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY belum ditemukan di file .env")

client = AsyncGroq(api_key=api_key)


# =========================
# FASTAPI
# =========================

app = FastAPI(
    title="Assignment Requirement Analyzer",
    description="Aplikasi GenAI untuk menganalisis instruksi tugas.",
    version="1.0.0"
)


# =========================
# REQUEST BODY
# =========================

class AnalyzeRequest(BaseModel):
    text: str


class ExperimentRequest(BaseModel):
    text: str
    prompt_version: str


# =========================
# MAIN PROMPT / PROMPT C
# =========================

MAIN_PROMPT = """
Role:
Kamu adalah AI yang membantu menganalisis instruksi tugas.

Task:
Analisis instruksi tugas yang diberikan user dan ambil informasi penting dari tugas tersebut.

Context:
User biasanya menerima instruksi tugas yang panjang dan ingin mengetahui inti tugas,
requirement, hasil yang harus dikumpulkan, deadline, dan checklist pengerjaan.

Constraint:
- Gunakan hanya informasi yang terdapat pada instruksi user untuk menentukan requirements, deliverables, dan deadline.
- Jangan membuat requirement atau deadline yang tidak disebutkan.
- Jangan melewatkan requirement penting.
- Checklist harus memuat poin penting dari instruksi user.
- Checklist boleh menambahkan langkah pengecekan umum yang membantu user sebelum mengumpulkan tugas, seperti mengecek kelengkapan atau format file.
- Tambahan checklist tidak boleh dianggap sebagai requirement wajib jika tidak disebutkan dalam instruksi user.
- Jangan membuat checklist yang bertentangan dengan instruksi user.
- Jika deadline tidak disebutkan, isi dengan "Tidak disebutkan".
- Jawaban harus berupa JSON valid.
- Jangan menambahkan teks apa pun di luar JSON.
- Checklist boleh menambahkan langkah pengecekan umum, tetapi tidak boleh membuat detail spesifik baru seperti nama file, format penamaan, jumlah, tanggal, atau aturan lain yang tidak disebutkan user.

Output Format:
{
  "task_summary": "ringkasan tugas utama",
  "requirements": ["requirement 1", "requirement 2"],
  "deliverables": ["hasil yang harus dikumpulkan"],
  "deadline": "deadline tugas",
  "checklist": ["hal yang harus diperiksa sebelum mengumpulkan"]
}
"""


# =========================
# FUNGSI GROQ
# =========================

async def call_llm(text, system_prompt):
    response = await client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )

    return response.choices[0].message.content


async def analyze_structured(text):
    result = await call_llm(text, MAIN_PROMPT)

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        raise ValueError(
            "AI tidak mengembalikan JSON yang valid."
        )


# =========================
# FASTAPI ENDPOINT
# =========================

@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/app")


@app.get("/health")
def health():
    return {
        "message": "Assignment Requirement Analyzer API is running"
    }


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):

    try:
        return await analyze_structured(request.text)

    except ValueError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan: {str(error)}"
        )


# =========================
# PROMPT EXPERIMENT A / B / C
# =========================

@app.post("/experiment")
async def experiment(request: ExperimentRequest):

    prompt_version = request.prompt_version.upper()


    # PROMPT A
    if prompt_version == "A":

        system_prompt = """
Analisis instruksi tugas berikut.
Berikan hasil dalam format JSON.
"""


    # PROMPT B
    elif prompt_version == "B":

        system_prompt = """
Role:
Kamu adalah AI yang membantu mahasiswa memahami instruksi tugas.

Task:
Analisis instruksi tugas yang diberikan user dan ambil informasi penting.

Context:
User menerima instruksi tugas dan ingin mengetahui inti tugas,
requirement, hasil yang harus dikumpulkan, deadline, dan checklist pengerjaan.

Berikan jawaban dalam format JSON.
"""


    # PROMPT C
    elif prompt_version == "C":

        system_prompt = MAIN_PROMPT


    else:

        raise HTTPException(
            status_code=400,
            detail="prompt_version harus A, B, atau C."
        )


    try:

        result = await call_llm(
            request.text,
            system_prompt
        )


        try:

            structured_result = json.loads(result)

            return {
                "prompt_version": prompt_version,
                "is_valid_json": True,
                "output": structured_result
            }


        except json.JSONDecodeError:

            return {
                "prompt_version": prompt_version,
                "is_valid_json": False,
                "output": result
            }


    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Terjadi kesalahan: {str(error)}"
        )


# =========================
# GRADIO FRONTEND
# =========================

def format_list(items):

    if not items:
        return "Tidak disebutkan"

    return "\n".join(
        f"• {item}" for item in items
    )


async def gradio_analyze(text):

    if not text or not text.strip():

        return (
            "Masukkan instruksi tugas terlebih dahulu.",
            "",
            "",
            "",
            ""
        )


    try:

        result = await analyze_structured(text)


        return (
            result.get(
                "task_summary",
                "Tidak disebutkan"
            ),

            format_list(
                result.get("requirements", [])
            ),

            format_list(
                result.get("deliverables", [])
            ),

            result.get(
                "deadline",
                "Tidak disebutkan"
            ),

            format_list(
                result.get("checklist", [])
            )
        )


    except Exception as error:

        return (
            f"Error: {str(error)}",
            "",
            "",
            "",
            ""
        )


# =========================
# DESAIN GRADIO
# =========================

with gr.Blocks(
    title="Assignment Requirement Analyzer"
) as demo:

    gr.Markdown(
        """
        # 📚 Assignment Requirement Analyzer

        Tempel instruksi tugas kamu di bawah ini.

        AI akan membantu mengambil **inti tugas, requirement,
        hasil yang harus dikumpulkan, deadline, dan checklist**.
        """
    )


    task_input = gr.Textbox(
        label="Instruksi Tugas",
        placeholder=(
            "Contoh: Buat laporan tentang penggunaan "
            "Generative AI dalam pendidikan..."
        ),
        lines=8
    )


    analyze_button = gr.Button(
        "Analisis Tugas",
        variant="primary"
    )


    gr.Markdown("## Hasil Analisis")


    task_summary = gr.Textbox(
        label="Ringkasan Tugas",
        interactive=False
    )


    requirements = gr.Textbox(
        label="Requirements",
        lines=5,
        interactive=False
    )


    deliverables = gr.Textbox(
        label="Yang Harus Dikumpulkan",
        lines=4,
        interactive=False
    )


    deadline = gr.Textbox(
        label="Deadline",
        interactive=False
    )


    checklist = gr.Textbox(
        label="Checklist",
        lines=6,
        interactive=False
    )


    analyze_button.click(
        fn=gradio_analyze,
        inputs=task_input,
        outputs=[
            task_summary,
            requirements,
            deliverables,
            deadline,
            checklist
        ]
    )


# Memasang Gradio ke dalam FastAPI
app = gr.mount_gradio_app(
    app,
    demo,
    path="/app"
)