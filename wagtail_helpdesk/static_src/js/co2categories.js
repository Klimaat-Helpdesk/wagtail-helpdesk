const rawtext = carbonemissioncategoriesvar;
export const co2categories = ReadCO2CategoriesFromJSONFormat(rawtext);

function ReadCategoryNamesFromConfig(co2categories) {
  var categorynames = [];

  for (var i = 0; i < co2categories.length; i++) {
      categorynames.push(co2categories[i].fields["name"]);
  }
  return categorynames;
}
function ReadCO2CategoriesFromJSONFormat( rawdata) {
  var co2categories = [];
  var parseddata = "";
  try {
    var parseddata = JSON.parse(rawdata);
  } 
  catch (error) {
    console.error("JSON parse error:", error);
  
  }
  //console.log("retrieved parseddata json data size" + Object.keys(parseddata).length);
  for (var i = 0; i < Object.keys(parseddata).length; i++) {
      console.log("json data i: " + JSON.stringify(parseddata[i].fields));
      co2categories.push(parseddata[i].fields);
  }
  return co2categories;
}
function ReadCarbonCalculatorConfig(json_data) {

  console.log("read data: " + json_data);
  co2categories = json_data;
  return co2categories;

}
/*
export const co2categories = [
  {
    name: "kg CO2",
    value: 1,
    icon: "https://cdn-icons-png.flaticon.com/512/3492/3492640.png",
  },
  {
    name: "cheeseburgers",
    value: 3,
    icon: "https://cdn-icons-png.flaticon.com/512/3075/3075977.png",
  },
  {
    name: "vegaburgers",
    value: 0.4,
    icon: "https://cdn-icons-png.flaticon.com/512/1687/1687009.png",
  },
  {
    name: "uur autorijden",
    value: 7,
    icon: "https://cdn-icons-png.flaticon.com/512/8308/8308414.png",
  },
  {
    name: "uur vliegen",
    value: 400,
    icon: "https://cdn-icons-png.flaticon.com/512/7893/7893979.png",
  },
  {
    name: "keer 10 min. douchen",
    value: 0.6,
    icon: "https://cdn-icons-png.flaticon.com/512/760/760637.png",
  },
  {
    name: "dagen computer gebruiken",
    value: 0.48,
    icon: "https://img.freepik.com/premium-vector/desktop-computer-icon-vector-design-template-simple-clean_1309366-1987.jpg",
  },
  {
    name: "dagen huis verwarmen (gas)",
    value: 5.22,
    icon: "https://cdn-icons-png.flaticon.com/512/9879/9879880.png",
  },
  {
    name: "dagen huis verwarmen (warmtepomp)",
    value: 3.13,
    icon: "https://us.123rf.com/450wm/vectorwin/vectorwin2401/vectorwin240100503/221481784-heat-recovery-system-geothermal-color-icon-vector-illustration.jpg?ver=6",
  },
];*/