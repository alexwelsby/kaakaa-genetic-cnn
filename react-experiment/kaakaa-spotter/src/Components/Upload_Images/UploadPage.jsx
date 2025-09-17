import UploadSection from "./UploadSection";
import ViewSection from "./ViewSection";
import styles from "./uploadpage.module.css";

function Upload_Images() {
  return (
    <div className={styles.whole}>
      <UploadSection></UploadSection>
      <ViewSection></ViewSection>
    </div>
  );
}
export default Upload_Images;
