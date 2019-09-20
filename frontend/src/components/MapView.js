import React from "react";
import PropTypes from "prop-types";
const MapView = ({ data }) =>

    <div className="column">
        <p>{JSON.stringify(data)}</p>
    </div>

MapView.propTypes = {
  data: PropTypes.object.isRequired
};

  export default MapView;
