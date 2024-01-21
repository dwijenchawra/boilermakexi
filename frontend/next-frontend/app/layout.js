import { Rubik } from "next/font/google";
import "./globals.css";

const rub = Rubik({ subsets: ["latin"], weight: ["400", "600"] });

export const metadata = {
  title: "Wave",
  description: "submission to boilermakexi",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${rub.className} w-full h-screen flex flex-col justify-center noise items-center relative`}
      >
        <div className="draggable absolute w-full h-8 top-0"></div>
        {children}
      </body>
    </html>
  );
}
