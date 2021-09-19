import "../styles/globals.css";
import firebase from "firebase/app";
import 'bootstrap/dist/css/bootstrap.css'
import AppNavbar from "../components/navbar";
import { AuthWrapper } from "../context/auth";
import styles from "../styles/Index.module.css";
import { siteTitle } from "../components/layout"

// Configure Firebase.
const config = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

if (!firebase.apps.length) {
  firebase.initializeApp(config);
} else {
  firebase.app(); // if already initialized, use that one
}

function MyApp({ Component, pageProps }) {
  return (
    <AuthWrapper>
      {/* <Navbar /> */}
      <AppNavbar />
      <Component {...pageProps} />
      <footer className={styles.footer}>
        © {new Date().getFullYear()} { siteTitle }
      </footer>
    </AuthWrapper>
  );
}

export default MyApp
