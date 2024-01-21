"use client";

import { useState } from "react";

export default function Wave() {
  const [isRecording, setIsRecording] = useState(false);
  return (
    <div className="w-full h-full rounded-lg flex justify-center items-center">
      {isRecording ? (
        <div className="w-full h-full rounded-lg relative">
          <iframe
            src="http://127.0.0.1:5000/video_feed"
            className="w-full h-full rounded-lg"
            frameborder="0"
          />
        </div>
      ) : (
        <div
          className="border p-3 rounded-md text-red-500 border-red-500 hover:cursor-pointer"
          onClick={async () => {
            setIsRecording(true);
            // try {
            //   const response = await axios.get(
            //     "http://127.0.0.1:5000/start_wave"
            //   );
            //   console.log(response);
            // } catch (e) {
            //   console.log(e);
            // }
          }}
        >
          Start Recording
        </div>
      )}
    </div>
  );
}
