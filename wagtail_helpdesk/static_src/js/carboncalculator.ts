import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";
import Konva from "konva";
import { co2categories } from "./co2categories.js";

window.Stimulus = Application.start();
const context = require.context("./controllers", true, /\.js$/);
Stimulus.load(definitionsFromContext(context));

console.log("carboncalculator.ts toegevoegd");

let currentCategories = [];
currentCategories.push(co2categories.find((cat) => cat.name == "kg CO2"));
currentCategories.push(...co2categories.filter((cat) => cat.name !== "kg CO2"));

/*
const select = document.getElementById("co2categories");
const button = document.getElementById("co2button");

for (const category of co2categories) {
  select.options[select.options.length] = new Option(
    category.name,
    category.name
  );
}

button.addEventListener("click", (value) => {
  if (
    currentCategories.length < 9 &&
    currentCategories.some(cat => cat.name === select.value) === false
  ) {
    for (const category of co2categories) {
      if (category.name == select.value) {
        currentCategories.push(category);

        redraw();
      }
    }
  }
});
*/

// Konva
// first we need to create a stage
const stage = new Konva.Stage({
  container: "cc__konva", // id of container <div>
});

stage.width(stage.container().offsetWidth);
stage.height(stage.container().offsetHeight);

// then create layer
const layer = new Konva.Layer();

//functions
function redraw() {
  layer.destroyChildren();
  drawCategories(currentCategories);
}

function createCircle(x, y, radius, fill, stroke) {
  let circle = new Konva.Circle({
    x: x,
    y: y,
    radius: radius,
    fill: fill,
    stroke: stroke,
  });

  return circle;
}

function createText(x, y, width, text, fontSize, fontFamily, fill) {
  return new Konva.Text({
    x: x - width / 2,
    y: y,
    text: text,
    fontSize: fontSize,
    fontFamily: fontFamily,
    fill: fill,
    width: width,
    align: "center"
  });
}

function createImage(x, y, width, height, source, name) {
  const imgObj = new Image();
  imgObj.src = source;

  let img = new Konva.Image({
    x: x - width / 2,
    y: y - height / 2,
    image: imgObj,
    width: width,
    height: height,
  });

  return img;
}

function drawCategories(currentCategories) {

  let circleRadius = Math.min(stage.height() * 0.13, stage.width() * 0.13);
  let categoryZero;

  for (let i = 0; i < currentCategories.length; i++) {
    let posX;
    let posY;

    if (i == 0) {
      posX = stage.width() * 0.5;
      posY = stage.height() * 0.5;
    } else {
      let degrees = (360 * i) / (currentCategories.length - 1);
      let rad = (degrees / 360) * 2 * Math.PI;
      posX =
        Math.sin(rad) * (stage.width() * 0.5 - circleRadius - Math.max(0, 0.4 * (stage.width() - stage.height())) - 3) +
        stage.width() * 0.5;
      posY =
        Math.cos(rad) * (stage.height() * 0.5 - circleRadius - Math.max(0, 0.4 * (stage.height() - stage.width())) - 3) +
        stage.height() * 0.5;
    }

    const category = new Konva.Group({
      x: posX,
      y: posY,
      name: currentCategories[i].name
    });

    const circle = createCircle(
      0,
      0,
      circleRadius,
      "white",
      "black"
    );
    
    const numText = createText(
      0,
      -circleRadius * 0.7 - 14,
      circleRadius * 1.4,
      Math.round(
        (currentCategories[0].conversion_to_kg_CO2 /
          currentCategories[i].conversion_to_kg_CO2) *
          1000
      ) / 1000,
      13,
      "Geomanist Webfont",
      "red"
    );

    numText.on('mouseover', () => {
      numText.fontStyle("bold");
    });

    numText.on('mouseout', () => {
      numText.fontStyle("normal");
    });

    numText.on('mousedown touchend', () => {
      redraw();
      window.location.href = "https://www.klimaathelpdesk.org/";
    });

    const nameText = createText(
      0,
      -circleRadius * 0.7,
      circleRadius * 1.2,
      currentCategories[i].name,
      13,
      "Geomanist Webfont",
      "black"
    );

    const img = createImage(
      0,
      25,
      circleRadius * 0.8,
      circleRadius * 0.8,
      currentCategories[i].image_url,
      currentCategories[i].name
    );

    category.add(circle);
    category.add(numText);
    category.add(nameText);
    category.add(img);

    if (category.x() === stage.width() / 2 && category.y() === stage.height() / 2) {
      categoryZero = category;
    }
    else {
      category.on('mousedown touchend', () => {
        const index = currentCategories.map(cat => cat.name).indexOf(category.name());
        const cat = currentCategories[index];

        const xSpeed = (stage.width() / 2 - category.x()) / stage.height() * 0.2;
        const ySpeed = (stage.height() / 2 - category.y()) / stage.height() * 0.2;
        
        const anim = new Konva.Animation(function(frame) {
          category.zIndex(2);
          categoryZero.zIndex(1);

          categoryZero.x(
            categoryZero.x() + -xSpeed * frame.time
          );
          categoryZero.y(
            categoryZero.y() + -ySpeed * frame.time
          );

          category.x(
            category.x() + xSpeed * frame.time
          );
          category.y(
            category.y() + ySpeed * frame.time
          );

          if (stage.width() / 2 * 0.95 <= category.x() && category.x() <= stage.width() / 2 * 1.05 &&
        stage.height() / 2 * 0.95 <= category.y() && category.y() <= stage.height() / 2 * 1.05) {
            anim.stop();

            currentCategories[index] = currentCategories[0];
            currentCategories[0] = cat;  

            redraw();
          }

        }, layer);

        anim.start();
      });
    }

    layer.add(category);
  }
}

// create our shapes and add the shapes to the layer
drawCategories(currentCategories);

// add the layer to the stage
stage.add(layer);
