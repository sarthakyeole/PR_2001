import React, { useEffect, useState } from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { Avatar, Backdrop, CircularProgress } from "@mui/material";
import axios from "axios";
import { stringToAv, stringToColor } from "../../Data/Methods";
import { serverLink, isFaceRecognitionEnable } from "../../Data/Variables";
import { useNavigate } from "react-router-dom";

const CandidateLayout = (props) => {
  const navigate = useNavigate();
  const [data, setData] = useState("");
  const [msg, setMsg] = useState("");
  const link = "/login";

  const [loading, setLoading] = useState(false);

  const handleClick = async (id) => {
    setLoading(true);
    if (isFaceRecognitionEnable) {
      setMsg("🔍 Initializing Face Recognition...");
      try {
        // Use the new face recognition endpoint
        var res = await axios.post(serverLink + "face-recognition");
        
        // Check if face recognition was successful
        if (!res.data.success) {
          alert("Face recognition failed: " + (res.data.error || "Unknown error"));
          setLoading(false);
          return;
        }
        
        let userName = res.data.username;
        setMsg("✅ " + userName + " Detected");
        
        // Get user details by username
        res = await axios.get(serverLink + "user/username/" + userName);
        let user = res.data[0];
        if (!user) {
          alert("User with " + userName + " username Not Found");
          setLoading(false);
          return;
        }
        
        const tmp = {
          candidate_id: data._id,
          candidate_username: props.username,
          election_id: props.id,
          user_id: user._id,
          user_username: user.username,
        };
        
        setMsg("");
        setLoading(false);
        navigate(link, { state: { info: tmp } });
        
      } catch (err) {
        console.error("Face recognition error:", err);
        alert("Face recognition failed: " + (err.response?.data?.error || err.message || "Unknown error"));
        setLoading(false);
        return;
      }
    } else {
      const sendingData = {
        candidate_id: data._id,
        candidate_username: props.username,
        election_id: props.id,
      };
      setLoading(false);
      navigate(link, { state: { info: sendingData } });
    }
  };

  useEffect(() => {
    async function getData() {
      let res = await axios.get(serverLink + "candidate/" + props.username);
      let user = res.data;
      setData(user);
    }
    getData();
    // eslint-disable-next-line
  }, [props.username]);

  return (
    <>
      <Backdrop
        sx={{ 
          color: "#fff", 
          zIndex: (theme) => theme.zIndex.drawer + 1,
          flexDirection: 'column',
          gap: 2
        }}
        open={loading}
      >
        <CircularProgress color="inherit" size={60} />
        <Typography variant="h6" sx={{ textAlign: 'center' }}>
          {msg || "Processing..."}
        </Typography>
        {msg.includes("Initializing") && (
          <Typography variant="body2" sx={{ textAlign: 'center', opacity: 0.8 }}>
            Please position your face clearly in front of the camera
          </Typography>
        )}
      </Backdrop>

      <Card sx={{ maxWidth: 345 }}>
        <CardMedia
          height="140"
          sx={{
            display: "flex",
            justifyContent: "center",
            height: "285px",
            alignItems: "center",
          }}
        >
          {" "}
          <Avatar
            aria-label="recipe"
            sx={{
              width: "200px",
              height: "200px",
              fontSize: "50px",
              bgcolor: stringToColor(data.firstName + " " + data.lastName),
            }}
          >
            {data !== "" && stringToAv(data.firstName, data.lastName)}
          </Avatar>
        </CardMedia>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {props.username}
          </Typography>
          <Typography variant="body2" color="text.secondary" component="div">
            {data !== null && (
              <>
                <Typography>
                  Name : {data.firstName + " " + data.lastName}
                </Typography>
                <Typography>Location: {data.location}</Typography>
              </>
            )}
          </Typography>
        </CardContent>
        <CardActions>
          <Button 
            size="small" 
            onClick={() => handleClick(data._id)}
            variant="contained"
            color="primary"
            disabled={loading}
            sx={{ 
              width: '100%',
              display: 'flex',
              alignItems: 'center',
              gap: 1
            }}
          >
            {isFaceRecognitionEnable && !loading && "📷"}
            {loading ? "Processing..." : (isFaceRecognitionEnable ? "Vote with Face ID" : "Vote")}
          </Button>
        </CardActions>
      </Card>
    </>
  );
};

export default CandidateLayout;
