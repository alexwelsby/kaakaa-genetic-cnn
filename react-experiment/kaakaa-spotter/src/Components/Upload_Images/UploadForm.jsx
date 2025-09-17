import styles from "./uploadpage.module.css";
import React, { useState, useEffect } from "react";

function UploadForm() {
  const [preview, setPreview] = useState([]);

  const handleFile = (event) => {
    const files = Array.from(event.target.files);

    const newPreview = files.map((file) => ({
      url: URL.createObjectURL(file),
      name: file.name,
    }));

    setPreview(newPreview[0]);
    console.log(preview);
    event.target.value = null;
  };

  return (
    <form>
      <input
        type="file"
        accept="image/*"
        id="file-input"
        name="filename"
        onChange={handleFile}
      />
      <input type="submit" />
      <img className={styles.previewImg} src={preview.url} />
    </form>
  );
}

export default UploadForm;
