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

    if (user) {
      return NextResponse.json(
        { error: "User already exists" },
        { status: 400 }
      );
    }

    const salt = await bcryptjs.genSalt(10);
    const hashedPassword = await bcryptjs.hash(password, salt);

    const newUser = new User({
      username,
      password: hashedPassword,
    });

    newUser.save();

    return NextResponse.json({
      message: "User created successfully",
      success: true,
    });
  } catch (error) {
    console.log("there was an error");
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
