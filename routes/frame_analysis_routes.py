from fastapi import  UploadFile, File,APIRouter, HTTPException
from PIL import Image
import io
from typing import Dict, Any
from services.frame_analyzer import FrameAnalyzer
from services.display_image import show_frame_with_report

frame_analysis_router = APIRouter(
    prefix="/frame-analysis",
    tags=["Frame Analysis"]
)

@frame_analysis_router.post("/analyze-frame")
async def analyze_frame(
        frame: UploadFile = File(...),
        frame_id: str = "unknown"
) -> Dict[str, Any]:

    try:
        analyzer = FrameAnalyzer()

        # Validate file type
        if not frame.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="Uploaded file must be an image"
            )

        # Read and convert the uploaded image
        contents = await frame.read()
        pil_image = Image.open(io.BytesIO(contents))

        # Convert to RGB if needed
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')

        # Analyze the frame
        result = analyzer.analyze_frame(pil_image, frame_id)

        report =  {
            "success": True,
            "frame_id": frame_id,
            "violations": result.get('violations', []),
            "angles": result.get('angles', []),
            "violation_count": len(result.get('violations', [])),
            "has_violations": len(result.get('violations', [])) > 0
        }
        show_frame_with_report(pil_image, report)
        return report

    except Exception as e:
        print(f"Error processing frame: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing frame: {str(e)}"
        )