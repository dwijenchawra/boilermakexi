"use client";

import { useState, useEffect } from "react";

export default function HomepageLayout({ children }) {
  const [isLoading, setIsLoading] = useState(true);
  useEffect(() => {
    setTimeout(() => {
      setIsLoading(false);
    }, 500);
  }, []);
  return (
    <div
      className={`w-full h-full flex transition duration-[2000ms] ${
        isLoading ? "opacity-0" : ""
      }`}
    >
      <div className="h-full w-[22%] pt-8 pb-3 pl-3">
        <div className="w-full h-full flex flex-col justify-between items-center px-3 pt-4 text-lg">
          <div>
            <div className="w-full rounded-md p-3 bg-gradient-to-r from-purple-500 to-purple-700 inline-block text-transparent bg-clip-text mb-3">
              My Gestures
            </div>
            <div className="w-full rounded-md p-3 bg-gradient-to-r from-purple-500 to-purple-700 inline-block text-transparent bg-clip-text mb-3">
              My Actions
            </div>
            <div className="w-full rounded-md p-3 bg-gradient-to-r from-purple-500 to-purple-700 inline-block text-transparent bg-clip-text mb-3">
              Pair
            </div>
            <div className="w-full rounded-md p-3 bg-gradient-to-r from-purple-500 to-purple-700 inline-block text-transparent bg-clip-text">
              Start Wave
            </div>
          </div>
          <div className="w-full text-center rounded-md mb-5 bg-[#c11740] text-base py-2">
            Sign Out
          </div>
        </div>
      </div>
      <div className="h-full flex-grow p-3">
        <div className="rounded-lg shadow-[0_0px_10px_rgba(0,0,0,0.50)] w-full h-full">
          {children}
        </div>
      </div>
    </div>
  );
}
