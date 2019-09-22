import React from "react";
import ReactDOM from "react-dom";
import ListDataProvider from "./ListDataProvider";
import MapList from "./MapList";
import DetailDataProvider from "./DetailDataProvider";
import MapView from "./MapView";

var USER = document.querySelector('#loggedIn').dataset['username']
var USERNAME = document.querySelector('#loggedIn').dataset['userstring']

var mapListEP = "api/user_maps/" + USER;

// const App = () => (
//   <ListDataProvider endpoint={mapListEP} 
//               render={data => <MapList data={data} />} />
// );



class App extends React.Component {
  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
    this.state = {
      page: 'home',
      pk: 0
    };
  }

  handleClick(e) {
    console.log(e.target)
    this.setState({page: 'detail', pk: e.target.dataset['pk']})
  }
  render() {
    if (this.state.page === "home") {
      return (
        <ListDataProvider endpoint={mapListEP} 
              render={data => <MapList data={data} 
              onClick={this.handleClick}/>} />
      )
    }
    if (this.state.page === "detail") {
      return (
        <DetailDataProvider endpoint={"api/map/"}
      render={data => <MapView data={data} />} 
                            pk={this.state.pk} /> 
      )
    }
  }
}

const wrapper = document.getElementById("app");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
