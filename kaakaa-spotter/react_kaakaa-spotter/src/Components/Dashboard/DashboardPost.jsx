import styles from "./dashpost.module.css";

function DashboardPost() {
  return (
    <div className={styles.indivPost}>
      <div className={styles.postHeader}>Uploaded XX minutes ago</div>
      <div className={styles.postContent}>
        <img
          className={styles.postImg}
          src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fafrican-parrot.com%2Fwp-content%2Fuploads%2F2020%2F01%2FNew-Zealand-Kaka-parrot-1.png&f=1&nofb=1&ipt=7e4008be4761ddd554422410379c30970292eb2d262c8721b00db4d109914f1c"
        />
        <div className={styles.postBody}>DASHPOST lol. lmao even</div>
      </div>
    </div>
  );
}
export default DashboardPost;
