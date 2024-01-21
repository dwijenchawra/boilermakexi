"use client";

import { useState, useEffect } from "react";
import Sign from "./components/Sign";

export default function Home() {
  const [isLoading, setIsLoading] = useState(true);
  const [isMoving, setIsMoving] = useState(false);
  const [canLoadText, setCanLoadText] = useState(false);
  const [isFinishing, setIsFinishing] = useState(false);
  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
      setTimeout(() => {
        setIsMoving(true);
        setTimeout(() => {
          setCanLoadText(true);
        }, 400);
      }, 3000);
    }, 800);
  }, []);
  return (
    <div
      className={`w-full h-screen flex flex-col justify-center items-center transition duration-[2000ms] ${
        isFinishing ? "opacity-0" : ""
      }`}
    >
      <div
        className={`flex justify-center items-center flex-col absolute m-auto top-0 bottom-0 left-0 right-0 transition duration-[2000ms] ${
          isLoading ? "opacity-0" : ""
        } ${isMoving ? "animate-welcome-move" : ""}`}
      >
        <div className={`text-3xl font-bold`}>
          Welcome to{" "}
          <span className="bg-gradient-to-r from-purple-500 to-purple-700 inline-block text-transparent bg-clip-text">
            Wave
          </span>
        </div>
        <div
          className={`flex justify-center items-center flex-col ${
            isMoving ? "opacity-0" : ""
          } transition duration-[1200ms]`}
        >
          <div>Change the way you use your computer. Forever.</div>
        </div>
      </div>
      <Sign canLoadText={canLoadText} setIsFinishing={setIsFinishing} />
    </div>
  );
}
