import UploadForm from "./UploadForm";
import styles from "./uploadpage.module.css";
import styles2 from "../Dashboard/dashpost.module.css";
function UploadSection() {
  return (
    <div className={styles.half}>
      <div className={styles2.postHeader}>Upload section</div>
      <UploadForm />
    </div>
  );
}

export default UploadSection;
