import { connect } from "../../../dbConfig/dbConfig";
import User from "../../../models/userModel";
import { NextResponse } from "next/server";
import bcryptjs from "bcryptjs";
import jwt from "jsonwebtoken";

connect();

export async function POST(request) {
  try {
    const reqBody = await request.json();
    const { username, password } = reqBody;
    const user = await User.findOne({ username });

    if (!user) {
      return NextResponse.json({ error: "Invalid login" }, { status: 400 });
    }

    const result = await bcryptjs.compare(password, user.password);
    if (!result) {
      return NextResponse.json({ error: "Invalid login" }, { status: 400 });
    }

    const response = NextResponse.json({
      message: "User successfully logged in",
      success: true,
    });

    const tokenData = {
      id: user._id,
      username: user.username,
    };

    const token = await jwt.sign(
      tokenData,
      process.env.NEXT_PUBLIC_TOKEN_SECRET,
      {
        expiresIn: "7d",
      }
    );

    response.cookies.set("sessionID", token, {
      httpOnly: true,
    });

    return response;
  } catch (error) {
    console.log("there was an error");
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
