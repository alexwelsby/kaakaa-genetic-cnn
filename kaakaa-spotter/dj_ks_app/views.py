from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
import numpy as np
import os
import time
import json

def index(request):
    return render(request, "index.html")

@api_view(["POST"])
@renderer_classes([JSONRenderer])
def upload_image(request):
    image_file = request.FILES.get("image")

    if not image_file:
        return JsonResponse({"error": "No image provided"}, status=400)
    
    sanitized = image_file.name.replace(" ", "_")
    
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,  "uploads"),
                            base_url=os.path.join(settings.MEDIA_URL,  "uploads"))
    filename = fs.save(sanitized, image_file)
    file_url = fs.url(filename)
    print(file_url)

    file_path = os.path.join(settings.MEDIA_ROOT, "uploads", filename)

    mask_urls = detect_kaakaa(file_path)

    url = request.build_absolute_uri(file_url)

    absolute_uris = []
    for mask_url in mask_urls:
        absolute_uris.append(request.build_absolute_uri(mask_url))

    if len(mask_urls) > 0:
        add_to_library(url, absolute_uris)

    return JsonResponse({
        "success": 0 if len(mask_urls) == 0 else 1,
        "filename": filename,
        "url": url,
        "mask_urls": absolute_uris,
    })

@api_view(["GET"])
@renderer_classes([JSONRenderer])
def get_image_library(request):
    file_path = get_library_path()
    data = get_library(file_path)

    return JsonResponse(data,safe=False)

def create_library():
    filename = "image_library"

    json_dir = os.path.join(settings.MEDIA_ROOT, "json")

    os.makedirs(json_dir, exist_ok=True)
    file_path = os.path.join(json_dir, filename)

    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)  # empty list as starting structure

    return file_path

def get_library_path():
    filename = "image_library"
    json_dir = os.path.join(settings.MEDIA_ROOT, "json")
    return os.path.join(json_dir, filename)

def get_library(file_path):
    data = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    pass #will just return data = []
            except json.JSONDecodeError:
                pass #will just return data = []
    return list(reversed(data))

def add_to_library(upload_url, mask_urls):
    #seconds elapsed since 1970... we'll use this to decide when to cull images later
    today = int(time.time() * 1000)
    d = { "original": upload_url, "masks": mask_urls, "date": today}

    file_path = get_library_path()

    data = get_library(file_path)
    if len(data) == 0:
        create_library()
    
    data.append(d)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    

def detect_kaakaa(img_path):
    from ultralytics import YOLO
    import cv2

    print(img_path)

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
    mask_urls = []
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

        #converting to jpg w cv2 and contentfile (this is so we can use filesystemstorage...)
        success, buffer = cv2.imencode(".jpg", cropped_image)
        image_file = ContentFile(buffer.tobytes())

        #saving to mirror folder media/kaakaa/cropped
        #this way ensures we're only saving masked images of genuine kaakaa
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT,  "masked"),
                               base_url=os.path.join(settings.MEDIA_URL,  "masked"))

        file_name = os.path.basename(img_path)

        print(f"filename: {file_name}")

        # Save cropped image
        filename = fs.save(file_name, image_file)

        mask_urls.append(fs.url(filename))

    return mask_urls




