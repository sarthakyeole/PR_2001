import { Router } from "express";
import {
  register,
  login,
  users,
  elections,
  candidates,
  phase,
  votingMail,
  a,
} from "../Controller/AuthController.js";
import { faceRecognitionFallback } from "../Controller/FaceAuthFallback.js";

const router = Router();

router.post("/register", register.validator, register.controller);

router.post("/election/register", elections.register);
router.post("/phase/edit/:id", phase.controller);
router.get("/voting/elections", elections.voting);
router.get("/result/elections", elections.result);

router.post("/login", login.validator, login.controller);
router.post("/candidate/register", candidates.register);
router.get("/candidate/:username", candidates.getCandidate);
router.get("/candidates", candidates.getCandidates);
router.get("/candidate/delete/:id", candidates.delete);

router.get("/elections", elections.controller);
router.get("/election/:id", elections.getElection);
router.get("/election/delete/:id", elections.delete);

router.get("/users", users.getUsers);
router.get("/user/:id", users.getUser);
router.get("/user/username/:id", users.getUserByName);
router.get("/user/delete/:id", users.delete);
router.post("/user/edit/:id", users.edit);

router.post("/op", faceRecognitionFallback.sc);
router.post("/face-recognition", faceRecognitionFallback.sc);  // Now using updated implementation with 10 80 parameters
router.post("/votingEmail", votingMail.send);

export default router;
