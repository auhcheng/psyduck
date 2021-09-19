import Head from "next/head";
import styles from "../styles/Index.module.css";
import SignIn from "../components/signin";
import siteTitle from "../components/layout"

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>{ siteTitle }</title>
        <link rel="icon" href="/logo.png" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>Login</h1>

        <p className={styles.description}>Please sign in</p>

        <SignIn redirectPath="/home"></SignIn>
      </main>
    </div>
  );
}