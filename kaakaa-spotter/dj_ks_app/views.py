from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
import numpy as np

def index(request):
    return render(request, "index.html")

@api_view(["POST"])
@renderer_classes([JSONRenderer])
def upload_image(request):
    image_file = request.FILES.get("image")

    if not image_file:
        return JsonResponse({"error": "No image provided"}, status=400)
    
    fs = FileSystemStorage(location="media/uploads/")  # saves inside media/uploads/
    filename = fs.save(image_file.name, image_file)
    file_url = fs.url(filename)

    return JsonResponse({
        "filename": filename,
        "url": request.build_absolute_uri(file_url)
    })

def detect_kaakaa(img_path):
    from ultralytics import YOLO
    import cv2

    MODEL_PATH = "C:/Users/alexw/Assignments/AIML339/Project/instance_segmentation/BEST_MODEL_YOLO/best-kaakaa-yolo11n-seg.pt" 
    model = YOLO(MODEL_PATH)

    TARGET_CLASSES = [80] #this is the kaakaa class

    original = cv2.imread(str(img_path))
    h, w, _ = original.shape

    results = model.predict(source=img_path, save=True, save_txt=False, stream=True)

    # Prepare empty masks
    #also making sure that we can parse multiple kaakaa in a single image
    full_masks = []
    blank_mask = np.zeros((h, w), dtype=np.uint8)

      # Go through all detected instances
    for result in results:
        if result.masks is not None:
            for i, mask in enumerate(result.masks.data.cpu().numpy()):
                cls_id = int(result.boxes.cls[i].item())
                if cls_id not in TARGET_CLASSES:
                    continue

                # Convert mask to binary
                m = (mask * 255).astype(np.uint8)
                m_resized = cv2.resize(m, (w, h), interpolation=cv2.INTER_NEAREST)
                full_masks.append(np.maximum(blank_mask, m_resized))

    #making a new image for each mask
    mask_int = 0
    for mask in full_masks:
        if cv2.countNonZero(mask) == 0:
            print(f"No objects found in {img_path}, skipping.")
            return

        # Apply mask to original image
        masked_image = cv2.bitwise_and(original, original, mask=mask)

        #getting ROI bounding box
        y_indices, x_indices = np.where(mask > 0)
        x_min, x_max = np.min(x_indices), np.max(x_indices)
        y_min, y_max = np.min(y_indices), np.max(y_indices)

        # cropping to ROI
        cropped_image = masked_image[y_min-10:y_max+10, x_min-10:x_max+10]

        #saving to mirror folder media/kaakaa/cropped
        save_path = save_dir / img_path.name
        cv2.imwrite(str(save_path), cropped_image)




