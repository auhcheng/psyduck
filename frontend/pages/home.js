import Head from "next/head";
import Link from "next/link";
import { Button, Card, Container } from "react-bootstrap";
import styles from "../styles/Home.module.css";
import { siteTitle } from '../components/layout'
import ReactPlayer from 'react-player'
import { getVideoPaths } from "../lib/videos";
import path from 'path'
// import myVideo from '/FinishedClips/0d18200cb381409fa6e4290a167d5d96-finaloutput.mp4'
export async function getServerSideProps(context) {
  const allVideoPaths = getVideoPaths();
  return {
    props: {
      allVideoPaths
    }
  }
}

export default function Home({ allVideoPaths }) {
  
  return (
    <div className={styles.container}>
      <Head>
        <title>{siteTitle}</title>
        <link rel="icon" href="/logo.png" />
      </Head>

       <Container>
         <h1>Home</h1>
          <div className={styles.cardGrid}> 
           {allVideoPaths.map((val, idx) => {
             return (
               <div className={styles.videoWrapper}>
                        <video
                         src={ val }
                         width="180"
                         height="180"
                         loop
                         autoPlay={false}
                         playsInline
                         webkit-playsinline="true"
                       />
                      </div>
             )})}
        </div>
       </Container>
     </div>
  );
}