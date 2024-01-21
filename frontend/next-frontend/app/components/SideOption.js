"use client";

import Link from "next/link";
export default function SideOption({ name, currPage, setCurrPage }) {
  return (
    <Link
      className={`w-full rounded-md p-3 mb-3 hover:cursor-pointer hover:bg-[#2e2e2e] transition duration-200 ${
        currPage == name ? "bg-[#2e2e2e]" : ""
      }`}
      href={`/homepage/${name}`}
      onClick={() => {
        setCurrPage(name);
      }}
    >
      {`My ${name.charAt(0).toUpperCase() + name.slice(1)}`}
    </Link>
  );
}
