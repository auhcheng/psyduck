import { useMemo, useState } from "react";
import Head from "next/head";
import { Alert, Button, Container, Form, Spinner } from "react-bootstrap";

import { BACKEND_HOST } from "../lib/constants";
import { postData, postFormData, toBase64 } from "../lib/util";
import styles from "../styles/Home.module.css";
import { siteTitle } from '../components/layout'
import { useAuthContext } from "../context/auth";

const baseStyle = {
  flex: 1,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  padding: "20px",
  borderWidth: 2,
  borderRadius: 2,
  borderColor: "#eeeeee",
  borderStyle: "dashed",
  backgroundColor: "#fafafa",
  color: "#bdbdbd",
  outline: "none",
  transition: "border .24s ease-in-out",
};

const activeStyle = {
  borderColor: "#2196f3",
};

const acceptStyle = {
  borderColor: "#00e676",
};

const rejectStyle = {
  borderColor: "#ff1744",
};

export default function Upload() {
  const authState = useAuthContext();
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [title, setTitle] = useState(null);
  const [email, setEmail] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadData = () => {
    setError(null);
    setSuccess(null);
    if (!title) {
      setError("Please fill out all fields.");
      return;
    }

    const formData = new FormData();
    formData.append("title", title);
    formData.append("email", email)
    formData.append("userId", authState.uid);
    formData.append("userIdToken", authState.idToken);

    console.log(formData)
    setLoading(true);
    postFormData(`${BACKEND_HOST}/submit`, formData)
      .then((data) => {
        console.log("Success:", data);
        setLoading(false);

        if (data.ok) {
          setSuccess(true);
        } else {
          setError(data.message);
        }
      })
      .catch((error) => {
        console.log(error);
        setLoading(false);
        setError("");
      });
  };

  return (
    <div classtitle={styles.container}>
      <Head>
        <title>{ siteTitle } | Submit</title>
        {/* <link rel="icon" href="/logo.svg" /> */}
      </Head>

      <Container>
        <h1>Submit</h1>
        {!!error ? <Alert variant="danger">{error}</Alert> : null}
        {!!success ? (
          <Alert variant="success">
            Your profile was uploaded successfully!
          </Alert>
        ) : null}
        <Form>
          <Form.Label>title</Form.Label>
          <Form.Control
            type="text"
            placeholder="Through a Forest Darkly"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <Form.Label>email</Form.Label>
          <Form.Control
            type="text"
            placeholder="auhcheng@gmail.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Button onClick={uploadData} disabled={loading}>
            Upload
          </Button>
          {loading ? <Spinner animation="border" /> : null}
        </Form>
      </Container>
    </div>
  );
}