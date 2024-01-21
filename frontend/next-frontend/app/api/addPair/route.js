import { NextResponse } from "next/server";
import { promises as fs } from "fs";

export async function POST(request) {
  const reqBody = await request.json();
  const { gesture1, direction, gesture2, action } = reqBody;
  const file = await fs.readFile("../../userConfig.json", "utf8");
  let data = JSON.parse(file);

  data.gesture_sequences.push({
    seq: [
      {
        p_class: gesture1,
      },
      {
        d_class: direction,
      },
      {
        p_class: gesture2,
      },
    ],
    action: action,
  });

  fs.writeFile(
    "../../userConfig.json",
    JSON.stringify(data, null, 2),
    function writeJSON(err) {
      if (err) return console.log(err);
      console.log(JSON.stringify(file));
      console.log("writing to " + fileName);
    }
  );

  return NextResponse.json({
    message: "UserConfig successfully modified",
    success: true,
  });
}
