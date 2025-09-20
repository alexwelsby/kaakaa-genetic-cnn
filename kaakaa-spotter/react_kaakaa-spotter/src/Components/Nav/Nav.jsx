import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import LogoHeader from "./LogoHeader";
import styles from "./nav.module.css";

function Nav() {
  return (
    <nav className={styles.navBar}>
      <LogoHeader />
      <div className={styles.pageOptions}>
        <Link to="/app">Dashboard</Link>
        <Link to="/app/stats">Statistics</Link>
        <Link to="/app/upload">Upload images</Link>
      </div>
    </nav>
  );
}
export default Nav;
