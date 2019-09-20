import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import MapView from "./MapView";
const App = () => (
  <DataProvider endpoint="api/map/30" 
                render={data => <MapView data={data} />} />
);
const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
