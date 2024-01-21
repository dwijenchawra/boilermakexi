"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import SideOption from "../components/SideOption";

export default function HomepageLayout({ children }) {
  const [currPage, setCurrPage] = useState("gestures");
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
      <div className="h-full w-[20%] pt-8 pb-3 pl-3">
        <div className="w-full h-full flex flex-col justify-between px-1 pt-4 text-lg font-bold opacity-80">
          <div className="flex flex-col">
            <SideOption
              name="gestures"
              currPage={currPage}
              setCurrPage={setCurrPage}
            />
            <SideOption
              name="actions"
              currPage={currPage}
              setCurrPage={setCurrPage}
            />
            <Link
              className={`w-full rounded-md p-3 mb-3 hover:cursor-pointer hover:bg-[#2e2e2e] transition duration-200 ${
                currPage == "pair" ? "bg-[#2e2e2e]" : ""
              }`}
              href={`/homepage/pair`}
              onClick={() => {
                setCurrPage("pair");
              }}
            >
              Pair
            </Link>
            <Link
              className={`w-full rounded-md p-3 hover:cursor-pointer hover:bg-[#2e2e2e] transition duration-200 ${
                currPage == "wave" ? "bg-[#2e2e2e]" : ""
              }`}
              href={`/homepage/wave`}
              onClick={() => {
                setCurrPage("wave");
              }}
            >
              Start{" "}
              <span className="bg-gradient-to-r from-purple-500 to-purple-700 inline-block text-transparent bg-clip-text text-xl">
                Wave
              </span>
            </Link>
          </div>
          <div className="w-full text-center rounded-md mb-2 bg-[#c11740] text-base py-2">
            Sign Out
          </div>
        </div>
      </div>
      <div className="h-full flex-grow p-3">
        <div className="rounded-lg shadow-[0_0px_10px_rgba(0,0,0,0.50)] w-full h-full bg-[#2e2e2e]">
          {children}
        </div>
      </div>
    </div>
  );
}
