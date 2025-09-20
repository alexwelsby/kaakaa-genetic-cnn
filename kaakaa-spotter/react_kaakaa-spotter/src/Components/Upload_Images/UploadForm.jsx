import styles from "./uploadpage.module.css";
import React, { useState, useEffect } from "react";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [checked, setChecked] = useState(false);
  const [bands, setBands] = useState("");

  const handleText = (event) => {
    setMessage(event.target.value);
  };

  const handle_labelCheckbox = (event) => {
    setChecked(!checked);
    if (!checked) {
      //if they've unchecked that they know bands, forget the bands
      setBands("");
    }
  };

  const handleFile = (event) => {
    const files = Array.from(event.target.files);

    console.log(files);

    setFile(files[0]);
    console.log(file);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("image", file);
    formData.append("label", bands);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/upload/", {
        method: "POST",
        body: formData,
      });
      console.log(res);
    } catch (error) {
      console.error("Failed to send/fetch to upload api ", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="file"
        accept="image/*"
        id="file-input"
        name="filename"
        onChange={handleFile}
      />
      <input type="submit" />
      <label for="toggle_label">Do you know the bands for this bird?:</label>
      <input
        type="checkbox"
        name="toggle_label"
        onChange={handle_labelCheckbox}
      />
      {checked ? (
        <>
          <label for="b_label">Band code:</label>
          <input
            type="text"
            id="b_label"
            name="b_label"
            onChange={handleText}
          />
        </>
      ) : (
        <></>
      )}

      <img className={styles.previewImg} />
    </form>
  );
}

export default UploadForm;
