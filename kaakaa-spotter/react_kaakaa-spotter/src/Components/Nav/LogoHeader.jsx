//import styles from "./logoHeader.module.css";
import headerLogo from "../../assets/react.svg";
import styles from "./nav.module.css";
export default function LogoHeader() {
  return (
    <header className={styles.logoHeader}>
      <img src={headerLogo} />
      <h2>
        DSA <br />
        Membership
        <br />
        Visualizer
      </h2>
    </header>
  );
}
