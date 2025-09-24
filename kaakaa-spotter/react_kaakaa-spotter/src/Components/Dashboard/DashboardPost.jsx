import styles from "./dashpost.module.css";

import { useState } from "react";

function DashboardPost({ key, post }) {
  //converts
  const relative_date = Math.floor((Date.now() - post.date) / 1000);

  const [currentUrl, setUrl] = useState(post.original);

  //chatGPT special.
  function timeAgoOrAhead(unixMillis) {
    const diff = unixMillis - Date.now();
    const seconds = Math.floor(Math.abs(diff) / 1000);

    const intervals = [
      { label: "year", seconds: 31536000 },
      { label: "month", seconds: 2592000 },
      { label: "day", seconds: 86400 },
      { label: "hour", seconds: 3600 },
      { label: "minute", seconds: 60 },
      { label: "second", seconds: 1 },
    ];

    for (const interval of intervals) {
      const count = Math.floor(seconds / interval.seconds);
      if (count >= 1) {
        const label = interval.label + (count > 1 ? "s" : "");
        return diff < 0 ? `${count} ${label} ago` : `in ${count} ${label}`;
      }
    }
    return "just now";
  }

  return (
    <div className={styles.indivPost}>
      <div className={styles.postHeader}>
        Uploaded {timeAgoOrAhead(post.date)}
      </div>
      <div className={styles.postContent}>
        <button onClick={() => setUrl(post.original)}>Original</button>
        {post.masks.map((mask, index) => (
          <button onClick={() => setUrl(mask)}>Mask {index}</button>
        ))}
        <img className={styles.postImg} src={currentUrl} />
      </div>
    </div>
  );
}
export default DashboardPost;
