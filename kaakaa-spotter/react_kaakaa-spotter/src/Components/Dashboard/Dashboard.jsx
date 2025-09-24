import DashboardPost from "./DashboardPost";
import { useState, useEffect } from "react";
import styles from "./dashpost.module.css";

function Dashboard() {
  const [posts, setPosts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchPosts() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/images-library"
        );
        if (!response.ok) throw new Error("Failed to fetch posts");
        const data = await response.json();
        setPosts(data);
      } catch (error) {
        console.error(error);
      } finally {
        setIsLoading(false);
      }
    }

    fetchPosts();
  }, []);

  if (isLoading) return <></>;
  return (
    <div className={styles.dashboard}>
      {posts.map((post, index) => (
        <DashboardPost key={index} post={post} />
      ))}
    </div>
  );
}
export default Dashboard;
