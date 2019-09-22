import React, { Component } from "react";
import PropTypes from "prop-types";
import Cookies from 'js-cookie';

class DetailDataProvider extends Component {
  static propTypes = {
    endpoint: PropTypes.string.isRequired,
    render: PropTypes.func.isRequired,
    pk: PropTypes.number.isRequired
  };
  state = {
      data: [],
      loaded: false,
      placeholder: "Loading..."
    };
  componentDidMount() {
    let csrftoken = Cookies.get('csrftoken');
    fetch(this.props.endpoint + encodeURIComponent(this.props.pk), {
        headers: { "X-CSRFToken": csrftoken }
    })
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(data => this.setState({ data: data, loaded: true }));
  }
  render() {
    const { data, loaded, placeholder } = this.state;
    return loaded ? this.props.render(data) : <p>{placeholder}</p>;
  }
}
export default DetailDataProvider;
