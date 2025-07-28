# 🗳️ Blockchain-Based E-Voting System using Facial Recognition

In a digital age where election integrity and voter verification are more critical than ever, this project presents a secure and efficient **web-based e-voting application**. It leverages **blockchain technology** for transparent vote recording and **facial recognition** for real-time voter authentication—ensuring that each vote is legitimate, tamper-proof, and verifiable.

The backend is powered by **MongoDB**, structured into three primary collections:
- `users`: stores voter data and facial encodings
- `candidates`: stores information about registered candidates
- `elections`: tracks active and historical election details

This system is ideal for organizations or institutions looking to implement reliable, technology-driven election processes.

📄 **[Read the Official Project Report](https://docs.google.com/document/d/1k7lf8o5dhVp0AC389TcDwiigGQ0nUTjB/edit?usp=sharing&ouid=115487462551101368253&rtpof=true&sd=true)**

---

## 📁 Project Structure

The repository is organized into modular components to separate concerns across client, server, and smart contract logic:

```
Blockchain-Based-E-Voting-System-using-Facial-Recognition/
│
├── client/                 # Frontend (React or similar) for voter interaction
├── server/                 # Backend (Node.js or Python) for authentication, facial recognition, and API logic
├── smart_contract/         # Solidity smart contracts to manage blockchain-based voting logic
│
├── dlib-*.whl              # Dlib wheel file for facial recognition support (Windows specific)
├── package.json            # Project dependencies and scripts (likely for Node.js environment)
├── readme.md               # Project documentation
```

### 🔍 Folder Descriptions

- **`client/`**:  
  Houses the frontend code for the voting interface, user registration, login, and candidate selection.

- **`server/`**:  
  Backend server logic, including user authentication, facial recognition, database interactions, and communication with the blockchain.

- **`smart_contract/`**:  
  Contains the smart contract(s) written in Solidity, deployed to a local or public Ethereum-compatible blockchain for secure and verifiable voting.

- **`dlib-*.whl`**:  
  Pre-built binary of the Dlib library for Windows, used for facial recognition.

- **`package.json`**:  
  Defines Node.js project metadata, dependencies, and scripts (if Node.js is used).

---

## ▶️ How to Run

Follow the steps below to install, configure, and run the **Blockchain-Based E-Voting System using Facial Recognition**.

---

### 🧩 Installation and Setup

#### 📦 MongoDB Configuration
1. Open `/server/.env` and add your MongoDB connection URL on **line 2**.
2. Database collections (`users`, `candidates`, `elections`) will be automatically managed via the schema files in `/server/Models`.

#### 📧 Third-Party Email Verification
1. Register your email application (e.g., with Gmail).
2. Generate an **app-specific password** using Google Support.
3. Add your email credentials (EMAIL, PASSWORD) to `/server/.env`.

---

### 🔗 Blockchain & Smart Contract Setup

#### 🪙 Ganache (Local Blockchain)
1. Install [Ganache](https://trufflesuite.com/ganache/).
2. Open it to access 10 free Ethereum accounts, each funded with 100 ETH.
3. Link Ganache to `/smart_contract/truffle-config.js` to sync accounts.

#### 🦊 MetaMask (Browser Extension)
1. Install [MetaMask](https://metamask.io/) for Chrome.
2. Import an account using the private keys provided by Ganache.
3. Use this for managing transactions during contract interaction.

#### ⚒️ Compile & Deploy Smart Contract
```bash
cd smart_contract
npm install -g truffle      # Skip if already installed
truffle compile
truffle migrate
```
4. After deployment:
   - Copy the deployed contract **address** to `client/utils/Constant.js`.
   - Copy the `Transaction.json` ABI file from `smart_contract/build/contracts/` to `client/utils/Transaction.json`.

---

### 🧠 Facial Recognition Setup

#### 🐍 Python Environment
Install the required packages:

```bash
pip install opencv-python numpy os face_recognition
```

> If you face issues installing `face_recognition`, try manually installing `dlib` using:
```bash
pip install dlib-19.24.99-cp312-cp312-win_amd64.whl
```
> Still having issues? Try **downgrading `numpy`** to a compatible version.

#### 📸 Image Encoding
1. Add user images to the `/Face/` directory.
2. Ensure the image filenames match corresponding usernames.
3. In `/server/Controller/encoded.py`, update **line 6** to specify the correct photo directory.

---

### 🚀 Running the Web Application

#### Step 1: Start the Client
```bash
cd client
npm install
npm run start
```

#### Step 2: Start the Server
```bash
cd server
npm install
nodemon main
```

Wait a few moments, then open your browser and access the application to begin the voting process.

---
## ✨ Features

This project integrates secure voting, identity verification, and blockchain technology into a seamless web experience.

- 🔐 **Blockchain Integration**  
  Ensures vote immutability and prevents tampering with election data.

- 👤 **Facial Recognition Authentication**  
  Uses computer vision to verify voters' identity before allowing access to the ballot.

- 🗳️ **Real-Time Voting Interface**  
  Interactive UI for casting votes, viewing candidates, and election status.

- 📬 **Email Verification**  
  Automatically sends confirmation emails after successful registration or vote casting.

- 🧾 **Smart Contract-Driven Voting**  
  Every vote is recorded on a decentralized ledger using Ethereum smart contracts.

- 📊 **Admin Panel & Results Display**  
  View aggregated results and manage election data via the backend.

---

## ⚙️ Technology Stack

### 🧠 Backend
- **Node.js** – Server-side logic and API handling
- **Express.js** – Web server framework
- **MongoDB** – NoSQL database for storing users, elections, and votes
- **Dlib + face_recognition** – Facial recognition engine
- **Python** – For facial image processing and encoding

### 🖼️ Frontend
- **React.js** – User interface for voters and admins
- **MetaMask** – Handles Ethereum transactions through the browser

### ⛓️ Blockchain
- **Solidity** – Smart contracts for decentralized voting
- **Truffle** – Ethereum development framework
- **Ganache** – Local blockchain environment for testing

### 🔧 Dev Tools
- **Nodemon** – Auto-reloading Node.js server
- **dotenv** – Environment variable management
- **Google SMTP** – For email verification (via app password)

---
## 📝 License

This project is licensed under the **MIT License**.