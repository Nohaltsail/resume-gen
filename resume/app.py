from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


from resume.model.resume_model import ResumePdfRes
from resume.service.service.resume_service import ResumeService

app = FastAPI(title="简历生成系统", description="", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

resume_service = ResumeService()


@app.post("/generate-pdf")
async def generate_pdf(resume_data: dict):
    try:
        res: ResumePdfRes = resume_service.generate_pdf(resume_data)
        return FileResponse(
            res.path,
            media_type='application/pdf',
            filename=f"{res.name}_简历.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成PDF失败: {str(e)}")


@app.post("/save-resume")
async def save_resume(resume_data: dict):
    try:
        resume_id = resume_service.save_content(resume_data)
        return {"success": True, "resume_id": resume_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存失败: {str(e)}")


@app.get("/load-resume")
async def load_resume(recruitment_type: str):
    try:
        resume_data = resume_service.load_content(recruitment_type)
        if resume_data:
            return resume_data
        else:
            return {}
            # raise HTTPException(status_code=404, detail="简历未找到")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加载失败: {str(e)}")


app.mount("/", StaticFiles(directory="../static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
