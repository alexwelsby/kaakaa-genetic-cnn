import styles from "./defaultpage.module.css";

function DefaultPage({ children }) {
  return <div className={styles.defaultPage}>{children}</div>;
}

export default DefaultPage;
