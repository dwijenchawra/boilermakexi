// electron.js
import { app, BrowserWindow } from "electron";
import path from "node:path";
import { spawn } from "node:child_process";

let mainWindow;

const __dirname = path.resolve();

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 700,
    titleBarStyle: "hiddenInset",
    webPreferences: {
      nodeIntegration: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  const startURL = "http://localhost:3000";

  mainWindow.loadURL(startURL);

  mainWindow.on("closed", () => (mainWindow = null));
};

const child = spawn("flask", ["--app", "../server/app", "run"]);

child.on("error", function (err) {
  console.log(err);
});

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});
