"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

export default function SignUp({ canLoadText, setIsFinishing }) {
  const [isOnUp, setIsOnUp] = useState(true);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [buttonMsg, setButtonMsg] = useState("Get started");
  const [errorMsg, setErrorMsg] = useState("");
  const router = useRouter();
  return (
    <div
      className={`${
        canLoadText ? "" : "opacity-0"
      } transition duration-[1800ms] flex justify-center items-center flex-col select-all z-10 w-72 relative`}
    >
      <div className="text-xl font-bold text-center mb-4 select-none relative w-full h-6">
        <span
          className={`absolute m-auto top-0 right-0 transition duration-300 left-0 bottom-0 ${
            !isOnUp ? "opacity-0" : ""
          }`}
        >
          Create an Account
        </span>
        <span
          className={`absolute m-auto top-0 right-0 transition duration-300 left-0 bottom-0 ${
            isOnUp ? "opacity-0" : ""
          }`}
        >
          Sign in
        </span>
      </div>
      <input
        type="text"
        className="rounded-md bg-[#2e2e2e] p-3 text-purple-400 mb-3 placeholder-purple-400 placeholder-opacity-50 transition duration-200 w-full focus:outline-none shadow-inner focus:shadow-[inset_0_8px_8px_0_rgb(0_0_0_/_0.05)]"
        placeholder="Username"
        onChange={(e) => {
          setUsername(e.target.value);
        }}
      />
      <input
        type="password"
        className="rounded-md bg-[#2e2e2e] p-3 text-purple-400 mb-3 placeholder-purple-400 placeholder-opacity-50 transition duration-200 w-full focus:outline-none shadow-inner focus:shadow-[inset_0_8px_8px_0_rgb(0_0_0_/_0.05)]"
        placeholder="Password"
        onChange={(e) => {
          setPassword(e.target.value);
        }}
      />
      <div
        className={`bg-gradient-to-r from-purple-500 to-purple-700 hover:shadow-xl w-[80%] h-10 rounded-md mt-3 flex justify-center items-center hover:cursor-pointer select-none transition duration-200 ${
          buttonMsg == "Fetching data..." ? "opacity-60" : ""
        }`}
        onClick={async () => {
          // send a request to the mongodb backend to check for the user
          setButtonMsg("Fetching data...");
          setErrorMsg("");
          const urlPath = `api/validateSign${isOnUp ? "Up" : "In"}`;
          try {
            await axios.post(urlPath, {
              username: username,
              password: password,
            });
            // it was successful
            setButtonMsg("Hello!");
            setTimeout(() => {
              setIsFinishing(true);
              setTimeout(() => {
                router.push("/homepage/gestures");
              }, 2000);
            }, 500);
          } catch (e) {
            setErrorMsg(e.response.data.error);
            setButtonMsg("Get started");
          }
        }}
      >
        {buttonMsg}
      </div>
      <div className="text-sm mt-4 select-none">
        {isOnUp ? "Already been here?" : "Need an account?"}
        <div
          className="bg-gradient-to-r from-purple-500 to-purple-700 inline-block text-transparent bg-clip-text hover:cursor-pointer ml-[4px]"
          onClick={() => {
            setIsOnUp(!isOnUp);
            setErrorMsg("");
          }}
        >
          {isOnUp ? "Sign in" : "Sign up"}
        </div>
      </div>
      <div className="text-red-500 text-sm mt-2 absolute top-[245px]">
        {errorMsg}
      </div>
    </div>
  );
}
