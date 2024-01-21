"use client";

import { useState, useEffect } from "react";
import axios from "axios";

let value = 0;

export default function Pair() {
  const [directionList, setDirectionList] = useState(null);
  const [poseList, setPoseList] = useState(null);
  const [actionList, setActionList] = useState(null);
  const [isFinishedLoading, setIsFinishedLoading] = useState(false);

  const [gesture1, setGesture1] = useState("");
  const [gesture2, setGesture2] = useState("");
  const [action, setAction] = useState("");
  const [direction, setDirection] = useState("");

  const [currType, setCurrType] = useState("gesture");
  const [currStep, setCurrStep] = useState("1");

  useEffect(() => {
    const myFunc = async () => {
      const response = await axios.get("/api/grabUserData");
      const data = response.data;
      const directions = [
        "LEFT",
        "RIGHT",
        "UP",
        "DOWN",
        "INTO_SCREEN",
        "OUT_OF_SCREEN",
        "CW",
        "CCW",
      ];
      let directionList = [];
      for (let index = 0; index < directions.length; index++) {
        const direction = directions[index];
        directionList.push(
          <div
            key={index}
            className={`w-full rounded-lg flex justify-center items-center p-1 bg-purple-700 mb-2 hover:shadow-xl transition duration-200 hover:cursor-pointer hover:bg-purple-500`}
            onClick={() => {
              setDirection(direction);
            }}
          >
            {direction}
          </div>
        );
      }
      setDirectionList(directionList);
      // list of poses
      let poseList = [];
      const poseClasses = data.pose_classes;
      for (let index = 0; index < poseClasses.length; index++) {
        const poseName = poseClasses[index].p_class;
        poseList.push(
          <div
            key={index}
            className={`w-full rounded-lg flex justify-center items-center p-1 bg-purple-700 mb-2 hover:shadow-xl transition duration-200 hover:cursor-pointer hover:bg-purple-500`}
            onClick={() => {
              if (value == 1) {
                setGesture2(poseName);
              } else {
                setGesture1(poseName);
                value++;
              }
            }}
          >
            {poseName}
          </div>
        );
      }
      setPoseList(poseList);
      // list of actions
      let actionList = [];
      const actions = data.actions;
      for (let index = 0; index < actions.length; index++) {
        const actionName = actions[index].name.replace(/\.[^/.]+$/, "");
        actionList.push(
          <div
            key={index}
            className={`w-full rounded-lg flex justify-center items-center p-1 bg-purple-700 mb-2 hover:shadow-xl transition duration-200 hover:cursor-pointer hover:bg-purple-500`}
            onClick={() => {
              setAction(actionName);
            }}
          >
            {actionName}
          </div>
        );
      }
      setActionList(actionList);
      setIsFinishedLoading(true);
    };
    myFunc();
  }, []);

  // need to load all of the data from userconfig file
  //const file = await fs.readFile("../../userConfig.json", "utf8");
  // list of directions
  return (
    <div className="w-full h-full flex justify-start items-center p-5 flex-col pt-10">
      <div className="text-2xl font-bold bg-gradient-to-r from-purple-500 to-purple-700 inline-block text-transparent bg-clip-text">
        Make a New Pair
      </div>
      <div className="mb-4 mt-1">
        Assign a sequence of gestures and directions to an executable task on
        your computer.
      </div>
      <div className="w-[90%] h-[250px] flex justify-between items-center">
        <div className="w-[31%] border h-full rounded-lg flex flex-col items-center p-2">
          <div>Gestures</div>
          <div className="w-full px-2 mt-2 overflow-scroll flex justify-start items-center flex-col">
            {poseList}
          </div>
        </div>
        <div className="w-[31%] border h-full rounded-lg flex flex-col items-center p-2">
          <div>Directions</div>
          <div className="w-full px-2 mt-2 overflow-scroll flex justify-start items-center flex-col">
            {directionList}
          </div>
        </div>
        <div className="w-[31%] border h-full rounded-lg flex flex-col items-center p-2">
          <div>Actions</div>
          <div className="w-full px-2 mt-2 overflow-scroll flex justify-start items-center flex-col">
            {actionList}
          </div>
        </div>
      </div>
      <div className="w-full h-[240px] mt-10 flex flex-col justify-between items-center py-16">
        <div className="flex justify-between items-center w-full">
          {gesture1 == "" ? (
            <div
              className={`border w-[170px] p-1 border-dashed rounded-lg flex justify-center items-center transition duration-200 ${
                currStep != 1 ? "opacity-60" : ""
              }`}
            >
              gesture 1
            </div>
          ) : (
            <div className="w-[170px] p-1 rounded-lg flex justify-center items-center bg-gradient-to-r from-purple-500 to-purple-700">
              {gesture1}
            </div>
          )}
          {direction == "" ? (
            <div
              className={`border w-[170px] p-1 border-dashed rounded-lg flex justify-center items-center transition duration-200 ${
                gesture1 == "" ? "opacity-60" : ""
              }`}
            >
              direction
            </div>
          ) : (
            <div className="w-[170px] p-1 rounded-lg flex justify-center items-center bg-gradient-to-r from-purple-500 to-purple-700">
              {direction}
            </div>
          )}
          {gesture2 == "" ? (
            <div
              className={`border w-[170px] p-1 border-dashed rounded-lg flex justify-center items-center transition duration-200 ${
                direction == "" ? "opacity-60" : ""
              }`}
            >
              gesture 2
            </div>
          ) : (
            <div className="w-[170px] p-1 rounded-lg flex justify-center items-center bg-gradient-to-r from-purple-500 to-purple-700">
              {gesture2}
            </div>
          )}
          {action == "" ? (
            <div
              className={`border w-[170px] p-1 border-dashed rounded-lg flex justify-center items-center transition duration-200 ${
                gesture2 == "" ? "opacity-60" : ""
              }`}
            >
              action
            </div>
          ) : (
            <div className="w-[170px] p-1 rounded-lg flex justify-center items-center bg-gradient-to-r from-purple-500 to-purple-700">
              {action}
            </div>
          )}
        </div>
        <div
          className={`w-[40%] text-center px-4 py-2 rounded-lg hover:cursor-pointer hover:bg-purple-500 bg-purple-700 mb-2 hover:shadow-xl transition duration-200 ${
            action != "" ? "" : "opacity-60"
          }`}
          onClick={async () => {
            if (action == "") {
              return;
            }
            try {
              await axios.post("/api/addPair", {
                gesture1: gesture1,
                direction: direction,
                gesture2: gesture2,
                action: action,
              });
            } catch (e) {
              console.log(e);
            }
          }}
        >
          Create your new pair
        </div>
      </div>
    </div>
  );
}
